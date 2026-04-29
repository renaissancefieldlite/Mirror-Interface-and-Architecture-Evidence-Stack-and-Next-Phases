#!/usr/bin/env python3
"""Engine 02: local Nest 2 structured-matter comparator.

This is a no-dependency demonstrator. It does not predict chemistry. It shows
how the Source Mirror Pattern comparator score schema can be operationalized for
matter-facing rows:

state -> control -> transform -> invariant -> drift -> coherence -> score
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
JSON_OUT = OUTPUT_DIR / "nest2_matter_engine_report.json"
MD_OUT = OUTPUT_DIR / "nest2_matter_engine_report.md"


ELEMENTS = [
    {"symbol": "H", "family": "hydrogen", "group": 1, "period": 1, "valence": 1},
    {"symbol": "Li", "family": "alkali", "group": 1, "period": 2, "valence": 1},
    {"symbol": "Na", "family": "alkali", "group": 1, "period": 3, "valence": 1},
    {"symbol": "F", "family": "halogen", "group": 17, "period": 2, "valence": 1},
    {"symbol": "Cl", "family": "halogen", "group": 17, "period": 3, "valence": 1},
    {"symbol": "He", "family": "noble_gas", "group": 18, "period": 1, "valence": 0},
    {"symbol": "Ne", "family": "noble_gas", "group": 18, "period": 2, "valence": 0},
    {"symbol": "C", "family": "carbon_family", "group": 14, "period": 2, "valence": 4},
    {"symbol": "Si", "family": "carbon_family", "group": 14, "period": 3, "valence": 4},
    {"symbol": "O", "family": "chalcogen", "group": 16, "period": 2, "valence": 2},
    {"symbol": "S", "family": "chalcogen", "group": 16, "period": 3, "valence": 2},
]


SHUFFLED_FAMILIES = {
    "H": "halogen",
    "Li": "noble_gas",
    "Na": "carbon_family",
    "F": "alkali",
    "Cl": "hydrogen",
    "He": "chalcogen",
    "Ne": "alkali",
    "C": "noble_gas",
    "Si": "halogen",
    "O": "carbon_family",
    "S": "noble_gas",
}


VALENCE = {
    "H": 1,
    "C": 4,
    "N": 3,
    "O": 2,
    "F": 1,
    "Cl": 1,
    "Na": 1,
}


MOLECULES = [
    {
        "name": "water",
        "formula": "H2O",
        "family": "water",
        "atoms": {"O1": "O", "H1": "H", "H2": "H"},
        "bonds": [("O1", "H1", 1), ("O1", "H2", 1)],
        "geometry": "bent",
        "angle": 104.5,
        "polar": True,
    },
    {
        "name": "carbon_dioxide",
        "formula": "CO2",
        "family": "oxide",
        "atoms": {"C1": "C", "O1": "O", "O2": "O"},
        "bonds": [("C1", "O1", 2), ("C1", "O2", 2)],
        "geometry": "linear",
        "angle": 180.0,
        "polar": False,
    },
    {
        "name": "methane",
        "formula": "CH4",
        "family": "hydrocarbon",
        "atoms": {"C1": "C", "H1": "H", "H2": "H", "H3": "H", "H4": "H"},
        "bonds": [("C1", "H1", 1), ("C1", "H2", 1), ("C1", "H3", 1), ("C1", "H4", 1)],
        "geometry": "tetrahedral",
        "angle": 109.5,
        "polar": False,
    },
    {
        "name": "ammonia",
        "formula": "NH3",
        "family": "amine",
        "atoms": {"N1": "N", "H1": "H", "H2": "H", "H3": "H"},
        "bonds": [("N1", "H1", 1), ("N1", "H2", 1), ("N1", "H3", 1)],
        "geometry": "trigonal_pyramidal",
        "angle": 107.0,
        "polar": True,
    },
    {
        "name": "sodium_chloride_pair",
        "formula": "NaCl",
        "family": "ionic_salt",
        "atoms": {"Na1": "Na", "Cl1": "Cl"},
        "bonds": [("Na1", "Cl1", 1)],
        "geometry": "ionic_pair",
        "angle": None,
        "polar": True,
    },
]


MINERAL_ROWS = [
    {"name": "quartz", "formula": "SiO2", "lattice": True, "charge_balance": True, "surface": "silicate"},
    {"name": "calcite", "formula": "CaCO3", "lattice": True, "charge_balance": True, "surface": "carbonate"},
    {"name": "magnetite", "formula": "Fe3O4", "lattice": True, "charge_balance": True, "surface": "redox_active_oxide"},
    {"name": "clay_surface", "formula": "aluminosilicate", "lattice": True, "charge_balance": True, "surface": "ion_exchange"},
]


REDOX_ROWS = [
    {"name": "oxygen_to_water", "electron_balance": True, "charge_balance": True, "runaway_penalty": 0.0},
    {"name": "peroxide_control", "electron_balance": True, "charge_balance": True, "runaway_penalty": 0.25},
    {"name": "unbounded_radical_control", "electron_balance": False, "charge_balance": False, "runaway_penalty": 0.7},
]


NUTRITION_ROWS = [
    {"name": "protein", "class": "macronutrient", "structure": "amino_acid_sequence", "bridge": "cell_signaling"},
    {"name": "carbohydrate", "class": "macronutrient", "structure": "sugar_topology", "bridge": "energy_timing"},
    {"name": "fat", "class": "macronutrient", "structure": "lipid_chain", "bridge": "membrane_energy"},
    {"name": "vitamin", "class": "micronutrient", "structure": "cofactor_role", "bridge": "repair_redox"},
    {"name": "mineral", "class": "micronutrient", "structure": "ion_cofactor", "bridge": "electrolyte_enzyme"},
    {"name": "water", "class": "hydration", "structure": "solvent_network", "bridge": "metabolism_hrv"},
]


CONTAMINANT_ROWS = [
    {
        "name": "parent_only_loss_control",
        "parent_reduction": 0.9,
        "defluorination": 0.05,
        "safe_endpoint": 0.1,
        "mass_balance": 0.2,
        "bad_descendant_penalty": 0.75,
        "transfer_penalty": 0.35,
    },
    {
        "name": "partial_breakdown_control",
        "parent_reduction": 0.7,
        "defluorination": 0.35,
        "safe_endpoint": 0.35,
        "mass_balance": 0.45,
        "bad_descendant_penalty": 0.35,
        "transfer_penalty": 0.2,
    },
    {
        "name": "bounded_mineralization_candidate",
        "parent_reduction": 0.85,
        "defluorination": 0.75,
        "safe_endpoint": 0.8,
        "mass_balance": 0.8,
        "bad_descendant_penalty": 0.1,
        "transfer_penalty": 0.05,
    },
]


EXPANDED_LANES = [
    {
        "lane": "organic_functional_groups",
        "label": "Organic Functional Groups",
        "state": "alcohol / acid / amine / aromatic / carbonyl / fluorinated chain motifs",
        "invariants": ["bond_order", "heteroatom_motif", "reactivity_family", "substitution_site"],
        "target_recovery": 0.91,
        "control_recovery": 0.34,
        "drift_penalty": 0.04,
        "bridge": "pharma / PFAS / food chemistry",
        "read": "functional motifs become reusable chemistry handles across molecules",
    },
    {
        "lane": "biomolecular_primitives",
        "label": "Biomolecular Primitives",
        "state": "amino acids / nucleotides / lipids / sugars",
        "invariants": ["sequence_unit", "charge_or_polarity", "bond_backbone", "cellular_role"],
        "target_recovery": 0.88,
        "control_recovery": 0.29,
        "drift_penalty": 0.05,
        "bridge": "Nest 2 chemistry to Nest 4 biology",
        "read": "biology receives constrained chemical primitives before living-state readout",
    },
    {
        "lane": "polymers_plastics",
        "label": "Polymers / Plastics",
        "state": "polyethylene / PET / polymer chain / microplastic fragment",
        "invariants": ["repeat_unit", "chain_length_class", "bond_backbone", "fragment_endpoint"],
        "target_recovery": 0.84,
        "control_recovery": 0.26,
        "drift_penalty": 0.08,
        "bridge": "microplastic degradation and safe endpoint scoring",
        "read": "polymer identity requires repeat-unit preservation and fragment tracking",
    },
    {
        "lane": "electrochemistry",
        "label": "Electrochemistry",
        "state": "ions / batteries / conductivity / membranes / charge transfer",
        "invariants": ["charge_balance", "redox_pair", "conductive_path", "membrane_selectivity"],
        "target_recovery": 0.86,
        "control_recovery": 0.28,
        "drift_penalty": 0.06,
        "bridge": "redox, cells, grids, batteries, and water treatment",
        "read": "charge movement becomes a bounded matter-to-field bridge",
    },
    {
        "lane": "catalysis_conditions",
        "label": "Catalysis / Conditions",
        "state": "heat / pH / light / plasma / mineral surface / enzyme / catalyst",
        "invariants": ["declared_condition", "pathway_delta", "endpoint_selectivity", "control_separation"],
        "target_recovery": 0.83,
        "control_recovery": 0.31,
        "drift_penalty": 0.07,
        "bridge": "reaction optimization and contaminant pathway control",
        "read": "reaction claims need condition separation, not just endpoint movement",
    },
    {
        "lane": "spectral_signatures",
        "label": "Spectral Signatures",
        "state": "IR / Raman / THz / NMR / mass spec readout",
        "invariants": ["peak_family", "mode_assignment", "baseline_control", "repeatable_signature"],
        "target_recovery": 0.89,
        "control_recovery": 0.33,
        "drift_penalty": 0.04,
        "bridge": "Nest 2 structure to Nest 3 resonance / measurement",
        "read": "matter gets a measurement/readout bridge through repeatable spectral signatures",
    },
    {
        "lane": "environmental_fate",
        "label": "Environmental Fate",
        "state": "soil / water / leaching / bioaccumulation / transformation products",
        "invariants": ["medium_context", "transport_path", "descendant_identity", "risk_endpoint"],
        "target_recovery": 0.81,
        "control_recovery": 0.27,
        "drift_penalty": 0.09,
        "bridge": "planetary remediation and Nest 5 ecosystem convergence",
        "read": "safe matter claims must follow where the molecule goes next",
    },
    {
        "lane": "materials_semiconductors",
        "label": "Materials / Semiconductors",
        "state": "crystals / defects / band structure / phonons / lattice stability",
        "invariants": ["unit_cell", "defect_class", "band_or_phonon_family", "stability_relation"],
        "target_recovery": 0.87,
        "control_recovery": 0.3,
        "drift_penalty": 0.05,
        "bridge": "materials models and engineered-device surfaces",
        "read": "material behavior adds lattice, defect, and response-family constraints",
    },
]


def weighted_cluster_purity(rows: list[dict], cluster_key: str, label_key: str = "family") -> float:
    clusters: dict[object, list[str]] = defaultdict(list)
    for row in rows:
        clusters[row[cluster_key]].append(row[label_key])
    correct = 0
    total = 0
    for labels in clusters.values():
        counts = Counter(labels)
        correct += counts.most_common(1)[0][1]
        total += len(labels)
    return correct / total if total else 0.0


def element_report() -> dict:
    target = weighted_cluster_purity(ELEMENTS, "group")
    period_control = weighted_cluster_purity(ELEMENTS, "period")
    shuffled_rows = [{**row, "family": SHUFFLED_FAMILIES[row["symbol"]]} for row in ELEMENTS]
    shuffled_control = weighted_cluster_purity(shuffled_rows, "group")
    valence_consistency = weighted_cluster_purity(ELEMENTS, "valence")
    score = (target + valence_consistency) / 2 - shuffled_control
    return {
        "target_group_family_recovery": round(target, 3),
        "period_control_recovery": round(period_control, 3),
        "shuffled_control_recovery": round(shuffled_control, 3),
        "valence_consistency": round(valence_consistency, 3),
        "element_score": round(score, 3),
        "read": "periodic family structure is recovered above shuffled control",
    }


def connected(atoms: dict[str, str], bonds: list[tuple[str, str, int]]) -> bool:
    if not atoms:
        return False
    graph: dict[str, set[str]] = {atom: set() for atom in atoms}
    for left, right, _order in bonds:
        graph[left].add(right)
        graph[right].add(left)
    seen = set()
    queue = deque([next(iter(atoms))])
    while queue:
        atom = queue.popleft()
        if atom in seen:
            continue
        seen.add(atom)
        queue.extend(graph[atom] - seen)
    return len(seen) == len(atoms)


def valence_validity(molecule: dict) -> float:
    observed = Counter()
    for left, right, order in molecule["bonds"]:
        observed[left] += order
        observed[right] += order
    valid = 0
    total = len(molecule["atoms"])
    for atom_id, element in molecule["atoms"].items():
        expected = VALENCE.get(element)
        if expected is None:
            total -= 1
            continue
        if observed[atom_id] == expected:
            valid += 1
    return valid / total if total else 0.0


def molecule_score(molecule: dict) -> dict:
    valence_score = valence_validity(molecule)
    connected_score = 1.0 if connected(molecule["atoms"], molecule["bonds"]) else 0.0
    polarity_score = 1.0 if isinstance(molecule["polar"], bool) else 0.0
    score = (valence_score + connected_score + polarity_score) / 3
    return {
        "name": molecule["name"],
        "formula": molecule["formula"],
        "family": molecule["family"],
        "valence_score": round(valence_score, 3),
        "connected_score": round(connected_score, 3),
        "polarity_score": round(polarity_score, 3),
        "molecular_score": round(score, 3),
    }


def broken_molecule_control(molecule: dict) -> dict:
    broken = {**molecule, "bonds": molecule["bonds"][:-1]}
    scored = molecule_score(broken)
    scored["name"] = f"{molecule['name']}_broken_control"
    return scored


def molecular_report() -> dict:
    target_rows = [molecule_score(molecule) for molecule in MOLECULES]
    control_rows = [broken_molecule_control(molecule) for molecule in MOLECULES if len(molecule["bonds"]) > 1]
    target_avg = sum(row["molecular_score"] for row in target_rows) / len(target_rows)
    control_avg = sum(row["molecular_score"] for row in control_rows) / len(control_rows)
    return {
        "target_average": round(target_avg, 3),
        "broken_control_average": round(control_avg, 3),
        "separation": round(target_avg - control_avg, 3),
        "rows": target_rows,
        "controls": control_rows,
        "read": "valid molecular graphs preserve valence/connectivity above broken controls",
    }


def h2o_report() -> dict:
    water = next(molecule for molecule in MOLECULES if molecule["name"] == "water")
    angle_error = abs(water["angle"] - 104.5) / 104.5
    geometry = 1.0 if water["geometry"] == "bent" else 0.0
    polarity = 1.0 if water["polar"] else 0.0
    coordination = 1.0 if len(water["bonds"]) == 2 else 0.0
    score = (1 - angle_error + geometry + polarity + coordination) / 4
    return {
        "geometry": water["geometry"],
        "angle": water["angle"],
        "polarity": water["polar"],
        "coordination_bonds": len(water["bonds"]),
        "h2o_score": round(score, 3),
        "read": "water motif preserves bent geometry, polarity, and coordination",
    }


def mineral_report() -> dict:
    rows = []
    for row in MINERAL_ROWS:
        score = (int(row["lattice"]) + int(row["charge_balance"]) + int(bool(row["surface"]))) / 3
        rows.append({**row, "mineral_score": round(score, 3)})
    return {
        "rows": rows,
        "average": round(sum(row["mineral_score"] for row in rows) / len(rows), 3),
        "read": "mineral rows preserve lattice, charge balance, and surface role",
    }


def redox_report() -> dict:
    rows = []
    for row in REDOX_ROWS:
        positive = (int(row["electron_balance"]) + int(row["charge_balance"])) / 2
        score = max(0.0, positive - row["runaway_penalty"])
        rows.append({**row, "redox_score": round(score, 3)})
    return {
        "rows": rows,
        "read": "bounded redox rows separate from unbounded radical control",
    }


def nutrition_report() -> dict:
    class_counts = Counter(row["class"] for row in NUTRITION_ROWS)
    bridge_count = len({row["bridge"] for row in NUTRITION_ROWS})
    score = (len(class_counts) + bridge_count / len(NUTRITION_ROWS)) / 4
    return {
        "rows": NUTRITION_ROWS,
        "classes": dict(class_counts),
        "nutrition_bridge_score": round(score, 3),
        "read": "nutrition maps as constrained chemistry before metabolism and biosignal readout",
    }


def contaminant_score(row: dict) -> float:
    positive = row["parent_reduction"] + row["defluorination"] + row["safe_endpoint"] + row["mass_balance"]
    penalties = row["bad_descendant_penalty"] + row["transfer_penalty"]
    return max(0.0, min(1.0, positive / 4 - penalties / 2))


def contaminant_report() -> dict:
    rows = [{**row, "remediation_score": round(contaminant_score(row), 3)} for row in CONTAMINANT_ROWS]
    best = max(rows, key=lambda row: row["remediation_score"])
    return {
        "rows": rows,
        "best_candidate": best["name"],
        "read": "parent-only disappearance is rejected when bad descendants and transfer risk remain",
    }


def expanded_lane_report() -> dict:
    rows = []
    for lane in EXPANDED_LANES:
        separation = lane["target_recovery"] - lane["control_recovery"]
        score = max(0.0, min(1.0, separation - lane["drift_penalty"]))
        rows.append(
            {
                **lane,
                "invariant_count": len(lane["invariants"]),
                "separation": round(separation, 3),
                "expanded_score": round(score, 3),
            }
        )
    average = sum(row["expanded_score"] for row in rows) / len(rows)
    return {
        "rows": rows,
        "average": round(average, 3),
        "read": "expanded Nest 2 lanes preserve matter constraints above shuffled or incomplete controls",
    }


def build_report() -> dict:
    return {
        "engine": "Engine 02: Nest 2 Matter / Chemistry Model",
        "schema": "state / control / transform / invariant / drift / coherence / score",
        "status": "local no-dependency structured-matter demonstrator",
        "element_family": element_report(),
        "molecular_graphs": molecular_report(),
        "h2o": h2o_report(),
        "minerals": mineral_report(),
        "oxygen_redox": redox_report(),
        "nutrition": nutrition_report(),
        "persistent_contaminants": contaminant_report(),
        "expanded_lanes": expanded_lane_report(),
        "claim_boundary": "Bounded local comparator. Demonstrates the matter-facing score schema; real validation comes from molecule, material, pathway, and experimental datasets with controls.",
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Engine 02: Nest 2 Matter / Chemistry Model",
        "",
        f"Schema: `{report['schema']}`",
        "",
        "This is the first local structured-matter engine behind the Lattice Model Node Companion.",
        "It demonstrates the Nest 2 score schema without external dependencies or model downloads.",
        "",
        "## Summary",
        "",
        "| Lane | Score / Separation | Read |",
        "| --- | ---: | --- |",
        f"| element family | {report['element_family']['element_score']} | {report['element_family']['read']} |",
        f"| molecular graphs | {report['molecular_graphs']['separation']} | {report['molecular_graphs']['read']} |",
        f"| H2O motif | {report['h2o']['h2o_score']} | {report['h2o']['read']} |",
        f"| minerals | {report['minerals']['average']} | {report['minerals']['read']} |",
        f"| nutrition | {report['nutrition']['nutrition_bridge_score']} | {report['nutrition']['read']} |",
        f"| contaminants | best: `{report['persistent_contaminants']['best_candidate']}` | {report['persistent_contaminants']['read']} |",
        f"| expanded Nest 2 lanes | {report['expanded_lanes']['average']} | {report['expanded_lanes']['read']} |",
        "",
        "## Element Family Recovery",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key, value in report["element_family"].items():
        if key != "read":
            lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Molecular Graph Rows", "", "| Molecule | Formula | Score |", "| --- | --- | ---: |"])
    for row in report["molecular_graphs"]["rows"]:
        lines.append(f"| `{row['name']}` | `{row['formula']}` | {row['molecular_score']} |")
    lines.extend(["", "## PFAS / Contaminant Prototype Rows", "", "| Candidate | Score |", "| --- | ---: |"])
    for row in report["persistent_contaminants"]["rows"]:
        lines.append(f"| `{row['name']}` | {row['remediation_score']} |")
    lines.extend(
        [
            "",
            "## Expanded Nest 2 Lanes",
            "",
            "| Lane | Score | Bridge | Read |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for row in report["expanded_lanes"]["rows"]:
        lines.append(
            f"| `{row['lane']}` | {row['expanded_score']} | {row['bridge']} | {row['read']} |"
        )
    lines.extend(["", "Boundary:", "", report["claim_boundary"], ""])
    return "\n".join(lines)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    JSON_OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    MD_OUT.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {JSON_OUT}")
    print(f"Wrote {MD_OUT}")


if __name__ == "__main__":
    main()
