#!/usr/bin/env python3
"""GRAPH-2B raw token/layer pathway graph.

This runner avoids toy data. It builds a hub-reduced graph from real V8
point-cloud exports, then tests whether independently sourced Phase 6
quantum-encoding pairs are recoverable above degree and shuffled-label
controls.

The runner publishes derived graph rows only; it never writes raw hidden
vectors into the validation artifact.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
import random
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POINT_CLOUD_DIR = (
    REPO_ROOT / "artifacts" / "v8" / "residual_stream_bridge" / "point_clouds_expanded"
)
PHASE6_JSON = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase6_pennylane_encoding"
    / "v8_phase6_pennylane_encoding_data_2026-04-22.json"
)
DEFAULT_OUT_DIR = (
    REPO_ROOT / "artifacts" / "validation" / "graph2b_raw_token_layer_pathway"
)

PRIMARY_MODE = "phase6_amplitude_top3"
CONTEXTS = {"lattice", "neutral", "technical"}
TOKEN_OFFSET_LIMIT = 8
CROSS_K = 2
CROSS_DEGREE_CAP = 4
MAX_BFS_DEPTH = 8
SEED = 67


def normalized_signature_parts(
    token_role: str,
    token_region: str,
    token_offset: int,
) -> tuple[str, str, int]:
    if token_role == "last_token":
        return ("target_window_token", "post_anchor", TOKEN_OFFSET_LIMIT)
    return (token_role, token_region, token_offset)


@dataclass(frozen=True)
class Node:
    node_id: str
    model: str
    context: str
    layer_index: int
    layer_depth: str
    depth_slot: int
    token_role: str
    token_region: str
    token_offset: int
    feature_family: str
    feature_vector: tuple[float, ...]

    @property
    def score_signature(self) -> tuple[str, str, int, str, str, int]:
        token_role, token_region, token_offset = normalized_signature_parts(
            self.token_role, self.token_region, self.token_offset
        )
        return (
            self.context,
            self.layer_depth,
            self.depth_slot,
            token_region,
            token_role,
            token_offset,
        )

    @property
    def cross_signature(self) -> tuple[str, str, int, str, str, int]:
        return self.score_signature


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def norm_pair(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def zscore(values: np.ndarray) -> np.ndarray:
    mean = float(np.nanmean(values))
    std = float(np.nanstd(values))
    if not math.isfinite(std) or std == 0.0:
        std = 1.0
    return (values - mean) / std


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(numeric):
        return default
    return numeric


def depth_slot(layer_index: int, layer_depth: str, depth_layers: dict[str, list[int]]) -> int:
    layers = sorted(set(depth_layers.get(layer_depth, [])))
    if not layers:
        return 0
    rank = layers.index(layer_index) if layer_index in layers else 0
    if len(layers) <= 1:
        return 0
    return min(3, int(4 * rank / len(layers)))


def include_row(feature_family: str, token_role: str, token_offset: int, context: str) -> bool:
    if context not in CONTEXTS:
        return False
    if feature_family == "token_window" and token_role == "target_window_token":
        return abs(token_offset) <= TOKEN_OFFSET_LIMIT
    if feature_family == "compact" and token_role in {"last_token", "target_span_mean"}:
        return True
    return False


def derive_layer_depths(layer_indices: np.ndarray) -> np.ndarray:
    max_layer = int(np.max(layer_indices)) if len(layer_indices) else 0
    if max_layer <= 0:
        return np.array(["early"] * len(layer_indices))
    depths: list[str] = []
    for layer in layer_indices:
        ratio = float(layer) / float(max_layer)
        if ratio < 1.0 / 3.0:
            depths.append("early")
        elif ratio < 2.0 / 3.0:
            depths.append("middle")
        else:
            depths.append("late")
    return np.array(depths)


def derive_token_regions(feature_families: np.ndarray, token_offsets: np.ndarray) -> np.ndarray:
    regions: list[str] = []
    for family, offset in zip(feature_families.astype(str), token_offsets.astype(int)):
        if family == "compact":
            regions.append("summary")
        elif offset < 0:
            regions.append("pre_anchor")
        elif offset == 0:
            regions.append("anchor_phrase")
        else:
            regions.append("post_anchor")
    return np.array(regions)


def model_name_from_metadata(npz_path: Path) -> str:
    meta_path = npz_path.with_suffix(".metadata.json")
    if meta_path.exists():
        data = read_json(meta_path)
        return str(data.get("display_name") or npz_path.name.split("_")[0]).strip()
    return npz_path.name.split("_")[0].title()


def row_key(
    model: str,
    context: str,
    token_role: str,
    token_offset: int,
    layer_index: int,
) -> tuple[str, str, str, int, int]:
    return (model, context, token_role, token_offset, layer_index)


def load_model_nodes(npz_path: Path) -> tuple[list[Node], list[tuple[str, str, str]]]:
    model = model_name_from_metadata(npz_path)
    with np.load(npz_path, allow_pickle=False) as payload:
        points = np.asarray(payload["points"], dtype=np.float32)
        context = np.asarray(payload["context_label"]).astype(str)
        layer_index = np.asarray(payload["layer_index"]).astype(int)
        token_role = np.asarray(payload["token_role"]).astype(str)
        token_offset = np.asarray(payload["token_offset"]).astype(int)
        feature_family = np.asarray(payload["feature_family"]).astype(str)
        if "layer_depth" in payload.files:
            layer_depth = np.asarray(payload["layer_depth"]).astype(str)
        else:
            layer_depth = derive_layer_depths(layer_index).astype(str)
        if "token_region" in payload.files:
            token_region = np.asarray(payload["token_region"]).astype(str)
        else:
            token_region = derive_token_regions(feature_family, token_offset).astype(str)
        activation = np.asarray(payload["behavioral_activation"], dtype=np.float32)
        cohesion = np.asarray(payload["behavioral_input_cohesion"], dtype=np.float32)
        coherence = np.asarray(payload["behavioral_coherence_10"], dtype=np.float32)
        marker = np.asarray(payload["behavioral_marker_score"], dtype=np.float32)

        finite = np.isfinite(points).all(axis=1)
        norms = np.linalg.norm(points, axis=1)
        means = points.mean(axis=1)
        stds = points.std(axis=1)

        selected = [
            index
            for index in range(len(points))
            if finite[index]
            and include_row(
                str(feature_family[index]),
                str(token_role[index]),
                int(token_offset[index]),
                str(context[index]),
            )
        ]
        if not selected:
            return [], []

        selected_array = np.array(selected, dtype=np.int64)
        norm_z = zscore(norms[selected_array])
        mean_z = zscore(means[selected_array])
        std_z = zscore(stds[selected_array])

        raw_by_key: dict[tuple[str, str, str, int, int], int] = {}
        for index in selected:
            raw_by_key[
                row_key(
                    model,
                    str(context[index]),
                    str(token_role[index]),
                    int(token_offset[index]),
                    int(layer_index[index]),
                )
            ] = index

        layer_delta = np.zeros(len(selected), dtype=np.float64)
        token_delta = np.zeros(len(selected), dtype=np.float64)
        selected_position = {raw_index: pos for pos, raw_index in enumerate(selected)}

        for raw_index in selected:
            current_key = row_key(
                model,
                str(context[raw_index]),
                str(token_role[raw_index]),
                int(token_offset[raw_index]),
                int(layer_index[raw_index]),
            )
            prev_key = (*current_key[:4], current_key[4] - 1)
            next_key = (*current_key[:4], current_key[4] + 1)
            candidates = [raw_by_key[key] for key in (prev_key, next_key) if key in raw_by_key]
            if candidates:
                distances = [
                    float(np.linalg.norm(points[raw_index] - points[candidate]))
                    for candidate in candidates
                ]
                layer_delta[selected_position[raw_index]] = min(distances)

        by_token_group: dict[tuple[str, str, int], list[int]] = defaultdict(list)
        for raw_index in selected:
            if str(feature_family[raw_index]) == "token_window":
                by_token_group[
                    (str(context[raw_index]), str(layer_index[raw_index]), int(layer_index[raw_index]))
                ].append(raw_index)
        for group_indices in by_token_group.values():
            sorted_group = sorted(group_indices, key=lambda idx: int(token_offset[idx]))
            for left, right in zip(sorted_group, sorted_group[1:]):
                if abs(int(token_offset[right]) - int(token_offset[left])) == 1:
                    distance = float(np.linalg.norm(points[left] - points[right]))
                    token_delta[selected_position[left]] = max(token_delta[selected_position[left]], distance)
                    token_delta[selected_position[right]] = max(token_delta[selected_position[right]], distance)

        layer_delta_z = zscore(layer_delta)
        token_delta_z = zscore(token_delta)
        depth_layers: dict[str, list[int]] = defaultdict(list)
        for raw_index in selected:
            depth_layers[str(layer_depth[raw_index])].append(int(layer_index[raw_index]))

        nodes: list[Node] = []
        node_ids_by_raw: dict[int, str] = {}
        for pos, raw_index in enumerate(selected):
            node_id = f"{model}|{len(nodes)}"
            node_ids_by_raw[raw_index] = node_id
            feature_vector = (
                round(float(norm_z[pos]), 6),
                round(float(mean_z[pos]), 6),
                round(float(std_z[pos]), 6),
                round(float(layer_delta_z[pos]), 6),
                round(float(token_delta_z[pos]), 6),
                round(float(activation[raw_index]), 6),
                round(float(cohesion[raw_index]), 6),
                round(float(coherence[raw_index]) / 10.0, 6),
                round(float(marker[raw_index]), 6),
            )
            nodes.append(
                Node(
                    node_id=node_id,
                    model=model,
                    context=str(context[raw_index]),
                    layer_index=int(layer_index[raw_index]),
                    layer_depth=str(layer_depth[raw_index]),
                    depth_slot=depth_slot(int(layer_index[raw_index]), str(layer_depth[raw_index]), depth_layers),
                    token_role=str(token_role[raw_index]),
                    token_region=str(token_region[raw_index]),
                    token_offset=int(token_offset[raw_index]),
                    feature_family=str(feature_family[raw_index]),
                    feature_vector=feature_vector,
                )
            )

        local_edges: list[tuple[str, str, str]] = []
        by_layer_transition: dict[tuple[str, str, str, int], list[Node]] = defaultdict(list)
        by_token_transition: dict[tuple[str, str, int], list[Node]] = defaultdict(list)
        for node in nodes:
            by_layer_transition[
                (node.model, node.context, node.token_role, node.token_offset)
            ].append(node)
            if node.feature_family == "token_window":
                by_token_transition[(node.model, node.context, node.layer_index)].append(node)

        for group in by_layer_transition.values():
            ordered = sorted(group, key=lambda node: node.layer_index)
            for left, right in zip(ordered, ordered[1:]):
                if right.layer_index - left.layer_index == 1:
                    local_edges.append((left.node_id, right.node_id, "layer_transition"))

        for group in by_token_transition.values():
            ordered = sorted(group, key=lambda node: node.token_offset)
            for left, right in zip(ordered, ordered[1:]):
                if right.token_offset - left.token_offset == 1:
                    local_edges.append((left.node_id, right.node_id, "token_transition"))

        return nodes, local_edges


def feature_distance(left: Node, right: Node) -> float:
    return math.sqrt(
        sum((left_value - right_value) ** 2 for left_value, right_value in zip(left.feature_vector, right.feature_vector))
    )


def build_cross_edges(nodes: list[Node]) -> list[tuple[str, str, str]]:
    grouped: dict[tuple[str, str, int, str, str, int], list[Node]] = defaultdict(list)
    for node in nodes:
        grouped[node.cross_signature].append(node)

    cross_degree: dict[str, int] = defaultdict(int)
    edges: set[tuple[str, str, str]] = set()
    for group in grouped.values():
        by_model: dict[str, list[Node]] = defaultdict(list)
        for node in group:
            by_model[node.model].append(node)
        if len(by_model) < 2:
            continue
        for source in group:
            candidates = [node for node in group if node.model != source.model]
            ranked = sorted(candidates, key=lambda node: feature_distance(source, node))
            added = 0
            for target in ranked:
                if added >= CROSS_K:
                    break
                if cross_degree[source.node_id] >= CROSS_DEGREE_CAP:
                    break
                if cross_degree[target.node_id] >= CROSS_DEGREE_CAP:
                    continue
                left, right = sorted((source.node_id, target.node_id))
                edge = (left, right, "capped_cross_model_nearest")
                if edge in edges:
                    continue
                edges.add(edge)
                cross_degree[source.node_id] += 1
                cross_degree[target.node_id] += 1
                added += 1
    return sorted(edges)


def build_graph(
    nodes: list[Node],
    local_edges: list[tuple[str, str, str]],
    shuffle_mode: str = "none",
) -> tuple[list[dict[str, Any]], dict[str, set[str]], dict[str, int]]:
    rng = random.Random(SEED)
    adjusted_edges = list(local_edges)
    if shuffle_mode in {"layer_order", "token_window"}:
        by_type = defaultdict(list)
        passthrough = []
        for edge in local_edges:
            if shuffle_mode == "layer_order" and edge[2] == "layer_transition":
                by_type[edge[2]].append(edge)
            elif shuffle_mode == "token_window" and edge[2] == "token_transition":
                by_type[edge[2]].append(edge)
            else:
                passthrough.append(edge)
        adjusted_edges = passthrough
        for edge_type, edges in by_type.items():
            sources = [edge[0] for edge in edges]
            targets = [edge[1] for edge in edges]
            rng.shuffle(targets)
            adjusted_edges.extend((source, target, f"{edge_type}_{shuffle_mode}_control") for source, target in zip(sources, targets))

    all_edges = adjusted_edges + build_cross_edges(nodes)
    edge_rows: list[dict[str, Any]] = []
    adjacency: dict[str, set[str]] = defaultdict(set)
    for source, target, edge_type in all_edges:
        if source == target:
            continue
        left, right = sorted((source, target))
        adjacency[left].add(right)
        adjacency[right].add(left)
        edge_rows.append({"source": left, "target": right, "edge_type": edge_type})
    degrees = {node_id: len(neighbors) for node_id, neighbors in adjacency.items()}
    return edge_rows, adjacency, degrees


def bounded_shortest_path(
    adjacency: dict[str, set[str]],
    sources: set[str],
    targets: set[str],
    max_depth: int = MAX_BFS_DEPTH,
) -> int | None:
    if sources & targets:
        return 0
    left_seen = set(sources)
    right_seen = set(targets)
    left_frontier = set(sources)
    right_frontier = set(targets)
    left_depth = 0
    right_depth = 0

    while left_frontier and right_frontier and left_depth + right_depth < max_depth:
        if len(left_frontier) <= len(right_frontier):
            next_frontier: set[str] = set()
            for node in left_frontier:
                for neighbor in adjacency.get(node, set()):
                    if neighbor in right_seen:
                        return left_depth + right_depth + 1
                    if neighbor not in left_seen:
                        left_seen.add(neighbor)
                        next_frontier.add(neighbor)
            left_frontier = next_frontier
            left_depth += 1
        else:
            next_frontier = set()
            for node in right_frontier:
                for neighbor in adjacency.get(node, set()):
                    if neighbor in left_seen:
                        return left_depth + right_depth + 1
                    if neighbor not in right_seen:
                        right_seen.add(neighbor)
                        next_frontier.add(neighbor)
            right_frontier = next_frontier
            right_depth += 1
    return None


def positive_pairs() -> set[tuple[str, str]]:
    data = read_json(PHASE6_JSON)
    return {norm_pair(*item["pair"]) for item in data["amplitude_nearest_pairs"][:3]}


def auc(scores: list[float], labels: list[int]) -> float:
    positives = [score for score, label in zip(scores, labels) if label == 1]
    negatives = [score for score, label in zip(scores, labels) if label == 0]
    if not positives or not negatives:
        return 0.0
    wins = 0.0
    total = len(positives) * len(negatives)
    for positive in positives:
        for negative in negatives:
            if positive > negative:
                wins += 1.0
            elif positive == negative:
                wins += 0.5
    return wins / total


def exact_cluster_p_value(
    model_pairs: list[str],
    scores: list[float],
    labels: list[int],
    observed_auc: float,
) -> float:
    positive_count = sum(labels)
    if positive_count <= 0 or positive_count >= len(labels):
        return 1.0
    total = 0
    ge = 0
    for positive_indices in itertools.combinations(range(len(model_pairs)), positive_count):
        shuffled = [0] * len(labels)
        for index in positive_indices:
            shuffled[index] = 1
        total += 1
        if auc(scores, shuffled) >= observed_auc:
            ge += 1
    return ge / total if total else 1.0


def average_ranks(scores: list[float]) -> list[float]:
    indexed = sorted(enumerate(scores), key=lambda item: item[1])
    ranks = [0.0] * len(scores)
    index = 0
    while index < len(indexed):
        next_index = index + 1
        while next_index < len(indexed) and indexed[next_index][1] == indexed[index][1]:
            next_index += 1
        average_rank = (index + 1 + next_index) / 2.0
        for position in range(index, next_index):
            ranks[indexed[position][0]] = average_rank
        index = next_index
    return ranks


def cluster_label_shuffle_p(scored_rows: list[dict[str, Any]], cluster_rows: list[dict[str, Any]], observed_auc: float) -> float:
    model_pairs = [str(row["model_pair"]) for row in cluster_rows]
    cluster_labels = [int(row["label"]) for row in cluster_rows]
    positive_count = sum(cluster_labels)
    if positive_count <= 0 or positive_count >= len(cluster_labels):
        return 1.0
    row_scores = [float(row["mirror_path_score"]) for row in scored_rows]
    row_ranks = average_ranks(row_scores)
    total_rows = len(scored_rows)
    pair_counts: dict[str, int] = defaultdict(int)
    pair_rank_sums: dict[str, float] = defaultdict(float)
    for row, rank in zip(scored_rows, row_ranks):
        pair = str(row["model_pair"])
        pair_counts[pair] += 1
        pair_rank_sums[pair] += rank
    total = 0
    ge = 0
    for positive_indices in itertools.combinations(range(len(model_pairs)), positive_count):
        positive_pairs_set = [model_pairs[index] for index in positive_indices]
        positive_rows = sum(pair_counts[pair] for pair in positive_pairs_set)
        negative_rows = total_rows - positive_rows
        if positive_rows <= 0 or negative_rows <= 0:
            continue
        positive_rank_sum = sum(pair_rank_sums[pair] for pair in positive_pairs_set)
        shuffled_auc = (
            positive_rank_sum - (positive_rows * (positive_rows + 1) / 2.0)
        ) / (positive_rows * negative_rows)
        total += 1
        if shuffled_auc >= observed_auc:
            ge += 1
    return ge / total if total else 1.0


def metric_block(scored_rows: list[dict[str, Any]], clustered: bool) -> dict[str, Any]:
    labels = [int(row["label"]) for row in scored_rows]
    mirror_scores = [float(row["mirror_path_score"]) for row in scored_rows]
    degree_scores = [float(row["degree_baseline_score"]) for row in scored_rows]
    mirror_auc = auc(mirror_scores, labels)
    degree_auc = auc(degree_scores, labels)
    metrics = {
        "mirror_path_auc": round(mirror_auc, 6),
        "degree_baseline_auc": round(degree_auc, 6),
        "mirror_minus_degree_auc": round(mirror_auc - degree_auc, 6),
    }
    if clustered:
        model_pairs = [str(row["model_pair"]) for row in scored_rows]
        metrics["mirror_path_auc_exact_label_shuffle_p"] = round(
            exact_cluster_p_value(model_pairs, mirror_scores, labels, mirror_auc), 6
        )
        metrics["degree_baseline_auc_exact_label_shuffle_p"] = round(
            exact_cluster_p_value(model_pairs, degree_scores, labels, degree_auc), 6
        )
    return metrics


def score_rows(
    nodes: list[Node],
    adjacency: dict[str, set[str]],
    degrees: dict[str, int],
    labels: set[tuple[str, str]],
) -> list[dict[str, Any]]:
    by_model_signature: dict[tuple[str, tuple[str, str, int, str, str, int]], set[str]] = defaultdict(set)
    node_by_id = {node.node_id: node for node in nodes}
    for node in nodes:
        by_model_signature[(node.model, node.score_signature)].add(node.node_id)

    models = sorted({node.model for node in nodes})
    signatures = sorted({node.score_signature for node in nodes})
    max_degree = max(degrees.values()) if degrees else 1
    rows: list[dict[str, Any]] = []
    for left_index, left_model in enumerate(models):
        for right_model in models[left_index + 1 :]:
            pair = norm_pair(left_model, right_model)
            pair_label = int(pair in labels)
            pair_name = "|".join(pair)
            for signature in signatures:
                left_nodes = by_model_signature.get((left_model, signature), set())
                right_nodes = by_model_signature.get((right_model, signature), set())
                if not left_nodes or not right_nodes:
                    continue
                path_length = bounded_shortest_path(adjacency, left_nodes, right_nodes)
                mirror_score = 0.0 if path_length is None else 1.0 / (1.0 + path_length)
                left_degree = sum(degrees.get(node_id, 0) for node_id in left_nodes) / len(left_nodes)
                right_degree = sum(degrees.get(node_id, 0) for node_id in right_nodes) / len(right_nodes)
                degree_score = (left_degree + right_degree) / (2.0 * max_degree)
                context, layer_depth, slot, token_region, token_role, token_offset = signature
                rows.append(
                    {
                        "model_pair": pair_name,
                        "source_model": left_model,
                        "target_model": right_model,
                        "context": context,
                        "layer_depth": layer_depth,
                        "depth_slot": slot,
                        "token_region": token_region,
                        "token_role": token_role,
                        "token_offset": token_offset,
                        "label": pair_label,
                        "left_node_count": len(left_nodes),
                        "right_node_count": len(right_nodes),
                        "path_length": "" if path_length is None else path_length,
                        "mirror_path_score": round(mirror_score, 6),
                        "degree_baseline_score": round(degree_score, 6),
                    }
                )
    return rows


def cluster_rows(scored_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored_rows:
        grouped[str(row["model_pair"])].append(row)
    clusters: list[dict[str, Any]] = []
    for pair, rows in sorted(grouped.items()):
        label_values = {int(row["label"]) for row in rows}
        label = label_values.pop() if len(label_values) == 1 else 0
        clusters.append(
            {
                "model_pair": pair,
                "label": label,
                "signature_count": len(rows),
                "mirror_path_score": round(
                    sum(float(row["mirror_path_score"]) for row in rows) / len(rows), 6
                ),
                "degree_baseline_score": round(
                    sum(float(row["degree_baseline_score"]) for row in rows) / len(rows), 6
                ),
            }
        )
    return clusters


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(out_dir: Path, report: dict[str, Any]) -> None:
    (out_dir / "graph2b_raw_token_layer_pathway_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GRAPH-2B Raw Token / Layer Pathway Report",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Inputs",
        "",
        f"- Point-cloud source: `{report['inputs']['point_cloud_source']}`",
        f"- Label source: `{report['inputs']['label_source']}`",
        f"- Primary label mode: `{report['inputs']['primary_label_mode']}`",
        f"- Positive pairs: `{', '.join(report['inputs']['positive_pairs'])}`",
        "",
        "## Graph",
        "",
    ]
    for key, value in report["graph"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Cluster Metrics", ""])
    for key, value in report["cluster_metrics"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Row Metrics", ""])
    for key, value in report["row_metrics"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Perturbation Controls", ""])
    for name, metrics in report["perturbation_controls"].items():
        lines.append(f"### {name}")
        lines.append("")
        for key, value in metrics.items():
            lines.append(f"- `{key}`: `{value}`")
        lines.append("")
    lines.extend(
        [
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
    (out_dir / "graph2b_raw_token_layer_pathway_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def status_for(cluster_metrics: dict[str, Any], row_metrics: dict[str, Any]) -> str:
    cluster_hit = (
        cluster_metrics["mirror_path_auc"] > cluster_metrics["degree_baseline_auc"]
        and cluster_metrics["mirror_path_auc_exact_label_shuffle_p"] <= 0.05
    )
    row_hit = (
        row_metrics["mirror_path_auc"] > row_metrics["degree_baseline_auc"]
        and row_metrics["mirror_path_auc_pair_label_shuffle_p"] <= 0.05
    )
    if cluster_hit:
        return "completed_control_supported_internal_graph2b"
    if row_hit or cluster_metrics["mirror_path_auc"] > cluster_metrics["degree_baseline_auc"]:
        return "completed_soft_positive_internal_graph2b"
    return "completed_no_control_support_internal_graph2b"


def run_variant(nodes: list[Node], local_edges: list[tuple[str, str, str]], labels: set[tuple[str, str]], mode: str) -> tuple[dict[str, Any], dict[str, Any]]:
    _edge_rows, adjacency, degrees = build_graph(nodes, local_edges, shuffle_mode=mode)
    scored = score_rows(nodes, adjacency, degrees, labels)
    clusters = cluster_rows(scored)
    row_metrics = metric_block(scored, clustered=False)
    cluster_metrics = metric_block(clusters, clustered=True)
    row_metrics["mirror_path_auc_pair_label_shuffle_p"] = round(
        cluster_label_shuffle_p(scored, clusters, row_metrics["mirror_path_auc"]), 6
    )
    return row_metrics, cluster_metrics


def main() -> None:
    out_dir = DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    npz_files = sorted(DEFAULT_POINT_CLOUD_DIR.glob("*_v8_hidden_point_cloud.npz"))
    if not npz_files:
        raise SystemExit(f"No point-cloud exports found in {DEFAULT_POINT_CLOUD_DIR}")

    nodes: list[Node] = []
    local_edges: list[tuple[str, str, str]] = []
    for npz_path in npz_files:
        model_nodes, model_edges = load_model_nodes(npz_path)
        nodes.extend(model_nodes)
        local_edges.extend(model_edges)
    labels = positive_pairs()

    edge_rows, adjacency, degrees = build_graph(nodes, local_edges)
    scored = score_rows(nodes, adjacency, degrees, labels)
    clusters = cluster_rows(scored)
    row_metrics = metric_block(scored, clustered=False)
    cluster_metrics = metric_block(clusters, clustered=True)
    row_metrics["mirror_path_auc_pair_label_shuffle_p"] = round(
        cluster_label_shuffle_p(scored, clusters, row_metrics["mirror_path_auc"]), 6
    )

    perturbation_controls: dict[str, Any] = {}
    for mode in ("layer_order", "token_window"):
        variant_row_metrics, variant_cluster_metrics = run_variant(nodes, local_edges, labels, mode)
        perturbation_controls[mode] = {
            "row_mirror_path_auc": variant_row_metrics["mirror_path_auc"],
            "row_degree_baseline_auc": variant_row_metrics["degree_baseline_auc"],
            "row_pair_label_shuffle_p": variant_row_metrics["mirror_path_auc_pair_label_shuffle_p"],
            "cluster_mirror_path_auc": variant_cluster_metrics["mirror_path_auc"],
            "cluster_degree_baseline_auc": variant_cluster_metrics["degree_baseline_auc"],
            "cluster_exact_label_shuffle_p": variant_cluster_metrics["mirror_path_auc_exact_label_shuffle_p"],
        }

    status = status_for(cluster_metrics, row_metrics)
    if status == "completed_control_supported_internal_graph2b":
        read = (
            "GRAPH-2B closed internally at the model-pair cluster level using real "
            "raw token/layer point-cloud graph structure and independent Phase 6 labels."
        )
    elif status == "completed_soft_positive_internal_graph2b":
        read = (
            "GRAPH-2B produced a directional internal signal but did not close the "
            "full cluster-level control rule. The lane remains open for denser labels "
            "or external/domain graph validation."
        )
    else:
        read = (
            "GRAPH-2B ran on real raw token/layer point-cloud inputs but did not beat "
            "the locked controls."
        )

    node_models = sorted({node.model for node in nodes})
    graph = {
        "node_count": len(nodes),
        "edge_count": len(edge_rows),
        "local_edge_count": len(local_edges),
        "cross_edge_count": len(edge_rows) - len(local_edges),
        "model_count": len(node_models),
        "models": ", ".join(node_models),
        "scored_signature_rows": len(scored),
        "cluster_rows": len(clusters),
    }
    report = {
        "status": status,
        "read": read,
        "inputs": {
            "point_cloud_source": str(DEFAULT_POINT_CLOUD_DIR.relative_to(REPO_ROOT)),
            "label_source": str(PHASE6_JSON.relative_to(REPO_ROOT)),
            "primary_label_mode": PRIMARY_MODE,
            "positive_pairs": sorted("|".join(pair) for pair in labels),
        },
        "graph": graph,
        "cluster_metrics": cluster_metrics,
        "row_metrics": row_metrics,
        "perturbation_controls": perturbation_controls,
        "boundary": (
            "This is an internal raw token/layer graph validation over V8 point-cloud "
            "exports and Phase 6 quantum labels. It does not validate external "
            "molecular pathways, allostery, attention-flow, grid-flow, logistics, "
            "chemistry, or universal graph structure."
        ),
        "next_step": (
            "If cluster-level support remains open, the next GRAPH-2 fork should use "
            "a real independent domain graph: attention-flow if exported, then Nest 2 "
            "molecular/allostery labels, then grid/logistics flow labels when those "
            "datasets exist."
        ),
    }
    write_csv(out_dir / "graph2b_raw_token_layer_edges.csv", edge_rows)
    write_csv(out_dir / "graph2b_raw_token_layer_scored_rows.csv", scored)
    write_csv(out_dir / "graph2b_raw_token_layer_clustered_pairs.csv", clusters)
    write_report(out_dir, report)
    print(f"Wrote GRAPH-2B raw token/layer pathway report to {out_dir}")


if __name__ == "__main__":
    main()
