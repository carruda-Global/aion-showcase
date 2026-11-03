"""AgentGuard: one enforcement point for every LLM call, whichever agent makes it.

Modes (env AGENT_GUARD_MODE): off | shadow (default: observe and count, never change behavior) | enforce.
Any internal failure is fail-open: the guard logs and lets the call through. Only GuardBlocked
(budget exceeded, enforce mode) interrupts a call.
"""
import logging
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from threading import Lock
from typing import Any

from .budget import SpendStore, estimate_usd, tokens_from_usage
from .context import DEFAULT_TENANT, UNATTRIBUTED, current_context
from .pii import ALL_KINDS, find_pii, mask_pii
from .policy import Policy, PolicyRegistry

logger = logging.getLogger(__name__)

_INJECTION = re.compile(
    r"ignore (all |any )?(the )?(previous|prior|above) instructions|disregard .{0,30}instructions|"
    r"reveal (your )?system prompt|ignore (todas )?as instru[cç][õo]es anteriores|desconsidere .{0,30}instru[cç][õo]es",
    re.IGNORECASE,
)
_OUTPUT_ALLOWANCE_TOKENS = 500
_MAX_MASKABLE_CHARS = 200_000


class GuardBlocked(RuntimeError):
    """Raised in enforce mode when a daily budget would be exceeded."""


@dataclass(frozen=True)
class Limits:
    agent_usd: float
    tenant_usd: float
    global_usd: float


def _limits_from_env() -> Limits:
    def number(name: str, default: float) -> float:
        try:
            return float(os.getenv(name, default))
        except ValueError:
            return default

    return Limits(
        agent_usd=number("AGENT_GUARD_DAILY_USD_AGENT", 20.0),
        tenant_usd=number("AGENT_GUARD_DAILY_USD_TENANT", 50.0),
        global_usd=number("AGENT_GUARD_DAILY_USD_GLOBAL", 100.0),
    )


class AgentGuard:
    def __init__(self, policies: PolicyRegistry | None = None, store: SpendStore | None = None) -> None:
        allow = frozenset(a.strip() for a in os.getenv("AGENT_GUARD_PII_ALLOW", "").split(",") if a.strip())
        self.policies = policies or PolicyRegistry(pii_allow=allow)
        self.store = store or SpendStore()
        self._stats: dict[str, int] = {}
        self._lock = Lock()

    @property
    def mode(self) -> str:
        mode = os.getenv("AGENT_GUARD_MODE", "shadow").lower()
        return mode if mode in ("off", "shadow", "enforce") else "shadow"

    def _count(self, name: str, amount: int = 1) -> None:
        with self._lock:
            self._stats[name] = self._stats.get(name, 0) + amount

    def register_agent(self, agent_id: str, group: str | None = None) -> Policy:
        try:
            return self.policies.register(str(agent_id), group)
        except Exception as exc:  # fail-open: never break agent loading
            self._count("guard_errors")
            logger.warning("[guard] register_agent failed: %s", exc)
            return Policy(key=str(agent_id), group="default")

    def _over_budget(self, agent_id: str, tenant_id: str, estimated_usd: float) -> str | None:
        limits = _limits_from_env()
        checks: list[tuple[str, float, float]] = []
        if agent_id != UNATTRIBUTED:
            checks.append(("agent", self.store.total(agent_id=agent_id), limits.agent_usd))
        if tenant_id != DEFAULT_TENANT:
            checks.append(("tenant", self.store.total(tenant_id=tenant_id), limits.tenant_usd))
        checks.append(("global", self.store.total(), limits.global_usd))
        for scope, spent, limit in checks:
            if spent + estimated_usd > limit:
                return f"daily {scope} budget exceeded (${spent:.2f} of ${limit:.2f})"
        return None

    def before(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        mode = self.mode
        if mode == "off":
            return messages
        blocked_reason: str | None = None
        result = messages
        try:
            ctx = current_context()
            policy = self.policies.resolve(ctx.agent_id)
            self._count("calls")
            texts = [m["content"] if isinstance(m.get("content"), str) else "" for m in messages]
            if any(_INJECTION.search(t) for t in texts):
                self._count("injection_flagged")
                logger.warning("[guard] possible prompt injection (agent=%s)", ctx.agent_id)
            if policy.pii_mode == "mask":
                masked_msgs: list[dict[str, Any]] = []
                found = 0
                for msg, text in zip(messages, texts):
                    if len(text) > _MAX_MASKABLE_CHARS:
                        self._count("pii_skipped_oversized")
                        masked_msgs.append(msg)
                        continue
                    masked, counts = mask_pii(text, ALL_KINDS)
                    found += sum(counts.values())
                    masked_msgs.append({**msg, "content": masked} if counts else msg)
                if found:
                    self._count("pii_items_enforced" if mode == "enforce" else "pii_items_would_mask", found)
                    if mode == "enforce":
                        result = masked_msgs
            est_tokens = sum(len(t) for t in texts) // 4
            est_usd = estimate_usd("default", est_tokens, _OUTPUT_ALLOWANCE_TOKENS)
            blocked_reason = self._over_budget(ctx.agent_id, ctx.tenant_id, est_usd)
        except Exception as exc:  # fail-open by design
            self._count("guard_errors")
            logger.warning("[guard] before() failed, letting the call through: %s", exc)
            return messages
        if blocked_reason:
            self._count("blocked" if mode == "enforce" else "would_block")
            if mode == "enforce":
                raise GuardBlocked(blocked_reason)
        return result

    def before_text(self, prompt: str, system: str = "") -> tuple[str, str]:
        original = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        guarded = self.before(original)
        if guarded is original:
            return prompt, system
        return str(guarded[1]["content"]), str(guarded[0]["content"])

    def after(self, model: str, usage: Any) -> None:
        if self.mode == "off":
            return
        try:
            tokens_in, tokens_out = tokens_from_usage(usage)
            if tokens_in or tokens_out:
                ctx = current_context()
                self.store.add(ctx.agent_id, ctx.tenant_id, estimate_usd(model, tokens_in, tokens_out), tokens_in, tokens_out)
        except Exception as exc:  # fail-open by design
            self._count("guard_errors")
            logger.warning("[guard] after() failed: %s", exc)

    def status(self) -> dict[str, Any]:
        limits = _limits_from_env()
        try:
            spend = {"global_usd_today": round(self.store.total(), 4), "top_agents": self.store.top_agents()}
        except Exception as exc:
            logger.warning("[guard] status: spend unavailable: %s", exc)
            spend = {"error": "unavailable"}
        with self._lock:
            stats = dict(self._stats)
        return {
            "mode": self.mode,
            "limits_usd_per_day": {"agent": limits.agent_usd, "tenant": limits.tenant_usd, "global": limits.global_usd},
            "policies_known": self.policies.known(),
            "stats_since_start": stats,
            "spend": spend,
        }


class _NoopGuard:
    """Used if the real guard cannot be constructed: the platform keeps serving LLM calls unprotected-but-alive."""

    mode = "unavailable"

    def before(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return messages

    def before_text(self, prompt: str, system: str = "") -> tuple[str, str]:
        return prompt, system

    def after(self, model: str, usage: Any) -> None:
        return None

    def register_agent(self, agent_id: str, group: str | None = None) -> Policy:
        return Policy(key=str(agent_id), group="default")

    def status(self) -> dict[str, Any]:
        return {"mode": "unavailable"}


@lru_cache(maxsize=1)
def get_guard() -> AgentGuard | _NoopGuard:
    try:
        return AgentGuard()
    except Exception as exc:  # fail-open: a broken policy file must not take down every LLM call
        logger.error("[guard] could not initialize, running without protection: %s", exc)
        return _NoopGuard()


__all__ = ["AgentGuard", "GuardBlocked", "get_guard", "find_pii"]
