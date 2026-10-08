# Can a tool-using LLM agent catch silent errors in single-cell data?

**Question.** Single-cell datasets often carry silent metadata errors: swapped
sample labels, a batch column that is secretly the patient column, duplicate
columns whose names differ only by case. They don't crash anything; they just
make the analysis wrong. Can an LLM agent with QC tools find them, and does
forcing the agent to verify its own findings help?

Each bug type is modeled on an error I hit in real analyses:

| Bug type | Real-life origin | Dedicated tool? |
|---|---|---|
| `sample_swap` | ~70% of a CAR-T sample mislabeled | **No** (must reason from `compare_groups`) |
| `batch_patient_confound` | batch column was a relabeling of patient | `check_label_consistency` |
| `case_collision` | `numericMeta.All` vs `numericMeta.ALL` | `find_case_collisions` |
| `celltype_mislabel` | cluster annotation error | `run_marker_check` |
| `low_quality_cells` | unfiltered damaged cells | `check_qc_metrics` |

## Setup

**Data.** pbmc3k (Scanpy), 2,638 PBMCs from one donor. Because it has no
patient/sample/batch structure, I add a synthetic study design: 6 patients ×
2 timepoints = 12 samples, processed in 3 batches that each mix 4 patients.
Sex-linked genes (XIST, RPS4Y1) are simulated per cell from the true patient's
sex so that sample swaps leave a biological trace, as they do in real data.

**Benchmark.** `scripts/make_benchmark.py` makes N corrupted copies
(default 40: ~25% clean, ~50% one bug, ~25% two bugs, bug types balanced) and an
`answer_key.json`. All bugs act on `.obs`, so each copy stores only marker genes.

**Tools** (`qcagent/tools.py`). Six plain Python functions returning short text
(≤2,500 chars). They report facts and flags but never name a bug type.

**Conditions** (`qcagent/agent.py`):

1. `no_tools`: one call; the model sees only the `summarize_metadata()` text.
2. `tools`: agent loop with all six tools, max 15 steps.
3. `tools_verify`: condition 2, then a verification phase. **Rule, fixed before
   running:** the agent must re-check each suspected bug with ≥1 new tool call
   and mark it `confirmed` true/false. A bug is kept only if it is confirmed
   *and* the verification phase contained at least one tool call.

Every condition ends in the same JSON report, scored automatically.
A non-LLM rule-based agent (`rules`) runs the same tools with fixed thresholds
as a reference for "is this bug detectable from the tool outputs at all?"

**Models.** Claude (`claude-sonnet-5-5` by default, set `QC_ANTHROPIC_MODEL`)
and Qwen2.5-7B-Instruct via Ollama (`QC_OLLAMA_MODEL`). Qwen runs at temperature 0; Claude runs at its default sampling settings.

**Metrics.** Detection rate, false-alarm rate on clean datasets, precision,
exact-match rate, unsupported-evidence rate (reported evidence citing numbers
that appear in no tool output the model received; an automatic upper bound on
hallucinated evidence), tool calls and tokens per dataset.

## Prediction (write before running)

> _Condition 3 vs 2, false alarms:_ Fewer. Requiring a confirming tool call before a bug is reported should filter out guesses that the tool outputs don't support.
> _Condition 3 vs 2, detection:_ About the same. Verification can only remove findings, and I expect the model to rarely reverse a draft conclusion, so few real bugs should be dropped.
> _Which bug type will be hardest, and why:_ `low_quality_cells`. Spotting damaged cells means judging QC thresholds across several metrics, and the clean data already contains 25 high-count outlier cells that could blur the line between a real problem and normal variation.
## Results

> TODO after running. Paste `results/summary.md` tables and the two figures:
> `results/fig_detection.png`, `results/fig_by_bug_type.png`.

Background noise on clean pbmc3k (from `scripts/inspect_clean.py`): TODO

## Failure modes

> TODO. Categorize 5–10 runs from `results/failures.md`
> (never called relevant tool / misread output / too cautious / hallucinated
> evidence / wrong bug type / format failure / step cap).

## Limitations

- Patient/sample/batch structure and sex-gene expression are simulated on a
  single-donor dataset. Next step: repeat on a real multi-donor dataset.
- Four of five bug types have a tool built to expose them, so high detection
  there partly measures tool design. `sample_swap` is the one type that
  requires the agent to combine evidence; results are reported per type.
- Injected bugs are cleaner than real ones (e.g. a perfect 1:1 batch/patient map).
- The unsupported-evidence metric can flag correctly derived numbers (a percent
  computed from two counts); failures were spot-checked by hand.
- One run per condition; no variance estimate (Claude is not run at temperature 0, so reruns can differ).

## Reproduce

```bash
pip install -r requirements.txt
pytest -q                                   # offline tests, synthetic data

python scripts/inspect_clean.py             # tool outputs on clean pbmc3k
python scripts/make_benchmark.py --n 40     # -> benchmark/ + answer_key.json

python scripts/run_experiment.py --models rules                 # free reference
export ANTHROPIC_API_KEY=...
python scripts/run_experiment.py --models claude --limit 3      # smoke test
ollama pull qwen2.5:7b-instruct
python scripts/run_experiment.py --models claude,qwen           # full run, resumable
python scripts/evaluate.py                                      # -> results/
```

No network? `--source synthetic` on `make_benchmark.py` builds an offline
stand-in with the same structure. Don't report its numbers as pbmc3k results.

## Layout

```
qcagent/data.py      clean data + synthetic study design
qcagent/tools.py     the six QC tools + JSON schemas
qcagent/bugs.py      bug injectors
qcagent/llm.py       Anthropic / Ollama clients, one interface
qcagent/agent.py     agent loop, 3 conditions, verification rule, rule-based reference
scripts/             make_benchmark, run_experiment, evaluate, inspect_clean
tests/               offline tests (tools catch each bug; loop, verify, step cap, scoring)
```
