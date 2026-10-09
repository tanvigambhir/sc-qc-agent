"""Score runs against the answer key; write tables, plots and a failure dump.

    python scripts/evaluate.py --runs results/runs.jsonl --benchmark benchmark --out results/

Outputs in --out:
  summary.md            headline table + per-bug-type table (paste into README)
  metrics.csv           one row per model x condition
  by_bug_type.csv       detection per bug type
  fig_detection.png     detection & false-alarm rate by condition
  fig_by_bug_type.png   detection per bug type
  failures.md           every missed bug / false alarm with its tool trace,
                        with a blank category line for manual error analysis
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qcagent.bugs import BUG_TYPES  # noqa: E402

# Which tool would directly reveal each bug type (used for tool-coverage stats).
RELEVANT_TOOL = {
    "sample_swap": "compare_groups",
    "batch_patient_confound": "check_label_consistency",
    "case_collision": "find_case_collisions",
    "celltype_mislabel": "run_marker_check",
    "low_quality_cells": "check_qc_metrics",
}
COND_ORDER = ["no_tools", "tools", "tools_verify", "rules"]

NUM = re.compile(r"(?<![A-Za-z_\d.])(\d+(?:\.\d+)?)(%?)(?![A-Za-z_\d])")


def numbers(text: str):
    out = []
    for m in NUM.finditer(text or ""):
        v = float(m.group(1))
        out.append((v, m.group(2) == "%"))
    return out


def supported(x, is_pct, source_vals):
    """Is number x (optionally a percent) present in tool outputs, allowing rounding?"""
    cands = [x, x / 100] if is_pct else [x, x / 100, x * 100]
    for c in cands:
        for v in source_vals:
            if abs(c - v) <= max(0.05 * abs(v), 0.006):
                return True
    return False


def unsupported_numbers(evidence, source_text):
    src = [v for v, _ in numbers(source_text)]
    bad = []
    for x, pct in numbers(evidence):
        if not pct and x < 10 and float(x).is_integer():
            continue  # small integers (counts like "2 labels") are too common to judge
        if not supported(x, pct, src):
            bad.append(f"{x:g}{'%' if pct else ''}")
    return bad


def score_run(r, truth):
    found = {b["type"] for b in r.get("bugs", [])}
    t = set(truth)
    source = r.get("context_shown", "") + "\n".join(c["output"] for c in r["tool_calls"])
    unsup = {b["type"]: unsupported_numbers(str(b.get("evidence", "")), source)
             for b in r.get("bugs", [])}
    called = {c["name"] for c in r["tool_calls"]}
    return {
        "tp": len(found & t), "fn": len(t - found), "fp": len(found - t),
        "clean": not t, "false_alarm": (not t) and bool(found), "exact": found == t,
        "n_reported": len(found),
        "n_unsupported": sum(1 for v in unsup.values() if v), "unsup": unsup,
        "missed": sorted(t - found), "spurious": sorted(found - t),
        "called_relevant": {bt: RELEVANT_TOOL[bt] in called for bt in t},
        "n_calls": len(r["tool_calls"]),
        "tokens": r.get("in_tokens", 0) + r.get("out_tokens", 0),
        "parse_error": bool(r.get("parse_error")), "error": bool(r.get("error")),
        "step_cap": bool(r.get("hit_step_cap")),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="results/runs.jsonl")
    ap.add_argument("--benchmark", default="benchmark")
    ap.add_argument("--out", default="results")
    ap.add_argument("--matched", action="store_true",
                    help="compare conditions only on datasets every condition completed")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    key = json.loads((Path(args.benchmark) / "answer_key.json").read_text())["datasets"]
    runs = {}
    for line in Path(args.runs).read_text().splitlines():
        r = json.loads(line)
        runs[(r["dataset"], r["model"], r["condition"])] = r  # last write wins
    runs = list(runs.values())

    # Runs that crashed (timeouts, server errors) produced no report. Scoring
    # them would count infrastructure failures as missed bugs, so drop them
    # and report how many were dropped.
    errored = [r for r in runs if r.get("error")]
    runs = [r for r in runs if not r.get("error")]
    excluded = defaultdict(int)
    for r in errored:
        excluded[(r["model"], r["condition"])] += 1

    # --matched: per model, keep only datasets where every condition finished,
    # so conditions are compared on identical datasets.
    if args.matched:
        done = defaultdict(set)
        for r in runs:
            done[(r["model"], r["dataset"])].add(r["condition"])
        conds_per_model = defaultdict(set)
        for r in runs:
            conds_per_model[r["model"]].add(r["condition"])
        runs = [r for r in runs
                if done[(r["model"], r["dataset"])] == conds_per_model[r["model"]]]

    rows, type_rows, fails = [], [], []
    verify_rows = []
    groups = defaultdict(list)
    for r in runs:
        truth = [b["type"] for b in key[r["dataset"]]["bugs"]]
        s = score_run(r, truth)
        groups[(r["model"], r["condition"])].append((r, s, truth))
        if r["condition"] == "tools_verify" and "draft_bugs" in r:
            draft = {b["type"] for b in r["draft_bugs"]}
            final = {b["type"] for b in r.get("bugs", [])}
            for bt in draft - final:
                verify_rows.append({"model": r["model"], "dropped": bt,
                                    "was_real": bt in truth})

    for (model, cond), items in groups.items():
        S = [s for _, s, _ in items]
        tp, fn, fp = (sum(s[k] for s in S) for k in ("tp", "fn", "fp"))
        clean = [s for s in S if s["clean"]]
        rep = sum(s["n_reported"] for s in S)
        rows.append({
            "model": model, "condition": cond, "n_datasets": len(S),
            "detection_rate": tp / (tp + fn) if tp + fn else float("nan"),
            "false_alarm_rate_clean": (sum(s["false_alarm"] for s in clean) / len(clean)
                                       if clean else float("nan")),
            "precision": tp / (tp + fp) if tp + fp else float("nan"),
            "spurious_per_dataset": fp / len(S),
            "exact_match": sum(s["exact"] for s in S) / len(S),
            "unsupported_evidence_rate": (sum(s["n_unsupported"] for s in S) / rep
                                          if rep else float("nan")),
            "mean_tool_calls": sum(s["n_calls"] for s in S) / len(S),
            "mean_tokens": sum(s["tokens"] for s in S) / len(S),
            "parse_error_rate": sum(s["parse_error"] for s in S) / len(S),
            "step_cap_rate": sum(s["step_cap"] for s in S) / len(S),
            "runs_excluded_errors": excluded[(model, cond)],
        })
        for bt, (origin, has_tool) in BUG_TYPES.items():
            with_bt = [(r, s) for r, s, t in items if bt in t]
            if not with_bt:
                continue
            type_rows.append({
                "model": model, "condition": cond, "bug_type": bt,
                "dedicated_tool": has_tool, "n": len(with_bt),
                "detected": sum(bt not in s["missed"] for _, s in with_bt) / len(with_bt),
                "relevant_tool_called": (sum(s["called_relevant"][bt] for _, s in with_bt)
                                         / len(with_bt)) if cond != "no_tools" else float("nan"),
            })
        for r, s, truth in items:
            if s["missed"] or s["spurious"]:
                fails.append((model, cond, r, s, truth))

    order = {c: i for i, c in enumerate(COND_ORDER)}
    m = pd.DataFrame(rows).sort_values(["model", "condition"],
                                        key=lambda c: c.map(order) if c.name == "condition" else c)
    bt = pd.DataFrame(type_rows)
    m.to_csv(out / "metrics.csv", index=False)
    bt.to_csv(out / "by_bug_type.csv", index=False)

    # ------------------------------------------------------------ summary.md
    show = m[["model", "condition", "n_datasets", "detection_rate", "false_alarm_rate_clean",
              "precision", "exact_match", "unsupported_evidence_rate", "mean_tool_calls",
              "mean_tokens", "runs_excluded_errors"]].copy()
    md = ["# Results\n", f"Benchmark: `{args.benchmark}`, {len(key)} datasets."
          + (" Matched mode: each model's conditions are compared on the same datasets."
             if args.matched else "") + "\n",
          f"Runs excluded for crashing (timeouts/server errors): {len(errored)}."
          " `n_datasets` counts only completed runs.\n",
          "## Headline metrics\n", show.round(3).to_markdown(index=False), "\n"]
    if not bt.empty:
        piv = bt.pivot_table(index=["bug_type", "dedicated_tool"],
                             columns=["model", "condition"], values="detected")
        md += ["## Detection rate by bug type\n", piv.round(2).to_markdown(), "\n"]
    if verify_rows:
        v = pd.DataFrame(verify_rows)
        md += ["## What self-verification removed\n",
               "Bugs in the draft report that the verification phase dropped. "
               "`was_real=True` means verification threw away a correct finding.\n",
               v.groupby(["model", "was_real"]).size().rename("count").to_frame()
               .to_markdown(), "\n"]
    md += ["## Metric definitions\n",
           "- detection_rate: injected bugs whose type was reported / all injected bugs",
           "- false_alarm_rate_clean: clean datasets with >=1 reported bug / clean datasets",
           "- precision: correct reported bugs / all reported bugs",
           "- exact_match: datasets where the reported set equals the injected set",
           "- unsupported_evidence_rate: reported bugs whose evidence cites a number that "
           "appears in no tool output the model received (5% rounding tolerance; small "
           "integers ignored). An automatic upper bound on hallucinated evidence: "
           "correctly derived numbers (e.g. a percent computed from two counts) can be "
           "flagged, so spot-check before quoting it."]
    (out / "summary.md").write_text("\n".join(md))

    # ----------------------------------------------------------- failures.md
    fl = ["# Failed runs (for manual error analysis)\n",
          "For each run, fill in a category, e.g.: never called the relevant tool / "
          "called it but misread output / reasoned correctly but too cautious / "
          "hallucinated evidence / wrong bug type / format or parse failure / step cap.\n"]
    for model, cond, r, s, truth in sorted(fails, key=lambda x: (x[0], x[1], x[2]["dataset"])):
        fl.append(f"## {r['dataset']} | {model} | {cond}")
        fl.append(f"- truth: {truth}\n- reported: {[b['type'] for b in r.get('bugs', [])]}")
        fl.append(f"- missed: {s['missed']}  spurious: {s['spurious']}")
        if r.get("unverified"):
            fl.append(f"- dropped as unverified: {[b['type'] for b in r['unverified']]}")
        trace = [f"{c['phase']}:{c['name']}({json.dumps(c['args'])})" for c in r["tool_calls"]]
        fl.append(f"- tool calls ({len(trace)}): " + (" -> ".join(trace) or "none"))
        for b in r.get("bugs", []):
            u = s["unsup"].get(b["type"])
            fl.append(f"- evidence [{b['type']}]: {b.get('evidence', '')}"
                      + (f"  **unsupported numbers: {u}**" if u else ""))
        if r.get("error") or r.get("parse_error"):
            fl.append(f"- error: {r.get('error') or r.get('parse_error')}")
        fl.append("- **category:** ____\n")
    (out / "failures.md").write_text("\n".join(fl))

    # ----------------------------------------------------------------- plots
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    models = list(dict.fromkeys(m["model"]))
    conds = [c for c in COND_ORDER if c in set(m["condition"])]
    palette = ["#4C72B0", "#DD8452", "#55A868", "#8172B3"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, metric, title in zip(axes, ["detection_rate", "false_alarm_rate_clean"],
                                 ["Detection rate (higher is better)",
                                  "False alarms on clean data (lower is better)"]):
        w = 0.8 / max(len(models), 1)
        for i, mod in enumerate(models):
            sub = m[m["model"] == mod].set_index("condition")
            xs = [j for j, c in enumerate(conds) if c in sub.index]
            ys = [sub.loc[c, metric] for c in conds if c in sub.index]
            bars = ax.bar([x + (i - (len(models) - 1) / 2) * w for x in xs], ys, w,
                          label=mod, color=palette[i % 4])
            ax.bar_label(bars, fmt="%.2f", fontsize=8, padding=2)
        ax.set_xticks(range(len(conds)), conds)
        ax.set_ylim(0, 1.3)
        ax.set_title(title, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False, fontsize=8, loc="upper left", ncol=len(models))
    fig.tight_layout()
    fig.savefig(out / "fig_detection.png", dpi=160)
    plt.close(fig)

    if not bt.empty:
        bt["series"] = bt["model"] + " / " + bt["condition"]
        series = list(dict.fromkeys(bt.sort_values(
            ["model", "condition"], key=lambda c: c.map(order) if c.name == "condition" else c
        )["series"]))
        types = list(BUG_TYPES)
        fig, ax = plt.subplots(figsize=(10, 4))
        w = 0.8 / len(series)
        cmap = plt.get_cmap("tab10")
        for i, srs in enumerate(series):
            sub = bt[bt["series"] == srs].set_index("bug_type")
            ys = [sub.loc[t, "detected"] if t in sub.index else 0 for t in types]
            ax.bar([j + (i - (len(series) - 1) / 2) * w for j in range(len(types))], ys, w,
                   label=srs, color=cmap(i))
        labels = [t + ("" if BUG_TYPES[t][1] else "\n(no dedicated tool)") for t in types]
        ax.set_xticks(range(len(types)), labels, fontsize=8)
        ax.set_ylim(0, 1.3)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_ylabel("detection rate")
        ax.set_title("Detection by bug type", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False, fontsize=7, ncol=4, loc="upper center")
        fig.tight_layout()
        fig.savefig(out / "fig_by_bug_type.png", dpi=160)
        plt.close(fig)

    print(show.round(3).to_string(index=False))
    print(f"\nWrote summary.md, metrics.csv, by_bug_type.csv, failures.md and plots to {out}/")


if __name__ == "__main__":
    main()
