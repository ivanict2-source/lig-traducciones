from types import SimpleNamespace

import pytest
import yaml

from llm import LLM, BudgetExceeded, RefusalError


class FakeMessages:
    def __init__(self, stop_reason="end_turn", text="hola", inp=1000, out=500):
        self.calls = []
        self.stop_reason, self.text, self.inp, self.out = stop_reason, text, inp, out

    def create(self, **kw):
        self.calls.append(kw)
        return SimpleNamespace(
            stop_reason=self.stop_reason,
            content=[SimpleNamespace(type="text", text=self.text)],
            usage=SimpleNamespace(input_tokens=self.inp, output_tokens=self.out,
                                  cache_read_input_tokens=0, cache_creation_input_tokens=0),
        )


def make(tmp_path, monthly=30.0, per_task=1.5, **fake):
    cfg = yaml.safe_load(open("config/budget.yaml", encoding="utf-8"))
    cfg["limits"].update(monthly_usd=monthly, per_task_usd=per_task)
    cfg["ledger"] = "ledger.csv"
    cfg["cache"]["dir"] = "cache"
    p = tmp_path / "budget.yaml"
    p.write_text(yaml.safe_dump(cfg))
    msgs = FakeMessages(**fake)
    client = SimpleNamespace(messages=msgs, beta=SimpleNamespace(messages=msgs))
    return LLM(client=client, config_path=p, root=tmp_path), msgs


@pytest.fixture(autouse=True)
def _cwd(monkeypatch):
    from common import ROOT
    monkeypatch.chdir(ROOT)


def test_cost_and_ledger(tmp_path):
    llm, msgs = make(tmp_path)
    r = llm.run("metadata", "sistema", "usuario", target="x", max_tokens=500)
    # haiku: 1000*0.10/1e6 + 500*0.50/1e6
    assert r.cost_usd == pytest.approx(0.00035)
    assert (tmp_path / "ledger.csv").read_text().count("\n") == 2
    assert msgs.calls[0]["model"] == "claude-haiku-5-5"
    assert "fallbacks" not in msgs.calls[0]


def test_cache_hit_costs_nothing(tmp_path):
    llm, msgs = make(tmp_path)
    llm.run("metadata", "s", "u", max_tokens=500)
    r2 = llm.run("metadata", "s", "u", max_tokens=500)
    assert r2.cached and r2.cost_usd == 0 and len(msgs.calls) == 1


def test_per_task_budget(tmp_path):
    llm, _ = make(tmp_path, per_task=0.001)
    with pytest.raises(BudgetExceeded):
        llm.run("draft", "s", "u")


def test_monthly_budget(tmp_path):
    llm, _ = make(tmp_path, monthly=0.0001)
    with pytest.raises(BudgetExceeded):
        llm.run("metadata", "s", "u", max_tokens=500)


def test_refusal_raises(tmp_path):
    llm, _ = make(tmp_path, stop_reason="refusal")
    with pytest.raises(RefusalError):
        llm.run("draft", "s", "u", max_tokens=1000)


def test_sonnet_uses_server_fallback_and_escalation(tmp_path):
    llm, msgs = make(tmp_path)
    llm.run("draft", "s", "u", max_tokens=1000)
    assert msgs.calls[0]["fallbacks"] == "default"
    assert llm.model_for("draft", escalate=True) == "claude-opus-5-5"
