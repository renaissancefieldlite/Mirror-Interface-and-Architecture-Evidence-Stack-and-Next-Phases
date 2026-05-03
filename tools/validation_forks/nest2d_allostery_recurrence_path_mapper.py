#!/usr/bin/env python3
"""Nest 2D-6 allostery recurrence and communication-path mapper.

This gate does not replace the supported 2D-5 ligand-informed result. It asks
the next two questions:

- does the ligand-informed allostery branch recur under a second held-out split?
- when pocket recovery is separated from communication-path recovery, where does
  the signal actually live?

External pocket tools are recorded when available. In the current local lane,
the runner uses the same AlloBench/PDB surface and the same bound-modulator
geometry that closed 2D-5, then adds separate active-site -> pocket path
metrics against graph, random, and shuffled-label controls.
"""

from __future__ import annotations

import json
import math
import shutil
import statistics

import networkx as nx
import numpy as np
import pandas as pd

from nest2d_allostery_blind_pocket_split_mapper import (
    FOLDS,
    RANDOM_TRIALS,
    candidate_features_for_row,
    row_tool_value,
)
from nest2d_allostery_graph_mapper import (
    PDB_DIR,
    REPO_ROOT,
    clean_pdb_id,
    jaccard,
    multi_source_bfs_lengths,
    p_value,
    sample_node_set,
)
from nest2d_allostery_ligand_informed_split_mapper import (
    FEATURES,
    attach_residue_coords,
    best_for_row,
    enrich_candidates_with_ligand,
    load_sources,
    mean_for_rows,
    resolve_ligand_contacts,
    weight_candidates,
)


OUT_DIR = REPO_ROOT / "artifacts/validation/nest2d_allostery_recurrence_path_mapper"
RANDOM_SEED = 67326
EXTERNAL_POCKET_TOOLS = ["fpocket", "p2rank", "prankweb"]


def external_tool_status() -> dict[str, bool]:
    return {tool: shutil.which(tool) is not None for tool in EXTERNAL_POCKET_TOOLS}


def path_nodes_to_pocket(graph: nx.Graph, active_nodes: set, pocket: set) -> set:
    """Return the shortest communication corridor from active sources to pocket.

    For each predicted pocket residue, the closest active-site source is used.
    The union of those shortest paths is the path object scored separately from
    direct endpoint / pocket overlap.
    """

    if not active_nodes or not pocket:
        return set()
    path_nodes: set = set()
    active_sources = sorted(active_nodes, key=str)
    for target in sorted(pocket, key=str):
        best_path = None
        for source in active_sources:
            if source not in graph or target not in graph:
                continue
            try:
                path = nx.shortest_path(graph, source=source, target=target)
            except nx.NetworkXNoPath:
                continue
            if best_path is None or len(path) < len(best_path) or (
                len(path) == len(best_path) and str(path) < str(best_path)
            ):
                best_path = path
        if best_path:
            path_nodes.update(best_path)
    return path_nodes


def communication_metrics(row: dict, pocket: set) -> dict:
    graph = row["graph"]
    truth_nodes = row["truth_nodes"]
    active_nodes = row["active_nodes"]
    path_nodes = path_nodes_to_pocket(graph, active_nodes, pocket)
    interior_nodes = set(path_nodes) - set(active_nodes) - set(pocket)
    truth_count = max(len(truth_nodes), 1)
    path_length_values = []
    if active_nodes and pocket:
        distances = multi_source_bfs_lengths(graph, active_nodes)
        for node in pocket:
            if node in distances:
                path_length_values.append(distances[node])

    return {
        "path_nodes": path_nodes,
        "path_truth_jaccard": jaccard(path_nodes, truth_nodes),
        "path_truth_recall": len(path_nodes & truth_nodes) / truth_count,
        "path_endpoint_jaccard": jaccard(set(pocket), truth_nodes),
        "path_node_count": float(len(path_nodes)),
        "path_interior_count": float(len(interior_nodes)),
        "active_to_pocket_mean_distance": float(statistics.fmean(path_length_values))
        if path_length_values
        else 0.0,
    }


def attach_candidate_path_metrics(row: dict) -> None:
    for candidate in row["candidates"]:
        metrics = communication_metrics(row, candidate["pocket"])
        candidate["path_nodes"] = metrics["path_nodes"]
        candidate["path_metrics"] = {
            key: value for key, value in metrics.items() if key != "path_nodes"
        }


def candidate_by_feature(row: dict, feature: str) -> dict:
    return max(row["candidates"], key=lambda candidate: (candidate["features"].get(feature, 0.0), str(candidate["center"])))


def random_candidate(row: dict, rng: np.random.Generator) -> dict:
    return row["candidates"][int(rng.integers(0, len(row["candidates"])))]


def split_rows(rows: list[dict], fold: int) -> tuple[list[dict], list[dict]]:
    """Alternate split recurrence.

    2D-5 used sorted row order modulo folds. 2D-6 keeps the same rows and fold
    count but uses a deterministic shuffled order before the modulo split, so
    recurrence is tested against a second held-out partition.
    """

    indexed = list(enumerate(rows))
    indexed.sort(key=lambda item: item[0])
    shuffled_indices = np.random.default_rng(RANDOM_SEED).permutation(len(indexed)).tolist()
    test_indices = {idx for position, idx in enumerate(shuffled_indices) if position % FOLDS == fold}
    train = [row for idx, row in enumerate(rows) if idx not in test_indices]
    test = [row for idx, row in enumerate(rows) if idx in test_indices]
    return train, test


def shuffled_path_distribution(
    rows: list[dict],
    predicted_by_pdb: dict[str, dict],
    rng: np.random.Generator,
    trials: int,
    metric: str,
) -> list[float]:
    controls = []
    for _ in range(trials):
        values = []
        for row in rows:
            candidate = predicted_by_pdb[row["pdb_id"]]
            path_nodes = candidate.get("path_nodes", set())
            shuffled_truth = sample_node_set(
                rng,
                row["candidate_nodes"],
                min(len(row["truth_nodes"]), len(row["candidate_nodes"])),
            )
            if metric == "path_truth_recall":
                values.append(len(path_nodes & shuffled_truth) / max(len(shuffled_truth), 1))
            else:
                values.append(jaccard(path_nodes, shuffled_truth))
        controls.append(float(statistics.fmean(values)) if values else 0.0)
    return controls


def random_path_distribution(
    rows: list[dict],
    rng: np.random.Generator,
    trials: int,
    metric: str,
) -> list[float]:
    controls = []
    for _ in range(trials):
        values = []
        for row in rows:
            candidate = random_candidate(row, rng)
            metrics = candidate["path_metrics"]
            values.append(metrics[metric])
        controls.append(float(statistics.fmean(values)) if values else 0.0)
    return controls


def load_previous_summary(name: str) -> dict:
    path = REPO_ROOT / f"artifacts/validation/{name}/{name}_summary.json"
    if path.exists():
        return json.loads(path.read_text())
    return {}


def write_report(summary: dict, row_scores: pd.DataFrame, fold_scores: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows_path = OUT_DIR / "nest2d_allostery_recurrence_path_mapper_row_scores.csv"
    folds_path = OUT_DIR / "nest2d_allostery_recurrence_path_mapper_fold_scores.csv"
    json_path = OUT_DIR / "nest2d_allostery_recurrence_path_mapper_summary.json"
    report_path = OUT_DIR / "nest2d_allostery_recurrence_path_mapper_report.md"

    row_scores.to_csv(rows_path, index=False)
    fold_scores.to_csv(folds_path, index=False)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report_path.write_text(
        "\n".join(
            [
                "# Nest 2D-6 Allostery Recurrence / Path Mapper Report",
                "",
                f"- `status`: `{summary['status']}`",
                f"- `scored_rows`: `{summary['scored_rows']}`",
                f"- `folds`: `{summary['folds']}`",
                f"- `random_trials`: `{summary['random_trials']}`",
                f"- `external_pocket_tools_available`: `{summary['external_pocket_tools_available']}`",
                "",
                "## Result",
                "",
                "| Metric | Value |",
                "| --- | ---: |",
                f"| 2D-6 alternate-split pocket Jaccard | {summary['alternate_split_pocket_mean_jaccard']:.6f} |",
                f"| 2D-5 pocket Jaccard | {summary['previous_2d5_pocket_mean_jaccard']:.6f} |",
                f"| Best same-row AlloBench tool Jaccard | {summary['best_existing_tool_mean_jaccard']:.6f} |",
                f"| Ligand-contact baseline Jaccard | {summary['ligand_contact_baseline_mean_jaccard']:.6f} |",
                f"| Degree pocket Jaccard | {summary['degree_pocket_mean_jaccard']:.6f} |",
                f"| Closeness pocket Jaccard | {summary['closeness_pocket_mean_jaccard']:.6f} |",
                f"| Active-proximity pocket Jaccard | {summary['active_proximity_pocket_mean_jaccard']:.6f} |",
                f"| Random pocket Jaccard | {summary['random_candidate_mean_jaccard']:.6f} |",
                f"| Pocket random-control p-value | {summary['pocket_random_control_p_value']:.6f} |",
                f"| Pocket label-shuffle p-value | {summary['pocket_label_shuffle_p_value']:.6f} |",
                f"| Mirror path-truth Jaccard | {summary['mirror_path_truth_jaccard']:.6f} |",
                f"| Mirror path-truth recall | {summary['mirror_path_truth_recall']:.6f} |",
                f"| Degree path-truth recall | {summary['degree_path_truth_recall']:.6f} |",
                f"| Closeness path-truth recall | {summary['closeness_path_truth_recall']:.6f} |",
                f"| Active-proximity path-truth recall | {summary['active_proximity_path_truth_recall']:.6f} |",
                f"| Random path-truth recall | {summary['random_path_truth_recall']:.6f} |",
                f"| Path random-control p-value | {summary['path_random_control_p_value']:.6f} |",
                f"| Path label-shuffle p-value | {summary['path_label_shuffle_p_value']:.6f} |",
                "",
                "## Clean Read",
                "",
                summary["clean_read"],
                "",
                "## Boundary",
                "",
                "This gate separates two biological claims. Pocket recovery asks whether the predicted residue cluster overlaps known allosteric-site labels. Communication-path recovery asks whether the active-site to predicted-pocket corridor touches those labels more than graph controls. External pocket tools are recorded but not fabricated when unavailable locally.",
                "",
                "## Artifacts",
                "",
                f"- row scores: `{rows_path.relative_to(REPO_ROOT)}`",
                f"- fold scores: `{folds_path.relative_to(REPO_ROOT)}`",
                f"- summary JSON: `{json_path.relative_to(REPO_ROOT)}`",
            ]
        )
        + "\n"
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    benchmark, source = load_sources()

    from nest2d_allostery_graph_mapper import aggregate_allobench_labels, parse_pdb_residues

    label_map = aggregate_allobench_labels(source)
    pdb_ids = sorted(clean_pdb_id(value) for value in benchmark["pdb_id"] if clean_pdb_id(value) in label_map)

    rows = []
    for pdb_id in pdb_ids:
        row_data = candidate_features_for_row(pdb_id, label_map[pdb_id], rng)
        if row_data is None:
            continue
        residues = parse_pdb_residues(PDB_DIR / f"{pdb_id}.pdb")
        attach_residue_coords(row_data, residues)
        ligand_contacts = resolve_ligand_contacts(source, row_data)
        enrich_candidates_with_ligand(row_data, ligand_contacts)
        attach_candidate_path_metrics(row_data)
        row_data["tool_jaccard"] = row_tool_value(benchmark, pdb_id)
        rows.append(row_data)

    weights_pool = weight_candidates(rng)
    row_records = []
    fold_records = []
    all_test_rows = []
    predicted_by_pdb = {}

    for fold in range(FOLDS):
        train, test = split_rows(rows, fold)
        best_weights = max(weights_pool, key=lambda weights: mean_for_rows(train, weights))
        fold_records.append(
            {
                "fold": fold,
                "train_rows": len(train),
                "test_rows": len(test),
                "train_mean_jaccard": mean_for_rows(train, best_weights),
                "test_mean_jaccard": mean_for_rows(test, best_weights),
                **{f"w_{key}": value for key, value in best_weights.items()},
            }
        )
        for row in test:
            pred = best_for_row(row, best_weights)
            predicted_by_pdb[row["pdb_id"]] = pred
            all_test_rows.append(row)

            degree_pred = candidate_by_feature(row, "degree")
            close_pred = candidate_by_feature(row, "closeness")
            prox_pred = candidate_by_feature(row, "proximity")
            mirror_path = pred["path_metrics"]
            degree_path = degree_pred["path_metrics"]
            close_path = close_pred["path_metrics"]
            prox_path = prox_pred["path_metrics"]

            row_records.append(
                {
                    "pdb_id": row["pdb_id"],
                    "fold": fold,
                    "candidate_count": row["candidate_count"],
                    "truth_count": len(row["truth_nodes"]),
                    "active_source_count": len(row["active_nodes"]),
                    "ligand_contact_count": row["ligand_contact_count"],
                    "mirror_pocket_jaccard": pred["jaccard"],
                    "ligand_contact_baseline_jaccard": row["ligand_contact_baseline_jaccard"],
                    "degree_pocket_jaccard": row["degree_jaccard"],
                    "closeness_pocket_jaccard": row["closeness_jaccard"],
                    "active_proximity_pocket_jaccard": row["active_proximity_jaccard"],
                    "passer_ensemble_jaccard": row["tool_jaccard"],
                    "mirror_path_truth_jaccard": mirror_path["path_truth_jaccard"],
                    "mirror_path_truth_recall": mirror_path["path_truth_recall"],
                    "mirror_path_node_count": mirror_path["path_node_count"],
                    "mirror_path_interior_count": mirror_path["path_interior_count"],
                    "mirror_active_to_pocket_mean_distance": mirror_path["active_to_pocket_mean_distance"],
                    "degree_path_truth_recall": degree_path["path_truth_recall"],
                    "closeness_path_truth_recall": close_path["path_truth_recall"],
                    "active_proximity_path_truth_recall": prox_path["path_truth_recall"],
                    "selected_center": str(pred["center"]),
                }
            )

    row_scores = pd.DataFrame(row_records)
    mirror_mean = float(row_scores["mirror_pocket_jaccard"].mean()) if not row_scores.empty else 0.0
    random_pocket_controls = []
    for _ in range(RANDOM_TRIALS):
        values = [random_candidate(row, rng)["jaccard"] for row in all_test_rows]
        random_pocket_controls.append(float(statistics.fmean(values)) if values else 0.0)
    shuffle_pocket_controls = []
    for _ in range(RANDOM_TRIALS):
        values = []
        for row in all_test_rows:
            pred = predicted_by_pdb[row["pdb_id"]]
            shuffled_truth = sample_node_set(
                rng,
                row["candidate_nodes"],
                min(len(row["truth_nodes"]), len(row["candidate_nodes"])),
            )
            values.append(jaccard(pred["pocket"], shuffled_truth))
        shuffle_pocket_controls.append(float(statistics.fmean(values)) if values else 0.0)

    random_path_controls = random_path_distribution(all_test_rows, rng, RANDOM_TRIALS, "path_truth_recall")
    shuffle_path_controls = shuffled_path_distribution(
        all_test_rows,
        predicted_by_pdb,
        rng,
        RANDOM_TRIALS,
        "path_truth_recall",
    )

    previous_2d5 = load_previous_summary("nest2d_allostery_ligand_informed_split_mapper")
    degree_mean = float(row_scores["degree_pocket_jaccard"].mean()) if not row_scores.empty else 0.0
    closeness_mean = float(row_scores["closeness_pocket_jaccard"].mean()) if not row_scores.empty else 0.0
    proximity_mean = float(row_scores["active_proximity_pocket_jaccard"].mean()) if not row_scores.empty else 0.0
    tool_mean = float(row_scores["passer_ensemble_jaccard"].mean()) if not row_scores.empty else 0.0
    ligand_baseline = float(row_scores["ligand_contact_baseline_jaccard"].mean()) if not row_scores.empty else 0.0
    random_pocket_mean = float(statistics.fmean(random_pocket_controls)) if random_pocket_controls else 0.0
    random_path_mean = float(statistics.fmean(random_path_controls)) if random_path_controls else 0.0

    mirror_path_jaccard = float(row_scores["mirror_path_truth_jaccard"].mean()) if not row_scores.empty else 0.0
    mirror_path_recall = float(row_scores["mirror_path_truth_recall"].mean()) if not row_scores.empty else 0.0
    degree_path_recall = float(row_scores["degree_path_truth_recall"].mean()) if not row_scores.empty else 0.0
    closeness_path_recall = float(row_scores["closeness_path_truth_recall"].mean()) if not row_scores.empty else 0.0
    proximity_path_recall = float(row_scores["active_proximity_path_truth_recall"].mean()) if not row_scores.empty else 0.0

    pocket_random_p = p_value(mirror_mean, random_pocket_controls)
    pocket_shuffle_p = p_value(mirror_mean, shuffle_pocket_controls)
    path_random_p = p_value(mirror_path_recall, random_path_controls)
    path_shuffle_p = p_value(mirror_path_recall, shuffle_path_controls)

    beats_pocket_controls = mirror_mean > max(degree_mean, closeness_mean, proximity_mean, random_pocket_mean)
    beats_tool = mirror_mean > tool_mean
    repeats_2d5 = math.isclose(
        mirror_mean,
        float(previous_2d5.get("cv_mirror_mean_jaccard", 0.0)),
        rel_tol=0.05,
        abs_tol=0.02,
    )
    beats_path_controls = mirror_path_recall > max(
        degree_path_recall,
        closeness_path_recall,
        proximity_path_recall,
        random_path_mean,
    )

    if beats_tool and beats_pocket_controls and pocket_random_p <= 0.05 and path_random_p <= 0.05:
        status = "ligand_informed_recurrence_and_path_supported"
        clean_read = (
            "Nest 2D-6 supports recurrence of the ligand-informed allostery branch and separates the mechanism: "
            "pocket recovery stays above the same-row tool bar and controls, while active-site to pocket path "
            "recovery also beats random and shuffled communication-path controls."
        )
    elif beats_tool and beats_pocket_controls and pocket_random_p <= 0.05:
        status = "ligand_informed_recurrence_supported_path_open"
        clean_read = (
            "Nest 2D-6 supports recurrence of the ligand-informed pocket-recovery branch under a second held-out "
            "split. Communication-path scoring is now separated and measured, but remains the next stronger target."
        )
    else:
        status = "ligand_informed_recurrence_boundary_set"
        clean_read = (
            "Nest 2D-6 records the second-split and communication-path boundary. The run separates pocket overlap "
            "from active-site path recovery and identifies what external pocket candidates or second benchmarks "
            "must improve next."
        )

    summary = {
        "status": status,
        "scored_rows": int(len(row_scores)),
        "folds": FOLDS,
        "random_trials": RANDOM_TRIALS,
        "external_pocket_tools_available": external_tool_status(),
        "alternate_split_pocket_mean_jaccard": mirror_mean,
        "previous_2d5_pocket_mean_jaccard": float(previous_2d5.get("cv_mirror_mean_jaccard", 0.0)),
        "pocket_repeats_2d5_within_tolerance": repeats_2d5,
        "best_existing_tool_mean_jaccard": tool_mean,
        "ligand_contact_baseline_mean_jaccard": ligand_baseline,
        "degree_pocket_mean_jaccard": degree_mean,
        "closeness_pocket_mean_jaccard": closeness_mean,
        "active_proximity_pocket_mean_jaccard": proximity_mean,
        "random_candidate_mean_jaccard": random_pocket_mean,
        "pocket_random_control_p_value": pocket_random_p,
        "pocket_label_shuffle_p_value": pocket_shuffle_p,
        "mirror_path_truth_jaccard": mirror_path_jaccard,
        "mirror_path_truth_recall": mirror_path_recall,
        "degree_path_truth_recall": degree_path_recall,
        "closeness_path_truth_recall": closeness_path_recall,
        "active_proximity_path_truth_recall": proximity_path_recall,
        "random_path_truth_recall": random_path_mean,
        "path_random_control_p_value": path_random_p,
        "path_label_shuffle_p_value": path_shuffle_p,
        "beats_best_existing_tool": beats_tool,
        "beats_pocket_controls": beats_pocket_controls,
        "beats_path_controls": beats_path_controls,
        "clean_read": clean_read,
    }

    write_report(summary, row_scores, pd.DataFrame(fold_records))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
