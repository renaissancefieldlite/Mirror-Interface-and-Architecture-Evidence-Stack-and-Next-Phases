#!/usr/bin/env python3
"""Nest 2G stronger RDKit descriptor / baseline comparison.

This checks whether the molecule-property lane survives a stronger comparison
than the original single descriptor composite:
- original composite correlation
- multifeature RDKit least-squares train/test model
- shuffled-target train/test controls
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors


ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = ROOT / "artifacts" / "validation" / "datasets"
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "nest2g_rdkit_baseline_comparison"

DATASETS = {
    "ESOL": ("delaney_esol.csv", "smiles", "measured log solubility in mols per litre", None),
    "Lipophilicity": ("lipophilicity.csv", "smiles", "exp", None),
    "FreeSolv": ("freesolv_sampl.csv", "smiles", "expt", None),
    "QM9_alpha": ("qm9.csv", "smiles", "alpha", 50000),
}


def pearson(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 3 or np.std(left) == 0 or np.std(right) == 0:
        return 0.0
    return float(np.corrcoef(left, right)[0, 1])


def descriptors(smiles: str) -> tuple[float, list[float]] | None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    composite = (
        Descriptors.MolWt(mol) * 0.01
        + Crippen.MolLogP(mol)
        + Lipinski.NumHDonors(mol)
        + Lipinski.NumHAcceptors(mol)
        + rdMolDescriptors.CalcNumRings(mol)
    )
    features = [
        Descriptors.MolWt(mol),
        Crippen.MolLogP(mol),
        Descriptors.TPSA(mol),
        float(Lipinski.NumHDonors(mol)),
        float(Lipinski.NumHAcceptors(mol)),
        float(Lipinski.NumRotatableBonds(mol)),
        float(rdMolDescriptors.CalcNumRings(mol)),
        float(rdMolDescriptors.CalcNumAromaticRings(mol)),
        float(Descriptors.HeavyAtomCount(mol)),
        float(Descriptors.FractionCSP3(mol)),
    ]
    return composite, features


def load_dataset(name: str, seed: int) -> pd.DataFrame:
    filename, smiles_col, target_col, sample_cap = DATASETS[name]
    df = pd.read_csv(DATASET_DIR / filename)
    if sample_cap and len(df) > sample_cap:
        df = df.sample(n=sample_cap, random_state=seed).reset_index(drop=True)
    rows: list[dict[str, object]] = []
    for _, row in df.iterrows():
        try:
            target = float(row[target_col])
        except (TypeError, ValueError):
            continue
        if math.isnan(target):
            continue
        desc = descriptors(str(row[smiles_col]))
        if desc is None:
            continue
        composite, features = desc
        rows.append({"target": target, "composite": composite, **{f"f{i}": v for i, v in enumerate(features)}})
    return pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)


def split_indices(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    split = int(n * 0.8)
    return idx[:split], idx[split:]


def fit_predict(x: np.ndarray, y: np.ndarray, train_idx: np.ndarray, test_idx: np.ndarray) -> dict[str, float]:
    x_train, x_test = x[train_idx], x[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    mu = x_train.mean(axis=0)
    sigma = x_train.std(axis=0)
    sigma[sigma == 0] = 1.0
    x_train = (x_train - mu) / sigma
    x_test = (x_test - mu) / sigma
    beta, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(x_train)), x_train]), y_train, rcond=None)
    pred = np.column_stack([np.ones(len(x_test)), x_test]) @ beta
    baseline = np.full_like(y_test, y_train.mean())
    rmse = float(np.sqrt(np.mean((pred - y_test) ** 2)))
    baseline_rmse = float(np.sqrt(np.mean((baseline - y_test) ** 2)))
    return {
        "test_pearson": pearson(pred, y_test),
        "test_abs_pearson": abs(pearson(pred, y_test)),
        "test_rmse": rmse,
        "baseline_mean_rmse": baseline_rmse,
        "rmse_improvement_fraction": float((baseline_rmse - rmse) / baseline_rmse),
    }


def run_dataset(name: str, seed: int, permutations: int) -> dict[str, object]:
    table = load_dataset(name, seed)
    if len(table) < 20:
        return {"dataset": name, "status": "blocked_insufficient_rows", "rows": int(len(table))}
    train_idx, test_idx = split_indices(len(table), seed)
    y = table["target"].to_numpy(dtype=float)
    composite = table["composite"].to_numpy(dtype=float)
    x = table[[c for c in table.columns if c.startswith("f")]].to_numpy(dtype=float)
    composite_corr = pearson(composite, y)
    metrics = fit_predict(x, y, train_idx, test_idx)
    rng = np.random.default_rng(seed)
    null_corr = []
    null_improve = []
    for _ in range(permutations):
        shuffled = rng.permutation(y)
        m = fit_predict(x, shuffled, train_idx, test_idx)
        null_corr.append(m["test_abs_pearson"])
        null_improve.append(m["rmse_improvement_fraction"])
    null_corr_a = np.array(null_corr)
    null_improve_a = np.array(null_improve)
    p_corr = (float((null_corr_a >= metrics["test_abs_pearson"]).sum()) + 1.0) / (len(null_corr_a) + 1.0)
    p_improve = (float((null_improve_a >= metrics["rmse_improvement_fraction"]).sum()) + 1.0) / (len(null_improve_a) + 1.0)
    status = "completed_stronger_baseline_supported" if p_corr <= 0.05 and p_improve <= 0.05 else "completed_no_control_support"
    return {
        "dataset": name,
        "status": status,
        "rows": int(len(table)),
        "composite_abs_pearson": abs(composite_corr),
        **metrics,
        "shuffle_abs_pearson_mean": float(null_corr_a.mean()),
        "shuffle_rmse_improvement_mean": float(null_improve_a.mean()),
        "pearson_permutation_p": p_corr,
        "rmse_improvement_permutation_p": p_improve,
        "permutations": permutations,
        "seed": seed,
    }


def write_report(rows: list[dict[str, object]], out_dir: Path) -> None:
    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "nest2g_rdkit_baseline_comparison_summary.csv", index=False)
    supported = int((df["status"] == "completed_stronger_baseline_supported").sum())
    status = "completed_multi_dataset_stronger_baseline_supported" if supported == len(df) else "completed_mixed_support"
    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "dataset_count": int(len(df)),
        "supported_count": supported,
        "rows": rows,
    }
    (out_dir / "nest2g_rdkit_baseline_comparison_report.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Nest 2G RDKit Stronger Baseline Comparison Report",
        "",
        f"Status: `{status}`",
        "",
        "## Purpose",
        "",
        "This pass checks whether the molecule-property lane survives stronger",
        "descriptor / baseline comparisons, not just a single hand-built composite.",
        "",
        "## Results",
        "",
        "| Dataset | Rows | Composite abs r | Multifeature test abs r | RMSE improvement | p(abs r) | p(RMSE improvement) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['dataset']}` | `{row['rows']}` | `{row.get('composite_abs_pearson', float('nan')):.6f}` | "
            f"`{row.get('test_abs_pearson', float('nan')):.6f}` | `{row.get('rmse_improvement_fraction', float('nan')):.6f}` | "
            f"`{row.get('pearson_permutation_p', float('nan')):.6f}` | `{row.get('rmse_improvement_permutation_p', float('nan')):.6f}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is still a descriptor benchmark, not completed chemistry. It strengthens",
            "the Nest 2C molecule-property result by adding held-out prediction and",
            "shuffled-target controls.",
            "",
        ]
    )
    (out_dir / "nest2g_rdkit_baseline_comparison_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    parser.add_argument("--permutations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=67)
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [run_dataset(name, args.seed, args.permutations) for name in DATASETS]
    write_report(rows, out_dir)
    print(json.dumps({"status": "ok", "report": str(out_dir / "nest2g_rdkit_baseline_comparison_report.md")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
