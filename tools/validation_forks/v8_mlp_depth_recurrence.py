#!/usr/bin/env python3
"""Validate all-layer MLP depth recurrence across base, rerun, and prompt shift."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUTS = {
    "base": ROOT / "artifacts" / "validation" / "v8_mlp_depth_base" / "v8_mlp_depth_base.csv",
    "rerun_02": ROOT
    / "artifacts"
    / "validation"
    / "v8_mlp_depth_rerun_02"
    / "v8_mlp_depth_rerun_02.csv",
    "prompt_set_02": ROOT
    / "artifacts"
    / "validation"
    / "v8_mlp_depth_prompt_set_02"
    / "v8_mlp_depth_prompt_set_02.csv",
}
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "v8_mlp_depth_recurrence"
CONTEXTS = ("lattice", "neutral", "technical")
FEATURE_COLUMNS = ("input_norm", "output_norm", "delta_norm", "input_output_cosine")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate V8 all-layer MLP depth recurrence.")
    parser.add_argument("--base-csv", default=str(DEFAULT_INPUTS["base"]))
    parser.add_argument("--rerun-csv", default=str(DEFAULT_INPUTS["rerun_02"]))
    parser.add_argument("--prompt-csv", default=str(DEFAULT_INPUTS["prompt_set_02"]))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT))
    parser.add_argument("--permutations", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=67)
    return parser.parse_args()


def require_file(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Required input missing: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"Required input is empty: {path}")


def row_vector(row: pd.Series) -> np.ndarray:
    token_count = float(row["token_count"])
    scale = np.sqrt(token_count) if token_count > 0 else 1.0
    return np.array(
        [
            float(row["input_norm"]) / scale,
            float(row["output_norm"]) / scale,
            float(row["delta_norm"]) / scale,
            float(row["input_output_cosine"]),
        ],
        dtype=float,
    )


def separation_score(vectors: dict[str, np.ndarray]) -> float:
    lattice = vectors["lattice"]
    neutral = vectors["neutral"]
    technical = vectors["technical"]
    lattice_to_controls = (np.linalg.norm(lattice - neutral) + np.linalg.norm(lattice - technical)) / 2.0
    control_to_control = np.linalg.norm(neutral - technical)
    return float(lattice_to_controls - control_to_control)


def load_units(path: Path) -> dict[tuple[str, int], dict[str, Any]]:
    require_file(path)
    frame = pd.read_csv(path)
    required = {"model", "context", "layer_index", "layer_depth", "token_count", *FEATURE_COLUMNS}
    missing = required - set(frame.columns)
    if missing:
        raise SystemExit(f"{path} missing columns: {sorted(missing)}")

    units: dict[tuple[str, int], dict[str, Any]] = {}
    for (model, layer_index), group in frame.groupby(["model", "layer_index"]):
        vectors: dict[str, np.ndarray] = {}
        depth_values = sorted(str(value) for value in group["layer_depth"].dropna().unique())
        for _, row in group.iterrows():
            context = str(row["context"])
            if context in CONTEXTS:
                vectors[context] = row_vector(row)
        if all(context in vectors for context in CONTEXTS):
            key = (str(model), int(layer_index))
            units[key] = {
                "model": str(model),
                "layer_index": int(layer_index),
                "layer_depth": depth_values[0] if depth_values else "unknown",
                "vectors": vectors,
                "score": separation_score(vectors),
            }
    return units


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0.0:
        return 0.0
    return float(np.dot(a, b) / denom)


def score_vector(units: dict[tuple[str, int], dict[str, Any]], keys: list[tuple[str, int]]) -> np.ndarray:
    return np.array([units[key]["score"] for key in keys], dtype=float)


def shuffled_score_vector(
    units: dict[tuple[str, int], dict[str, Any]],
    keys: list[tuple[str, int]],
    rng: np.random.Generator,
) -> np.ndarray:
    labels = np.array(CONTEXTS)
    scores = []
    for key in keys:
        original = units[key]["vectors"]
        shuffled_sources = rng.permutation(labels)
        shuffled = {label: original[source] for label, source in zip(labels, shuffled_sources)}
        scores.append(separation_score(shuffled))
    return np.array(scores, dtype=float)


def recurrence_pair(
    left: dict[tuple[str, int], dict[str, Any]],
    right: dict[tuple[str, int], dict[str, Any]],
    permutations: int,
    seed: int,
    depth: str | None = None,
    remove_model: str | None = None,
) -> dict[str, Any]:
    keys = sorted(set(left) & set(right))
    if depth:
        keys = [key for key in keys if left[key]["layer_depth"] == depth and right[key]["layer_depth"] == depth]
    if remove_model:
        keys = [key for key in keys if key[0] != remove_model]
    if not keys:
        return {"status": "input_pending_no_matched_units", "matched_units": 0}

    left_scores = score_vector(left, keys)
    right_scores = score_vector(right, keys)
    true_cosine = cosine(left_scores, right_scores)
    true_mae = float(np.mean(np.abs(left_scores - right_scores)))
    sign_agreement = float(np.mean(np.sign(left_scores) == np.sign(right_scores)))
    positive_agreement = float(np.mean((left_scores > 0.0) & (right_scores > 0.0)))

    rng = np.random.default_rng(seed)
    null_cosines = []
    for _ in range(permutations):
        shuffled_right = shuffled_score_vector(right, keys, rng)
        null_cosines.append(cosine(left_scores, shuffled_right))
    null_array = np.array(null_cosines, dtype=float)
    p_value = (float(np.sum(null_array >= true_cosine)) + 1.0) / (float(permutations) + 1.0)
    supported = true_cosine > 0.0 and p_value <= 0.01
    status = "recurrence_supported" if supported else "recurrence_directional" if true_cosine > 0.0 else "recurrence_open"
    return {
        "status": status,
        "matched_units": len(keys),
        "true_cosine": round(true_cosine, 9),
        "mean_absolute_score_delta": round(true_mae, 9),
        "sign_agreement": round(sign_agreement, 9),
        "positive_agreement": round(positive_agreement, 9),
        "permutations": permutations,
        "seed": seed,
        "null_mean": round(float(null_array.mean()), 9),
        "null_p95": round(float(np.quantile(null_array, 0.95)), 9),
        "p_value_one_sided": round(float(p_value), 9),
    }


def within_set(
    units: dict[tuple[str, int], dict[str, Any]],
    permutations: int,
    seed: int,
) -> dict[str, Any]:
    keys = sorted(units)
    true_scores = score_vector(units, keys)
    true_mean = float(true_scores.mean())
    rng = np.random.default_rng(seed)
    null_means = []
    for _ in range(permutations):
        null_means.append(float(shuffled_score_vector(units, keys, rng).mean()))
    null_array = np.array(null_means, dtype=float)
    p_value = (float(np.sum(null_array >= true_mean)) + 1.0) / (float(permutations) + 1.0)
    supported = true_mean > 0.0 and p_value <= 0.01
    return {
        "status": "mlp_depth_supported" if supported else "mlp_depth_directional" if true_mean > 0 else "mlp_depth_open",
        "matched_units": len(keys),
        "true_score": round(true_mean, 9),
        "positive_units": int(np.sum(true_scores > 0.0)),
        "unit_count": int(len(true_scores)),
        "permutations": permutations,
        "seed": seed,
        "null_mean": round(float(null_array.mean()), 9),
        "null_p95": round(float(np.quantile(null_array, 0.95)), 9),
        "p_value_one_sided": round(float(p_value), 9),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    pair = report["pair_recurrence"]
    within = report["within_set"]
    depth = report["depth_breakdown"]
    leave_one = report["leave_one_model_prompt_shift"]
    lines = [
        "# V8 MLP Depth Recurrence Report",
        "",
        f"Status: `{report['status']}`",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Inputs",
        "",
        f"- base CSV: `{report['inputs']['base']}`",
        f"- rerun_02 CSV: `{report['inputs']['rerun_02']}`",
        f"- prompt_set_02 CSV: `{report['inputs']['prompt_set_02']}`",
        f"- matched units per set: `{report['matched_units']}`",
        "",
        "## Within-Set MLP Depth Separation",
        "",
    ]
    for set_name, set_report in within.items():
        lines.append(
            f"- `{set_name}`: status `{set_report['status']}`, score `{set_report['true_score']}`, "
            f"p `{set_report['p_value_one_sided']}`, positive `{set_report['positive_units']} / {set_report['unit_count']}`"
        )
    lines.extend(["", "## Pair Recurrence", ""])
    for pair_name, pair_report in pair.items():
        lines.append(
            f"- `{pair_name}`: status `{pair_report['status']}`, cosine `{pair_report['true_cosine']}`, "
            f"p `{pair_report['p_value_one_sided']}`, sign agreement `{pair_report['sign_agreement']}`"
        )
    lines.extend(["", "## Depth Breakdown", ""])
    for pair_name, depth_reports in depth.items():
        lines.append(f"### {pair_name}")
        lines.append("")
        for depth_name, depth_report in depth_reports.items():
            lines.append(
                f"- `{depth_name}`: status `{depth_report['status']}`, cosine `{depth_report['true_cosine']}`, "
                f"p `{depth_report['p_value_one_sided']}`, matched `{depth_report['matched_units']}`"
            )
        lines.append("")
    lines.extend(["## Leave-One-Model Prompt-Shift Controls", ""])
    for model_name, model_report in leave_one.items():
        lines.append(
            f"- remove `{model_name}`: status `{model_report['status']}`, cosine `{model_report['true_cosine']}`, "
            f"p `{model_report['p_value_one_sided']}`, matched `{model_report['matched_units']}`"
        )
    lines.extend(
        [
            "",
            "## Outcome",
            "",
            report["outcome"],
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    paths = {
        "base": Path(args.base_csv).resolve(),
        "rerun_02": Path(args.rerun_csv).resolve(),
        "prompt_set_02": Path(args.prompt_csv).resolve(),
    }
    units = {name: load_units(path) for name, path in paths.items()}
    common_keys = sorted(set(units["base"]) & set(units["rerun_02"]) & set(units["prompt_set_02"]))

    within = {
        name: within_set(unit_map, args.permutations, args.seed + index * 100)
        for index, (name, unit_map) in enumerate(units.items())
    }
    pair_defs = {
        "base_to_rerun_02": ("base", "rerun_02"),
        "base_to_prompt_set_02": ("base", "prompt_set_02"),
        "rerun_02_to_prompt_set_02": ("rerun_02", "prompt_set_02"),
    }
    pair_reports = {
        name: recurrence_pair(units[left], units[right], args.permutations, args.seed + 1000 + index * 100)
        for index, (name, (left, right)) in enumerate(pair_defs.items())
    }
    depth_reports: dict[str, Any] = {}
    for pair_index, (pair_name, (left, right)) in enumerate(pair_defs.items()):
        depth_reports[pair_name] = {
            depth: recurrence_pair(
                units[left],
                units[right],
                args.permutations,
                args.seed + 2000 + pair_index * 300 + depth_index * 50,
                depth=depth,
            )
            for depth_index, depth in enumerate(("early", "middle", "late"))
        }

    model_names = sorted({key[0] for key in common_keys})
    leave_one = {
        model: recurrence_pair(
            units["base"],
            units["prompt_set_02"],
            args.permutations,
            args.seed + 4000 + index * 100,
            remove_model=model,
        )
        for index, model in enumerate(model_names)
    }

    same_prompt_supported = pair_reports["base_to_rerun_02"]["status"] == "recurrence_supported"
    prompt_shift_supported = pair_reports["base_to_prompt_set_02"]["status"] == "recurrence_supported"
    within_supported = all(item["status"] == "mlp_depth_supported" for item in within.values())
    status = (
        "mlp_depth_recurrence_supported"
        if same_prompt_supported and prompt_shift_supported and within_supported
        else "mlp_depth_recurrence_partial"
        if same_prompt_supported and prompt_shift_supported
        else "mlp_depth_recurrence_directional"
        if same_prompt_supported
        else "mlp_depth_recurrence_open"
    )
    clean_read = (
        "All-layer MLP depth recurrence is supported across same-prompt rerun and prompt shift above shuffled context-label controls."
        if status == "mlp_depth_recurrence_supported"
        else "All-layer MLP depth recurrence is supported at the pair level across same-prompt rerun and prompt shift, while one or more within-set separation reads remain directional."
        if status == "mlp_depth_recurrence_partial"
        else "All-layer MLP depth recurrence is strongest on same-prompt rerun. Prompt-shift recurrence remains the pressure point."
        if status == "mlp_depth_recurrence_directional"
        else "All-layer MLP depth recurrence remains open under the current controls."
    )
    outcome = (
        "This upgrades MLP from a small-sample same-prompt result plus prompt-set directional signal into a recurrence-tested transformer-internal lane."
        if status in {"mlp_depth_recurrence_supported", "mlp_depth_recurrence_partial"}
        else "This keeps attention-flow and SAE as the stronger middle-layer mechanisms while preserving MLP as a measured open gate."
    )

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "inputs": {name: str(path) for name, path in paths.items()},
        "matched_units": len(common_keys),
        "within_set": within,
        "pair_recurrence": pair_reports,
        "depth_breakdown": depth_reports,
        "leave_one_model_prompt_shift": leave_one,
        "clean_read": clean_read,
        "outcome": outcome,
    }
    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "v8_mlp_depth_recurrence_report.json"
    md_path = out_dir / "v8_mlp_depth_recurrence_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps({"status": status, "report": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
