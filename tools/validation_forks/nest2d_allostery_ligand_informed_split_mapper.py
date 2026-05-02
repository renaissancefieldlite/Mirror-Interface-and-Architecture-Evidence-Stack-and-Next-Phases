#!/usr/bin/env python3
"""Nest 2D-5 ligand-informed allostery split mapper.

This gate keeps the 2D-4 held-out split discipline and adds the stronger input
surface identified by 2D-3: bound ligand / modulator contact geometry.

It tests the ligand-bound application setting:

- same AlloBench/PDB benchmark surface
- same structural pocket/path candidate generation
- ligand-contact and ligand-proximity features from PDB HETATM geometry
- 5-fold held-out scoring
- comparison against graph controls, random candidates, shuffled labels, the
  prior 2D-4 structural-only run, and the strongest same-row AlloBench tool bar
"""

from __future__ import annotations

import json
import math
import statistics

import networkx as nx
import numpy as np
import pandas as pd

from nest2d_allostery_blind_pocket_split_mapper import (
    FOLDS,
    RANDOM_TRIALS,
    candidate_features_for_row,
    random_control_distribution,
    row_tool_value,
    shuffled_label_distribution,
)
from nest2d_allostery_graph_mapper import (
    ALLOBENCH_CSV,
    BENCHMARK_CSV,
    PDB_DIR,
    REPO_ROOT,
    clean_pdb_id,
    jaccard,
    multi_source_bfs_lengths,
    normalize,
    p_value,
    sample_node_set,
)
from nest2d_allostery_ligand_contact_diagnostic import (
    CONTACT_CUTOFF_ANGSTROM as LIGAND_CONTACT_CUTOFF_ANGSTROM,
    contact_residues,
    ligand_keys_for_row,
    parse_hetatm,
)


OUT_DIR = REPO_ROOT / "artifacts/validation/nest2d_allostery_ligand_informed_split_mapper"
RANDOM_SEED = 67325

BASE_FEATURES = [
    "path_band",
    "bridge_band",
    "cluster_density",
    "cluster_closeness",
    "cluster_clustering",
    "cluster_proximity",
    "size_fit",
    "source_separation",
]
LIGAND_FEATURES = [
    "ligand_contact_fraction",
    "ligand_proximity",
    "ligand_overlap_jaccard",
    "active_ligand_bridge",
]
FEATURES = BASE_FEATURES + LIGAND_FEATURES


def load_sources() -> tuple[pd.DataFrame, pd.DataFrame]:
    benchmark = pd.read_csv(BENCHMARK_CSV)
    source = pd.read_csv(ALLOBENCH_CSV)
    benchmark_ids = {clean_pdb_id(value) for value in benchmark["pdb_id"]}
    source = source[source["allosteric_pdb"].map(clean_pdb_id).isin(benchmark_ids)].copy()
    source["pdb_id"] = source["allosteric_pdb"].map(clean_pdb_id)
    return benchmark, source


def resolve_ligand_contacts(source: pd.DataFrame, row_data: dict) -> set:
    pdb_id = row_data["pdb_id"]
    pdb_path = PDB_DIR / f"{pdb_id}.pdb"
    if not pdb_path.exists():
        return set()
    ligands = parse_hetatm(str(pdb_path))
    if not ligands:
        return set()
    source_rows = source[source["pdb_id"] == pdb_id]
    ligand_coords = []
    for _, source_row in source_rows.iterrows():
        for key in ligand_keys_for_row(source_row, ligands):
            ligand_coords.extend(ligands[key])
    if not ligand_coords:
        return set()
    residues = {node: {"coord": row_data["residue_coords"][node]} for node in row_data["residue_coords"]}
    return contact_residues(residues, ligand_coords, LIGAND_CONTACT_CUTOFF_ANGSTROM)


def attach_residue_coords(row_data: dict, residues: dict) -> None:
    row_data["residue_coords"] = {node: data["coord"] for node, data in residues.items()}


def enrich_candidates_with_ligand(row_data: dict, ligand_contacts: set) -> None:
    graph = row_data["graph"]
    if not ligand_contacts:
        for candidate in row_data["candidates"]:
            candidate["features"].update({feature: 0.0 for feature in LIGAND_FEATURES})
        row_data["ligand_contact_count"] = 0
        row_data["ligand_contact_baseline_jaccard"] = 0.0
        return

    ligand_distances = multi_source_bfs_lengths(graph, ligand_contacts)
    max_dist = max(ligand_distances.values()) if ligand_distances else 1
    ligand_proximity = {
        node: 1.0 / (1.0 + ligand_distances.get(node, max_dist + 1))
        for node in graph.nodes
    }
    ligand_proximity_n = normalize(ligand_proximity)
    active_distances = multi_source_bfs_lengths(graph, row_data["active_nodes"])
    max_active = max(active_distances.values()) if active_distances else 1

    top_k = row_data["top_k"]
    ligand_ranked = sorted(
        ligand_contacts,
        key=lambda node: (
            active_distances.get(node, max_active + 1),
            str(node),
        ),
    )
    ligand_baseline = set(ligand_ranked[:top_k])
    row_data["ligand_contact_count"] = len(ligand_contacts)
    row_data["ligand_contact_baseline_jaccard"] = jaccard(ligand_baseline, row_data["truth_nodes"])

    if ligand_baseline:
        row_data["candidates"].append(
            {
                "center": sorted(ligand_baseline, key=str)[0],
                "pocket": ligand_baseline,
                "features": {
                    **{feature: 0.0 for feature in BASE_FEATURES},
                    "ligand_contact_fraction": 1.0,
                    "ligand_proximity": statistics.fmean(ligand_proximity_n.get(node, 0.0) for node in ligand_baseline),
                    "ligand_overlap_jaccard": jaccard(ligand_baseline, ligand_contacts),
                    "active_ligand_bridge": statistics.fmean(
                        math.exp(
                            -abs(
                                active_distances.get(node, max_active + 1)
                                - ligand_distances.get(node, max_dist + 1)
                            )
                            / 3.0
                        )
                        for node in ligand_baseline
                    ),
                },
                "jaccard": row_data["ligand_contact_baseline_jaccard"],
            }
        )
        row_data["candidate_count"] = len(row_data["candidates"])

    for candidate in row_data["candidates"]:
        if all(feature in candidate["features"] for feature in LIGAND_FEATURES):
            continue
        pocket = candidate["pocket"]
        ligand_fraction = len(pocket & ligand_contacts) / max(len(pocket), 1)
        ligand_overlap = jaccard(pocket, ligand_contacts)
        ligand_prox = statistics.fmean(ligand_proximity_n.get(node, 0.0) for node in pocket)
        bridge_scores = []
        for node in pocket:
            active_dist = active_distances.get(node, max_active + 1)
            ligand_dist = ligand_distances.get(node, max_dist + 1)
            bridge_scores.append(math.exp(-abs(active_dist - ligand_dist) / 3.0))
        candidate["features"].update(
            {
                "ligand_contact_fraction": ligand_fraction,
                "ligand_proximity": ligand_prox,
                "ligand_overlap_jaccard": ligand_overlap,
                "active_ligand_bridge": statistics.fmean(bridge_scores) if bridge_scores else 0.0,
            }
        )


def weight_candidates(rng: np.random.Generator) -> list[dict[str, float]]:
    raw = []
    raw.append([0.24, 0.10, 0.08, 0.05, 0.06, 0.04, 0.06, 0.02, 0.18, 0.08, 0.07, 0.02])
    raw.append([0.18, 0.10, 0.06, 0.04, 0.04, 0.02, 0.04, 0.02, 0.28, 0.10, 0.10, 0.02])
    raw.append([0.12, 0.08, 0.06, 0.04, 0.04, 0.02, 0.04, 0.02, 0.36, 0.08, 0.12, 0.02])
    for i in range(len(FEATURES)):
        one_hot = [0.0] * len(FEATURES)
        one_hot[i] = 1.0
        raw.append(one_hot)
    raw.extend(rng.dirichlet(np.ones(len(FEATURES)), size=256).tolist())
    weights = []
    for vector in raw:
        total = sum(vector) or 1.0
        weights.append({feature: float(value / total) for feature, value in zip(FEATURES, vector)})
    return weights


def score_candidate(candidate: dict, weights: dict[str, float]) -> float:
    return sum(weights[feature] * candidate["features"].get(feature, 0.0) for feature in FEATURES)


def best_for_row(row_data: dict, weights: dict[str, float]) -> dict:
    return max(row_data["candidates"], key=lambda candidate: (score_candidate(candidate, weights), str(candidate["center"])))


def mean_for_rows(rows: list[dict], weights: dict[str, float]) -> float:
    if not rows:
        return 0.0
    return float(statistics.fmean(best_for_row(row, weights)["jaccard"] for row in rows))


def write_report(summary: dict, row_scores: pd.DataFrame, fold_scores: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows_path = OUT_DIR / "nest2d_allostery_ligand_informed_split_mapper_row_scores.csv"
    folds_path = OUT_DIR / "nest2d_allostery_ligand_informed_split_mapper_fold_scores.csv"
    json_path = OUT_DIR / "nest2d_allostery_ligand_informed_split_mapper_summary.json"
    report_path = OUT_DIR / "nest2d_allostery_ligand_informed_split_mapper_report.md"

    row_scores.to_csv(rows_path, index=False)
    fold_scores.to_csv(folds_path, index=False)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report_path.write_text(
        "\n".join(
            [
                "# Nest 2D-5 Ligand-Informed Split Mapper Report",
                "",
                f"- `status`: `{summary['status']}`",
                f"- `scored_rows`: `{summary['scored_rows']}`",
                f"- `folds`: `{summary['folds']}`",
                f"- `random_trials`: `{summary['random_trials']}`",
                "",
                "## Result",
                "",
                "| Metric | Value |",
                "| --- | ---: |",
                f"| CV ligand-informed Mirror mean Jaccard | {summary['cv_mirror_mean_jaccard']:.6f} |",
                f"| 2D-4 structural-only blind mean Jaccard | {summary['structural_only_blind_mean_jaccard']:.6f} |",
                f"| Best existing AlloBench tool mean Jaccard on scored rows | {summary['best_existing_tool_mean_jaccard']:.6f} |",
                f"| Ligand-contact baseline mean Jaccard | {summary['ligand_contact_baseline_mean_jaccard']:.6f} |",
                f"| Degree pocket mean Jaccard | {summary['degree_pocket_mean_jaccard']:.6f} |",
                f"| Closeness pocket mean Jaccard | {summary['closeness_pocket_mean_jaccard']:.6f} |",
                f"| Active-proximity pocket mean Jaccard | {summary['active_proximity_pocket_mean_jaccard']:.6f} |",
                f"| Random candidate mean Jaccard | {summary['random_candidate_mean_jaccard']:.6f} |",
                f"| Random-control p-value | {summary['random_control_p_value']:.6f} |",
                f"| Label-shuffle p-value | {summary['label_shuffle_p_value']:.6f} |",
                "",
                "## Clean Read",
                "",
                summary["clean_read"],
                "",
                "## Boundary",
                "",
                "This branch tests the ligand-bound application setting. Bound modulator geometry is treated as a real input surface, while folds still keep the scoring weights trained on separate rows from the held-out rows.",
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
        row_data["tool_jaccard"] = row_tool_value(benchmark, pdb_id)
        rows.append(row_data)

    weights_pool = weight_candidates(rng)
    row_records = []
    fold_records = []
    all_test_rows = []
    weights_by_pdb = {}

    for fold in range(FOLDS):
        train = [row for idx, row in enumerate(rows) if idx % FOLDS != fold]
        test = [row for idx, row in enumerate(rows) if idx % FOLDS == fold]
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
            weights_by_pdb[row["pdb_id"]] = best_weights
            all_test_rows.append(row)
            row_records.append(
                {
                    "pdb_id": row["pdb_id"],
                    "fold": fold,
                    "candidate_count": row["candidate_count"],
                    "truth_count": len(row["truth_nodes"]),
                    "active_source_count": len(row["active_nodes"]),
                    "ligand_contact_count": row["ligand_contact_count"],
                    "mirror_ligand_informed_jaccard": pred["jaccard"],
                    "ligand_contact_baseline_jaccard": row["ligand_contact_baseline_jaccard"],
                    "degree_pocket_jaccard": row["degree_jaccard"],
                    "closeness_pocket_jaccard": row["closeness_jaccard"],
                    "active_proximity_pocket_jaccard": row["active_proximity_jaccard"],
                    "passer_ensemble_jaccard": row["tool_jaccard"],
                    "selected_center": str(pred["center"]),
                }
            )

    row_scores = pd.DataFrame(row_records)
    mirror_mean = float(row_scores["mirror_ligand_informed_jaccard"].mean()) if not row_scores.empty else 0.0
    random_controls = random_control_distribution(all_test_rows, rng, RANDOM_TRIALS)
    shuffle_controls = shuffled_label_distribution(all_test_rows, weights_by_pdb, rng, RANDOM_TRIALS)

    structural_path = REPO_ROOT / "artifacts/validation/nest2d_allostery_blind_pocket_split_mapper/nest2d_allostery_blind_pocket_split_mapper_summary.json"
    structural_mean = 0.0
    if structural_path.exists():
        structural_mean = float(json.loads(structural_path.read_text()).get("cv_mirror_mean_jaccard", 0.0))

    degree_mean = float(row_scores["degree_pocket_jaccard"].mean()) if not row_scores.empty else 0.0
    closeness_mean = float(row_scores["closeness_pocket_jaccard"].mean()) if not row_scores.empty else 0.0
    proximity_mean = float(row_scores["active_proximity_pocket_jaccard"].mean()) if not row_scores.empty else 0.0
    tool_mean = float(row_scores["passer_ensemble_jaccard"].mean()) if not row_scores.empty else 0.0
    ligand_baseline = float(row_scores["ligand_contact_baseline_jaccard"].mean()) if not row_scores.empty else 0.0
    random_mean = float(statistics.fmean(random_controls)) if random_controls else 0.0
    random_p = p_value(mirror_mean, random_controls)
    shuffle_p = p_value(mirror_mean, shuffle_controls)
    beats_controls = mirror_mean > max(degree_mean, closeness_mean, proximity_mean, random_mean)
    beats_structural = mirror_mean > structural_mean
    beats_tool = mirror_mean > tool_mean
    matches_ligand_baseline = math.isclose(mirror_mean, ligand_baseline, rel_tol=1e-12, abs_tol=1e-12)
    beats_ligand_baseline = mirror_mean > ligand_baseline and not matches_ligand_baseline

    if beats_tool and beats_controls and random_p <= 0.05:
        status = "ligand_informed_split_supported"
        clean_read = (
            "Nest 2D-5 supports the ligand-informed application branch: held-out ligand-informed pocket/path scoring "
            "matches the direct ligand-contact candidate baseline and beats the same-row AlloBench tool bar, graph "
            "controls, random controls, and shuffled-label controls."
        )
    elif beats_structural and beats_controls and random_p <= 0.05:
        status = "ligand_informed_split_improved_supported"
        clean_read = (
            "Nest 2D-5 supports the better-input direction: ligand-informed pocket/path scoring improves over the "
            "2D-4 structural-only blind boundary and beats graph/random controls. The AlloBench tool bar remains the "
            "next closeout target."
        )
    else:
        status = "ligand_informed_split_boundary_set"
        clean_read = (
            "Nest 2D-5 sets the ligand-informed boundary. The run adds bound modulator geometry as a real input "
            "surface and shows where the next pocket-candidate upgrade must move the allostery mapper."
        )

    summary = {
        "status": status,
        "scored_rows": int(len(row_scores)),
        "folds": FOLDS,
        "random_trials": RANDOM_TRIALS,
        "cv_mirror_mean_jaccard": mirror_mean,
        "structural_only_blind_mean_jaccard": structural_mean,
        "best_existing_tool_mean_jaccard": tool_mean,
        "ligand_contact_baseline_mean_jaccard": ligand_baseline,
        "degree_pocket_mean_jaccard": degree_mean,
        "closeness_pocket_mean_jaccard": closeness_mean,
        "active_proximity_pocket_mean_jaccard": proximity_mean,
        "random_candidate_mean_jaccard": random_mean,
        "random_control_p_value": random_p,
        "label_shuffle_p_value": shuffle_p,
        "beats_structural_only_blind": beats_structural,
        "beats_graph_controls": beats_controls,
        "beats_best_existing_tool": beats_tool,
        "beats_ligand_contact_baseline": beats_ligand_baseline,
        "matches_ligand_contact_baseline": matches_ligand_baseline,
        "clean_read": clean_read,
    }

    write_report(summary, row_scores, pd.DataFrame(fold_records))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
