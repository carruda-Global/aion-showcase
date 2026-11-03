import asyncio
import sqlite3
import time

import pytest

from src.security.guard import AgentGuard, GuardBlocked, agent_context
from src.security.guard.budget import SpendStore
from src.security.guard.pii import mask_pii
from src.security.guard.policy import PolicyRegistry

VALID_CPF = "529.982.247-25"


@pytest.fixture
def guard(tmp_path, monkeypatch):
    monkeypatch.delenv("AGENT_GUARD_MODE", raising=False)
    monkeypatch.delenv("AGENT_GUARD_PII_ALLOW", raising=False)
    return AgentGuard(store=SpendStore(str(tmp_path / "guard.db")))


def msgs(text):
    return [{"role": "system", "content": "sys"}, {"role": "user", "content": text}]


class TestPolicyAndConstruction:
    def test_malformed_policy_yaml_is_ignored(self, tmp_path):
        (tmp_path / "bad.yaml").write_text("agents: oops\n", encoding="utf-8")
        (tmp_path / "bad2.yaml").write_text(
            "agents:\n  - just-a-string\n  - agent_id: x_001\n    pii_mode: Mask\n", encoding="utf-8"
        )
        (tmp_path / "bad3.yaml").write_text("- a\n- b\n", encoding="utf-8")
        registry = PolicyRegistry(policy_dir=tmp_path)
        assert registry.resolve("x").pii_mode == "mask"
        assert registry.resolve("unknown").source == "default"

    def test_get_guard_is_fail_open_when_construction_fails(self, monkeypatch):
        import src.security.guard.guard as guard_module

        def explode():
            raise AttributeError("bad yaml")

        guard_module.get_guard.cache_clear()
        monkeypatch.setattr(guard_module, "AgentGuard", explode)
        try:
            noop = guard_module.get_guard()
            original = msgs("hello")
            assert noop.before(original) is original
            assert noop.before_text("p", "s") == ("p", "s")
            noop.after("m", None)
            assert noop.register_agent("x").key == "x"
            assert noop.status() == {"mode": "unavailable"}
        finally:
            guard_module.get_guard.cache_clear()

    def test_register_agent_is_fail_open(self, guard, monkeypatch):
        def explode(*_a, **_k):
            raise RuntimeError("boom")

        monkeypatch.setattr(guard.policies, "register", explode)
        assert guard.register_agent("x").group == "default"
        assert guard.status()["stats_since_start"]["guard_errors"] == 1


class TestPIIPrecision:
    def test_phone_requires_valid_ddd_and_ignores_year_ranges(self):
        assert mask_pii("tel (11) 99479-8464")[0] == "tel [PHONE]"
        for text in ("paginas 12 2023-2024", "(00) 1234-5678", "10 1234-5678"):
            assert mask_pii(text)[0] == text

    def test_bare_cpf_and_card_need_context(self):
        assert mask_pii("pedido 52998224725")[0] == "pedido 52998224725"
        assert mask_pii("cpf 52998224725")[0] == "cpf [CPF]"
        assert mask_pii("id 4111111111111111")[0] == "id 4111111111111111"
        assert mask_pii("cartao 4111111111111111")[0] == "cartao [CARD]"

    def test_email_regex_is_not_quadratic_on_long_runs(self):
        blob = "a" * 200_000
        started = time.perf_counter()
        assert mask_pii(blob)[0] == blob
        assert time.perf_counter() - started < 2.0


class TestShadowAndScope:
    def test_non_string_content_is_left_untouched(self, guard, monkeypatch):
        monkeypatch.setenv("AGENT_GUARD_MODE", "enforce")
        original = [{"role": "user", "content": [{"type": "text", "text": f"cpf {VALID_CPF}"}]}]
        assert guard.before(original) == original

    def test_before_text_returns_originals_when_unchanged(self, guard):
        assert guard.before_text(None, "") == (None, "")

    def test_unattributed_calls_are_not_budgeted_individually(self, guard, monkeypatch):
        monkeypatch.setenv("AGENT_GUARD_MODE", "enforce")
        monkeypatch.setenv("AGENT_GUARD_DAILY_USD_AGENT", "0.0001")
        guard.store.add("unattributed", "default", 5.0, 1, 1)
        assert guard.before(msgs("hello"))

    def test_attributed_agent_is_still_budgeted(self, guard, monkeypatch):
        monkeypatch.setenv("AGENT_GUARD_MODE", "enforce")
        monkeypatch.setenv("AGENT_GUARD_DAILY_USD_AGENT", "0.0001")
        guard.store.add("real_agent", "tenant-1", 5.0, 1, 1)
        with agent_context("real_agent", "tenant-1"), pytest.raises(GuardBlocked):
            guard.before(msgs("hello"))


class TestHotPath:
    def test_before_does_no_sqlite_io(self, guard, monkeypatch):
        guard.store.add("a1", "t1", 0.01, 1, 1)
        guard.store.flush()

        def no_disk(*_a, **_k):
            raise OSError("no disk")

        monkeypatch.setattr(sqlite3, "connect", no_disk)
        with agent_context("a1", "t1"):
            guard.before(msgs("hello"))
        assert "guard_errors" not in guard.status()["stats_since_start"]

    def test_ledger_persists_across_instances(self, tmp_path):
        path = str(tmp_path / "ledger.db")
        first = SpendStore(path)
        first.add("a1", "t1", 0.25, 10, 5)
        first.flush()
        assert SpendStore(path).total(agent_id="a1") == pytest.approx(0.25)

    def test_persistence_failure_keeps_in_memory_total(self, tmp_path, monkeypatch):
        store = SpendStore(str(tmp_path / "ledger.db"))

        def no_disk(*_a, **_k):
            raise OSError("no disk")

        monkeypatch.setattr(sqlite3, "connect", no_disk)
        store.add("a1", "t1", 0.5, 1, 1)
        store.flush()
        assert store.total(agent_id="a1") == pytest.approx(0.5)


class TestAsyncClients:
    def test_async_llm_clients_are_guarded(self, tmp_path, monkeypatch):
        import src.api.claude_client as claude
        import src.api.gemini_client as gemini

        monkeypatch.setenv("AGENT_GUARD_MODE", "enforce")
        g = AgentGuard(store=SpendStore(str(tmp_path / "g.db")))
        monkeypatch.setattr(claude, "get_guard", lambda: g)
        monkeypatch.setattr(gemini, "get_guard", lambda: g)
        monkeypatch.delenv("CLAUDE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        for client in (claude.ClaudeClient(), gemini.GeminiClient()):
            result = asyncio.run(client.generate(f"cpf {VALID_CPF}"))
            assert "[CPF]" in result["content"] and VALID_CPF not in result["content"]
