#!/usr/bin/env python3
"""GRAPH-2 quantum-label crosswalk.

This runner tests the useful Drumactually/Claude hypothesis without inflating
it: Phase 6/7 quantum fidelity pairs are independent of the Phase 5 bridge
graph scoring, so they can be used as an internal cross-artifact label source.

The result is still an internal Mirror-stack crosswalk, not external domain
graph validation. If the labels do not beat shuffled controls and degree
baselines, the lane stays open.
"""

from __future__ import annotations

import csv
import json
import random
from collections.abc import Iterable
from pathlib import Path

from graph12_pathway_validation import (
    auc,
    build_graph,
    greater_equal_p_value,
    read_csv,
    score_pairs,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EDGE_CSV = (
    REPO_ROOT
    / "artifacts"
    / "validation"
    / "graph2_phase5_bridge"
    / "graph2_phase5_bridge_edges.csv"
)
PHASE6_JSON = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase6_pennylane_encoding"
    / "v8_phase6_pennylane_encoding_data_2026-04-22.json"
)
PHASE7_JSON = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase7_qiskit_mirror"
    / "v8_phase7_qiskit_mirror_data_2026-04-22.json"
)
PHASE9_JSON = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase9_ibm_hardware_bridge"
    / "v8_phase9_ibm_hardware_bridge_data_2026-04-22.json"
)
DEFAULT_OUT_DIR = (
    REPO_ROOT / "artifacts" / "validation" / "graph2_quantum_label_crosswalk"
)


def norm_pair(pair: Iterable[str]) -> tuple[str, str]:
    left, right = pair
    return tuple(sorted((left, right)))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def all_unordered_pairs(nodes: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for index, source in enumerate(nodes):
        for target in nodes[index + 1 :]:
            pairs.append((source, target))
    return pairs


def nearest_modes() -> dict[str, dict]:
    phase6 = read_json(PHASE6_JSON)
    phase7 = read_json(PHASE7_JSON)
    modes: dict[str, dict] = {}
    sources = {
        "phase6_angle": phase6.get("angle_nearest_pairs", []),
        "phase6_amplitude": phase6.get("amplitude_nearest_pairs", []),
        "phase7_angle": phase7.get("qiskit_angle_nearest_pairs", []),
        "phase7_amplitude": phase7.get("qiskit_amplitude_nearest_pairs", []),
    }
    for source_name, pairs in sources.items():
        for top_k in range(1, 6):
            selected = {norm_pair(item["pair"]) for item in pairs[:top_k]}
            modes[f"{source_name}_top{top_k}"] = {
                "selected_pairs": selected,
                "label_source": source_name,
                "label_rule": f"top {top_k} nearest quantum-fidelity pairs",
            }
    # Phase 9 hardware has only Mistral, Hermes, Nemotron encoded. The only
    # stable pair-order claim we can audit here is the Mistral/Hermes hardware
    # subset relation; it is too small to close GRAPH-2 by itself.
    if PHASE9_JSON.exists():
        modes["phase9_hardware_subset_mistral_hermes"] = {
            "selected_pairs": {norm_pair(("Mistral", "Hermes"))},
            "label_source": "phase9_ibm_hardware_bridge",
            "label_rule": "Mistral/Hermes closest encoded hardware subset pair",
        }
    return modes


def write_label_csv(path: Path, nodes: list[str], mode: dict) -> list[dict[str, object]]:
    selected = mode["selected_pairs"]
    if "phase6" in mode["label_source"]:
        evidence_uri = str(PHASE6_JSON)
    elif "phase7" in mode["label_source"]:
        evidence_uri = str(PHASE7_JSON)
    else:
        evidence_uri = str(PHASE9_JSON)
    rows: list[dict[str, object]] = []
    for source, target in all_unordered_pairs(nodes):
        rows.append(
            {
                "source": source,
                "target": target,
                "label": int(norm_pair((source, target)) in selected),
                "label_source": mode["label_source"],
                "label_method": mode["label_rule"],
                "evidence_uri": evidence_uri,
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def score_label_rows(
    edge_csv: Path,
    label_rows: list[dict[str, object]],
    permutations: int,
    seed: int,
) -> tuple[dict, list[dict[str, object]]]:
    adjacency, degrees = build_graph(read_csv(edge_csv))
    scored = score_pairs(adjacency, degrees, [{k: str(v) for k, v in row.items()} for row in label_rows])
    labels = [int(row["label"]) for row in scored]
    mirror_scores = [float(row["mirror_path_score"]) for row in scored]
    degree_scores = [float(row["degree_baseline_score"]) for row in scored]
    mirror_auc = auc(mirror_scores, labels)
    degree_auc = auc(degree_scores, labels)
    metrics = {
        "positive_labels": sum(labels),
        "control_labels": len(labels) - sum(labels),
        "labeled_pair_count": len(labels),
        "mirror_path_auc": round(mirror_auc, 6),
        "degree_baseline_auc": round(degree_auc, 6),
        "mirror_minus_degree_auc": round(mirror_auc - degree_auc, 6),
    }
    if len(scored) >= 10 and len(set(labels)) >= 2:
        rng = random.Random(seed)
        mirror_null: list[float] = []
        degree_null: list[float] = []
        for _ in range(permutations):
            shuffled = labels[:]
            rng.shuffle(shuffled)
            mirror_null.append(auc(mirror_scores, shuffled))
            degree_null.append(auc(degree_scores, shuffled))
        metrics["mirror_path_auc_label_shuffle_p"] = round(
            greater_equal_p_value(mirror_auc, mirror_null), 6
        )
        metrics["degree_baseline_auc_label_shuffle_p"] = round(
            greater_equal_p_value(degree_auc, degree_null), 6
        )
    return metrics, scored


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def status_for(metrics: dict) -> str:
    if metrics["positive_labels"] < 1 or metrics["control_labels"] < 1:
        return "blocked_insufficient_label_classes"
    if (
        metrics.get("mirror_path_auc_label_shuffle_p", 1.0) <= 0.05
        and metrics["mirror_path_auc"] > metrics["degree_baseline_auc"]
    ):
        return "completed_control_supported_internal_crosswalk"
    if metrics["mirror_path_auc"] > metrics["degree_baseline_auc"]:
        return "completed_soft_positive_no_shuffle_support"
    return "completed_no_control_support"


def write_report(out_dir: Path, report: dict) -> None:
    (out_dir / "graph2_quantum_label_crosswalk_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GRAPH-2 Quantum-Label Crosswalk",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Best Mode",
        "",
    ]
    for key, value in report["best_mode"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Mode Summary", ""])
    for row in report["mode_summary"]:
        lines.append(
            "- "
            f"`{row['mode']}`: status `{row['status']}`, "
            f"mirror AUC `{row['mirror_path_auc']}`, "
            f"degree AUC `{row['degree_baseline_auc']}`, "
            f"shuffle p `{row.get('mirror_path_auc_label_shuffle_p', 'n/a')}`"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            report["boundary"],
            "",
            "## Next Requirement",
            "",
            report["next_requirement"],
            "",
        ]
    )
    (out_dir / "graph2_quantum_label_crosswalk_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    out_dir = DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    adjacency, _degrees = build_graph(read_csv(DEFAULT_EDGE_CSV))
    nodes = sorted(adjacency)
    summary_rows: list[dict[str, object]] = []
    all_details: dict[str, dict] = {}
    for mode_name, mode in nearest_modes().items():
        label_csv = out_dir / f"{mode_name}_labels.csv"
        scored_csv = out_dir / f"{mode_name}_scored_pairs.csv"
        label_rows = write_label_csv(label_csv, nodes, mode)
        metrics, scored = score_label_rows(DEFAULT_EDGE_CSV, label_rows, permutations=10000, seed=67)
        write_csv(scored_csv, scored)
        status = status_for(metrics)
        row = {"mode": mode_name, "status": status, **metrics}
        summary_rows.append(row)
        all_details[mode_name] = {
            "status": status,
            "label_rule": mode["label_rule"],
            "label_source": mode["label_source"],
            "metrics": metrics,
            "label_csv": str(label_csv.relative_to(REPO_ROOT)),
            "scored_csv": str(scored_csv.relative_to(REPO_ROOT)),
        }

    write_csv(out_dir / "graph2_quantum_label_crosswalk_summary.csv", summary_rows)
    best = max(
        summary_rows,
        key=lambda row: (
            row["status"] == "completed_control_supported_internal_crosswalk",
            row["mirror_minus_degree_auc"],
            -row.get("mirror_path_auc_label_shuffle_p", 1.0),
            row["mirror_path_auc"],
        ),
    )
    if best["status"] == "completed_control_supported_internal_crosswalk":
        status = "completed_control_supported_internal_crosswalk"
        read = (
            "A quantum-label crosswalk closed internally against the Phase 5 graph. "
            "This is still an internal cross-artifact result, not external GRAPH-2 domain validation."
        )
    elif any(row["status"] == "completed_soft_positive_no_shuffle_support" for row in summary_rows):
        status = "completed_internal_crosswalk_soft_positive_only"
        read = (
            "Quantum-derived labels produced at least one soft-positive internal GRAPH-2 crosswalk, "
            "but no mode cleanly beat both degree baseline and shuffled-label controls."
        )
    else:
        status = "completed_internal_crosswalk_no_control_closeout"
        read = (
            "Quantum-derived labels are a valid independent internal crosswalk attempt, "
            "but they did not close GRAPH-2 against the current Phase 5 graph."
        )
    report = {
        "status": status,
        "read": read,
        "edge_csv": str(DEFAULT_EDGE_CSV.relative_to(REPO_ROOT)),
        "source_artifacts": [
            str(PHASE6_JSON.relative_to(REPO_ROOT)),
            str(PHASE7_JSON.relative_to(REPO_ROOT)),
            str(PHASE9_JSON.relative_to(REPO_ROOT)),
        ],
        "best_mode": best,
        "mode_summary": summary_rows,
        "details": all_details,
        "boundary": (
            "This tests whether quantum bridge pair order can serve as an independent internal label source "
            "for the Phase 5 bridge graph. It does not validate external graph domains such as allostery, "
            "chemistry, grid flow, logistics, or molecular pathways."
        ),
        "next_requirement": (
            "GRAPH-2 still needs stronger independent labels from a real external or domain graph, "
            "or a richer attention-flow graph where labels are locked before scoring."
        ),
    }
    write_report(out_dir, report)
    print(f"Wrote GRAPH-2 quantum-label crosswalk to {out_dir}")


if __name__ == "__main__":
    main()
