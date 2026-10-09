# Results

Benchmark: `benchmark`, 40 datasets.

Runs excluded for crashing (timeouts/server errors): 8. `n_datasets` counts only completed runs.

## Headline metrics

| model   | condition    |   n_datasets |   detection_rate |   false_alarm_rate_clean |   precision |   exact_match |   unsupported_evidence_rate |   mean_tool_calls |   mean_tokens |   runs_excluded_errors |
|:--------|:-------------|-------------:|-----------------:|-------------------------:|------------:|--------------:|----------------------------:|------------------:|--------------:|-----------------------:|
| claude  | no_tools     |           40 |            0.605 |                        0 |       1     |         0.575 |                       0.038 |             0     |       1443.95 |                      0 |
| claude  | tools        |           40 |            1     |                        0 |       1     |         1     |                       0     |             6.475 |       8404.98 |                      0 |
| claude  | tools_verify |           40 |            1     |                        0 |       1     |         1     |                       0.023 |             8.425 |      16932.5  |                      0 |
| qwen    | no_tools     |           40 |            0.372 |                        1 |       0.4   |         0.15  |                       0     |             0     |        762.55 |                      0 |
| qwen    | tools        |           36 |            0.459 |                        1 |       0.472 |         0.194 |                       0     |            17.444 |      58794.2  |                      4 |
| qwen    | tools_verify |            8 |            0     |                        0 |       0     |         0.5   |                       0     |            51.5   |     368590    |                      4 |
| rules   | rules        |           40 |            1     |                        0 |       1     |         1     |                       0     |             5     |          0    |                      0 |


## Detection rate by bug type

|                                  |   ('claude', 'no_tools') |   ('claude', 'tools') |   ('claude', 'tools_verify') |   ('qwen', 'no_tools') |   ('qwen', 'tools') |   ('qwen', 'tools_verify') |   ('rules', 'rules') |
|:---------------------------------|-------------------------:|----------------------:|-----------------------------:|-----------------------:|--------------------:|---------------------------:|---------------------:|
| ('batch_patient_confound', True) |                     1    |                     1 |                            1 |                   0.89 |                0.89 |                          0 |                    1 |
| ('case_collision', True)         |                     1    |                     1 |                            1 |                   1    |                1    |                          0 |                    1 |
| ('celltype_mislabel', True)      |                     0.11 |                     1 |                            1 |                   0    |                0.12 |                          0 |                    1 |
| ('low_quality_cells', True)      |                     1    |                     1 |                            1 |                   0    |                0    |                          0 |                    1 |
| ('sample_swap', False)           |                     0    |                     1 |                            1 |                   0    |                0    |                          0 |                    1 |


## What self-verification removed

Bugs in the draft report that the verification phase dropped. `was_real=True` means verification threw away a correct finding.

|                 |   count |
|:----------------|--------:|
| ('qwen', False) |       5 |
| ('qwen', True)  |       2 |


## Metric definitions

- detection_rate: injected bugs whose type was reported / all injected bugs
- false_alarm_rate_clean: clean datasets with >=1 reported bug / clean datasets
- precision: correct reported bugs / all reported bugs
- exact_match: datasets where the reported set equals the injected set
- unsupported_evidence_rate: reported bugs whose evidence cites a number that appears in no tool output the model received (5% rounding tolerance; small integers ignored). An automatic upper bound on hallucinated evidence: correctly derived numbers (e.g. a percent computed from two counts) can be flagged, so spot-check before quoting it.