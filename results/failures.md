# Failed runs (for manual error analysis)

For each run, fill in a category, e.g.: never called the relevant tool / called it but misread output / reasoned correctly but too cautious / hallucinated evidence / wrong bug type / format or parse failure / step cap.

## ds001 | claude | no_tools
- truth: ['sample_swap']
- reported: []
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- **category:** ____

## ds004 | claude | no_tools
- truth: ['sample_swap', 'case_collision']
- reported: ['case_collision']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [case_collision]: Two columns differ only by letter case (cell_type vs cell_Type) and carry identical categories and counts (CD4 T cells=1144, CD14+ Monocytes=480, ...).
- **category:** ____

## ds005 | claude | no_tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [batch_patient_confound]: The design has 3 batches mixing several patients, but batch has 6 unique values whose counts match patient counts exactly one-to-one (B2=460/P1=460, B6=444/P6=444, B3=440/P3=440, B5=434/P4=434, B4=433/P5=433, B1=427/P2=427). Batch is a relabeling of patient.
- **category:** ____

## ds007 | claude | no_tools
- truth: ['celltype_mislabel']
- reported: []
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- **category:** ____

## ds012 | claude | no_tools
- truth: ['celltype_mislabel', 'case_collision']
- reported: ['case_collision']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- evidence [case_collision]: Two columns differ only by letter case and have identical value counts (B2=889, B3=878, B1=871).
- **category:** ____

## ds015 | claude | no_tools
- truth: ['celltype_mislabel']
- reported: []
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- **category:** ____

## ds018 | claude | no_tools
- truth: ['celltype_mislabel']
- reported: []
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- **category:** ____

## ds020 | claude | no_tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [batch_patient_confound]: batch has 6 unique values (design says 3 batches mixing patients) and its counts mirror patient counts one-to-one: B2=460/P1=460, B5=443/P6=443, B4=437/P3=437, B1=434/P4=434, B3=433/P5=433, B6=431/P2=431
- **category:** ____

## ds021 | claude | no_tools
- truth: ['sample_swap', 'low_quality_cells']
- reported: ['low_quality_cells']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [low_quality_cells]: percent_mito max=0.3998 (~40%) vs median 0.0208, indicating damaged cells not filtered; n_genes min=80 is below a typical 200-gene filter threshold
- **category:** ____

## ds022 | claude | no_tools
- truth: ['celltype_mislabel']
- reported: []
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- **category:** ____

## ds024 | claude | no_tools
- truth: ['celltype_mislabel', 'case_collision']
- reported: ['case_collision']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- evidence [case_collision]: Columns 'sample' and 'SAMPLE' differ only by case; both have 12 unique values with identical counts (P1_post=259, P6_post=236, P3_post=232, ...)
- **category:** ____

## ds027 | claude | no_tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [batch_patient_confound]: Design specifies 3 batches mixing several patients, but batch has 6 levels whose counts match patient counts one-to-one (B1=467=P1, B6=443=P6, B4=441=P3, B3=433=P5, B2=427=P4, B5=427=P2), so batch is a relabeling of patient.
- **category:** ____

## ds030 | claude | no_tools
- truth: ['sample_swap', 'low_quality_cells']
- reported: ['low_quality_cells']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [low_quality_cells]: percent_mito max=0.3963 against a median of 0.021 (about 40% mitochondrial reads), and n_genes min=80, below the standard 200-gene filter. This is consistent with damaged cells that were not filtered out.
- **category:** ____

## ds033 | claude | no_tools
- truth: ['celltype_mislabel', 'low_quality_cells']
- reported: ['low_quality_cells']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- evidence [low_quality_cells]: percent_mito max=0.3998 (~40%) vs median 0.021; n_genes min=80 (below the usual 200-gene filter) vs median 803; n_counts min=201. These indicate damaged or low-quality cells that were not filtered out.
- **category:** ____

## ds034 | claude | no_tools
- truth: ['celltype_mislabel', 'case_collision']
- reported: ['case_collision']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- evidence [case_collision]: Columns 'batch' and 'Batch' differ only in case and have identical distributions (B2=889, B3=878, B1=871).
- **category:** ____

## ds035 | claude | no_tools
- truth: ['sample_swap']
- reported: []
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- **category:** ____

## ds037 | claude | no_tools
- truth: ['sample_swap']
- reported: []
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- **category:** ____

## ds000 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds001 | qwen | no_tools
- truth: ['sample_swap']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds002 | qwen | no_tools
- truth: ['low_quality_cells', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells']  spurious: []
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains a mix of patients.
- **category:** ____

## ds003 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds004 | qwen | no_tools
- truth: ['sample_swap', 'case_collision']
- reported: ['case_collision']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [case_collision]: Column names differ only by case
- **category:** ____

## ds005 | qwen | no_tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds007 | qwen | no_tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as the unique values in batch match the unique values in patient and sample.
- **category:** ____

## ds008 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds010 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds011 | qwen | no_tools
- truth: ['batch_patient_confound', 'case_collision']
- reported: ['case_collision']
- missed: ['batch_patient_confound']  spurious: []
- tool calls (0): none
- evidence [case_collision]: batch and BATCH columns have identical unique values and counts
- **category:** ____

## ds012 | qwen | no_tools
- truth: ['celltype_mislabel', 'case_collision']
- reported: ['case_collision']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- evidence [case_collision]: batch and Batch are present as two separate columns with identical values.
- **category:** ____

## ds013 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds014 | qwen | no_tools
- truth: ['low_quality_cells', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells']  spurious: []
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch name corresponds to a patient name (e.g., B4=P1, B3=P6, etc.).
- **category:** ____

## ds015 | qwen | no_tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds016 | qwen | no_tools
- truth: ['low_quality_cells']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds017 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds018 | qwen | no_tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds019 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds020 | qwen | no_tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch size matches the number of cells from a single patient.
- **category:** ____

## ds021 | qwen | no_tools
- truth: ['sample_swap', 'low_quality_cells']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells', 'sample_swap']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds022 | qwen | no_tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds024 | qwen | no_tools
- truth: ['celltype_mislabel', 'case_collision']
- reported: ['case_collision']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- evidence [case_collision]: patient and SAMPLE columns have the same values but different cases
- **category:** ____

## ds025 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds026 | qwen | no_tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as the unique values in batch match the unique values in patient and sample.
- **category:** ____

## ds027 | qwen | no_tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains patients P1, P2, P3, P4, P5, P6.
- **category:** ____

## ds028 | qwen | no_tools
- truth: ['low_quality_cells']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds030 | qwen | no_tools
- truth: ['sample_swap', 'low_quality_cells']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells', 'sample_swap']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds031 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds032 | qwen | no_tools
- truth: ['low_quality_cells']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds033 | qwen | no_tools
- truth: ['celltype_mislabel', 'low_quality_cells']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel', 'low_quality_cells']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds034 | qwen | no_tools
- truth: ['celltype_mislabel', 'case_collision']
- reported: ['case_collision']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (0): none
- evidence [case_collision]: batch and Batch are present as two separate columns with identical values.
- **category:** ____

## ds035 | qwen | no_tools
- truth: ['sample_swap']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds036 | qwen | no_tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds037 | qwen | no_tools
- truth: ['sample_swap']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: ['batch_patient_confound']
- tool calls (0): none
- evidence [batch_patient_confound]: The batch column seems to be a relabeling of the patient column, as each batch contains samples from multiple patients.
- **category:** ____

## ds000 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_mito": 0.1, "min_genes": 200, "max_genes": 2500}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds001 | qwen | tools
- truth: ['sample_swap']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: ['batch_patient_confound']
- tool calls (7): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Cramer's V = 1.000, indicating a perfect one-to-one mapping between sample and patient values. This suggests that the batch column is a relabeling of the patient column.
- **category:** ____

## ds002 | qwen | tools
- truth: ['low_quality_cells', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells']  spurious: []
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds003 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"min_genes": 200, "max_genes": 2500, "max_mito": 0.1}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds004 | qwen | tools
- truth: ['sample_swap', 'case_collision']
- reported: ['case_collision']
- missed: ['sample_swap']  spurious: []
- tool calls (13): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:find_case_collisions({}) -> investigate:run_marker_check({"cluster_col": "cell_type"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:find_case_collisions({}) -> investigate:run_marker_check({"cluster_col": "cell_type"})
- evidence [case_collision]: values agree in 75.3% of cells
- **category:** ____

## ds005 | qwen | tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (5): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. This indicates that the batch column is a relabeling of the patient column.
- **category:** ____

## ds007 | qwen | tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"min_genes": 200, "max_genes": 2500, "max_mito": 0.1}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds008 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds010 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds011 | qwen | tools
- truth: ['batch_patient_confound', 'case_collision']
- reported: ['case_collision']
- missed: ['batch_patient_confound']  spurious: []
- tool calls (5): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"})
- evidence [case_collision]: 74.4% agreement in cell counts
- **category:** ____

## ds012 | qwen | tools
- truth: ['celltype_mislabel', 'case_collision']
- reported: ['case_collision']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (5): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [case_collision]: 75.8% agreement in cell counts
- **category:** ____

## ds013 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds014 | qwen | tools
- truth: ['low_quality_cells', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells']  spurious: []
- tool calls (15): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds015 | qwen | tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds017 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds018 | qwen | tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds019 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds020 | qwen | tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (5): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds021 | qwen | tools
- truth: ['sample_swap', 'low_quality_cells']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells', 'sample_swap']  spurious: ['batch_patient_confound']
- tool calls (5): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. This indicates that the batch column is a relabeling of the patient column.
- **category:** ____

## ds022 | qwen | tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds025 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds026 | qwen | tools
- truth: ['celltype_mislabel']
- reported: ['batch_patient_confound']
- missed: ['celltype_mislabel']  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds027 | qwen | tools
- truth: ['sample_swap', 'batch_patient_confound']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: []
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"min_genes": 200, "max_genes": 2500, "max_mito": 0.1}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds028 | qwen | tools
- truth: ['low_quality_cells']
- reported: []
- missed: ['low_quality_cells']  spurious: []
- tool calls (11): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:run_marker_check({"cluster_col": "cell_type"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:run_marker_check({"cluster_col": "cell_type"})
- **category:** ____

## ds031 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_mito": 0.1, "min_genes": 200, "max_genes": 2500}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds032 | qwen | tools
- truth: ['low_quality_cells']
- reported: ['batch_patient_confound']
- missed: ['low_quality_cells']  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds034 | qwen | tools
- truth: ['celltype_mislabel', 'case_collision']
- reported: ['case_collision']
- missed: ['celltype_mislabel']  spurious: []
- tool calls (5): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [case_collision]: 73.5% agreement in cell counts
- **category:** ____

## ds036 | qwen | tools
- truth: []
- reported: ['batch_patient_confound']
- missed: []  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds037 | qwen | tools
- truth: ['sample_swap']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: ['batch_patient_confound']
- tool calls (25): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_mito": 0.1, "min_genes": 200, "max_genes": 2500}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Each sample value maps to 1-1 patient values; each patient value maps to 2-2 sample values. Perfect one-to-one mapping: False. sample nested in patient: True.
- **category:** ____

## ds001 | qwen | tools_verify
- truth: ['sample_swap']
- reported: ['batch_patient_confound']
- missed: ['sample_swap']  spurious: ['batch_patient_confound']
- tool calls (9): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"})
- evidence [batch_patient_confound]: Cramer's V = 1.000, indicating a perfect one-to-one mapping between sample and patient values. This suggests that the batch column is a relabeling of the patient column.
- **category:** ____

## ds002 | qwen | tools_verify
- truth: ['low_quality_cells', 'batch_patient_confound']
- reported: []
- missed: ['batch_patient_confound', 'low_quality_cells']  spurious: []
- tool calls (55): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_genes": 2500, "max_mito": 0.1, "min_genes": 200}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"})
- **category:** ____

## ds006 | qwen | tools_verify
- truth: ['case_collision']
- reported: []
- missed: ['case_collision']  spurious: []
- tool calls (73): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"min_genes": 200, "max_genes": 2500, "max_mito": 0.1}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:find_case_collisions({}) -> investigate:run_marker_check({"cluster_col": "cell_type"}) -> investigate:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:find_case_collisions({}) -> investigate:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_b": "Cell_Type", "col_a": "cell_type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_b": "Cell_Type", "col_a": "cell_type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"}) -> verify:check_label_consistency({"col_a": "cell_type", "col_b": "Cell_Type"}) -> verify:compare_groups({"column": "sample"}) -> verify:find_case_collisions({}) -> verify:run_marker_check({"cluster_col": "cell_type"})
- **category:** ____

## ds007 | qwen | tools_verify
- truth: ['celltype_mislabel']
- reported: []
- missed: ['celltype_mislabel']  spurious: []
- tool calls (55): investigate:summarize_metadata({}) -> investigate:find_case_collisions({}) -> investigate:check_qc_metrics({"max_mito": 0.1, "min_genes": 200, "max_genes": 2500}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> investigate:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> investigate:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_b": "patient", "col_a": "sample"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"}) -> verify:check_label_consistency({"col_a": "sample", "col_b": "patient"}) -> verify:compare_groups({"column": "sample"})
- **category:** ____
