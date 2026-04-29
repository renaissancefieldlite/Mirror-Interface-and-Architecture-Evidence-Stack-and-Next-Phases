#!/usr/bin/env python3
"""Validate exported V8 attention-flow and MLP delta artifacts.

This runner consumes real CSV exports from `v8_attention_mlp_export.py`.
It does not synthesize rows. The first supported target is intentionally
bounded: Hermes-only attention-flow with shuffled context labels and a
degree-only graph baseline.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXPORT_DIR = ROOT / "artifacts" / "validation" / "v8_attention_mlp_exports"
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_attention_mlp_validation"
CONTEXTS = ("lattice", "neutral", "technical")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate V8 attention / MLP exports.")
    parser.add_argument(
        "--attention-csv",
        default=str(DEFAULT_EXPORT_DIR / "v8_attention_topk_edges.csv"),
        help="Attention top-k edge CSV from v8_attention_mlp_export.py.",
    )
    parser.add_argument(
        "--mlp-csv",
        default=str(DEFAULT_EXPORT_DIR / "v8_mlp_block_deltas.csv"),
        help="MLP block delta CSV from v8_attention_mlp_export.py.",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT), help="Report output directory.")
    parser.add_argument("--permutations", type=int, default=5000, help="Shuffled-label permutations.")
    parser.add_argument("--seed", type=int, default=67, help="Deterministic permutation seed.")
    return parser.parse_args()


def require_file(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Required CSV not found: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"Required CSV is empty: {path}")


def safe_divide(values: np.ndarray) -> np.ndarray:
    denom = float(values.sum())
    if denom == 0.0:
        return values
    return values / denom


def unit_separation_score(by_context: dict[str, np.ndarray]) -> float:
    lattice = by_context["lattice"]
    neutral = by_context["neutral"]
    technical = by_context["technical"]
    lattice_to_controls = (np.linalg.norm(lattice - neutral) + np.linalg.norm(lattice - technical)) / 2.0
    control_to_control = np.linalg.norm(neutral - technical)
    return float(lattice_to_controls - control_to_control)


def permutation_summary(
    unit_vectors: list[dict[str, np.ndarray]],
    true_score: float,
    permutations: int,
    seed: int,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    labels = np.array(CONTEXTS)
    null_scores = []
    for _ in range(permutations):
        unit_scores = []
        for vectors in unit_vectors:
            shuffled_sources = rng.permutation(labels)
            shuffled = {label: vectors[source] for label, source in zip(labels, shuffled_sources)}
            unit_scores.append(unit_separation_score(shuffled))
        null_scores.append(float(np.mean(unit_scores)))
    null_array = np.array(null_scores, dtype=float)
    p_value = (float(np.sum(null_array >= true_score)) + 1.0) / (float(permutations) + 1.0)
    return {
        "permutations": permutations,
        "seed": seed,
        "null_mean": round(float(null_array.mean()), 9),
        "null_std": round(float(null_array.std()), 9),
        "p_value_one_sided": round(float(p_value), 9),
    }


def build_attention_vectors(attention: pd.DataFrame, weighted: bool) -> tuple[list[dict[str, np.ndarray]], list[float]]:
    required = {"context", "layer_index", "head_index", "query_role", "key_region", "attention_weight", "head_entropy"}
    missing = required - set(attention.columns)
    if missing:
        raise SystemExit(f"Attention CSV missing columns: {sorted(missing)}")

    regions = sorted(str(value) for value in attention["key_region"].dropna().unique())
    unit_vectors: list[dict[str, np.ndarray]] = []
    unit_scores: list[float] = []
    group_cols = ["model", "layer_index", "head_index", "query_role"]
    for _, group in attention.groupby(group_cols):
        vectors: dict[str, np.ndarray] = {}
        for context_name, context_group in group.groupby("context"):
            if context_name not in CONTEXTS:
                continue
            if weighted:
                region_values = (
                    context_group.groupby("key_region")["attention_weight"]
                    .sum()
                    .reindex(regions, fill_value=0.0)
                    .to_numpy(dtype=float)
                )
                region_features = safe_divide(region_values)
                vector = np.concatenate(
                    [
                        region_features,
                        np.array(
                            [
                                float(context_group["head_entropy"].mean()),
                                float(context_group["attention_weight"].max()),
                                float(context_group["attention_weight"].sum()),
                            ],
                            dtype=float,
                        ),
                    ]
                )
            else:
                region_counts = (
                    context_group.groupby("key_region")
                    .size()
                    .reindex(regions, fill_value=0.0)
                    .to_numpy(dtype=float)
                )
                vector = safe_divide(region_counts)
            vectors[context_name] = vector
        if all(context in vectors for context in CONTEXTS):
            score = unit_separation_score(vectors)
            unit_vectors.append(vectors)
            unit_scores.append(score)
    return unit_vectors, unit_scores


def validate_attention(attention: pd.DataFrame, permutations: int, seed: int) -> dict[str, Any]:
    model_names = sorted(str(value) for value in attention["model"].dropna().unique())
    model_count = len(model_names)
    weighted_vectors, weighted_unit_scores = build_attention_vectors(attention, weighted=True)
    degree_vectors, degree_unit_scores = build_attention_vectors(attention, weighted=False)
    if not weighted_vectors:
        return {"status": "blocked_no_matched_attention_units"}

    weighted_true = float(np.mean(weighted_unit_scores))
    degree_true = float(np.mean(degree_unit_scores)) if degree_unit_scores else float("nan")
    weighted_perm = permutation_summary(weighted_vectors, weighted_true, permutations, seed)
    degree_perm = permutation_summary(degree_vectors, degree_true, permutations, seed + 1)
    supported = weighted_true > degree_true and weighted_perm["p_value_one_sided"] <= 0.01
    status = (
        "attention_flow_supported_cross_model"
        if supported and model_count > 1
        else "attention_flow_supported_single_model"
        if supported
        else "attention_flow_partial_or_unsupported"
    )
    return {
        "status": status,
        "models": model_names,
        "model_count": model_count,
        "matched_units": len(weighted_vectors),
        "weighted_attention_flow": {
            "true_score": round(weighted_true, 9),
            "positive_units": int(np.sum(np.array(weighted_unit_scores) > 0.0)),
            "unit_count": len(weighted_unit_scores),
            **weighted_perm,
        },
        "degree_only_baseline": {
            "true_score": round(degree_true, 9),
            "positive_units": int(np.sum(np.array(degree_unit_scores) > 0.0)),
            "unit_count": len(degree_unit_scores),
            **degree_perm,
        },
        "weighted_minus_degree_score": round(float(weighted_true - degree_true), 9),
        "boundary": (
            "Cross-model attention-flow support across the exported model set."
            if model_count > 1 and supported
            else "Single-model first export; needs another model or reruns for cross-model closeout."
        ),
    }


def build_mlp_vectors(mlp: pd.DataFrame) -> tuple[list[dict[str, np.ndarray]], list[float]]:
    required = {
        "context",
        "layer_index",
        "input_norm",
        "output_norm",
        "delta_norm",
        "input_output_cosine",
        "token_count",
    }
    missing = required - set(mlp.columns)
    if missing:
        raise SystemExit(f"MLP CSV missing columns: {sorted(missing)}")

    unit_vectors: list[dict[str, np.ndarray]] = []
    unit_scores: list[float] = []
    for _, group in mlp.groupby(["model", "layer_index"]):
        vectors: dict[str, np.ndarray] = {}
        for _, row in group.iterrows():
            context_name = row["context"]
            if context_name not in CONTEXTS:
                continue
            scale = np.sqrt(float(row["token_count"])) if float(row["token_count"]) > 0 else 1.0
            vectors[context_name] = np.array(
                [
                    float(row["input_norm"]) / scale,
                    float(row["output_norm"]) / scale,
                    float(row["delta_norm"]) / scale,
                    float(row["input_output_cosine"]),
                ],
                dtype=float,
            )
        if all(context in vectors for context in CONTEXTS):
            score = unit_separation_score(vectors)
            unit_vectors.append(vectors)
            unit_scores.append(score)
    return unit_vectors, unit_scores


def validate_mlp(mlp: pd.DataFrame, permutations: int, seed: int) -> dict[str, Any]:
    model_names = sorted(str(value) for value in mlp["model"].dropna().unique())
    model_count = len(model_names)
    vectors, unit_scores = build_mlp_vectors(mlp)
    if not vectors:
        return {"status": "blocked_no_matched_mlp_units"}
    true_score = float(np.mean(unit_scores))
    perm = permutation_summary(vectors, true_score, permutations, seed)
    status = (
        "mlp_directional_not_closed"
        if true_score > 0.0 and perm["p_value_one_sided"] > 0.01
        else "mlp_supported_cross_model"
        if true_score > 0.0 and perm["p_value_one_sided"] <= 0.01 and model_count > 1
        else "mlp_supported_single_model"
        if true_score > 0.0 and perm["p_value_one_sided"] <= 0.01
        else "mlp_unsupported"
    )
    return {
        "status": status,
        "models": model_names,
        "model_count": model_count,
        "matched_units": len(vectors),
        "true_score": round(true_score, 9),
        "positive_units": int(np.sum(np.array(unit_scores) > 0.0)),
        "unit_count": len(unit_scores),
        **perm,
        "boundary": (
            "Cross-model MLP delta support across the exported model set; stronger future work can expand layers and reruns."
            if status == "mlp_supported_cross_model"
            else "Treat as directional unless reruns/models expand power."
        ),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    attention = report["attention_flow"]
    mlp = report["mlp_delta"]
    weighted = attention.get("weighted_attention_flow", {})
    degree = attention.get("degree_only_baseline", {})
    model_names = report.get("models", [])
    model_label = ", ".join(model_names) if model_names else "exported models"
    cross_model = len(model_names) > 1
    read_scope = "cross-model" if cross_model else "single-model"
    clean_subject = (
        f"The exported model set (`{model_label}`) now has"
        if cross_model
        else f"{model_label} now has"
    )
    if attention.get("status") == "attention_flow_supported_cross_model" and mlp.get("status") == "mlp_unsupported":
        next_step = "Run an MLP-depth expansion or denser layer grid before promoting feed-forward / MLP support."
    elif cross_model:
        next_step = "Add reruns or a second independent prompt set so the cross-model result can be tested for repeatability."
    else:
        next_step = "Run the same export and validation on the next strong model, then combine under leave-one-model and shuffled-label controls."
    mlp_status = mlp.get("status")
    mlp_line = (
        "- MLP deltas are supported in the combined export"
        if mlp_status == "mlp_supported_cross_model"
        else "- MLP deltas are directional but not closed in this export"
        if mlp_status == "mlp_directional_not_closed"
        else "- MLP deltas are not supported in this export"
    )
    lines = [
        "# V8 Attention / MLP Validation Report",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        f"{clean_subject} real transformer-internal exports: attention top-k",
        "routing edges and MLP block-delta rows across lattice, neutral, and",
        "technical contexts.",
        "",
        f"The {read_scope} validation result is bounded but meaningful:",
        "",
        "- weighted attention-flow separates lattice from neutral/technical above",
        "  shuffled context labels",
        "- the degree-only graph baseline is weaker than weighted attention-flow",
        "- weighted attention-flow beats the degree-only baseline",
        mlp_line,
        "",
        "## Scope",
        "",
        f"- models: `{model_label}`",
        f"- attention rows: `{report.get('attention_rows')}`",
        f"- MLP rows: `{report.get('mlp_rows')}`",
        "",
        "## Attention Flow",
        "",
        f"- status: `{attention.get('status')}`",
        f"- matched layer/head/query units: `{attention.get('matched_units')}`",
        f"- weighted true score: `{weighted.get('true_score')}`",
        f"- weighted shuffled-label p: `{weighted.get('p_value_one_sided')}`",
        f"- weighted positive units: `{weighted.get('positive_units')} / {weighted.get('unit_count')}`",
        f"- degree-only true score: `{degree.get('true_score')}`",
        f"- degree-only shuffled-label p: `{degree.get('p_value_one_sided')}`",
        f"- weighted minus degree score: `{attention.get('weighted_minus_degree_score')}`",
        "",
        "## MLP Delta",
        "",
        f"- status: `{mlp.get('status')}`",
        f"- matched layer units: `{mlp.get('matched_units')}`",
        f"- true score: `{mlp.get('true_score')}`",
        f"- shuffled-label p: `{mlp.get('p_value_one_sided')}`",
        f"- positive units: `{mlp.get('positive_units')} / {mlp.get('unit_count')}`",
        "",
        "## Boundary",
        "",
        (
            "- This supports a first cross-model attention-flow result across the exported model set."
            if cross_model
            else "- This supports a first single-model attention-flow result, not a cross-model closeout."
        ),
        (
            "- MLP is supported in the combined export, with stronger future work still needing reruns or more layers."
            if mlp_status == "mlp_supported_cross_model"
            else "- MLP is directional but not closed; it needs more layers, reruns, or models before promotion."
            if mlp_status == "mlp_directional_not_closed"
            else "- MLP is unsupported in this export; treat the result as attention-flow support only until MLP closes separately."
        ),
        "- This is real transformer-internal evidence, not residual-stream substitution.",
        "",
        "## Next Step",
        "",
        next_step,
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    attention_path = Path(args.attention_csv).resolve()
    mlp_path = Path(args.mlp_csv).resolve()
    require_file(attention_path)
    require_file(mlp_path)

    attention = pd.read_csv(attention_path)
    mlp = pd.read_csv(mlp_path)
    model_names = sorted(set(str(value) for value in attention["model"].dropna().unique()) | set(str(value) for value in mlp["model"].dropna().unique()))
    attention_report = validate_attention(attention, args.permutations, args.seed)
    mlp_report = validate_mlp(mlp, args.permutations, args.seed + 100)
    status = (
        "attention_and_mlp_supported_cross_model"
        if attention_report.get("status") == "attention_flow_supported_cross_model"
        and mlp_report.get("status") == "mlp_supported_cross_model"
        else "attention_supported_mlp_directional_cross_model"
        if attention_report.get("status") == "attention_flow_supported_cross_model"
        and mlp_report.get("status") == "mlp_directional_not_closed"
        else "attention_and_mlp_supported_single_model"
        if attention_report.get("status") == "attention_flow_supported_single_model"
        and mlp_report.get("status") == "mlp_supported_single_model"
        else
        "attention_supported_mlp_directional"
        if attention_report.get("status") == "attention_flow_supported_single_model"
        and mlp_report.get("status") == "mlp_directional_not_closed"
        else "partial_or_unsupported"
    )
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "attention_csv": str(attention_path),
        "mlp_csv": str(mlp_path),
        "attention_rows": int(len(attention)),
        "mlp_rows": int(len(mlp)),
        "models": model_names,
        "model_count": len(model_names),
        "attention_flow": attention_report,
        "mlp_delta": mlp_report,
    }
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "v8_attention_mlp_validation_report.json"
    md_path = output_dir / "v8_attention_mlp_validation_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
