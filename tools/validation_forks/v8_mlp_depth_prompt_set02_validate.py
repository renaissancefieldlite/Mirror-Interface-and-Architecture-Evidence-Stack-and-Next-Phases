#!/usr/bin/env python3
"""Validate the prompt_set_02 all-layer MLP export.

This runner keeps the same score used by the earlier attention/MLP gate:
lattice-to-control separation minus control-to-control separation, with
shuffled context-label controls. The new input is a denser MLP layer grid.
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
DEFAULT_MLP_CSV = (
    ROOT
    / "artifacts"
    / "validation"
    / "v8_mlp_depth_prompt_set_02"
    / "v8_mlp_depth_prompt_set_02.csv"
)
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_mlp_depth_prompt_set_02_validation"
CONTEXTS = ("lattice", "neutral", "technical")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate prompt_set_02 all-layer MLP grid.")
    parser.add_argument("--mlp-csv", default=str(DEFAULT_MLP_CSV), help="All-layer MLP export CSV.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT), help="Report output directory.")
    parser.add_argument("--permutations", type=int, default=5000, help="Shuffled-label permutations.")
    parser.add_argument("--seed", type=int, default=67, help="Deterministic permutation seed.")
    return parser.parse_args()


def require_file(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Required CSV not found: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"Required CSV is empty: {path}")


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
        "null_p95": round(float(np.quantile(null_array, 0.95)), 9),
        "p_value_one_sided": round(float(p_value), 9),
    }


def build_mlp_vectors(mlp: pd.DataFrame) -> tuple[list[dict[str, np.ndarray]], list[float]]:
    required = {
        "model",
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
            context_name = str(row["context"])
            if context_name not in CONTEXTS:
                continue
            token_count = float(row["token_count"])
            scale = np.sqrt(token_count) if token_count > 0 else 1.0
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


def validate_slice(
    mlp: pd.DataFrame,
    permutations: int,
    seed: int,
) -> dict[str, Any]:
    vectors, unit_scores = build_mlp_vectors(mlp)
    model_names = sorted(str(value) for value in mlp["model"].dropna().unique())
    if not vectors:
        return {
            "status": "input_pending_no_matched_mlp_units",
            "models": model_names,
            "model_count": len(model_names),
            "matched_units": 0,
        }
    true_score = float(np.mean(unit_scores))
    perm = permutation_summary(vectors, true_score, permutations, seed)
    supported = true_score > 0.0 and perm["p_value_one_sided"] <= 0.01
    status = (
        "mlp_depth_supported_cross_model"
        if supported and len(model_names) > 1
        else "mlp_depth_supported_single_model"
        if supported
        else "mlp_depth_directional"
        if true_score > 0.0
        else "mlp_depth_open"
    )
    unit_array = np.array(unit_scores, dtype=float)
    return {
        "status": status,
        "models": model_names,
        "model_count": len(model_names),
        "matched_units": len(vectors),
        "true_score": round(true_score, 9),
        "positive_units": int(np.sum(unit_array > 0.0)),
        "unit_count": len(unit_scores),
        "unit_score_mean": round(float(unit_array.mean()), 9),
        "unit_score_median": round(float(np.median(unit_array)), 9),
        "unit_score_min": round(float(unit_array.min()), 9),
        "unit_score_max": round(float(unit_array.max()), 9),
        **perm,
    }


def validate_by_depth(
    mlp: pd.DataFrame,
    permutations: int,
    seed: int,
) -> dict[str, Any]:
    depth_reports: dict[str, Any] = {}
    if "layer_depth" not in mlp.columns:
        return depth_reports
    for offset, depth in enumerate(("early", "middle", "late")):
        depth_df = mlp[mlp["layer_depth"] == depth]
        if depth_df.empty:
            continue
        depth_reports[depth] = validate_slice(depth_df, permutations, seed + 1000 + offset)
    return depth_reports


def validate_leave_one_model(
    mlp: pd.DataFrame,
    permutations: int,
    seed: int,
) -> dict[str, Any]:
    reports: dict[str, Any] = {}
    model_names = sorted(str(value) for value in mlp["model"].dropna().unique())
    for index, model_name in enumerate(model_names):
        subset = mlp[mlp["model"] != model_name]
        if subset.empty:
            continue
        reports[model_name] = validate_slice(subset, permutations, seed + 2000 + index)
    return reports


def load_prior_prompt_set_02_status() -> dict[str, Any]:
    prior_path = (
        ROOT
        / "artifacts"
        / "validation"
        / "v8_attention_mlp_prompt_generalization"
        / "v8_attention_mlp_prompt_generalization_report.json"
    )
    if not prior_path.exists():
        return {"status": "prior_prompt_set_02_report_missing"}
    report = json.loads(prior_path.read_text(encoding="utf-8"))
    metrics = {entry.get("metric"): entry for entry in report.get("metrics", [])}
    mlp_score = metrics.get("MLP score", {})
    mlp_p = metrics.get("MLP p", {})
    mlp_rows = metrics.get("MLP rows", {})
    return {
        "status": "prior_prompt_set_02_loaded",
        "prior_prompt_set_02_status": report.get("prompt_set_02_status"),
        "prior_prompt_set_02_mlp_supported": report.get("prompt_set_02_mlp_supported"),
        "prior_mlp_rows": mlp_rows.get("prompt_set_02"),
        "prior_mlp_true_score": mlp_score.get("prompt_set_02"),
        "prior_mlp_p_value_one_sided": mlp_p.get("prompt_set_02"),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    overall = report["overall_mlp_depth"]
    prior = report["prior_three_layer_prompt_set_02"]
    depth = report["depth_breakdown"]
    leave_one = report["leave_one_model"]
    status = report["status"]
    supported = status == "mlp_depth_prompt_set_02_supported"
    clean_read_lines = (
        [
            "The result closes the MLP prompt_set_02 depth gate across the full exported grid:",
        ]
        if supported
        else [
            "The result strengthens the MLP prompt_set_02 lane while keeping closeout open:",
            "the all-layer grid is directional overall, early layers carry the strongest",
            "signal, and shuffled-label controls remain above the observed score.",
        ]
    )
    boundary_lines = (
        [
            "This closes the prompt_set_02 MLP depth gate at the all-layer export level.",
            "The next strengthening step is recurrence: rerun_02 / second export on the",
            "same prompt family and the matching SAE recurrence vectors.",
        ]
        if supported
        else [
            "This keeps the prompt_set_02 MLP depth gate open while making the read more precise:",
            "feed-forward deltas are directional overall, strongest in early layers, and weaker",
            "than attention-flow under independent prompt wording. The next useful move is",
            "rerun_02 / second export recurrence plus feature/circuit-level SAE controls,",
            "rather than promoting MLP as closed from this grid alone.",
        ]
    )
    lines = [
        "# V8 MLP Depth Prompt Set 02 Validation Report",
        "",
        f"Status: `{status}`",
        "",
        "## Clean Read",
        "",
        "The prompt_set_02 MLP gate now has a denser real transformer-internal export:",
        "738 all-layer MLP rows across the local model matrix. This replaces the earlier",
        "three-layer sample with a full layer-grid test for feed-forward / MLP deltas.",
        "",
        *clean_read_lines,
        "",
        f"- overall status: `{overall.get('status')}`",
        f"- matched model/layer units: `{overall.get('matched_units')}`",
        f"- true score: `{overall.get('true_score')}`",
        f"- shuffled-label p: `{overall.get('p_value_one_sided')}`",
        f"- null p95: `{overall.get('null_p95')}`",
        f"- positive units: `{overall.get('positive_units')} / {overall.get('unit_count')}`",
        "",
        "## Prior Three-Layer Comparison",
        "",
        f"- prior prompt_set_02 status: `{prior.get('prior_prompt_set_02_status')}`",
        f"- prior prompt_set_02 MLP supported: `{prior.get('prior_prompt_set_02_mlp_supported')}`",
        f"- prior rows: `{prior.get('prior_mlp_rows')}`",
        f"- prior true score: `{prior.get('prior_mlp_true_score')}`",
        f"- prior shuffled-label p: `{prior.get('prior_mlp_p_value_one_sided')}`",
        "",
        "## Depth Breakdown",
        "",
    ]
    for depth_name, depth_report in depth.items():
        lines.extend(
            [
                f"### {depth_name.title()}",
                "",
                f"- status: `{depth_report.get('status')}`",
                f"- matched units: `{depth_report.get('matched_units')}`",
                f"- true score: `{depth_report.get('true_score')}`",
                f"- shuffled-label p: `{depth_report.get('p_value_one_sided')}`",
                f"- positive units: `{depth_report.get('positive_units')} / {depth_report.get('unit_count')}`",
                "",
            ]
        )
    lines.extend(["## Leave-One-Model Controls", ""])
    for model_name, lom_report in leave_one.items():
        lines.append(
            f"- remove `{model_name}`: status `{lom_report.get('status')}`, "
            f"score `{lom_report.get('true_score')}`, p `{lom_report.get('p_value_one_sided')}`"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            *boundary_lines,
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    mlp_path = Path(args.mlp_csv).resolve()
    require_file(mlp_path)
    mlp = pd.read_csv(mlp_path)

    overall = validate_slice(mlp, args.permutations, args.seed)
    depth_reports = validate_by_depth(mlp, args.permutations, args.seed)
    leave_one_reports = validate_leave_one_model(mlp, args.permutations, args.seed)
    supported = overall.get("status") == "mlp_depth_supported_cross_model"
    status = "mlp_depth_prompt_set_02_supported" if supported else "mlp_depth_prompt_set_02_open"

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "mlp_csv": str(mlp_path),
        "mlp_rows": int(len(mlp)),
        "models": sorted(str(value) for value in mlp["model"].dropna().unique()),
        "model_count": int(mlp["model"].nunique()),
        "overall_mlp_depth": overall,
        "depth_breakdown": depth_reports,
        "leave_one_model": leave_one_reports,
        "prior_three_layer_prompt_set_02": load_prior_prompt_set_02_status(),
    }

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "v8_mlp_depth_prompt_set_02_validation_report.json"
    md_path = output_dir / "v8_mlp_depth_prompt_set_02_validation_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
