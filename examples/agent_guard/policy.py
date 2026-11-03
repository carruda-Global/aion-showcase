"""Policy resolution: an agent gets the policy declared in src/security/policies/*.yaml,
or inherits a secure default. New agents never start unprotected."""
import logging
import re
from dataclasses import dataclass, replace
from pathlib import Path
from threading import Lock

import yaml

logger = logging.getLogger(__name__)

_POLICY_DIR = Path(__file__).resolve().parents[1] / "policies"


@dataclass(frozen=True)
class Policy:
    key: str
    group: str
    pii_mode: str = "mask"  # "mask" | "allow"
    source: str = "default"  # "yaml" | "inherited" | "default"


def normalize(agent_id: str) -> str:
    key = agent_id.lower().removeprefix("did:aip:")
    key = re.sub(r"_\d+$", "", key)
    return re.sub(r"_agent$", "", key)


class PolicyRegistry:
    def __init__(self, policy_dir: Path | None = None, pii_allow: frozenset[str] = frozenset()) -> None:
        self._by_key: dict[str, Policy] = {}
        self._registered: dict[str, Policy] = {}
        self._allow = frozenset(normalize(a) for a in pii_allow)
        self._lock = Lock()
        self._load(policy_dir or _POLICY_DIR)

    def _load(self, directory: Path) -> None:
        for path in sorted(directory.glob("*.yaml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except (OSError, yaml.YAMLError) as exc:
                logger.warning("[guard] could not read policy file %s: %s", path.name, exc)
                continue
            agents = data.get("agents", []) if isinstance(data, dict) else []
            if not isinstance(agents, list):
                logger.warning("[guard] policy file %s has a malformed 'agents' section", path.name)
                continue
            for entry in agents:
                if not isinstance(entry, dict):
                    continue
                key = normalize(str(entry.get("agent_id", "")))
                if key:
                    mode = str(entry.get("pii_mode", "mask")).strip().lower()
                    self._by_key[key] = Policy(
                        key=key, group=path.stem, pii_mode=mode if mode in ("mask", "allow") else "mask", source="yaml"
                    )

    def _lookup(self, key: str) -> Policy | None:
        if key in self._registered:
            return self._registered[key]
        if key in self._by_key:
            return self._by_key[key]
        first = key.split("_")[0]
        for known_key, policy in self._by_key.items():
            if known_key.split("_")[0] == first:
                return policy
        return None

    def resolve(self, agent_id: str) -> Policy:
        key = normalize(agent_id)
        policy = self._lookup(key) or Policy(key=key, group="default")
        if key in self._allow:
            return replace(policy, pii_mode="allow")
        return policy

    def register(self, agent_id: str, group: str | None = None) -> Policy:
        """Attach a newly discovered agent to the architecture, inheriting the group default."""
        key = normalize(agent_id)
        with self._lock:
            existing = self._lookup(key)
            if existing is not None:
                return existing
            policy = Policy(key=key, group=group or "inherited", source="inherited")
            self._registered[key] = policy
            logger.info("[guard] agent %s registered with inherited policy (group=%s)", key, policy.group)
            return policy

    def known(self) -> int:
        return len(self._by_key) + len(self._registered)
