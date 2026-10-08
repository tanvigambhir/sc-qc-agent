"""QC tools the agent can call.

Design rules (this is the main agent-design lever in the project):
  * Each tool returns SHORT plain text. The model only ever sees this text.
  * Outputs lead with a one-line summary, then a compact table.
  * Tools report facts and simple flags; they do not name a "bug type".
    The agent has to make that call itself.
  * Every output is capped at MAX_CHARS so one call can't flood the context.
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np
import pandas as pd

from .data import MARKERS, QC_COLS

MAX_CHARS = 2500


def _cap(s: str) -> str:
    return s if len(s) <= MAX_CHARS else s[: MAX_CHARS - 20] + "\n...[truncated]"


def _gene(adata, g):
    x = adata[:, g].X
    x = x.toarray() if hasattr(x, "toarray") else np.asarray(x)
    return x.ravel()


def _check_col(adata, col):
    if col not in adata.obs.columns:
        return f"ERROR: column {col!r} not found. Columns: {list(adata.obs.columns)}"
    return None


# --------------------------------------------------------------------- tools
def summarize_metadata(adata) -> str:
    lines = [f"{adata.n_obs} cells, {adata.n_vars} genes stored, "
             f"{adata.obs.shape[1]} metadata columns."]
    for c in adata.obs.columns:
        s = adata.obs[c]
        if pd.api.types.is_numeric_dtype(s):
            lines.append(f"- {c} (numeric): min={s.min():.4g}, median={s.median():.4g}, "
                         f"max={s.max():.4g}")
        else:
            vc = s.astype(str).value_counts()
            top = ", ".join(f"{k}={v}" for k, v in vc.head(8).items())
            more = f", ... (+{len(vc) - 8} more)" if len(vc) > 8 else ""
            lines.append(f"- {c} (categorical, {len(vc)} unique): {top}{more}")
    return _cap("\n".join(lines))


def check_qc_metrics(adata, max_mito: float = 0.10, min_genes: int = 200,
                     max_genes: int = 2500) -> str:
    o = adata.obs
    hi_mito = o["percent_mito"] > max_mito
    lo_genes = o["n_genes"] < min_genes
    hi_genes = o["n_genes"] > max_genes
    med = o["n_counts"].median()
    mad = (o["n_counts"] - med).abs().median() or 1.0
    hi_counts = o["n_counts"] > med + 5 * 1.4826 * mad
    flagged = hi_mito | lo_genes | hi_genes
    lines = [
        f"Thresholds: percent_mito>{max_mito}, n_genes<{min_genes}, n_genes>{max_genes} "
        f"(percent_mito is a fraction 0-1).",
        f"Flagged cells: {int(flagged.sum())} of {len(o)} ({flagged.mean():.1%}).",
        f"  high mito: {int(hi_mito.sum())}; low genes: {int(lo_genes.sum())}; "
        f"high genes (doublet-like): {int(hi_genes.sum())}",
        f"  n_counts >5 MAD above median (possible doublets, informational): "
        f"{int(hi_counts.sum())}",
    ]
    if flagged.any() and "sample" in o.columns:
        by = flagged.groupby(o["sample"]).agg(["sum", "mean"]).sort_values("sum", ascending=False)
        lines.append("Flagged cells by sample (top 6):")
        for s, r in by.head(6).iterrows():
            lines.append(f"  {s}: {int(r['sum'])} ({r['mean']:.1%})")
    return _cap("\n".join(lines))


def compare_groups(adata, column: str) -> str:
    err = _check_col(adata, column)
    if err:
        return err
    o = adata.obs
    g = o.groupby(column, observed=True)
    df = pd.DataFrame({"n_cells": g.size()})
    for c in QC_COLS:
        df[f"med_{c}"] = g[c].median()
    for gene in ("XIST", "RPS4Y1"):
        if gene in adata.var_names:
            df[f"frac_{gene}+"] = pd.Series(_gene(adata, gene) > 0, index=o.index).groupby(
                o[column], observed=True).mean()
    if "sex" in o.columns and column != "sex":
        df["recorded_sex"] = g["sex"].agg(lambda s: "/".join(sorted(s.unique())))
    if len(df) > 25:
        head = f"{len(df)} groups; showing the 25 largest.\n"
        df = df.sort_values("n_cells", ascending=False).head(25)
    else:
        head = f"{len(df)} groups in {column!r}.\n"
    return _cap(head + df.round(3).to_string())


def check_label_consistency(adata, col_a: str, col_b: str) -> str:
    for c in (col_a, col_b):
        err = _check_col(adata, c)
        if err:
            return err
    a = adata.obs[col_a].astype(str)
    b = adata.obs[col_b].astype(str)
    ct = pd.crosstab(a, b)
    # Cramer's V
    n = ct.to_numpy().sum()
    exp = np.outer(ct.sum(1), ct.sum(0)) / n
    chi2 = ((ct.to_numpy() - exp) ** 2 / np.where(exp == 0, 1, exp)).sum()
    k = min(ct.shape) - 1
    v = float(np.sqrt(chi2 / (n * k))) if k > 0 else float("nan")
    b_per_a = (ct > 0).sum(1)
    a_per_b = (ct > 0).sum(0)
    one_to_one = bool((b_per_a == 1).all() and (a_per_b == 1).all())
    nested = bool((b_per_a == 1).all()) and not one_to_one
    lines = [
        f"{col_a} ({ct.shape[0]} values) x {col_b} ({ct.shape[1]} values). Cramer's V = {v:.3f}.",
        f"Each {col_a} value maps to {b_per_a.min()}-{b_per_a.max()} {col_b} values; "
        f"each {col_b} value maps to {a_per_b.min()}-{a_per_b.max()} {col_a} values.",
        f"Perfect one-to-one mapping: {one_to_one}. {col_a} nested in {col_b}: {nested}.",
    ]
    if ct.shape[0] <= 15 and ct.shape[1] <= 15:
        lines.append("Cross-tab (cell counts):")
        lines.append(ct.to_string())
    else:
        lines.append("Cross-tab too large to print.")
    return _cap("\n".join(lines))


def find_case_collisions(adata) -> str:
    groups = defaultdict(list)
    for c in adata.obs.columns:
        groups[c.lower()].append(c)
    for g in adata.var_names:
        groups["gene:" + g.lower()].append("gene:" + g)
    hits = {k: v for k, v in groups.items() if len(v) > 1}
    if not hits:
        return (f"No case-insensitive name collisions among {adata.obs.shape[1]} metadata "
                f"columns or {adata.n_vars} gene names.")
    lines = [f"{len(hits)} case-insensitive collision group(s):"]
    for names in hits.values():
        lines.append(f"- {names}")
        obs_names = [n for n in names if not n.startswith("gene:")]
        if len(obs_names) >= 2:
            x, y = adata.obs[obs_names[0]].astype(str), adata.obs[obs_names[1]].astype(str)
            lines.append(f"  values agree in {(x == y).mean():.1%} of cells")
    return _cap("\n".join(lines))


def run_marker_check(adata, cluster_col: str = "cell_type") -> str:
    err = _check_col(adata, cluster_col)
    if err:
        return err
    labels = adata.obs[cluster_col].astype(str)
    genes = sorted({g for gs in MARKERS.values() for g in gs if g in adata.var_names})
    means = pd.DataFrame({g: pd.Series(_gene(adata, g), index=adata.obs_names)
                          .groupby(labels.values).mean() for g in genes})
    z = (means - means.mean()) / means.std(ddof=0).replace(0, 1)
    score = pd.DataFrame({t: z[[g for g in gs if g in z.columns]].mean(1)
                          for t, gs in MARKERS.items()})
    lines = [f"Marker check on {cluster_col!r}: for each label, which reference cell type's "
             f"markers score highest (z-scored mean expression across labels)."]
    n_bad = 0
    for lab in score.index:
        best = score.loc[lab].idxmax()
        known = lab in MARKERS
        ok = (best == lab) if known else None
        if ok is False:
            n_bad += 1
        own = f"{score.loc[lab, lab]:+.2f}" if known else "n/a"
        status = "MATCH" if ok else ("MISMATCH" if ok is False else "label not in reference")
        lines.append(f"- {lab} (n={int((labels == lab).sum())}): best={best} "
                     f"({score.loc[lab, best]:+.2f}), own-markers score={own} -> {status}")
    lines.insert(1, f"{n_bad} of {len(score)} labels mismatch their expected markers.")
    return _cap("\n".join(lines))


# ------------------------------------------------------------- registry
TOOLS = {
    "summarize_metadata": summarize_metadata,
    "check_qc_metrics": check_qc_metrics,
    "compare_groups": compare_groups,
    "check_label_consistency": check_label_consistency,
    "find_case_collisions": find_case_collisions,
    "run_marker_check": run_marker_check,
}

# JSON-schema descriptions sent to the model. Neutral format; agent.py converts.
TOOL_SPECS = [
    {"name": "summarize_metadata",
     "description": "List every metadata column with its type, unique values and counts "
                    "(or min/median/max for numeric columns).",
     "parameters": {"type": "object", "properties": {}, "required": []}},
    {"name": "check_qc_metrics",
     "description": "Count cells failing standard QC thresholds (high mitochondrial fraction, "
                    "too few or too many genes) and break flagged cells down by sample.",
     "parameters": {"type": "object", "properties": {
         "max_mito": {"type": "number", "description": "max percent_mito fraction, default 0.10"},
         "min_genes": {"type": "integer", "description": "default 200"},
         "max_genes": {"type": "integer", "description": "default 2500"}},
         "required": []}},
    {"name": "compare_groups",
     "description": "For each value of a metadata column: cell count, median QC metrics, "
                    "fraction of cells expressing sex genes XIST and RPS4Y1, and recorded sex.",
     "parameters": {"type": "object", "properties": {
         "column": {"type": "string", "description": "metadata column to group by"}},
         "required": ["column"]}},
    {"name": "check_label_consistency",
     "description": "Cross-tabulate two metadata columns and report association "
                    "(Cramer's V) and whether one is a relabeling of, or nested in, the other.",
     "parameters": {"type": "object", "properties": {
         "col_a": {"type": "string"}, "col_b": {"type": "string"}},
         "required": ["col_a", "col_b"]}},
    {"name": "find_case_collisions",
     "description": "Find metadata columns or gene names that differ only by letter case, "
                    "and how often duplicated columns agree.",
     "parameters": {"type": "object", "properties": {}, "required": []}},
    {"name": "run_marker_check",
     "description": "Check whether known marker genes support each cell-type label in a column.",
     "parameters": {"type": "object", "properties": {
         "cluster_col": {"type": "string", "description": "default 'cell_type'"}},
         "required": []}},
]


def call_tool(adata, name: str, args: dict | None) -> str:
    """Run a tool by name. Errors come back as text so the agent can recover."""
    fn = TOOLS.get(name)
    if fn is None:
        return f"ERROR: unknown tool {name!r}. Available: {list(TOOLS)}"
    try:
        return fn(adata, **(args or {}))
    except TypeError as e:
        return f"ERROR: bad arguments for {name}: {e}"
    except Exception as e:  # keep the loop alive
        return f"ERROR: {name} failed: {type(e).__name__}: {e}"
