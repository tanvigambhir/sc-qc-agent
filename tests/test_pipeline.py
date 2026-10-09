"""Offline tests: tools catch injected bugs, the agent loop works, scoring works.

Run: pytest -q   (uses the synthetic dataset; no network, no API key)
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qcagent import bugs as B  # noqa: E402
from qcagent import tools as T  # noqa: E402
from qcagent.agent import parse_report, run_agent, run_rules  # noqa: E402
from qcagent.data import load_clean  # noqa: E402
from qcagent.llm import Reply, ScriptedClient  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from evaluate import unsupported_numbers  # noqa: E402


@pytest.fixture(scope="module")
def clean():
    return load_clean("synthetic", seed=0)


def test_clean_data_triggers_nothing(clean):
    assert run_rules(clean)["bugs"] == []


@pytest.mark.parametrize("bug", list(B.INJECTORS))
def test_each_bug_is_detectable(clean, bug):
    a, _ = B.INJECTORS[bug](clean, np.random.default_rng(7))
    assert [b["type"] for b in run_rules(a)["bugs"]] == [bug]


def test_tool_errors_are_text(clean):
    assert T.call_tool(clean, "compare_groups", {"column": "nope"}).startswith("ERROR")
    assert T.call_tool(clean, "not_a_tool", {}).startswith("ERROR")
    assert T.call_tool(clean, "compare_groups", {"bad": 1}).startswith("ERROR")


def test_outputs_are_capped(clean):
    for name in T.TOOLS:
        args = {"column": "sample"} if name == "compare_groups" else {}
        if name == "check_label_consistency":
            args = {"col_a": "batch", "col_b": "patient"}
        assert len(T.call_tool(clean, name, args)) <= T.MAX_CHARS


def test_parse_report_handles_prose():
    bugs, err = parse_report('Thinking {not json}. Final:\n{"bugs": [{"type": "case_collision"}]}')
    assert err is None and bugs[0]["type"] == "case_collision"
    assert parse_report("no json here")[1] is not None


def _call(name, **args):
    return {"id": name + "1", "name": name, "args": args}


def test_tools_condition_loop(clean):
    client = ScriptedClient([
        Reply("", [_call("find_case_collisions")], 10, 5),
        Reply('{"bugs": []}', [], 10, 5),
    ])
    log = run_agent(client, clean, "tools")
    assert log["error"] is None and log["bugs"] == []
    assert [c["name"] for c in log["tool_calls"]] == ["find_case_collisions"]
    assert log["in_tokens"] == 20


def test_verify_drops_unverified_and_refuted(clean):
    draft = ('{"bugs": [{"type": "low_quality_cells", "evidence": "x"},'
             ' {"type": "sample_swap", "evidence": "y"}]}')
    final = ('{"bugs": [{"type": "low_quality_cells", "confirmed": true},'
             ' {"type": "sample_swap", "confirmed": false}]}')
    # verified with a tool call: keeps only the confirmed bug
    c1 = ScriptedClient([Reply(draft), Reply("", [_call("check_qc_metrics")]), Reply(final)])
    log = run_agent(c1, clean, "tools_verify")
    assert [b["type"] for b in log["bugs"]] == ["low_quality_cells"]
    # "confirmed" without any verification-phase tool call: dropped as unverified
    c2 = ScriptedClient([Reply(draft), Reply(final)])
    log = run_agent(c2, clean, "tools_verify")
    assert log["bugs"] == [] and [b["type"] for b in log["unverified"]] == ["low_quality_cells"]


def test_step_cap(clean):
    client = ScriptedClient([Reply("", [_call("summarize_metadata")])] * 3 + [Reply('{"bugs": []}')])
    log = run_agent(client, clean, "tools", max_steps=3)
    assert log["hit_step_cap"] and len(log["tool_calls"]) == 3


def test_no_tools_condition(clean):
    log = run_agent(ScriptedClient([Reply('{"bugs": [{"type": "case_collision"}]}')]),
                    clean, "no_tools")
    assert log["tool_calls"] == [] and "context_shown" in log


def test_unsupported_numbers():
    src = "Flagged cells: 232 of 2600 (8.9%). frac 0.861"
    assert unsupported_numbers("232 cells (8.9%), 86% XIST+", src) == []
    assert unsupported_numbers("517 cells flagged", src) == ["517"]


def test_empty_reply_gets_one_nudge(clean):
    client = ScriptedClient([
        Reply("", [_call("check_qc_metrics")]),
        Reply("", []),                       # empty final answer
        Reply('{"bugs": [{"type": "low_quality_cells"}]}'),
    ])
    log = run_agent(client, clean, "tools")
    assert log["empty_nudges"] == 1
    assert [b["type"] for b in log["bugs"]] == ["low_quality_cells"]
