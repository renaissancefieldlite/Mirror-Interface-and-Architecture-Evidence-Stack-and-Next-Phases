#!/usr/bin/env python3
"""Nest 1 control-closeout pass for the first four lanes.

This runner adds explicit null controls to the first real Nest 1 evidence
lanes. It uses existing real artifacts only:

- LA/GEO: Phase 6 feature geometry with exact shuffled-label controls.
- STAT/PROB: Phase 2 and Phase 4 rerun matrices with run-label permutation.
- NUM/GRP: Phase 9D hardware signs with pass/circuit shuffled controls.
- TOPOG: Phase 4 anchor stability with random-anchor controls, plus Phase 5
  anchor summary for context.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PHASE6 = REPO_ROOT / "artifacts" / "v8" / "phase6_pennylane_encoding" / "v8_phase6_pennylane_encoding_data_2026-04-22.json"
DEFAULT_PHASE2 = REPO_ROOT / "artifacts" / "v8" / "phase2_variance_pack" / "v8_phase2_variance_pack_data_2026-04-21.json"
DEFAULT_PHASE4 = REPO_ROOT / "artifacts" / "v8" / "phase4_localization_variance_pack" / "v8_phase4_localization_variance_pack_data_2026-04-21.json"
DEFAULT_PHASE5 = REPO_ROOT / "artifacts" / "v8" / "phase5_internal_bridge" / "v8_phase5_internal_bridge_pack_data_2026-04-22.json"
DEFAULT_PHASE9D = REPO_ROOT / "artifacts" / "v8" / "phase9d_pennylane_remote_repeat" / "v8_phase9d_pennylane_remote_repeat_data_2026-04-22.json"
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "nest1_control_closeout"

EXPECTED_BRIDGE_PAIRS = [
    ("Mistral", "Hermes"),
    ("Qwen", "DeepSeek"),
    ("GLM", "Nemotron"),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def as_float(value: Any, default: float = float("nan")) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def clean_float(value: Any, digits: int = 6) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(numeric):
        return None
    return round(numeric, digits)


def zscore(matrix: np.ndarray) -> np.ndarray:
    mean = np.mean(matrix, axis=0)
    std = np.std(matrix, axis=0)
    std[std == 0] = 1.0
    return (matrix - mean) / std


def pairwise_distances(matrix: np.ndarray) -> np.ndarray:
    diff = matrix[:, None, :] - matrix[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=2))


def load_phase6_matrix(path: Path) -> tuple[list[str], list[str], np.ndarray]:
    data = load_json(path)
    features = list(data["features"])
    models = []
    rows = []
    for model in data["models"]:
        models.append(str(model["model"]))
        rows.append([as_float(model["normalized_features"].get(feature)) for feature in features])
    return models, features, np.array(rows, dtype=float)


def bridge_pair_score(labels: tuple[str, ...] | list[str], distances: np.ndarray) -> dict[str, Any]:
    index = {label: i for i, label in enumerate(labels)}
    checks = []
    mutual_hits = 0
    top2_hits = 0
    total_distance = 0.0
    for left, right in EXPECTED_BRIDGE_PAIRS:
        left_i = index[left]
        right_i = index[right]
        left_order = [j for j in np.argsort(distances[left_i]) if j != left_i]
        right_order = [j for j in np.argsort(distances[right_i]) if j != right_i]
        left_rank = left_order.index(right_i) + 1
        right_rank = right_order.index(left_i) + 1
        distance = float(distances[left_i, right_i])
        mutual = left_rank == 1 and right_rank == 1
        top2 = left_rank <= 2 and right_rank <= 2
        mutual_hits += int(mutual)
        top2_hits += int(top2)
        total_distance += distance
        checks.append(
            {
                "pair": f"{left}/{right}",
                "distance": clean_float(distance),
                "left_rank_of_right": left_rank,
                "right_rank_of_left": right_rank,
                "mutual_nearest": mutual,
                "within_top2_both_directions": top2,
            }
        )
    return {
        "mutual_hits": mutual_hits,
        "top2_hits": top2_hits,
        "total_pair_distance": total_distance,
        "checks": checks,
    }


def la_geo_control(phase6_path: Path) -> dict[str, Any]:
    labels, features, matrix = load_phase6_matrix(phase6_path)
    scaled = zscore(matrix)
    distances = pairwise_distances(scaled)
    observed = bridge_pair_score(labels, distances)

    null_mutual = []
    null_top2 = []
    null_distance = []
    total = 0
    for perm in itertools.permutations(labels):
        score = bridge_pair_score(perm, distances)
        null_mutual.append(score["mutual_hits"])
        null_top2.append(score["top2_hits"])
        null_distance.append(score["total_pair_distance"])
        total += 1

    observed_distance = observed["total_pair_distance"]
    mutual_ge = sum(1 for value in null_mutual if value >= observed["mutual_hits"])
    top2_ge = sum(1 for value in null_top2 if value >= observed["top2_hits"])
    distance_le = sum(1 for value in null_distance if value <= observed_distance)
    return {
        "lane": "LA/GEO",
        "input": str(phase6_path),
        "control": "exact shuffled-label null over Phase 6 feature geometry",
        "models": labels,
        "features": features,
        "observed": {
            "mutual_hits": f"{observed['mutual_hits']}/{len(EXPECTED_BRIDGE_PAIRS)}",
            "top2_hits": f"{observed['top2_hits']}/{len(EXPECTED_BRIDGE_PAIRS)}",
            "total_pair_distance": clean_float(observed_distance),
            "pair_checks": observed["checks"],
        },
        "null": {
            "permutations": total,
            "mean_mutual_hits": clean_float(np.mean(null_mutual)),
            "mean_top2_hits": clean_float(np.mean(null_top2)),
            "mean_total_pair_distance": clean_float(np.mean(null_distance)),
            "p_mutual_hits_ge_observed": clean_float(mutual_ge / total),
            "p_top2_hits_ge_observed": clean_float(top2_ge / total),
            "p_total_distance_le_observed": clean_float(distance_le / total),
        },
    }


def exact_after_baseline(values: list[Any]) -> bool:
    if len(values) < 2:
        return False
    post = values[1:]
    return len({json.dumps(value, sort_keys=True) for value in post}) == 1


def phase_exact_count(models: list[dict[str, Any]], key: str) -> int:
    return sum(1 for model in models if exact_after_baseline(model.get(key, [])))


def column_shuffle_exact_null(
    models: list[dict[str, Any]],
    key: str,
    trials: int,
    seed: int,
) -> dict[str, Any]:
    rng = random.Random(seed)
    matrix = [list(model.get(key, []))[1:] for model in models]
    if not matrix or not matrix[0]:
        return {"trials": trials, "null_counts": [], "p_ge_observed": None}

    columns = list(zip(*matrix, strict=True))
    observed = phase_exact_count(models, key)
    null_counts = []
    for _ in range(trials):
        shuffled_columns = []
        for column in columns:
            values = list(column)
            rng.shuffle(values)
            shuffled_columns.append(values)
        shuffled_rows = list(zip(*shuffled_columns, strict=True))
        count = sum(1 for row in shuffled_rows if len(set(row)) == 1)
        null_counts.append(count)
    ge = sum(1 for count in null_counts if count >= observed)
    return {
        "trials": trials,
        "observed_exact_count": observed,
        "mean_null_exact_count": clean_float(np.mean(null_counts)),
        "max_null_exact_count": int(max(null_counts)) if null_counts else None,
        "p_ge_observed": clean_float((ge + 1) / (trials + 1)),
    }


def stat_prob_control(phase2_path: Path, phase4_path: Path, trials: int, seed: int) -> dict[str, Any]:
    phase2 = load_json(phase2_path)
    phase4 = load_json(phase4_path)
    phase2_models = phase2.get("models", [])
    phase4_models = phase4.get("models", [])

    phase2_target_null = column_shuffle_exact_null(phase2_models, "target_values", trials, seed)
    phase2_layer_null = column_shuffle_exact_null(phase2_models, "target_layers", trials, seed + 1)
    phase4_target_null = column_shuffle_exact_null(phase4_models, "target_values", trials, seed + 2)
    phase4_anchor_null = column_shuffle_exact_null(phase4_models, "dominant_anchors", trials, seed + 3)

    return {
        "lane": "STAT/PROB",
        "inputs": [str(phase2_path), str(phase4_path)],
        "control": "run-label permutation over rerun matrices",
        "phase2": {
            "model_count": len(phase2_models),
            "reported_exact_after_baseline_count": sum(1 for model in phase2_models if model.get("rerun_exact_after_baseline")),
            "target_value_exact_control": phase2_target_null,
            "target_layer_exact_control": phase2_layer_null,
            "only_live_variance_row": phase2.get("only_live_variance_row"),
        },
        "phase4": {
            "model_count": len(phase4_models),
            "reported_exact_after_baseline_count": sum(1 for model in phase4_models if model.get("rerun_exact_after_baseline")),
            "target_value_exact_control": phase4_target_null,
            "dominant_anchor_exact_control": phase4_anchor_null,
        },
    }


def hardware_rows(phase9d_path: Path) -> list[dict[str, Any]]:
    data = load_json(phase9d_path)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pass_item in data.get("passes", []):
        label = pass_item.get("label")
        backend = pass_item.get("backend", {}).get("name")
        for result in pass_item.get("circuit_results", []):
            parity = as_float(result.get("parity_expectation"))
            sign = 1 if parity > 0 else -1 if parity < 0 else 0
            grouped[str(result.get("name"))].append(
                {
                    "pass_label": label,
                    "backend": backend,
                    "parity": parity,
                    "sign": sign,
                }
            )
    rows = []
    for circuit, items in sorted(grouped.items()):
        signs = [item["sign"] for item in items]
        nonzero = [sign for sign in signs if sign != 0]
        parities = [item["parity"] for item in items]
        rows.append(
            {
                "circuit": circuit,
                "signs": signs,
                "parities": parities,
                "sign_stable": len(set(nonzero)) <= 1,
                "mean_parity": clean_float(np.mean(parities)),
                "std_parity": clean_float(np.std(parities)),
            }
        )
    return rows


def stable_sign_count(sign_matrix: list[list[int]]) -> int:
    count = 0
    for signs in sign_matrix:
        nonzero = [sign for sign in signs if sign != 0]
        count += int(len(set(nonzero)) <= 1)
    return count


def num_grp_control(phase9d_path: Path, trials: int, seed: int) -> dict[str, Any]:
    rows = hardware_rows(phase9d_path)
    sign_matrix = [row["signs"] for row in rows]
    observed = stable_sign_count(sign_matrix)
    rng = random.Random(seed)
    transposed = list(zip(*sign_matrix, strict=True))
    null_counts = []
    for _ in range(trials):
        shuffled_columns = []
        for column in transposed:
            values = list(column)
            rng.shuffle(values)
            shuffled_columns.append(values)
        shuffled_rows = [list(row) for row in zip(*shuffled_columns, strict=True)]
        null_counts.append(stable_sign_count(shuffled_rows))
    ge = sum(1 for count in null_counts if count >= observed)
    return {
        "lane": "NUM/GRP",
        "input": str(phase9d_path),
        "control": "circuit-label shuffle within each hardware pass",
        "observed": {
            "stable_sign_circuits": f"{observed}/{len(rows)}",
            "circuit_rows": rows,
        },
        "null": {
            "trials": trials,
            "mean_stable_sign_circuits": clean_float(np.mean(null_counts)),
            "max_stable_sign_circuits": int(max(null_counts)) if null_counts else None,
            "p_ge_observed": clean_float((ge + 1) / (trials + 1)),
        },
    }


def phase5_topography_summary(phase5_path: Path) -> dict[str, Any]:
    data = load_json(phase5_path)
    rows = data.get("models", [])
    return {
        "model_count": len(rows),
        "dominant_anchor_counts": dict(Counter(str(row.get("dominant_anchor")) for row in rows)),
        "path_archetype_counts": dict(Counter(str(row.get("path_archetype")) for row in rows)),
        "mean_overlap_jaccard": clean_float(np.mean([as_float(row.get("overlap_jaccard")) for row in rows])),
    }


def topog_control(phase4_path: Path, phase5_path: Path, trials: int, seed: int) -> dict[str, Any]:
    phase4 = load_json(phase4_path)
    models = phase4.get("models", [])
    anchor_null = column_shuffle_exact_null(models, "dominant_anchors", trials, seed)
    layer_null = column_shuffle_exact_null(models, "dominant_layers", trials, seed + 1)
    return {
        "lane": "TOPOG",
        "inputs": [str(phase4_path), str(phase5_path)],
        "control": "random-anchor and random-layer controls over Phase 4 localization reruns",
        "phase4": {
            "model_count": len(models),
            "dominant_anchor_stability": anchor_null,
            "dominant_layer_stability": layer_null,
        },
        "phase5_context": phase5_topography_summary(phase5_path),
    }


def lane_status(p_values: list[float | None], threshold: float = 0.05) -> str:
    valid = [p for p in p_values if p is not None]
    if not valid:
        return "blocked"
    if any(p <= threshold for p in valid):
        return "control_supported"
    return "control_not_significant"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    la_geo = la_geo_control(args.phase6)
    stat_prob = stat_prob_control(args.phase2, args.phase4, args.trials, args.seed)
    num_grp = num_grp_control(args.phase9d, args.trials, args.seed + 10)
    topog = topog_control(args.phase4, args.phase5, args.trials, args.seed + 20)

    lanes = [
        {
            "lane": "LA/GEO",
            "status": lane_status(
                [
                    la_geo["null"]["p_mutual_hits_ge_observed"],
                    la_geo["null"]["p_top2_hits_ge_observed"],
                    la_geo["null"]["p_total_distance_le_observed"],
                ]
            ),
            "headline": (
                f"Observed {la_geo['observed']['mutual_hits']} mutual bridge-pair hits "
                f"against exact shuffled-label null p={la_geo['null']['p_mutual_hits_ge_observed']}."
            ),
        },
        {
            "lane": "STAT/PROB",
            "status": lane_status(
                [
                    stat_prob["phase2"]["target_value_exact_control"]["p_ge_observed"],
                    stat_prob["phase4"]["target_value_exact_control"]["p_ge_observed"],
                    stat_prob["phase4"]["dominant_anchor_exact_control"]["p_ge_observed"],
                ]
            ),
            "headline": (
                "Phase 2 / Phase 4 exact rerun structure tested against run-label "
                "permutation controls."
            ),
        },
        {
            "lane": "NUM/GRP",
            "status": lane_status([num_grp["null"]["p_ge_observed"]]),
            "headline": (
                f"Observed {num_grp['observed']['stable_sign_circuits']} sign-stable "
                f"circuits against pass-shuffled null p={num_grp['null']['p_ge_observed']}."
            ),
        },
        {
            "lane": "TOPOG",
            "status": lane_status(
                [
                    topog["phase4"]["dominant_anchor_stability"]["p_ge_observed"],
                    topog["phase4"]["dominant_layer_stability"]["p_ge_observed"],
                ]
            ),
            "headline": "Phase 4 anchor/layer stability tested against random-anchor controls.",
        },
    ]

    return {
        "status": "completed_local_control_closeout",
        "claim_boundary": (
            "Explicit controls for the first four Nest 1 lanes. This strengthens "
            "the real-data evidence ladder but does not close every Nest 1 lane."
        ),
        "trials": args.trials,
        "seed": args.seed,
        "lanes": lanes,
        "results": {
            "la_geo": la_geo,
            "stat_prob": stat_prob,
            "num_grp": num_grp,
            "topog": topog,
        },
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(report: dict[str, Any]) -> str:
    results = report["results"]
    lines = [
        "# Nest 1 Control-Closeout Pass",
        "",
        f"Status: `{report['status']}`",
        "",
        report["claim_boundary"],
        "",
        "## Lane Summary",
        "",
        "| Lane | Status | Headline |",
        "| --- | --- | --- |",
    ]
    for lane in report["lanes"]:
        lines.append(f"| `{lane['lane']}` | `{lane['status']}` | {lane['headline']} |")

    la_geo = results["la_geo"]
    lines.extend(
        [
            "",
            "## LA/GEO Shuffled-Label Control",
            "",
            f"- Observed mutual bridge-pair hits: `{la_geo['observed']['mutual_hits']}`",
            f"- Observed top-2 reciprocal hits: `{la_geo['observed']['top2_hits']}`",
            f"- Exact permutations: `{la_geo['null']['permutations']}`",
            f"- Null mean mutual hits: `{la_geo['null']['mean_mutual_hits']}`",
            f"- p(mutual hits >= observed): `{la_geo['null']['p_mutual_hits_ge_observed']}`",
            f"- p(top-2 hits >= observed): `{la_geo['null']['p_top2_hits_ge_observed']}`",
            f"- p(total pair distance <= observed): `{la_geo['null']['p_total_distance_le_observed']}`",
            "",
            "| Pair | Distance | Rank L->R | Rank R->L | Mutual | Top-2 Both |",
            "| --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for check in la_geo["observed"]["pair_checks"]:
        lines.append(
            f"| {check['pair']} | {check['distance']} | {check['left_rank_of_right']} | "
            f"{check['right_rank_of_left']} | {check['mutual_nearest']} | "
            f"{check['within_top2_both_directions']} |"
        )

    stat = results["stat_prob"]
    lines.extend(
        [
            "",
            "## STAT/PROB Rerun Permutation Controls",
            "",
            "| Pack | Observed Exact Count | Null Mean | Null Max | p >= Observed |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    stat_rows = [
        ("Phase 2 target values", stat["phase2"]["target_value_exact_control"]),
        ("Phase 2 target layers", stat["phase2"]["target_layer_exact_control"]),
        ("Phase 4 target values", stat["phase4"]["target_value_exact_control"]),
        ("Phase 4 dominant anchors", stat["phase4"]["dominant_anchor_exact_control"]),
    ]
    for label, row in stat_rows:
        lines.append(
            f"| {label} | {row['observed_exact_count']} | {row['mean_null_exact_count']} | "
            f"{row['max_null_exact_count']} | {row['p_ge_observed']} |"
        )

    num = results["num_grp"]
    lines.extend(
        [
            "",
            "## NUM/GRP Hardware Sign-Shuffle Control",
            "",
            f"- Observed sign-stable circuits: `{num['observed']['stable_sign_circuits']}`",
            f"- Null mean stable sign circuits: `{num['null']['mean_stable_sign_circuits']}`",
            f"- Null max stable sign circuits: `{num['null']['max_stable_sign_circuits']}`",
            f"- p(stable signs >= observed): `{num['null']['p_ge_observed']}`",
            "",
            "| Circuit | Signs | Mean Parity | Std Parity | Sign Stable |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in num["observed"]["circuit_rows"]:
        lines.append(
            f"| `{row['circuit']}` | `{row['signs']}` | {row['mean_parity']} | "
            f"{row['std_parity']} | {row['sign_stable']} |"
        )

    topog = results["topog"]
    lines.extend(
        [
            "",
            "## TOPOG Random-Anchor Controls",
            "",
            "| Control | Observed Stable Count | Null Mean | Null Max | p >= Observed |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    topog_rows = [
        ("Phase 4 dominant anchors", topog["phase4"]["dominant_anchor_stability"]),
        ("Phase 4 dominant layers", topog["phase4"]["dominant_layer_stability"]),
    ]
    for label, row in topog_rows:
        lines.append(
            f"| {label} | {row['observed_exact_count']} | {row['mean_null_exact_count']} | "
            f"{row['max_null_exact_count']} | {row['p_ge_observed']} |"
        )
    lines.extend(
        [
            "",
            "Phase 5 context:",
            "",
            f"- dominant anchor counts: `{topog['phase5_context']['dominant_anchor_counts']}`",
            f"- path archetype counts: `{topog['phase5_context']['path_archetype_counts']}`",
            "",
            "## Boundary",
            "",
            "This pass closes explicit controls for the first four near-term Nest 1 lanes. "
            "`TOP`, `OPT`, `CTRL`, and `COMP/CAT` remain separate lanes with their own "
            "requirements.",
            "",
        ]
    )
    return "\n".join(lines)


def json_ready(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, dict):
        return {key: json_ready(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [json_ready(inner) for inner in value]
    return value


def run(args: argparse.Namespace) -> dict[str, Any]:
    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(args)
    (args.out_dir / "nest1_control_closeout_report.json").write_text(
        json.dumps(json_ready(report), indent=2),
        encoding="utf-8",
    )
    (args.out_dir / "nest1_control_closeout_report.md").write_text(
        render_markdown(report),
        encoding="utf-8",
    )

    lane_rows = [
        {"lane": lane["lane"], "status": lane["status"], "headline": lane["headline"]}
        for lane in report["lanes"]
    ]
    write_csv(args.out_dir / "nest1_control_closeout_lane_summary.csv", lane_rows)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase6", type=Path, default=DEFAULT_PHASE6)
    parser.add_argument("--phase2", type=Path, default=DEFAULT_PHASE2)
    parser.add_argument("--phase4", type=Path, default=DEFAULT_PHASE4)
    parser.add_argument("--phase5", type=Path, default=DEFAULT_PHASE5)
    parser.add_argument("--phase9d", type=Path, default=DEFAULT_PHASE9D)
    parser.add_argument("--trials", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=6701)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()
    report = run(args)
    print(
        json.dumps(
            {
                "status": report["status"],
                "out_dir": str(args.out_dir),
                "lanes": report["lanes"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
