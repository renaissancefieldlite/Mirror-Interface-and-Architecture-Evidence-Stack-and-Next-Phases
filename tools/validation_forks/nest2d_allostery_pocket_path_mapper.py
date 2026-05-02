#!/usr/bin/env python3
"""Nest 2D-2 allostery pocket/path mapper.

This runner upgrades the first Nest 2D graph pass from exact residue top-k
contact scoring into the biological object allostery actually uses:

- chain-resolved active-site sources where the AlloBench labels allow it
- local pocket candidates built from residue-contact neighborhoods
- active-site-to-pocket path/bottleneck scoring
- pocket controls: degree, closeness, active proximity, random pockets, shuffled labels

It keeps the same benchmark surface as the first run: the 100-row AlloBench
tool table, the public AlloBench residue labels, and cached RCSB PDB structures.
"""

from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from nest2d_allostery_graph_mapper import (
    ALLOBENCH_CSV,
    BENCHMARK_CSV,
    OUT_DIR as GRAPH_OUT_DIR,
    PDB_DIR,
    REPO_ROOT,
    aggregate_allobench_labels,
    build_contact_graph,
    clean_pdb_id,
    jaccard,
    match_active_nodes,
    match_allosteric_nodes,
    multi_source_bfs_lengths,
    normalize,
    parse_pdb_residues,
    p_value,
    sample_node_set,
    z_scores,
)


OUT_DIR = REPO_ROOT / "artifacts/validation/nest2d_allostery_pocket_path_mapper"
RANDOM_SEED = 67322
CONTACT_CUTOFF_ANGSTROM = 8.0


def chain_resolved_active_nodes(graph: nx.Graph, active_resnums: set[int]) -> set:
    """Map active-site residue numbers to the best chain instead of all chains.

    AlloBench active-site labels are sequence-number lists, while allosteric
    labels are chain-residue strings. The first graph pass matched active
    numbers across every chain, which made large multimer structures too broad.
    This version selects the chain with the strongest active-label coverage and
    uses that as the source for path scoring.
    """

    if not active_resnums:
        return set()

    by_chain: dict[str, set] = defaultdict(set)
    for node in graph.nodes:
        if node[1] in active_resnums:
            by_chain[node[0]].add(node)
    if not by_chain:
        return set()

    max_count = max(len(nodes) for nodes in by_chain.values())
    candidate_chains = sorted(chain for chain, nodes in by_chain.items() if len(nodes) == max_count)
    selected_chain = candidate_chains[0]
    return by_chain[selected_chain]


def graph_radius_cluster(graph: nx.Graph, center, radius: int = 1) -> set:
    if center not in graph:
        return set()
    cluster = {center}
    frontier = {center}
    for _ in range(radius):
        next_frontier = set()
        for node in frontier:
            next_frontier.update(graph.neighbors(node))
        next_frontier -= cluster
        cluster.update(next_frontier)
        frontier = next_frontier
    return cluster


def cluster_density(graph: nx.Graph, cluster: set) -> float:
    n = len(cluster)
    if n < 2:
        return 0.0
    edge_count = graph.subgraph(cluster).number_of_edges()
    return (2.0 * edge_count) / (n * (n - 1))


def prune_cluster_to_size(graph: nx.Graph, center, cluster: set, size: int, node_scores: dict) -> set:
    if len(cluster) <= size:
        return set(cluster)
    lengths = nx.single_source_shortest_path_length(graph, center, cutoff=2)
    ranked = sorted(
        cluster,
        key=lambda node: (lengths.get(node, 99), -node_scores.get(node, 0.0), str(node)),
    )
    return set(ranked[:size])


def pocket_predictions(
    graph: nx.Graph,
    active_nodes: set,
    truth_nodes: set,
    rng: np.random.Generator,
    random_trials: int,
) -> dict:
    candidate_nodes = [node for node in graph.nodes if node not in active_nodes]
    if not candidate_nodes:
        candidate_nodes = list(graph.nodes)
    top_k = max(1, min(len(candidate_nodes), len(truth_nodes)))

    distances = multi_source_bfs_lengths(graph, active_nodes) if active_nodes else {}
    max_dist = max(distances.values()) if distances else 1
    active_distance = {node: distances.get(node, max_dist + 1) for node in graph.nodes}
    degrees = dict(graph.degree())
    degree_z = z_scores(degrees)
    clustering = nx.clustering(graph)
    closeness = nx.closeness_centrality(graph) if graph.number_of_edges() else {node: 0.0 for node in graph.nodes}

    degree_n = normalize(degrees)
    closeness_n = normalize(closeness)
    proximity = {node: 1.0 / (1.0 + active_distance[node]) for node in graph.nodes}
    proximity_n = normalize(proximity)
    clustering_n = normalize(clustering)

    node_scores = {}
    for node in candidate_nodes:
        dist = active_distance[node]
        path_band = math.exp(-((dist - 4.0) ** 2) / (2.0 * 2.0**2))
        bridge_band = math.exp(-(degree_z.get(node, 0.0) ** 2) / (2.0 * 1.10**2))
        source_separation = 1.0 if dist >= 2 else 0.35
        node_scores[node] = (
            0.38 * path_band
            + 0.20 * bridge_band
            + 0.17 * clustering_n.get(node, 0.0)
            + 0.13 * closeness_n.get(node, 0.0)
            + 0.07 * proximity_n.get(node, 0.0)
            + 0.05 * source_separation
        )

    # Rank candidate pocket centers by path-band, local pocket cohesion, and
    # non-hub bridge structure. Then predict a pocket-sized residue cluster.
    center_scores = {}
    center_clusters = {}
    for center in candidate_nodes:
        cluster = graph_radius_cluster(graph, center, radius=1) - active_nodes
        if not cluster:
            cluster = {center}
        pruned = prune_cluster_to_size(graph, center, cluster, max(top_k, 3), node_scores)
        density = cluster_density(graph, pruned)
        size_fit = math.exp(-((len(pruned) - top_k) ** 2) / (2.0 * max(top_k, 1) ** 2))
        mean_node = statistics.fmean(node_scores.get(node, 0.0) for node in pruned)
        center_scores[center] = 0.58 * mean_node + 0.24 * density + 0.18 * size_fit
        center_clusters[center] = pruned

    top_center = max(center_scores, key=center_scores.get)
    mirror_pocket = set(center_clusters[top_center])
    if len(mirror_pocket) < top_k:
        for node, _score in sorted(node_scores.items(), key=lambda item: (-item[1], str(item[0]))):
            mirror_pocket.add(node)
            if len(mirror_pocket) >= top_k:
                break
    if len(mirror_pocket) > top_k:
        mirror_pocket = prune_cluster_to_size(graph, top_center, mirror_pocket, top_k, node_scores)

    degree_center = max(candidate_nodes, key=lambda node: degree_n.get(node, 0.0))
    closeness_center = max(candidate_nodes, key=lambda node: closeness_n.get(node, 0.0))
    proximity_center = max(candidate_nodes, key=lambda node: proximity_n.get(node, 0.0))

    degree_pocket = prune_cluster_to_size(
        graph, degree_center, graph_radius_cluster(graph, degree_center, radius=1) - active_nodes, top_k, degree_n
    )
    closeness_pocket = prune_cluster_to_size(
        graph, closeness_center, graph_radius_cluster(graph, closeness_center, radius=1) - active_nodes, top_k, closeness_n
    )
    proximity_pocket = prune_cluster_to_size(
        graph, proximity_center, graph_radius_cluster(graph, proximity_center, radius=1) - active_nodes, top_k, proximity_n
    )

    random_scores = []
    shuffle_scores = []
    for _ in range(random_trials):
        center = list(sample_node_set(rng, candidate_nodes, 1))[0]
        random_pocket = prune_cluster_to_size(
            graph,
            center,
            graph_radius_cluster(graph, center, radius=1) - active_nodes,
            top_k,
            node_scores,
        )
        random_scores.append(jaccard(random_pocket, truth_nodes))
        shuffled_truth = sample_node_set(rng, candidate_nodes, min(len(truth_nodes), len(candidate_nodes)))
        shuffle_scores.append(jaccard(mirror_pocket, shuffled_truth))

    return {
        "top_k": top_k,
        "candidate_nodes": len(candidate_nodes),
        "mirror_pocket_jaccard": jaccard(mirror_pocket, truth_nodes),
        "degree_pocket_jaccard": jaccard(degree_pocket, truth_nodes),
        "closeness_pocket_jaccard": jaccard(closeness_pocket, truth_nodes),
        "active_proximity_pocket_jaccard": jaccard(proximity_pocket, truth_nodes),
        "random_mean_jaccard": float(statistics.fmean(random_scores)) if random_scores else 0.0,
        "random_p95_jaccard": float(np.percentile(random_scores, 95)) if random_scores else 0.0,
        "label_shuffle_mean_jaccard": float(statistics.fmean(shuffle_scores)) if shuffle_scores else 0.0,
        "label_shuffle_p95_jaccard": float(np.percentile(shuffle_scores, 95)) if shuffle_scores else 0.0,
        "random_scores": random_scores,
        "shuffle_scores": shuffle_scores,
        "selected_center": str(top_center),
        "active_source_count": len(active_nodes),
    }


def mean_col(df: pd.DataFrame, column: str) -> float:
    if df.empty or column not in df:
        return 0.0
    return float(pd.to_numeric(df[column], errors="coerce").mean())


def write_report(summary: dict, row_scores: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows_path = OUT_DIR / "nest2d_allostery_pocket_path_mapper_row_scores.csv"
    json_path = OUT_DIR / "nest2d_allostery_pocket_path_mapper_summary.json"
    report_path = OUT_DIR / "nest2d_allostery_pocket_path_mapper_report.md"
    row_scores.to_csv(rows_path, index=False)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Nest 2D-2 Allostery Pocket / Path Mapper Report",
        "",
        f"- `status`: `{summary['status']}`",
        f"- `benchmark_rows`: `{summary['benchmark_rows']}`",
        f"- `scored_rows`: `{summary['scored_rows']}`",
        f"- `source_label_overlap_rows`: `{summary['source_label_overlap_rows']}`",
        f"- `structures_available`: `{summary['structures_available']}`",
        f"- `random_trials`: `{summary['random_trials']}`",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Mirror pocket/path mean Jaccard | {summary['mirror_pocket_mean_jaccard']:.6f} |",
        f"| Previous contact-only Mirror mean Jaccard | {summary['previous_contact_only_mirror_mean_jaccard']:.6f} |",
        f"| Best existing AlloBench tool mean Jaccard | {summary['best_existing_tool_mean_jaccard']:.6f} |",
        f"| Best existing tool | {summary['best_existing_tool']} |",
        f"| Degree pocket mean Jaccard | {summary['degree_pocket_mean_jaccard']:.6f} |",
        f"| Closeness pocket mean Jaccard | {summary['closeness_pocket_mean_jaccard']:.6f} |",
        f"| Active-proximity pocket mean Jaccard | {summary['active_proximity_pocket_mean_jaccard']:.6f} |",
        f"| Random pocket mean Jaccard | {summary['random_mean_jaccard']:.6f} |",
        f"| Random pocket p95 Jaccard | {summary['random_p95_jaccard']:.6f} |",
        f"| Label-shuffle mean Jaccard | {summary['label_shuffle_mean_jaccard']:.6f} |",
        f"| Label-shuffle p95 Jaccard | {summary['label_shuffle_p95_jaccard']:.6f} |",
        f"| Random-control p-value | {summary['random_control_p_value']:.6f} |",
        f"| Label-shuffle p-value | {summary['label_shuffle_p_value']:.6f} |",
        "",
        "## Clean Read",
        "",
        summary["clean_read"],
        "",
        "## What This Moves",
        "",
        "- Upgrades the 2D object from residue top-k to pocket/path scoring.",
        "- Uses chain-resolved active-site sources instead of matching active-site numbers across every chain.",
        "- Keeps the same AlloBench/PDB benchmark surface, so the comparison is against the previous 2D graph run.",
        "- Establishes whether geometric pocket/path scoring improves the allostery lane before adding external pocket tools.",
        "",
        "## Next 2D-3 Upgrade",
        "",
        "- add real pocket-tool candidates (`fpocket`, `P2Rank`, or `PrankWeb`) when locally available",
        "- add ligand/contact pocket features from HETATM / binding-site geometry",
        "- compare pocket-cluster recovery and communication-path recovery as separate metrics",
        "- repeat on a second benchmark set if the same-100-PDB pocket/path run clears controls",
        "",
        "## Artifacts",
        "",
        f"- row scores: `{rows_path.relative_to(REPO_ROOT)}`",
        f"- summary JSON: `{json_path.relative_to(REPO_ROOT)}`",
    ]
    report_path.write_text("\n".join(lines) + "\n")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    benchmark = pd.read_csv(BENCHMARK_CSV)
    source = pd.read_csv(ALLOBENCH_CSV)
    label_map = aggregate_allobench_labels(source)
    rng = np.random.default_rng(RANDOM_SEED)
    random_trials = 500

    tool_cols = [
        column
        for column in benchmark.columns
        if column not in {"row", "pdb_id"} and not column.endswith("_raw")
    ]
    tool_means = benchmark[tool_cols].apply(pd.to_numeric, errors="coerce").mean().sort_values(ascending=False)
    best_tool = str(tool_means.index[0])
    best_tool_mean = float(tool_means.iloc[0])

    previous_summary_path = GRAPH_OUT_DIR / "nest2d_allostery_graph_mapper_summary.json"
    previous_mirror = 0.0
    if previous_summary_path.exists():
        previous_mirror = float(json.loads(previous_summary_path.read_text()).get("mirror_mean_jaccard", 0.0))

    row_records = []
    random_trial_means: list[list[float]] = [[] for _ in range(random_trials)]
    shuffle_trial_means: list[list[float]] = [[] for _ in range(random_trials)]

    for _, row in benchmark.iterrows():
        pdb_id = clean_pdb_id(row["pdb_id"])
        label_entry = label_map.get(pdb_id)
        pdb_path = PDB_DIR / f"{pdb_id}.pdb"
        if label_entry is None:
            row_records.append({"pdb_id": pdb_id, "status": "missing_allobench_labels"})
            continue
        if not pdb_path.exists():
            row_records.append({"pdb_id": pdb_id, "status": "missing_structure"})
            continue

        residues = parse_pdb_residues(pdb_path)
        graph = build_contact_graph(residues, CONTACT_CUTOFF_ANGSTROM)
        allosteric_nodes = match_allosteric_nodes(graph, label_entry["allosteric"])
        active_nodes = chain_resolved_active_nodes(graph, label_entry["active"])
        if not active_nodes:
            active_nodes = match_active_nodes(graph, label_entry["active"])
        if not allosteric_nodes:
            row_records.append({"pdb_id": pdb_id, "status": "allosteric_labels_unmatched"})
            continue
        if not active_nodes:
            row_records.append({"pdb_id": pdb_id, "status": "active_labels_unmatched"})
            continue

        scored = pocket_predictions(graph, active_nodes, allosteric_nodes, rng, random_trials)
        for idx, value in enumerate(scored["random_scores"]):
            random_trial_means[idx].append(value)
        for idx, value in enumerate(scored["shuffle_scores"]):
            shuffle_trial_means[idx].append(value)

        row_records.append(
            {
                "pdb_id": pdb_id,
                "status": "scored",
                "residue_count": graph.number_of_nodes(),
                "edge_count": graph.number_of_edges(),
                "allosteric_matched_count": len(allosteric_nodes),
                "active_source_count": scored["active_source_count"],
                "top_k": scored["top_k"],
                "candidate_nodes": scored["candidate_nodes"],
                "mirror_pocket_jaccard": scored["mirror_pocket_jaccard"],
                "degree_pocket_jaccard": scored["degree_pocket_jaccard"],
                "closeness_pocket_jaccard": scored["closeness_pocket_jaccard"],
                "active_proximity_pocket_jaccard": scored["active_proximity_pocket_jaccard"],
                "random_mean_jaccard": scored["random_mean_jaccard"],
                "random_p95_jaccard": scored["random_p95_jaccard"],
                "label_shuffle_mean_jaccard": scored["label_shuffle_mean_jaccard"],
                "label_shuffle_p95_jaccard": scored["label_shuffle_p95_jaccard"],
                "selected_center": scored["selected_center"],
            }
        )

    rows = pd.DataFrame(row_records)
    scored_rows = rows[rows["status"] == "scored"].copy()
    mirror_mean = mean_col(scored_rows, "mirror_pocket_jaccard")
    random_controls = [float(statistics.fmean(values)) for values in random_trial_means if values]
    shuffle_controls = [float(statistics.fmean(values)) for values in shuffle_trial_means if values]

    beats_graph_controls = mirror_mean > max(
        mean_col(scored_rows, "degree_pocket_jaccard"),
        mean_col(scored_rows, "closeness_pocket_jaccard"),
        mean_col(scored_rows, "active_proximity_pocket_jaccard"),
        mean_col(scored_rows, "random_mean_jaccard"),
    )
    beats_previous = mirror_mean > previous_mirror
    beats_best_tool = mirror_mean > best_tool_mean
    random_p = p_value(mirror_mean, random_controls)
    shuffle_p = p_value(mirror_mean, shuffle_controls)

    if beats_best_tool and beats_graph_controls and random_p <= 0.05:
        status = "allostery_pocket_path_supported"
        clean_read = (
            "Nest 2D-2 supports the pocket/path mapper: it beats the strongest AlloBench mean-Jaccard bar, "
            "graph pocket controls, and random controls on the same resolved benchmark surface."
        )
    elif beats_previous and beats_graph_controls:
        status = "allostery_pocket_path_partial_improved"
        clean_read = (
            "Nest 2D-2 improves the biological representation: pocket/path scoring beats the first contact-only "
            "mapper and graph pocket controls, while the strongest existing AlloBench tool remains the higher "
            "closeout bar."
        )
    elif beats_previous:
        status = "allostery_pocket_path_directional_open"
        clean_read = (
            "Nest 2D-2 improves over the first contact-only mapper, but graph pocket controls still define the "
            "remaining gap. The next upgrade should add real pocket-tool candidates and ligand/contact geometry."
        )
    else:
        status = "allostery_pocket_path_open"
        clean_read = (
            "Nest 2D-2 remains open: the current pocket/path heuristic does not improve over the first contact-only "
            "mapper enough to claim support. The useful boundary is now specific: add real pocket-tool candidates, "
            "ligand-contact geometry, and separate communication-path recovery metrics."
        )

    summary = {
        "status": status,
        "benchmark_rows": int(len(benchmark)),
        "source_label_overlap_rows": int(sum(clean_pdb_id(v) in label_map for v in benchmark["pdb_id"])),
        "structures_available": int(sum((PDB_DIR / f"{clean_pdb_id(v)}.pdb").exists() for v in benchmark["pdb_id"])),
        "scored_rows": int(len(scored_rows)),
        "random_trials": random_trials,
        "best_existing_tool": best_tool,
        "best_existing_tool_mean_jaccard": best_tool_mean,
        "previous_contact_only_mirror_mean_jaccard": previous_mirror,
        "mirror_pocket_mean_jaccard": mirror_mean,
        "degree_pocket_mean_jaccard": mean_col(scored_rows, "degree_pocket_jaccard"),
        "closeness_pocket_mean_jaccard": mean_col(scored_rows, "closeness_pocket_jaccard"),
        "active_proximity_pocket_mean_jaccard": mean_col(scored_rows, "active_proximity_pocket_jaccard"),
        "random_mean_jaccard": mean_col(scored_rows, "random_mean_jaccard"),
        "random_p95_jaccard": mean_col(scored_rows, "random_p95_jaccard"),
        "label_shuffle_mean_jaccard": mean_col(scored_rows, "label_shuffle_mean_jaccard"),
        "label_shuffle_p95_jaccard": mean_col(scored_rows, "label_shuffle_p95_jaccard"),
        "random_control_p_value": random_p,
        "label_shuffle_p_value": shuffle_p,
        "beats_previous_contact_only": beats_previous,
        "beats_graph_controls": beats_graph_controls,
        "beats_best_existing_tool": beats_best_tool,
        "clean_read": clean_read,
    }
    write_report(summary, rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
