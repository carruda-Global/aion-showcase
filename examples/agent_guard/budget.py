"""Persistent daily spend ledger (SQLite) and token-to-USD estimation."""
import logging
import os
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from queue import Queue
from threading import Lock, Thread
from typing import Any, Iterator

logger = logging.getLogger(__name__)

# Estimated USD per 1M tokens (input, output). Estimates, not billing data.
_PRICES_PER_M: tuple[tuple[str, tuple[float, float]], ...] = (
    ("deepseek", (0.30, 1.20)),
    ("claude", (3.00, 15.00)),
    ("gemini", (1.25, 5.00)),
    ("kimi", (0.60, 2.50)),
)
_DEFAULT_PRICE = (1.00, 3.00)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS spend (
    day TEXT NOT NULL, agent_id TEXT NOT NULL, tenant_id TEXT NOT NULL,
    usd REAL NOT NULL DEFAULT 0, tokens_in INTEGER NOT NULL DEFAULT 0,
    tokens_out INTEGER NOT NULL DEFAULT 0, calls INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (day, agent_id, tenant_id)
)
"""


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def estimate_usd(model: str, tokens_in: int, tokens_out: int) -> float:
    name = (model or "").lower()
    price_in, price_out = next((p for k, p in _PRICES_PER_M if k in name), _DEFAULT_PRICE)
    return (tokens_in * price_in + tokens_out * price_out) / 1_000_000


def tokens_from_usage(usage: Any) -> tuple[int, int]:
    """Accepts OpenAI-style objects/dicts and Anthropic/Gemini-style dicts."""
    if usage is None:
        return 0, 0

    def pick(*names: str) -> int:
        for name in names:
            value = usage.get(name) if isinstance(usage, dict) else getattr(usage, name, None)
            if isinstance(value, int):
                return value
        return 0

    return pick("prompt_tokens", "input_tokens"), pick("completion_tokens", "output_tokens")


class SpendStore:
    """In-memory daily totals (read path, no I/O) with write-behind persistence to SQLite.

    Reads never touch the database. Writes are queued to a single daemon thread, so callers
    (including the asyncio event loop) never block on disk. On Render, point AGENT_GUARD_DB
    at a persistent disk or budgets reset on every deploy.
    """

    def __init__(self, path: str | None = None) -> None:
        self._path = Path(path or os.getenv("AGENT_GUARD_DB", "data/agent_guard.db"))
        self._lock = Lock()
        self._cache: dict[tuple[str, str, str], list[float]] = {}
        self._queue: Queue[tuple[str, str, str, float, int, int]] = Queue()
        self._writer: Thread | None = None
        self._last_warning = 0.0
        self._load_today()

    @contextmanager
    def _session(self) -> Iterator[sqlite3.Connection]:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self._path, timeout=5)
        try:
            conn.execute("PRAGMA journal_mode=DELETE")
            conn.execute(_SCHEMA)
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _warn(self, message: str) -> None:
        now = time.monotonic()
        if now - self._last_warning > 60:
            self._last_warning = now
            logger.warning("[guard] spend ledger: %s", message)

    def _load_today(self) -> None:
        try:
            with self._session() as conn:
                rows = conn.execute(
                    "SELECT agent_id, tenant_id, usd, tokens_in, tokens_out, calls FROM spend WHERE day = ?", (today(),)
                ).fetchall()
            for agent_id, tenant_id, usd, tin, tout, calls in rows:
                self._cache[(today(), agent_id, tenant_id)] = [usd, tin, tout, calls]
        except Exception as exc:  # fail-open: start empty
            self._warn(f"could not load today's totals: {exc}")

    def _ensure_writer(self) -> None:
        if self._writer is None or not self._writer.is_alive():
            self._writer = Thread(target=self._write_loop, name="agent-guard-ledger", daemon=True)
            self._writer.start()

    def _write_loop(self) -> None:
        while True:
            row = self._queue.get()
            try:
                with self._session() as conn:
                    conn.execute(
                        """INSERT INTO spend (day, agent_id, tenant_id, usd, tokens_in, tokens_out, calls)
                           VALUES (?, ?, ?, ?, ?, ?, 1)
                           ON CONFLICT(day, agent_id, tenant_id) DO UPDATE SET
                             usd = usd + excluded.usd, tokens_in = tokens_in + excluded.tokens_in,
                             tokens_out = tokens_out + excluded.tokens_out, calls = calls + 1""",
                        (today(), *row),
                    )
            except Exception as exc:  # fail-open: keep the in-memory total, drop persistence
                self._warn(f"could not persist spend: {exc}")
            finally:
                self._queue.task_done()

    def add(self, agent_id: str, tenant_id: str, usd: float, tokens_in: int, tokens_out: int) -> None:
        day = today()
        with self._lock:
            for old in [k for k in self._cache if k[0] != day]:
                del self._cache[old]
            entry = self._cache.setdefault((day, agent_id, tenant_id), [0.0, 0, 0, 0])
            entry[0] += usd
            entry[1] += tokens_in
            entry[2] += tokens_out
            entry[3] += 1
        self._ensure_writer()
        self._queue.put((agent_id, tenant_id, usd, tokens_in, tokens_out))

    def flush(self, timeout: float = 5.0) -> None:
        """Wait until queued writes are persisted (tests and graceful shutdown)."""
        waiter = Thread(target=self._queue.join, daemon=True)
        waiter.start()
        waiter.join(timeout)

    def total(self, agent_id: str | None = None, tenant_id: str | None = None) -> float:
        day = today()
        with self._lock:
            return float(
                sum(
                    v[0]
                    for (d, a, t), v in self._cache.items()
                    if d == day and (agent_id is None or a == agent_id) and (tenant_id is None or t == tenant_id)
                )
            )

    def top_agents(self, limit: int = 5) -> list[dict[str, Any]]:
        day = today()
        totals: dict[str, list[float]] = {}
        with self._lock:
            for (d, a, _t), v in self._cache.items():
                if d == day:
                    acc = totals.setdefault(a, [0.0, 0])
                    acc[0] += v[0]
                    acc[1] += int(v[3])
        ranked = sorted(totals.items(), key=lambda kv: kv[1][0], reverse=True)[:limit]
        return [{"agent_id": a, "usd": round(u, 4), "calls": c} for a, (u, c) in ranked]
