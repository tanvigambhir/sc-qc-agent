"""Print every tool's output on the CLEAN dataset. Run this first.

Anything a tool flags here is background noise the agent will also see on
every benchmark copy (e.g. CD4 vs CD8 T-cell marker overlap in real pbmc3k).
Record it in the README so false alarms can be interpreted.

    python scripts/inspect_clean.py               # real pbmc3k
    python scripts/inspect_clean.py synthetic     # offline
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qcagent.agent import run_rules  # noqa: E402
from qcagent.data import load_clean  # noqa: E402
from qcagent.tools import call_tool  # noqa: E402

source = sys.argv[1] if len(sys.argv) > 1 else "pbmc3k"
a = load_clean(source)
for name, args in [("summarize_metadata", {}), ("check_qc_metrics", {}),
                   ("find_case_collisions", {}),
                   ("check_label_consistency", {"col_a": "batch", "col_b": "patient"}),
                   ("compare_groups", {"column": "sample"}),
                   ("run_marker_check", {"cluster_col": "cell_type"})]:
    print(f"\n=== {name}({args}) ===\n{call_tool(a, name, args)}")
print(f"\nRule-based reference on clean data reports: {run_rules(a)['bugs'] or 'nothing'}")
