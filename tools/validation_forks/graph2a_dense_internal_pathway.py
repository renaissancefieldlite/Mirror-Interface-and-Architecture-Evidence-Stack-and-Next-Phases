#!/usr/bin/env python3
"""GRAPH-2A dense internal pathway graph.

Builds a denser measured graph from Phase 4/5 localization and bridge
structure, then tests whether independently sourced Phase 6/7 quantum-pair
labels are recoverable by graph path score above degree and shuffled-label
controls.

No synthetic graph. No label derived from the path score itself.
"""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict, deque
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE5_JSON = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase5_internal_bridge"
    / "v8_phase5_internal_bridge_pack_data_2026-04-22.json"
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
DEFAULT_OUT_DIR = (
    REPO_ROOT / "artifacts" / "validation" / "graph2a_dense_internal_pathway"
)
PRIMARY_MODE = "phase6_amplitude_top3"
ANCHORS = ["early", "mid", "pre", "target", "post", "last"]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def norm_pair(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def normalize_text(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("/", "_")


def anchor_key(value: object) -> str:
    text = normalize_text(value)
    return {
        "early_window": "early",
        "mid_window": "mid",
        "pre_target_window": "pre",
        "target_span": "target",
        "post_target_window": "post",
        "last_window": "last",
        "last_token": "last",
    }.get(text, text)


def add_edge(
    edges: list[dict[str, object]],
    source: str,
    target: str,
    edge_type: str,
    edge_source: str,
    weight: float = 1.0,
) -> None:
    if source == target:
        return
    edges.append(
        {
            "source": source,
            "target": target,
            "edge_weight": round(weight, 6),
            "edge_type": edge_type,
            "edge_source": edge_source,
        }
    )


def build_dense_edges(phase5: dict) -> tuple[list[dict[str, object]], dict[str, dict]]:
    rows = phase5["models"]
    by_model = {row["display_name"]: row for row in rows}
    edges: list[dict[str, object]] = []
    for row in rows:
        model = row["display_name"]
        model_node = f"model:{model}"
        archetype = normalize_text(row["path_archetype"])
        dominant = normalize_text(row["dominant_anchor"])
        dominant_anchor = anchor_key(row["dominant_anchor"])
        variance = normalize_text(row["variance_note"])
        add_edge(edges, model_node, f"archetype:{archetype}", "model_to_archetype", "phase5")
        add_edge(edges, model_node, f"dominant_anchor_class:{dominant}", "model_to_dominant_anchor", "phase5")
        add_edge(edges, model_node, f"variance_class:{variance}", "model_to_variance_class", "phase5")

        anchor_values = row["anchor_values"]
        anchor_layers = row["anchor_layers"]
        previous_anchor_node = ""
        for anchor in ANCHORS:
            anchor_node = f"anchor:{model}:{anchor}"
            layer_node = f"layer:{model}:{anchor_layers[anchor]}"
            add_edge(
                edges,
                model_node,
                anchor_node,
                "model_to_anchor_window",
                "phase5_anchor_values",
                float(anchor_values[anchor]),
            )
            add_edge(edges, anchor_node, layer_node, "anchor_to_measured_layer", "phase5_anchor_layers")
            add_edge(edges, layer_node, model_node, "layer_to_model", "phase5_anchor_layers")
            if previous_anchor_node:
                add_edge(edges, previous_anchor_node, anchor_node, "anchor_order_sequence", "phase5_anchor_order")
            previous_anchor_node = anchor_node

        top3 = [str(anchor).replace("target", "target").replace("last", "last") for anchor in row["top3_sequence"]]
        for rank, anchor in enumerate(top3, start=1):
            add_edge(
                edges,
                model_node,
                f"anchor:{model}:{anchor}",
                f"top3_anchor_rank_{rank}",
                "phase5_top3_sequence",
                1.0 / rank,
            )
        add_edge(edges, f"anchor:{model}:target", f"anchor:{model}:last", "target_to_readout", "phase5_bridge")
        add_edge(edges, f"anchor:{model}:{dominant_anchor}", model_node, "dominant_anchor_to_model", "phase5")

    return dedupe_edges(edges), by_model


def dedupe_edges(edges: list[dict[str, object]]) -> list[dict[str, object]]:
    deduped: dict[tuple[str, str, str], dict[str, object]] = {}
    for edge in edges:
        source = str(edge["source"])
        target = str(edge["target"])
        left, right = sorted((source, target))
        key = (left, right, str(edge["edge_type"]))
        if key not in deduped:
            deduped[key] = edge
        else:
            deduped[key]["edge_weight"] = max(
                float(deduped[key]["edge_weight"]), float(edge["edge_weight"])
            )
    return list(deduped.values())


def quantum_positive_pairs() -> dict[str, set[tuple[str, str]]]:
    phase6 = read_json(PHASE6_JSON)
    phase7 = read_json(PHASE7_JSON)
    return {
        "phase6_amplitude_top3": {
            norm_pair(*item["pair"]) for item in phase6["amplitude_nearest_pairs"][:3]
        },
        "phase7_amplitude_top3": {
            norm_pair(*item["pair"]) for item in phase7["qiskit_amplitude_nearest_pairs"][:3]
        },
    }


def all_model_pairs(models: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for index, source in enumerate(models):
        for target in models[index + 1 :]:
            pairs.append((source, target))
    return pairs


def node_for_role(model: str, row: dict, role: str) -> str:
    if role == "model":
        return f"model:{model}"
    if role in ANCHORS:
        return f"anchor:{model}:{role}"
    if role == "dominant_anchor":
        anchor = anchor_key(row["dominant_anchor"])
        return f"anchor:{model}:{anchor}"
    if role == "target_layer":
        return f"layer:{model}:{row['target_layer']}"
    if role == "last_layer":
        return f"layer:{model}:{row['last_layer']}"
    raise ValueError(f"unknown label role: {role}")


def build_label_rows(
    by_model: dict[str, dict],
    positive_pairs: set[tuple[str, str]],
) -> list[dict[str, object]]:
    roles = [
        "model",
        "early",
        "mid",
        "pre",
        "target",
        "post",
        "last",
        "dominant_anchor",
        "target_layer",
        "last_layer",
    ]
    rows: list[dict[str, object]] = []
    for source_model, target_model in all_model_pairs(sorted(by_model)):
        model_pair = norm_pair(source_model, target_model)
        label = int(model_pair in positive_pairs)
        for role in roles:
            rows.append(
                {
                    "source": node_for_role(source_model, by_model[source_model], role),
                    "target": node_for_role(target_model, by_model[target_model], role),
                    "label": label,
                    "role": role,
                    "model_pair": "|".join(model_pair),
                    "label_source": PRIMARY_MODE,
                    "label_method": "Phase 6 amplitude top-3 nearest-pair preservation",
                    "evidence_uri": str(PHASE6_JSON.relative_to(REPO_ROOT)),
                }
            )
    return rows


def adjacency_from_edges(edges: list[dict[str, object]]) -> tuple[dict[str, set[str]], dict[str, int]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        source = str(edge["source"])
        target = str(edge["target"])
        adjacency[source].add(target)
        adjacency[target].add(source)
    degrees = {node: len(neighbors) for node, neighbors in adjacency.items()}
    return adjacency, degrees


def shortest_path_length(adjacency: dict[str, set[str]], source: str, target: str) -> int | None:
    if source == target:
        return 0
    seen = {source}
    queue: deque[tuple[str, int]] = deque([(source, 0)])
    while queue:
        node, distance = queue.popleft()
        for neighbor in adjacency.get(node, set()):
            if neighbor == target:
                return distance + 1
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, distance + 1))
    return None


def auc(scores: list[float], labels: list[int]) -> float:
    positives = [score for score, label in zip(scores, labels) if label == 1]
    negatives = [score for score, label in zip(scores, labels) if label == 0]
    if not positives or not negatives:
        return 0.0
    wins = 0.0
    total = len(positives) * len(negatives)
    for pos in positives:
        for neg in negatives:
            if pos > neg:
                wins += 1.0
            elif pos == neg:
                wins += 0.5
    return wins / total


def greater_equal_p_value(real: float, null_values: list[float]) -> float:
    return (sum(1 for value in null_values if value >= real) + 1) / (len(null_values) + 1)


def score_rows(
    edges: list[dict[str, object]],
    labels: list[dict[str, object]],
) -> list[dict[str, object]]:
    adjacency, degrees = adjacency_from_edges(edges)
    max_degree = max(degrees.values()) if degrees else 1
    rows: list[dict[str, object]] = []
    for row in labels:
        source = str(row["source"])
        target = str(row["target"])
        path_length = shortest_path_length(adjacency, source, target)
        mirror_score = 0.0 if path_length is None else 1.0 / (1.0 + path_length)
        degree_score = (degrees.get(source, 0) + degrees.get(target, 0)) / (2.0 * max_degree)
        rows.append(
            {
                **row,
                "path_length": path_length if path_length is not None else "",
                "mirror_path_score": round(mirror_score, 6),
                "degree_baseline_score": round(degree_score, 6),
            }
        )
    return rows


def metric_block(scores: list[float], degree_scores: list[float], labels: list[int], permutations: int) -> dict:
    mirror_auc = auc(scores, labels)
    degree_auc = auc(degree_scores, labels)
    rng = random.Random(67)
    mirror_null: list[float] = []
    degree_null: list[float] = []
    for _ in range(permutations):
        shuffled = labels[:]
        rng.shuffle(shuffled)
        mirror_null.append(auc(scores, shuffled))
        degree_null.append(auc(degree_scores, shuffled))
    return {
        "mirror_path_auc": round(mirror_auc, 6),
        "degree_baseline_auc": round(degree_auc, 6),
        "mirror_minus_degree_auc": round(mirror_auc - degree_auc, 6),
        "mirror_path_auc_label_shuffle_p": round(greater_equal_p_value(mirror_auc, mirror_null), 6),
        "degree_baseline_auc_label_shuffle_p": round(greater_equal_p_value(degree_auc, degree_null), 6),
    }


def clustered_rows(scored_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in scored_rows:
        grouped[str(row["model_pair"])].append(row)
    clusters: list[dict[str, object]] = []
    for model_pair, rows in sorted(grouped.items()):
        label_values = {int(row["label"]) for row in rows}
        label = label_values.pop() if len(label_values) == 1 else 0
        clusters.append(
            {
                "model_pair": model_pair,
                "label": label,
                "role_count": len(rows),
                "mirror_path_score": round(
                    sum(float(row["mirror_path_score"]) for row in rows) / len(rows), 6
                ),
                "degree_baseline_score": round(
                    sum(float(row["degree_baseline_score"]) for row in rows) / len(rows), 6
                ),
            }
        )
    return clusters


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def status_for(row_metrics: dict, cluster_metrics: dict) -> str:
    row_hit = (
        row_metrics["mirror_path_auc"] > row_metrics["degree_baseline_auc"]
        and row_metrics["mirror_path_auc_label_shuffle_p"] <= 0.05
    )
    cluster_hit = (
        cluster_metrics["mirror_path_auc"] > cluster_metrics["degree_baseline_auc"]
        and cluster_metrics["mirror_path_auc_label_shuffle_p"] <= 0.05
    )
    if row_hit and cluster_hit:
        return "completed_control_supported_internal_graph2a"
    if row_hit or cluster_hit or row_metrics["mirror_path_auc"] > row_metrics["degree_baseline_auc"]:
        return "completed_soft_positive_internal_graph2a"
    return "completed_no_control_support"


def write_report(out_dir: Path, report: dict) -> None:
    (out_dir / "graph2a_dense_internal_pathway_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GRAPH-2A Dense Internal Pathway Report",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Graph",
        "",
        f"- `node_count`: `{report['graph']['node_count']}`",
        f"- `edge_count`: `{report['graph']['edge_count']}`",
        f"- `label_rows`: `{report['graph']['label_rows']}`",
        f"- `positive_label_rows`: `{report['graph']['positive_label_rows']}`",
        f"- `positive_model_pairs`: `{report['graph']['positive_model_pairs']}`",
        "",
        "## Row-Level Metrics",
        "",
    ]
    for key, value in report["row_level_metrics"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Cluster-Level Metrics", ""])
    for key, value in report["cluster_level_metrics"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            report["boundary"],
            "",
            "## Next Step",
            "",
            report["next_step"],
            "",
        ]
    )
    (out_dir / "graph2a_dense_internal_pathway_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    out_dir = DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    phase5 = read_json(PHASE5_JSON)
    edges, by_model = build_dense_edges(phase5)
    positive_pairs = quantum_positive_pairs()[PRIMARY_MODE]
    labels = build_label_rows(by_model, positive_pairs)
    scored = score_rows(edges, labels)
    clusters = clustered_rows(scored)
    row_metrics = metric_block(
        [float(row["mirror_path_score"]) for row in scored],
        [float(row["degree_baseline_score"]) for row in scored],
        [int(row["label"]) for row in scored],
        permutations=10000,
    )
    cluster_metrics = metric_block(
        [float(row["mirror_path_score"]) for row in clusters],
        [float(row["degree_baseline_score"]) for row in clusters],
        [int(row["label"]) for row in clusters],
        permutations=10000,
    )
    status = status_for(row_metrics, cluster_metrics)
    if status == "completed_control_supported_internal_graph2a":
        read = (
            "GRAPH-2A dense internal pathway graph closed against row-level and "
            "model-pair-cluster shuffled controls."
        )
    elif status == "completed_soft_positive_internal_graph2a":
        read = (
            "GRAPH-2A dense internal pathway graph produced a directional / partial "
            "signal, but did not close both row-level and cluster-level controls."
        )
    else:
        read = "GRAPH-2A ran on real dense internal graph inputs but did not beat controls."
    write_csv(out_dir / "graph2a_dense_internal_edges.csv", edges)
    write_csv(out_dir / "graph2a_dense_internal_labels.csv", labels)
    write_csv(out_dir / "graph2a_dense_internal_scored_pairs.csv", scored)
    write_csv(out_dir / "graph2a_dense_internal_clustered_pairs.csv", clusters)
    node_count = len({edge["source"] for edge in edges} | {edge["target"] for edge in edges})
    report = {
        "status": status,
        "read": read,
        "primary_label_mode": PRIMARY_MODE,
        "source_artifacts": {
            "graph_source": str(PHASE5_JSON.relative_to(REPO_ROOT)),
            "label_source": str(PHASE6_JSON.relative_to(REPO_ROOT)),
            "secondary_crosscheck_label_source": str(PHASE7_JSON.relative_to(REPO_ROOT)),
        },
        "graph": {
            "node_count": node_count,
            "edge_count": len(edges),
            "label_rows": len(labels),
            "positive_label_rows": sum(int(row["label"]) for row in labels),
            "control_label_rows": len(labels) - sum(int(row["label"]) for row in labels),
            "positive_model_pairs": sorted("|".join(pair) for pair in positive_pairs),
            "cluster_rows": len(clusters),
        },
        "row_level_metrics": row_metrics,
        "cluster_level_metrics": cluster_metrics,
        "boundary": (
            "This is an internal GRAPH-2A pathway validation over Phase 4/5 graph structure "
            "and Phase 6 quantum labels. It does not validate external allostery, chemistry, "
            "grid flow, logistics, molecular pathways, or universal graph structure."
        ),
        "next_step": (
            "If supported, rerun with Phase 7 labels and leave-one-model-family controls. "
            "If soft or unsupported, build a still denser token/layer graph from raw V8 "
            "point-cloud exports before moving to external domain graphs."
        ),
    }
    write_report(out_dir, report)
    print(f"Wrote GRAPH-2A dense internal pathway report to {out_dir}")


if __name__ == "__main__":
    main()
