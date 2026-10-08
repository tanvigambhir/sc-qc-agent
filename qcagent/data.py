"""Load the clean reference dataset and attach synthetic study metadata.

pbmc3k comes from a single donor, so it has no patient/sample/batch columns.
We add a plausible synthetic study design on top of it:

  6 patients (P1-P6, alternating F/M) x 2 timepoints (pre/post) = 12 samples
  3 processing batches; every batch mixes samples from 4 different patients,
  so batch is NOT confounded with patient in the clean data.

Sex-linked genes (XIST, RPS4Y1) are SIMULATED per cell from the true patient's
sex. They give sample-swap bugs a biological signal to be caught by, the way a
real swap is caught with sex genes or genotypes. This is a stated limitation.

Bugs only ever modify `.obs`, so each benchmark copy stores a small `.X` with
just the marker genes. That keeps 40+ copies to a few MB in total.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import anndata as ad

PATIENTS = ["P1", "P2", "P3", "P4", "P5", "P6"]
SEX = {"P1": "F", "P2": "M", "P3": "F", "P4": "M", "P5": "F", "P6": "M"}
TIMEPOINTS = ["pre", "post"]

# Canonical pbmc3k markers (Seurat/Scanpy tutorial).
MARKERS = {
    "CD4 T cells": ["IL7R", "CD3D"],
    "CD14+ Monocytes": ["CD14", "LYZ"],
    "B cells": ["MS4A1", "CD79A"],
    "CD8 T cells": ["CD8A", "CD8B", "CD3D"],
    "NK cells": ["GNLY", "NKG7"],
    "FCGR3A+ Monocytes": ["FCGR3A", "MS4A7"],
    "Dendritic cells": ["FCER1A", "CST3"],
    "Megakaryocytes": ["PPBP"],
}
SEX_GENES = ["XIST", "RPS4Y1"]
MARKER_GENES = sorted({g for gs in MARKERS.values() for g in gs})
QC_COLS = ["n_genes", "n_counts", "percent_mito"]


def _samples():
    out = []
    for p in PATIENTS:
        for t in TIMEPOINTS:
            out.append(f"{p}_{t}")
    return out


def sample_table() -> pd.DataFrame:
    """One row per sample: patient, timepoint, sex, batch."""
    rows = []
    for i, s in enumerate(_samples()):
        p, t = s.split("_")
        # Round-robin batches: each batch gets 4 samples from 4 different patients.
        rows.append({"sample": s, "patient": p, "timepoint": t,
                     "sex": SEX[p], "batch": f"B{i % 3 + 1}"})
    return pd.DataFrame(rows).set_index("sample")


def _simulate_sex_genes(sex: np.ndarray, rng) -> np.ndarray:
    n = len(sex)
    female = sex == "F"
    # Fraction of cells with detectable expression, then a log-normal-ish level.
    xist_on = np.where(female, rng.random(n) < 0.85, rng.random(n) < 0.02)
    y_on = np.where(female, rng.random(n) < 0.02, rng.random(n) < 0.80)
    xist = xist_on * np.clip(rng.normal(1.6, 0.5, n), 0.1, None)
    y = y_on * np.clip(rng.normal(1.4, 0.5, n), 0.1, None)
    return np.column_stack([xist, y])


def add_study_design(obs: pd.DataFrame, rng) -> pd.DataFrame:
    """Randomly assign cells to the 12 samples and attach per-sample metadata."""
    st = sample_table()
    obs = obs.copy()
    obs["sample"] = rng.choice(st.index.to_numpy(), size=len(obs))
    for col in ["patient", "timepoint", "sex", "batch"]:
        obs[col] = obs["sample"].map(st[col]).to_numpy()
    return obs


def _finalize(expr: pd.DataFrame, obs: pd.DataFrame, rng) -> ad.AnnData:
    sexg = _simulate_sex_genes(obs["sex"].to_numpy(), rng)
    for j, g in enumerate(SEX_GENES):
        expr[g] = sexg[:, j]
    genes = MARKER_GENES + SEX_GENES
    a = ad.AnnData(X=expr[genes].to_numpy(dtype=np.float32), obs=obs,
                   var=pd.DataFrame(index=genes))
    a.obs_names = [f"cell{i}" for i in range(a.n_obs)]
    order = ["cell_type", "patient", "sample", "timepoint", "sex", "batch"] + QC_COLS
    a.obs = a.obs[order]
    for c in ["cell_type", "patient", "sample", "timepoint", "sex", "batch"]:
        a.obs[c] = a.obs[c].astype(str)
    a.obs[QC_COLS] = a.obs[QC_COLS].astype("float64")
    return a


def load_pbmc3k(seed: int = 0) -> ad.AnnData:
    """Real pbmc3k (downloads ~24 MB on first use) + synthetic study design."""
    import scanpy as sc

    rng = np.random.default_rng(seed)
    full = sc.datasets.pbmc3k_processed()
    raw = full.raw.to_adata()  # log-normalized counts, all genes
    missing = [g for g in MARKER_GENES if g not in raw.var_names]
    if missing:
        raise RuntimeError(f"Marker genes missing from pbmc3k raw: {missing}")
    sub = raw[:, MARKER_GENES].X
    sub = sub.toarray() if hasattr(sub, "toarray") else np.asarray(sub)
    expr = pd.DataFrame(sub, columns=MARKER_GENES)
    obs = full.obs[["louvain", "n_genes", "n_counts", "percent_mito"]].copy()
    obs = obs.rename(columns={"louvain": "cell_type"}).reset_index(drop=True)
    obs = add_study_design(obs, rng)
    return _finalize(expr, obs, rng)


# Approximate pbmc3k composition, used only by the offline synthetic dataset.
_PROPS = {"CD4 T cells": 0.43, "CD14+ Monocytes": 0.18, "B cells": 0.13,
          "CD8 T cells": 0.11, "NK cells": 0.06, "FCGR3A+ Monocytes": 0.06,
          "Dendritic cells": 0.02, "Megakaryocytes": 0.01}


def load_synthetic(n_cells: int = 2600, seed: int = 0) -> ad.AnnData:
    """Offline stand-in with the same structure as load_pbmc3k().

    Used for tests and when pbmc3k can't be downloaded. Do not report
    results from this dataset as pbmc3k results.
    """
    rng = np.random.default_rng(seed)
    types = list(_PROPS)
    p = np.array(list(_PROPS.values()))
    ct = rng.choice(types, size=n_cells, p=p / p.sum())
    expr = np.zeros((n_cells, len(MARKER_GENES)))
    gi = {g: i for i, g in enumerate(MARKER_GENES)}
    # background dropout-y noise
    expr += (rng.random(expr.shape) < 0.08) * rng.normal(0.8, 0.3, expr.shape).clip(0)
    for t, genes in MARKERS.items():
        idx = np.where(ct == t)[0]
        for g in genes:
            on = rng.random(len(idx)) < 0.75
            expr[idx, gi[g]] = on * rng.normal(2.2, 0.6, len(idx)).clip(0.1)
    obs = pd.DataFrame({
        "cell_type": ct,
        "n_genes": rng.integers(300, 2400, n_cells),
        "n_counts": rng.lognormal(7.7, 0.4, n_cells).round(),
        "percent_mito": rng.uniform(0.005, 0.045, n_cells),
    })
    obs = add_study_design(obs, rng)
    return _finalize(pd.DataFrame(expr, columns=MARKER_GENES), obs, rng)


def load_clean(source: str = "pbmc3k", seed: int = 0) -> ad.AnnData:
    if source == "pbmc3k":
        return load_pbmc3k(seed)
    if source == "synthetic":
        return load_synthetic(seed=seed)
    raise ValueError(f"unknown source {source!r}")
