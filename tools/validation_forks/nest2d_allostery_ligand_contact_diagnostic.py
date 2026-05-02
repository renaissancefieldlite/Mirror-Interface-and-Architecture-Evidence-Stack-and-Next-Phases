#!/usr/bin/env python3
"""Nest 2D-3 bound-ligand contact diagnostic.

This diagnostic checks whether the AlloBench allosteric residue labels align
with ligand-contact geometry in the corresponding bound PDB structures.

It is not a blind allosteric-site predictor. It is a mapping sanity check and a
feature-source test: if bound ligand contacts recover the labels, the next
mapper should include ligand/contact pocket features or external pocket-tool
candidates when available.
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from nest2d_allostery_graph_mapper import (
    ALLOBENCH_CSV,
    BENCHMARK_CSV,
    PDB_DIR,
    REPO_ROOT,
    clean_pdb_id,
    jaccard,
    match_allosteric_nodes,
    parse_allosteric_labels,
    parse_pdb_residues,
)


OUT_DIR = REPO_ROOT / "artifacts/validation/nest2d_allostery_ligand_contact_diagnostic"
CONTACT_CUTOFF_ANGSTROM = 5.0
WATER_OR_ION_NAMES = {
    "HOH",
    "WAT",
    "DOD",
    "NA",
    "CL",
    "K",
    "CA",
    "MG",
    "ZN",
    "MN",
    "FE",
    "CU",
    "CO",
    "NI",
    "CD",
    "SO4",
    "PO4",
}


def residue_number(value) -> int | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


@lru_cache(maxsize=None)
def parse_hetatm(path_text: str) -> dict[tuple[str, int, str], list[np.ndarray]]:
    path = Path(path_text)
    ligands: dict[tuple[str, int, str], list[np.ndarray]] = {}
    if not path.exists():
        return ligands
    for line in path.read_text(errors="ignore").splitlines():
        if not line.startswith("HETATM"):
            continue
        resname = line[17:20].strip().upper()
        if resname in WATER_OR_ION_NAMES:
            continue
        chain = (line[21].strip() or "_").upper()
        try:
            resseq = int(line[22:26])
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
        except ValueError:
            continue
        ligands.setdefault((chain, resseq, resname), []).append(np.array([x, y, z], dtype=float))
    return ligands


def ligand_keys_for_row(row: pd.Series, ligands: dict) -> list[tuple[str, int, str]]:
    chain = str(row.get("modulator_chain", "")).strip().upper()
    alias = str(row.get("modulator_alias", "")).strip().upper()
    resseq = residue_number(row.get("modulator_resi"))
    keys = []
    if chain and resseq is not None:
        keys.extend(key for key in ligands if key[0] == chain and key[1] == resseq)
    if alias:
        keys.extend(key for key in ligands if key[2] == alias)
    # preserve order while removing duplicates
    out = []
    seen = set()
    for key in keys:
        if key not in seen:
            out.append(key)
            seen.add(key)
    return out


def contact_residues(residues: dict, ligand_coords: list[np.ndarray], cutoff: float) -> set:
    if not residues or not ligand_coords:
        return set()
    ligand_matrix = np.stack(ligand_coords)
    contacts = set()
    for key, data in residues.items():
        coord = data["coord"]
        dists = np.sqrt(np.sum((ligand_matrix - coord) ** 2, axis=1))
        if float(np.min(dists)) <= cutoff:
            contacts.add(key)
    return contacts


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    benchmark = pd.read_csv(BENCHMARK_CSV)
    source = pd.read_csv(ALLOBENCH_CSV)
    benchmark_ids = {clean_pdb_id(value) for value in benchmark["pdb_id"]}
    source = source[source["allosteric_pdb"].map(clean_pdb_id).isin(benchmark_ids)].copy()
    source["pdb_id"] = source["allosteric_pdb"].map(clean_pdb_id)

    row_records = []
    residue_cache = {}
    for _, row in source.iterrows():
        pdb_id = row["pdb_id"]
        pdb_path = PDB_DIR / f"{pdb_id}.pdb"
        if not pdb_path.exists():
            row_records.append({"pdb_id": pdb_id, "status": "missing_structure"})
            continue
        residues = residue_cache.get(pdb_id)
        if residues is None:
            residues = parse_pdb_residues(pdb_path)
            residue_cache[pdb_id] = residues
        ligands = parse_hetatm(str(pdb_path))
        keys = ligand_keys_for_row(row, ligands)
        if not keys:
            row_records.append({"pdb_id": pdb_id, "status": "modulator_ligand_unmatched"})
            continue

        ligand_coords = []
        for key in keys:
            ligand_coords.extend(ligands[key])
        predicted = contact_residues(residues, ligand_coords, CONTACT_CUTOFF_ANGSTROM)
        truth_labels = parse_allosteric_labels([row["allosteric_site_residue"]])
        # Build a tiny graph-like shim for the existing matcher.
        class NodeView:
            nodes = set(residues.keys())

        truth = match_allosteric_nodes(NodeView, truth_labels)
        if not truth:
            row_records.append({"pdb_id": pdb_id, "status": "allosteric_labels_unmatched"})
            continue
        if not predicted:
            row_records.append({"pdb_id": pdb_id, "status": "no_ligand_contacts", "truth_count": len(truth)})
            continue

        row_records.append(
            {
                "pdb_id": pdb_id,
                "status": "scored",
                "target_id": row.get("target_id", ""),
                "modulator_alias": row.get("modulator_alias", ""),
                "modulator_chain": row.get("modulator_chain", ""),
                "modulator_resi": row.get("modulator_resi", ""),
                "ligand_keys": ";".join(f"{key[0]}:{key[1]}:{key[2]}" for key in keys),
                "truth_count": len(truth),
                "contact_count": len(predicted),
                "intersection_count": len(predicted & truth),
                "ligand_contact_jaccard": jaccard(predicted, truth),
            }
        )

    rows = pd.DataFrame(row_records)
    scored = rows[rows["status"] == "scored"].copy()
    mean_jaccard = float(pd.to_numeric(scored["ligand_contact_jaccard"], errors="coerce").mean()) if not scored.empty else 0.0
    median_jaccard = float(pd.to_numeric(scored["ligand_contact_jaccard"], errors="coerce").median()) if not scored.empty else 0.0
    rows_over_02 = int((pd.to_numeric(scored["ligand_contact_jaccard"], errors="coerce") >= 0.2).sum()) if not scored.empty else 0
    rows_over_05 = int((pd.to_numeric(scored["ligand_contact_jaccard"], errors="coerce") >= 0.5).sum()) if not scored.empty else 0

    status = "ligand_contact_mapping_supported" if mean_jaccard > 0.19733 else "ligand_contact_mapping_partial"
    clean_read = (
        "Bound-ligand contact geometry recovers the AlloBench allosteric labels above the strongest mean-Jaccard "
        "tool bar, confirming that the labels and structures align as real pocket/contact objects. This is a "
        "feature-source diagnostic for the next blind allosteric prediction closeout."
        if status == "ligand_contact_mapping_supported"
        else "Bound-ligand contact geometry provides a useful pocket/contact diagnostic, but it does not clear the "
        "strongest mean-Jaccard tool bar on the scored rows."
    )
    summary = {
        "status": status,
        "source_rows_in_benchmark": int(len(source)),
        "scored_rows": int(len(scored)),
        "contact_cutoff_angstrom": CONTACT_CUTOFF_ANGSTROM,
        "mean_ligand_contact_jaccard": mean_jaccard,
        "median_ligand_contact_jaccard": median_jaccard,
        "rows_jaccard_ge_0_2": rows_over_02,
        "rows_jaccard_ge_0_5": rows_over_05,
        "best_existing_tool_mean_jaccard": 0.19733,
        "clean_read": clean_read,
    }

    rows_path = OUT_DIR / "nest2d_allostery_ligand_contact_diagnostic_row_scores.csv"
    json_path = OUT_DIR / "nest2d_allostery_ligand_contact_diagnostic_summary.json"
    report_path = OUT_DIR / "nest2d_allostery_ligand_contact_diagnostic_report.md"
    rows.to_csv(rows_path, index=False)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report_path.write_text(
        "\n".join(
            [
                "# Nest 2D-3 Allostery Ligand-Contact Diagnostic",
                "",
                f"- `status`: `{status}`",
                f"- `source_rows_in_benchmark`: `{len(source)}`",
                f"- `scored_rows`: `{len(scored)}`",
                f"- `contact_cutoff_angstrom`: `{CONTACT_CUTOFF_ANGSTROM}`",
                "",
                "## Result",
                "",
                "| Metric | Value |",
                "| --- | ---: |",
                f"| Mean ligand-contact Jaccard | {mean_jaccard:.6f} |",
                f"| Median ligand-contact Jaccard | {median_jaccard:.6f} |",
                f"| Rows >= 0.2 Jaccard | {rows_over_02} |",
                f"| Rows >= 0.5 Jaccard | {rows_over_05} |",
                f"| Best existing AlloBench tool mean Jaccard | {0.19733:.6f} |",
                "",
                "## Clean Read",
                "",
                clean_read,
                "",
                "## Boundary",
                "",
                "This diagnostic uses bound ligand/contact geometry present in the PDB files. It validates that the allosteric labels map onto real pocket/contact structure and supplies a strong feature source for the next blind allosteric-site mapper.",
                "",
                "## Artifacts",
                "",
                f"- row scores: `{rows_path.relative_to(REPO_ROOT)}`",
                f"- summary JSON: `{json_path.relative_to(REPO_ROOT)}`",
            ]
        )
        + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
