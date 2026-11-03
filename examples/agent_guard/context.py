"""Per-request agent identity, carried by contextvars so every LLM call knows who is asking."""
import functools
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Iterator


UNATTRIBUTED = "unattributed"
DEFAULT_TENANT = "default"


@dataclass(frozen=True)
class AgentContext:
    agent_id: str = UNATTRIBUTED
    tenant_id: str = DEFAULT_TENANT


_current: ContextVar[AgentContext] = ContextVar("agent_guard_context", default=AgentContext())


def current_context() -> AgentContext:
    return _current.get()


@contextmanager
def agent_context(agent_id: str, tenant_id: str = "default") -> Iterator[AgentContext]:
    ctx = AgentContext(agent_id or UNATTRIBUTED, tenant_id or DEFAULT_TENANT)
    token = _current.set(ctx)
    try:
        yield ctx
    finally:
        _current.reset(token)


def with_agent_context(fn: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """Decorator for `async def method(self, task: dict, user_id: str = ...)` entry points."""

    @functools.wraps(fn)
    async def wrapper(self: Any, task: Any, *args: Any, **kwargs: Any) -> Any:
        agent_id = task.get("agent_id", "meta_orchestrator") if isinstance(task, dict) else UNATTRIBUTED
        tenant = kwargs.get("user_id") or (args[0] if args else "default")
        with agent_context(agent_id, str(tenant)):
            return await fn(self, task, *args, **kwargs)

    return wrapper
