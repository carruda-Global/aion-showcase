"""Offline demo of the central agent guard: new agent inherits protection, PII is masked,
budget is enforced, and every LLM call (any agent) goes through the same chokepoint.
Run: python scripts/demo_agent_guard.py"""
import os
import sys
import tempfile
import types
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DEEPSEEK_API_KEY", "demo")

from src.security.guard import AgentGuard, GuardBlocked, agent_context  # noqa: E402
from src.security.guard.budget import SpendStore  # noqa: E402


def banner(text: str) -> None:
    print(f"\n=== {text}")


def main() -> None:
    import src.api.deepseek_client as ds
    import src.core.agent_loader as loader

    sent: list = []

    class Completions:
        def create(self, model, messages, **_):
            sent.append(messages)
            usage = SimpleNamespace(prompt_tokens=4000, completion_tokens=1000)
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))], usage=usage)

    class FakeOpenAI:
        def __init__(self, **_):
            self.chat = SimpleNamespace(completions=Completions())

    guard = AgentGuard(store=SpendStore(str(Path(tempfile.mkdtemp()) / "demo.db")))
    ds.get_guard = loader.get_guard = lambda: guard
    ds.OpenAI = FakeOpenAI
    llm = ds.DeepSeekClient(ds.Settings())

    banner("1. SHADOW mode (default): observes, never changes behavior")
    os.environ["AGENT_GUARD_MODE"] = "shadow"
    with agent_context("nr1_psicossocial", "acme"):
        llm.chat("Voce e um analista de NR-1.", "Colaborador CPF 529.982.247-25, email ana@acme.com")
    print("prompt sent to the model :", sent[-1][1]["content"])
    print("would have masked        :", guard.status()["stats_since_start"].get("pii_items_would_mask"), "items")

    banner("2. ENFORCE mode: same call, PII never leaves the platform")
    os.environ["AGENT_GUARD_MODE"] = "enforce"
    with agent_context("nr1_psicossocial", "acme"):
        llm.chat("Voce e um analista de NR-1.", "Colaborador CPF 529.982.247-25, email ana@acme.com")
    print("prompt sent to the model :", sent[-1][1]["content"])

    banner("3. A NEW agent is plugged in (no security code written for it)")
    module = types.ModuleType("src.agents.partner_demo_agent")
    module.agent = object()
    sys.modules["src.agents.partner_demo_agent"] = module
    loader.load_agent("partner_demo_agent")
    policy = guard.policies.resolve("partner_demo_agent")
    print(f"policy inherited         : group={policy.group} pii_mode={policy.pii_mode} source={policy.source}")
    with agent_context("partner_demo_agent", "globex"):
        llm.chat("sys", "Cliente CNPJ 11.222.333/0001-81 pediu reembolso")
    print("prompt sent to the model :", sent[-1][1]["content"])

    banner("4. Budget kill-switch (tiny limit for the demo)")
    os.environ["AGENT_GUARD_DAILY_USD_AGENT"] = "0.0001"
    try:
        with agent_context("partner_demo_agent", "globex"):
            llm.chat("sys", "outra chamada")
    except GuardBlocked as exc:
        print("blocked                  :", exc)

    banner("5. Status endpoint payload (GET /api/security/guard/status)")
    status = guard.status()
    print("mode                     :", status["mode"])
    print("counters                 :", status["stats_since_start"])
    print("top spenders today       :", status["spend"]["top_agents"])


if __name__ == "__main__":
    main()
