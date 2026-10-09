"""The agent loop and the three experimental conditions.

  no_tools      one call; the model sees only summarize_metadata() output
  tools         agent loop with all QC tools, capped at MAX_STEPS
  tools_verify  `tools`, then a verification phase (rule below)

SELF-VERIFICATION RULE (fixed before any results were run):
  After the draft report, the harness asks the agent to re-check every
  suspected bug with at least one NEW tool call and mark each confirmed or
  rejected. A bug is kept only if (a) the agent marks it "confirmed": true and
  (b) the agent made >= 1 tool call during the verification phase. Bugs marked
  confirmed with zero verification-phase tool calls are dropped and logged as
  "unverified". The harness does not check WHICH tool was called; that is
  analysed afterwards in evaluate.py.

Every run returns a log dict with all tool calls (name, args, output), token
counts and the parsed report, so evaluation never has to re-run the model.
"""
from __future__ import annotations

import json
import re
import time

from .bugs import BUG_TYPES
from .tools import TOOL_SPECS, call_tool, summarize_metadata

MAX_STEPS = 15
CONDITIONS = ["no_tools", "tools", "tools_verify"]

REPORT_FORMAT = (
    "End with ONLY a JSON object, no prose after it:\n"
    '{"bugs": [{"type": <one of ' + json.dumps(list(BUG_TYPES)) + '>, '
    '"columns": [<metadata columns involved>], '
    '"evidence": "<specific numbers or values you observed>"}]}\n'
    'Use {"bugs": []} if the dataset looks clean. Report each bug type at most once.'
)

SYSTEM = (
    "You are a careful single-cell data QC analyst. A dataset may contain 0, 1 or 2 "
    "silent data errors in its metadata. Possible error types:\n"
    "- sample_swap: some cells carry the wrong sample/patient label\n"
    "- batch_patient_confound: the batch column is just a relabeling of patient\n"
    "- case_collision: two columns whose names differ only by letter case\n"
    "- celltype_mislabel: a cell-type label is attached to the wrong cluster\n"
    "- low_quality_cells: damaged/low-quality cells were not filtered out\n"
    "Study design you can rely on: 6 patients x 2 timepoints = 12 samples; samples were "
    "processed in 3 batches, each mixing several patients; each patient has a recorded sex. "
    "Only report an error when you have concrete evidence. False alarms are costly.\n"
)


# ------------------------------------------------------------------ parsing
def parse_report(text: str) -> tuple[list, str | None]:
    """Extract the last JSON object with a "bugs" key. Returns (bugs, error)."""
    if not text:
        return [], "empty response"
    candidates = re.findall(r"\{.*\}", text, flags=re.S)
    for cand in reversed(candidates):
        # try progressively later starting braces to skip leading prose braces
        for start in [m.start() for m in re.finditer(r"\{", cand)]:
            try:
                obj = json.loads(cand[start:])
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and isinstance(obj.get("bugs"), list):
                bugs = [b for b in obj["bugs"] if isinstance(b, dict) and "type" in b]
                return bugs, None
    return [], "no parseable JSON report"


def _dedupe(bugs):
    seen, out = set(), []
    for b in bugs:
        t = str(b.get("type", "")).strip()
        if t in BUG_TYPES and t not in seen:
            seen.add(t)
            out.append({**b, "type": t})
    return out


# --------------------------------------------------------------- the loop
def _loop(client, adata, messages, log, phase, max_steps):
    """Run tool calls until the model answers in text or steps run out."""
    calls_this_phase = 0
    for _ in range(max_steps):
        r = client.chat(SYSTEM, messages, TOOL_SPECS)
        log["in_tokens"] += r.in_tokens
        log["out_tokens"] += r.out_tokens
        log["steps"] += 1
        messages.append({"role": "assistant", "content": r.text, "tool_calls": r.tool_calls})
        if not r.tool_calls:
            if not r.text.strip():
                # Empty reply: ask once for the report (tools off). Never fired for Claude.
                log["empty_nudges"] = log.get("empty_nudges", 0) + 1
                messages.append({"role": "user",
                                 "content": "Your last reply was empty. " + REPORT_FORMAT})
                r = client.chat(SYSTEM, messages, None)
                log["in_tokens"] += r.in_tokens
                log["out_tokens"] += r.out_tokens
                log["steps"] += 1
                messages.append({"role": "assistant", "content": r.text, "tool_calls": []})
            return r.text, calls_this_phase
        for tc in r.tool_calls:
            out = call_tool(adata, tc["name"], tc["args"])
            log["tool_calls"].append({"phase": phase, "name": tc["name"],
                                      "args": tc["args"], "output": out})
            messages.append({"role": "tool", "tool_call_id": tc["id"],
                             "name": tc["name"], "content": out})
            calls_this_phase += 1
    # out of steps: force a final answer with tools disabled
    messages.append({"role": "user", "content": "Step limit reached. " + REPORT_FORMAT})
    r = client.chat(SYSTEM, messages, None)
    log["in_tokens"] += r.in_tokens
    log["out_tokens"] += r.out_tokens
    log["steps"] += 1
    log["hit_step_cap"] = True
    messages.append({"role": "assistant", "content": r.text, "tool_calls": []})
    return r.text, calls_this_phase


def run_agent(client, adata, condition: str, max_steps: int = MAX_STEPS) -> dict:
    log = {"condition": condition, "tool_calls": [], "in_tokens": 0, "out_tokens": 0,
           "steps": 0, "hit_step_cap": False, "unverified": [], "error": None}
    t0 = time.time()
    try:
        if condition == "no_tools":
            summary = summarize_metadata(adata)
            log["context_shown"] = summary
            msg = ("Here is a summary of the dataset's metadata:\n\n" + summary +
                   "\n\nYou cannot run any analysis. Based on this summary alone, "
                   "identify any data errors. " + REPORT_FORMAT)
            r = client.chat(SYSTEM, [{"role": "user", "content": msg}], None)
            log.update(in_tokens=r.in_tokens, out_tokens=r.out_tokens, steps=1)
            final_text = r.text

        elif condition in ("tools", "tools_verify"):
            messages = [{"role": "user", "content":
                         "Investigate this dataset for data errors using the tools. "
                         "Call tools as needed, then give your report. " + REPORT_FORMAT}]
            final_text, _ = _loop(client, adata, messages, log, "investigate", max_steps)

            if condition == "tools_verify":
                draft, perr = parse_report(final_text)
                draft = _dedupe(draft)
                log["draft_bugs"] = draft
                if draft:
                    messages.append({"role": "user", "content":
                        "VERIFICATION STEP. For EACH suspected bug in your draft, call at least "
                        "one tool whose output would confirm or refute it. Then output the final "
                        "JSON, adding \"confirmed\": true or false to every bug. Drop nothing "
                        "silently; mark refuted bugs false. " + REPORT_FORMAT})
                    final_text, n_verify = _loop(client, adata, messages, log, "verify",
                                                 max_steps)
                    bugs, perr = parse_report(final_text)
                    kept = []
                    for b in _dedupe(bugs):
                        if b.get("confirmed") is True and n_verify > 0:
                            kept.append(b)
                        elif b.get("confirmed") is True:
                            log["unverified"].append(b)
                    log["raw_text"] = final_text
                    log["bugs"], log["parse_error"] = kept, perr
                    log["seconds"] = round(time.time() - t0, 1)
                    return log
        else:
            raise ValueError(f"unknown condition {condition!r}")

        bugs, perr = parse_report(final_text)
        log["raw_text"] = final_text
        log["bugs"], log["parse_error"] = _dedupe(bugs), perr
    except Exception as e:
        log["error"] = f"{type(e).__name__}: {e}"
        log.setdefault("bugs", [])
    log["seconds"] = round(time.time() - t0, 1)
    return log


# ------------------------------------------------- non-LLM reference agent
def run_rules(adata) -> dict:
    """Hand-written thresholds over the same tools. Not an LLM.

    Answers "is each bug detectable from tool outputs at all?" and gives a
    ceiling/sanity reference. Free to run, so it also checks the benchmark.
    """
    log = {"condition": "rules", "tool_calls": [], "in_tokens": 0, "out_tokens": 0,
           "steps": 0, "hit_step_cap": False, "unverified": [], "error": None}

    def call(name, **args):
        out = call_tool(adata, name, args)
        log["tool_calls"].append({"phase": "rules", "name": name, "args": args, "output": out})
        return out

    bugs = []
    o = adata.obs
    qc = call("check_qc_metrics")
    m = re.search(r"Flagged cells: (\d+) of (\d+)", qc)
    if m and int(m.group(1)) / int(m.group(2)) > 0.01:
        bugs.append({"type": "low_quality_cells", "columns": ["percent_mito", "n_genes"],
                     "evidence": m.group(0)})
    cc = call("find_case_collisions")
    if "collision group" in cc:
        bugs.append({"type": "case_collision", "columns": [], "evidence": cc.splitlines()[1]})
    lc = call("check_label_consistency", col_a="batch", col_b="patient")
    if "one-to-one mapping: True" in lc:
        bugs.append({"type": "batch_patient_confound", "columns": ["batch", "patient"],
                     "evidence": "batch is a one-to-one relabeling of patient"})
    mk = call("run_marker_check", cluster_col="cell_type")
    m = re.search(r"(\d+) of \d+ labels mismatch", mk)
    if m and int(m.group(1)) >= 2:  # a swap produces two mismatches
        bugs.append({"type": "celltype_mislabel", "columns": ["cell_type"],
                     "evidence": m.group(0)})
    call("compare_groups", column="sample")
    # sample swap: a sample whose recorded sex disagrees with >15% of its cells
    from .tools import _gene
    xist = _gene(adata, "XIST") > 0
    y = _gene(adata, "RPS4Y1") > 0
    for s, idx in o.groupby("sample").indices.items():
        sex = o["sex"].iloc[idx].mode()[0]
        wrong = (y[idx] if sex == "F" else xist[idx]).mean()
        if wrong > 0.15:
            bugs.append({"type": "sample_swap", "columns": ["sample"],
                         "evidence": f"{s}: {wrong:.0%} of cells express opposite-sex gene"})
            break
    log["bugs"] = _dedupe(bugs)
    log["parse_error"] = None
    return log
