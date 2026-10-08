"""Run every (model x condition x dataset) and append one JSON line per run.

Resumable: runs already in the output file are skipped, so a crash or rate
limit costs nothing. Delete the file to start over.

    python scripts/run_experiment.py --models rules                # free sanity check
    python scripts/run_experiment.py --models claude --limit 3     # cheap smoke test
    python scripts/run_experiment.py --models claude,qwen          # full experiment
"""
import argparse
import json
import sys
from pathlib import Path

import anndata as ad

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qcagent.agent import CONDITIONS, run_agent, run_rules  # noqa: E402
from qcagent.llm import make_client  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default="benchmark")
    ap.add_argument("--models", default="claude,qwen", help="comma list: claude,qwen,rules")
    ap.add_argument("--conditions", default=",".join(CONDITIONS))
    ap.add_argument("--out", default="results/runs.jsonl")
    ap.add_argument("--limit", type=int, default=None, help="only first N datasets")
    ap.add_argument("--max-steps", type=int, default=15)
    args = ap.parse_args()

    bench = Path(args.benchmark)
    key = json.loads((bench / "answer_key.json").read_text())["datasets"]
    ids = sorted(key)[: args.limit] if args.limit else sorted(key)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            if not r.get("error"):
                done.add((r["dataset"], r["model"], r["condition"]))

    for model in args.models.split(","):
        conds = ["rules"] if model == "rules" else args.conditions.split(",")
        client = None if model == "rules" else make_client(model)
        for cond in conds:
            for did in ids:
                if (did, model, cond) in done:
                    continue
                adata = ad.read_h5ad(bench / f"{did}.h5ad")
                if model == "rules":
                    log = run_rules(adata)
                else:
                    log = run_agent(client, adata, cond, max_steps=args.max_steps)
                log.update(dataset=did, model=model,
                           model_id=getattr(client, "model", "rules"))
                with out.open("a") as f:
                    f.write(json.dumps(log, default=str) + "\n")
                found = [b["type"] for b in log.get("bugs", [])]
                truth = [b["type"] for b in key[did]["bugs"]]
                flag = f" ERROR {log['error']}" if log.get("error") else ""
                print(f"{model:6s} {cond:12s} {did}  truth={truth}  found={found}  "
                      f"calls={len(log['tool_calls'])}{flag}", flush=True)


if __name__ == "__main__":
    main()
