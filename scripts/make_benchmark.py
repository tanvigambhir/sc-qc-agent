"""Build the benchmark: N corrupted copies of the clean dataset + an answer key.

Each copy gets 0, 1 or 2 bugs (default ~25% / 50% / 25%). Dataset IDs are
shuffled so filenames reveal nothing about content.

    python scripts/make_benchmark.py --n 40 --out benchmark/
    python scripts/make_benchmark.py --source synthetic --out benchmark_synth/  # offline
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qcagent.bugs import BUG_TYPES, INJECTORS  # noqa: E402
from qcagent.data import load_clean  # noqa: E402

# Fixed application order so bugs compose sensibly (e.g. the stale duplicate
# column from case_collision is made last, from already-corrupted data).
ORDER = ["sample_swap", "celltype_mislabel", "low_quality_cells",
         "batch_patient_confound", "case_collision"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--source", default="pbmc3k", choices=["pbmc3k", "synthetic"])
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--p", default="0.25,0.5,0.25", help="P(0 bugs),P(1),P(2)")
    ap.add_argument("--out", default="benchmark")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    clean = load_clean(args.source, seed=args.seed)
    p = np.array([float(x) for x in args.p.split(",")])

    # Balanced bug counts: cycle through types so each type appears ~equally.
    n_bugs = rng.choice([0, 1, 2], size=args.n, p=p / p.sum())
    used = {t: 0 for t in BUG_TYPES}
    key = {}
    ids = rng.permutation(args.n)
    for i in range(args.n):
        chosen = []
        while len(chosen) < n_bugs[i]:
            # least-used type so far, random tie-break
            cands = [t for t in BUG_TYPES if t not in chosen]
            low = min(used[t] for t in cands)
            t = str(rng.choice([t for t in cands if used[t] == low]))
            chosen.append(t)
            used[t] += 1
        a = clean.copy()
        injected = []
        for t in sorted(chosen, key=ORDER.index):
            a, details = INJECTORS[t](a, rng)
            injected.append({"type": t, **details})
        did = f"ds{ids[i]:03d}"
        a.write_h5ad(out / f"{did}.h5ad")
        key[did] = {"bugs": injected, "source": args.source}

    meta = {"source": args.source, "seed": args.seed, "n": args.n,
            "bug_types": {k: {"origin": v[0], "dedicated_tool": v[1]}
                          for k, v in BUG_TYPES.items()}}
    (out / "answer_key.json").write_text(json.dumps(
        {"meta": meta, "datasets": dict(sorted(key.items()))}, indent=2))
    counts = {t: sum(any(b["type"] == t for b in v["bugs"]) for v in key.values())
              for t in BUG_TYPES}
    print(f"Wrote {args.n} datasets to {out}/ ({sum(n_bugs == 0)} clean). Bug counts: {counts}")


if __name__ == "__main__":
    main()
