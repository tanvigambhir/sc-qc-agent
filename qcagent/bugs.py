"""Bug injectors. Each takes (adata, rng), mutates a COPY, returns (adata, details).

All bugs act on `.obs` only. Real-life origin of each type is in BUG_TYPES.
"""
from __future__ import annotations

import numpy as np

from .data import sample_table

BUG_TYPES = {
    # name: (real-life origin, has a dedicated tool?)
    "sample_swap": ("CAR-T ~70% sample mislabel", False),
    "batch_patient_confound": ("batch column secretly equals patient", True),
    "case_collision": ("numericMeta.All vs numericMeta.ALL", True),
    "celltype_mislabel": ("classic cluster annotation error", True),
    "low_quality_cells": ("standard QC failure", True),
}


def sample_swap(adata, rng):
    """Relabel a fraction of one female sample's cells as a male sample, and vice versa."""
    a = adata.copy()
    st = sample_table()
    tp = rng.choice(["pre", "post"])
    f_s = rng.choice([s for s in st.index if st.loc[s, "sex"] == "F" and s.endswith(tp)])
    m_s = rng.choice([s for s in st.index if st.loc[s, "sex"] == "M" and s.endswith(tp)])
    frac = float(rng.uniform(0.3, 0.7))
    o = a.obs
    idx_f = o.index[o["sample"] == f_s]
    idx_m = o.index[o["sample"] == m_s]
    pick_f = rng.choice(idx_f, int(frac * len(idx_f)), replace=False)
    pick_m = rng.choice(idx_m, int(frac * len(idx_m)), replace=False)
    for picks, new in ((pick_f, m_s), (pick_m, f_s)):
        o.loc[picks, "sample"] = new
        for c in ["patient", "timepoint", "sex", "batch"]:
            o.loc[picks, c] = st.loc[new, c]
    return a, {"samples": [str(f_s), str(m_s)], "fraction": round(frac, 3),
               "columns": ["sample", "patient"]}


def batch_patient_confound(adata, rng):
    """Overwrite batch so it is a one-to-one relabeling of patient."""
    a = adata.copy()
    pats = sorted(a.obs["patient"].unique())
    perm = rng.permutation(len(pats))
    mapping = {p: f"B{perm[i] + 1}" for i, p in enumerate(pats)}
    a.obs["batch"] = a.obs["patient"].map(mapping)
    return a, {"mapping": mapping, "columns": ["batch", "patient"]}


def case_collision(adata, rng):
    """Add a stale duplicate of a column whose name differs only by case."""
    a = adata.copy()
    col = str(rng.choice(["cell_type", "sample", "batch"]))
    variants = {"cell_type": ["Cell_Type", "CELL_TYPE", "cell_Type"],
                "sample": ["Sample", "SAMPLE"], "batch": ["Batch", "BATCH"]}[col]
    new = str(rng.choice(variants))
    vals = a.obs[col].astype(str).to_numpy().copy()
    frac = float(rng.uniform(0.2, 0.5))
    pick = rng.random(len(vals)) < frac
    vals[pick] = rng.permutation(vals[pick])  # stale/out-of-sync values
    a.obs[new] = vals
    return a, {"columns": [col, new], "fraction_shuffled": round(frac, 3)}


SWAPPABLE = ["CD4 T cells", "CD14+ Monocytes", "B cells", "NK cells", "FCGR3A+ Monocytes"]


def celltype_mislabel(adata, rng):
    """Swap the labels of two transcriptionally distinct clusters."""
    a = adata.copy()
    t1, t2 = (str(x) for x in rng.choice(SWAPPABLE, 2, replace=False))
    ct = a.obs["cell_type"].astype(str)
    new = ct.copy()
    new[ct == t1] = t2
    new[ct == t2] = t1
    a.obs["cell_type"] = new.to_numpy()
    return a, {"swapped": [t1, t2], "columns": ["cell_type"]}


def low_quality_cells(adata, rng):
    """Corrupt QC metrics for 5-15% of cells (high mito, few genes, low counts)."""
    a = adata.copy()
    o = a.obs
    frac = float(rng.uniform(0.05, 0.15))
    n = int(frac * len(o))
    concentrated = bool(rng.random() < 0.5)
    if concentrated:  # damage mostly in one sample, like a bad prep
        s = rng.choice(o["sample"].unique())
        pool = o.index[o["sample"] == s].to_numpy()
        n = min(n, int(0.8 * len(pool)))
    else:
        s, pool = None, o.index.to_numpy()
    pick = rng.choice(pool, n, replace=False)
    o.loc[pick, "percent_mito"] = rng.uniform(0.15, 0.40, n)
    o.loc[pick, "n_genes"] = rng.integers(80, 190, n)
    o.loc[pick, "n_counts"] = rng.integers(200, 600, n).astype(float)
    return a, {"n_cells": int(n), "concentrated_in": None if s is None else str(s),
               "columns": ["percent_mito", "n_genes", "n_counts"]}


INJECTORS = {
    "sample_swap": sample_swap,
    "batch_patient_confound": batch_patient_confound,
    "case_collision": case_collision,
    "celltype_mislabel": celltype_mislabel,
    "low_quality_cells": low_quality_cells,
}
