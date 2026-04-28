#!/usr/bin/env python3
"""Nest 2F materials / crystal stability validation on Matbench MP e_form.

This uses real Materials Project-derived formation-energy rows from Matbench.
It tests whether fixed composition/structure descriptors recover DFT formation
energy above shuffled-target controls.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = ROOT / "artifacts" / "validation" / "datasets" / "matbench_mp_e_form_co_0.parquet"
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "nest2f_materials_stability"


def cell_volume(cell: object) -> float:
    try:
        matrix = np.array(cell, dtype=float)
        if matrix.shape == (3,):
            matrix = np.vstack([np.array(vector, dtype=float) for vector in cell])
        if matrix.shape != (3, 3):
            return float("nan")
        return abs(float(np.linalg.det(matrix)))
    except Exception:
        return float("nan")


def entropy(values: object) -> float:
    try:
        arr = np.array(values, dtype=float)
        arr = arr[arr > 0]
        if arr.size == 0:
            return 0.0
        return float(-(arr * np.log(arr)).sum())
    except Exception:
        return 0.0


def atomic_stats(values: object) -> tuple[float, float, float, float, float]:
    try:
        arr = np.array(values, dtype=float)
        if arr.size == 0:
            return (0.0, 0.0, 0.0, 0.0, 0.0)
        return (
            float(arr.mean()),
            float(arr.std()),
            float(arr.min()),
            float(arr.max()),
            float(arr.sum()),
        )
    except Exception:
        return (0.0, 0.0, 0.0, 0.0, 0.0)


def build_feature_table(dataset: Path, sample_size: int | None, seed: int) -> pd.DataFrame:
    df = pd.read_parquet(dataset)
    df = df[pd.notna(df["formation_energy"])].copy()
    if sample_size and len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=seed).reset_index(drop=True)
    rows: list[dict[str, float]] = []
    for _, row in df.iterrows():
        mean_z, std_z, min_z, max_z, sum_z = atomic_stats(row.get("atomic_numbers"))
        volume = cell_volume(row.get("cell"))
        nsites = float(row.get("nsites") or 0.0)
        nelements = float(row.get("nelements") or 0.0)
        volume_per_atom = volume / nsites if nsites > 0 and math.isfinite(volume) else float("nan")
        density_proxy = sum_z / volume if volume > 0 and math.isfinite(volume) else float("nan")
        rows.append(
            {
                "formation_energy": float(row["formation_energy"]),
                "nsites": nsites,
                "nelements": nelements,
                "mean_z": mean_z,
                "std_z": std_z,
                "min_z": min_z,
                "max_z": max_z,
                "sum_z_per_atom": sum_z / max(nsites, 1.0),
                "ratio_entropy": entropy(row.get("elements_ratios")),
                "volume_per_atom": volume_per_atom,
                "density_proxy": density_proxy,
            }
        )
    table = pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan)
    feature_cols = [c for c in table.columns if c != "formation_energy"]
    for col in feature_cols:
        median = table[col].median(skipna=True)
        table[col] = table[col].fillna(0.0 if pd.isna(median) else float(median))
    table = table.dropna(subset=["formation_energy"])
    return table.reset_index(drop=True)


def train_test_split(n: int, seed: int, train_fraction: float = 0.8) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    indices = rng.permutation(n)
    split = int(n * train_fraction)
    return indices[:split], indices[split:]


def zscore_train_test(x_train: np.ndarray, x_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mu = x_train.mean(axis=0)
    sigma = x_train.std(axis=0)
    sigma[sigma == 0] = 1.0
    return (x_train - mu) / sigma, (x_test - mu) / sigma


def fit_predict(table: pd.DataFrame, target: np.ndarray, train_idx: np.ndarray, test_idx: np.ndarray) -> dict[str, float]:
    feature_cols = [c for c in table.columns if c != "formation_energy"]
    x = table[feature_cols].to_numpy(dtype=float)
    y = target.astype(float)
    x_train, x_test = x[train_idx], x[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    x_train_z, x_test_z = zscore_train_test(x_train, x_test)
    x_train_aug = np.column_stack([np.ones(len(x_train_z)), x_train_z])
    x_test_aug = np.column_stack([np.ones(len(x_test_z)), x_test_z])
    beta, *_ = np.linalg.lstsq(x_train_aug, y_train, rcond=None)
    pred = x_test_aug @ beta
    baseline = np.full_like(y_test, y_train.mean())
    corr = float(np.corrcoef(pred, y_test)[0, 1])
    rmse = float(np.sqrt(np.mean((pred - y_test) ** 2)))
    baseline_rmse = float(np.sqrt(np.mean((baseline - y_test) ** 2)))
    return {
        "test_pearson": corr,
        "test_abs_pearson": abs(corr),
        "test_rmse": rmse,
        "baseline_mean_rmse": baseline_rmse,
        "rmse_improvement_fraction": float((baseline_rmse - rmse) / baseline_rmse),
    }


def shuffled_control(table: pd.DataFrame, train_idx: np.ndarray, test_idx: np.ndarray, permutations: int, seed: int) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    y = table["formation_energy"].to_numpy(dtype=float)
    true = fit_predict(table, y, train_idx, test_idx)
    null_abs_corr = []
    null_rmse_improvement = []
    for _ in range(permutations):
        shuffled = rng.permutation(y)
        metrics = fit_predict(table, shuffled, train_idx, test_idx)
        null_abs_corr.append(metrics["test_abs_pearson"])
        null_rmse_improvement.append(metrics["rmse_improvement_fraction"])
    null_corr = np.array(null_abs_corr)
    null_improve = np.array(null_rmse_improvement)
    p_corr = (float((null_corr >= true["test_abs_pearson"]).sum()) + 1.0) / (len(null_corr) + 1.0)
    p_improve = (float((null_improve >= true["rmse_improvement_fraction"]).sum()) + 1.0) / (len(null_improve) + 1.0)
    return {
        **true,
        "shuffle_abs_pearson_mean": float(null_corr.mean()),
        "shuffle_abs_pearson_std": float(null_corr.std()),
        "shuffle_rmse_improvement_mean": float(null_improve.mean()),
        "shuffle_rmse_improvement_std": float(null_improve.std()),
        "pearson_permutation_p": p_corr,
        "rmse_improvement_permutation_p": p_improve,
        "permutations": permutations,
    }


def write_report(table: pd.DataFrame, metrics: dict[str, float], args: argparse.Namespace, out_dir: Path) -> None:
    status = (
        "completed_real_materials_stability_supported"
        if metrics["pearson_permutation_p"] <= 0.05 and metrics["rmse_improvement_permutation_p"] <= 0.05
        else "completed_no_control_support"
    )
    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "dataset": str(Path(args.dataset)),
        "rows_used_after_cleaning": int(len(table)),
        "sample_size_requested": args.sample_size,
        "seed": args.seed,
        **metrics,
    }
    (out_dir / "nest2f_materials_stability_report.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    table.head(5000).to_csv(out_dir / "nest2f_materials_feature_sample.csv", index=False)
    lines = [
        "# Nest 2F Materials / Crystal Stability Validation Report",
        "",
        f"Status: `{status}`",
        "",
        "## Inputs",
        "",
        "- Dataset: Matbench `mp_e_form` / Materials Project-derived DFT formation energy",
        f"- Rows used after cleaning: `{len(table)}`",
        f"- Sample cap: `{args.sample_size}`",
        "",
        "## Test",
        "",
        "Fixed composition / structure descriptors were fit on a train split and",
        "evaluated on a held-out test split against DFT formation energy.",
        "",
        "Controls shuffled the formation-energy target while preserving descriptor",
        "rows and the same train/test split.",
        "",
        "## Result",
        "",
        f"- test Pearson: `{metrics['test_pearson']:.6f}`",
        f"- test absolute Pearson: `{metrics['test_abs_pearson']:.6f}`",
        f"- test RMSE: `{metrics['test_rmse']:.6f}`",
        f"- mean-baseline RMSE: `{metrics['baseline_mean_rmse']:.6f}`",
        f"- RMSE improvement fraction: `{metrics['rmse_improvement_fraction']:.6f}`",
        f"- shuffled abs Pearson mean: `{metrics['shuffle_abs_pearson_mean']:.6f}`",
        f"- Pearson permutation p: `{metrics['pearson_permutation_p']:.6f}`",
        f"- RMSE-improvement permutation p: `{metrics['rmse_improvement_permutation_p']:.6f}`",
        f"- permutations: `{metrics['permutations']}`",
        "",
        "## Boundary",
        "",
        "This validates a real materials-property descriptor lane against DFT",
        "formation energy. It does not claim completed crystal design, synthesis,",
        "or universal materials prediction.",
        "",
    ]
    (out_dir / "nest2f_materials_stability_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    parser.add_argument("--sample-size", type=int, default=50000)
    parser.add_argument("--permutations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=67)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table = build_feature_table(Path(args.dataset), args.sample_size, args.seed)
    if len(table) < 10:
        raise RuntimeError(f"Not enough usable material rows after cleaning: {len(table)}")
    train_idx, test_idx = train_test_split(len(table), args.seed)
    metrics = shuffled_control(table, train_idx, test_idx, args.permutations, args.seed)
    write_report(table, metrics, args, out_dir)
    print(
        json.dumps(
            {
                "status": "ok",
                "rows": int(len(table)),
                "pearson": metrics["test_pearson"],
                "p": metrics["pearson_permutation_p"],
                "report": str(out_dir / "nest2f_materials_stability_report.md"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
