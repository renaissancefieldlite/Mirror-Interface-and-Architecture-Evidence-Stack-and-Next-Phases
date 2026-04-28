#!/usr/bin/env python3
"""Nest 2E PFAS pathway validation on real EPA reaction-library data.

The test is intentionally bounded:
- true parent -> product rows come from the EPA PFAS reaction library
- controls shuffle product structures against parent structures
- support means true transformations are more chemically coherent than shuffled
  parent/product pairings under fixed RDKit descriptor scoring

This does not claim PFAS remediation or destruction.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = ROOT / "artifacts" / "validation" / "datasets" / "PFAS_RxnLibData_ESPI2022.xlsx"
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "nest2e_pfas_pathway"


@dataclass(frozen=True)
class MolFeatures:
    smiles: str
    atoms: int
    carbons: int
    fluorines: int
    oxygens: int
    nitrogens: int
    sulfurs: int
    halogens: int
    rings: int
    mol_wt: float
    logp: float
    cf_bonds: int


def mol_from_smiles(smiles: object):
    if not isinstance(smiles, str) or not smiles.strip():
        return None
    return Chem.MolFromSmiles(smiles.strip())


def atom_count(mol, atomic_num: int) -> int:
    return sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == atomic_num)


def count_cf_bonds(mol) -> int:
    count = 0
    for bond in mol.GetBonds():
        nums = {bond.GetBeginAtom().GetAtomicNum(), bond.GetEndAtom().GetAtomicNum()}
        if nums == {6, 9}:
            count += 1
    return count


def features(smiles: str) -> MolFeatures | None:
    mol = mol_from_smiles(smiles)
    if mol is None:
        return None
    halogens = sum(atom_count(mol, z) for z in (9, 17, 35, 53))
    return MolFeatures(
        smiles=smiles,
        atoms=mol.GetNumAtoms(),
        carbons=atom_count(mol, 6),
        fluorines=atom_count(mol, 9),
        oxygens=atom_count(mol, 8),
        nitrogens=atom_count(mol, 7),
        sulfurs=atom_count(mol, 16),
        halogens=halogens,
        rings=rdMolDescriptors.CalcNumRings(mol),
        mol_wt=float(Descriptors.MolWt(mol)),
        logp=float(Descriptors.MolLogP(mol)),
        cf_bonds=count_cf_bonds(mol),
    )


def load_pairs(dataset: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for sheet in ("EnvLib", "MetaLib"):
        df = pd.read_excel(dataset, sheet_name=sheet)
        for _, row in df.iterrows():
            for product_slot, product_col in (("product_1", "Product_SMILES"), ("product_2", "Product_2_SMILES")):
                parent_smiles = row.get("Parent_SMILES")
                product_smiles = row.get(product_col)
                if not isinstance(parent_smiles, str) or not isinstance(product_smiles, str):
                    continue
                parent_features = features(parent_smiles)
                product_features = features(product_smiles)
                if parent_features is None or product_features is None:
                    continue
                rows.append(
                    {
                        "sheet": sheet,
                        "rxn_type": row.get("Rxn_Type"),
                        "rxn": row.get("Rxn"),
                        "rxn_system": row.get("Rxn_System"),
                        "parent": row.get("Parent"),
                        "product": row.get("Product") if product_slot == "product_1" else row.get("Product_2"),
                        "parent_smiles": parent_smiles,
                        "product_smiles": product_smiles,
                        "product_slot": product_slot,
                        "half_life_days": row.get("HalfLife_calc (Days)"),
                        "doi": row.get("DOI"),
                    }
                )
    pairs = pd.DataFrame(rows).drop_duplicates(
        subset=["sheet", "rxn_type", "parent_smiles", "product_smiles", "product_slot"]
    )
    return pairs.reset_index(drop=True)


def feature_vector(f: MolFeatures) -> np.ndarray:
    return np.array(
        [
            f.atoms,
            f.carbons,
            f.fluorines,
            f.oxygens,
            f.nitrogens,
            f.sulfurs,
            f.halogens,
            f.rings,
            f.mol_wt / 50.0,
            f.logp,
            f.cf_bonds,
        ],
        dtype=float,
    )


def pair_score(parent_smiles: str, product_smiles: str) -> dict[str, float] | None:
    parent = features(parent_smiles)
    product = features(product_smiles)
    if parent is None or product is None:
        return None
    p = feature_vector(parent)
    q = feature_vector(product)
    delta = np.abs(p - q)
    # Coherence is high when the observed transformation is chemically local
    # relative to random parent/product pairings.
    coherence = 1.0 / (1.0 + float(delta.mean()))
    retained_f_ratio = product.fluorines / max(parent.fluorines, 1)
    retained_cf_ratio = product.cf_bonds / max(parent.cf_bonds, 1)
    bad_descendant_penalty = max(retained_f_ratio, retained_cf_ratio)
    defluorination = parent.fluorines - product.fluorines
    cf_reduction = parent.cf_bonds - product.cf_bonds
    return {
        "pathway_coherence_score": coherence,
        "descriptor_l1_mean": float(delta.mean()),
        "fluorine_delta": float(defluorination),
        "cf_bond_delta": float(cf_reduction),
        "retained_f_ratio": float(retained_f_ratio),
        "retained_cf_ratio": float(retained_cf_ratio),
        "bad_descendant_penalty": float(bad_descendant_penalty),
    }


def coherence_from_features(parent: MolFeatures, product: MolFeatures) -> float:
    delta = np.abs(feature_vector(parent) - feature_vector(product))
    return 1.0 / (1.0 + float(delta.mean()))


def score_pairs(pairs: pd.DataFrame) -> pd.DataFrame:
    scored: list[dict[str, object]] = []
    for _, row in pairs.iterrows():
        score = pair_score(str(row["parent_smiles"]), str(row["product_smiles"]))
        if score is None:
            continue
        scored.append({**row.to_dict(), **score})
    return pd.DataFrame(scored)


def permutation_p(scored: pd.DataFrame, permutations: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    true_mean = float(scored["pathway_coherence_score"].mean())
    parents = scored["parent_smiles"].to_numpy()
    products = scored["product_smiles"].to_numpy()
    feature_cache: dict[str, MolFeatures] = {}
    for smiles in set(parents).union(set(products)):
        f = features(str(smiles))
        if f is not None:
            feature_cache[str(smiles)] = f
    null_means: list[float] = []
    for _ in range(permutations):
        shuffled = rng.permutation(products)
        values = []
        for parent, product in zip(parents, shuffled, strict=False):
            parent_features = feature_cache.get(str(parent))
            product_features = feature_cache.get(str(product))
            if parent_features is not None and product_features is not None:
                values.append(coherence_from_features(parent_features, product_features))
        null_means.append(float(mean(values)) if values else 0.0)
    null = np.array(null_means)
    p = (float((null >= true_mean).sum()) + 1.0) / (len(null) + 1.0)
    return {
        "true_mean_pathway_coherence": true_mean,
        "shuffle_mean_pathway_coherence": float(null.mean()),
        "shuffle_std_pathway_coherence": float(null.std()),
        "permutation_p": p,
        "permutations": permutations,
        "seed": seed,
    }


def write_report(scored: pd.DataFrame, stats: dict[str, object], out_dir: Path) -> None:
    retained_high = float((scored["bad_descendant_penalty"] >= 0.8).mean())
    any_defluorination = float(((scored["fluorine_delta"] > 0) | (scored["cf_bond_delta"] > 0)).mean())
    by_type = (
        scored.groupby("rxn_type", dropna=False)
        .agg(
            rows=("pathway_coherence_score", "size"),
            mean_coherence=("pathway_coherence_score", "mean"),
            mean_bad_descendant_penalty=("bad_descendant_penalty", "mean"),
            mean_fluorine_delta=("fluorine_delta", "mean"),
            mean_cf_bond_delta=("cf_bond_delta", "mean"),
        )
        .sort_values("rows", ascending=False)
        .reset_index()
    )
    by_type.to_csv(out_dir / "nest2e_pfas_by_reaction_type.csv", index=False)
    scored.to_csv(out_dir / "nest2e_pfas_scored_pairs.csv", index=False)
    status = "completed_real_pfas_pathway_coherence_supported" if stats["permutation_p"] <= 0.05 else "completed_no_control_support"
    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "valid_parent_product_pairs": int(len(scored)),
        **stats,
        "fraction_rows_with_any_defluorination_or_cf_reduction": any_defluorination,
        "fraction_rows_retaining_high_fluorination_or_cf_bonds": retained_high,
        "rxn_type_count": int(scored["rxn_type"].nunique(dropna=True)),
    }
    (out_dir / "nest2e_pfas_pathway_report.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Nest 2E PFAS Pathway Validation Report",
        "",
        f"Status: `{status}`",
        "",
        "## Inputs",
        "",
        "- Dataset: EPA PFAS reaction library Excel (`EnvLib` + `MetaLib`)",
        f"- Valid parent/product transformation pairs: `{len(scored)}`",
        f"- Reaction-type classes: `{summary['rxn_type_count']}`",
        "",
        "## Test",
        "",
        "True EPA parent -> product pathway rows were compared against shuffled",
        "parent/product pairings using fixed RDKit descriptor deltas.",
        "",
        "The validation question was:",
        "",
        "```text",
        "are real PFAS transformation pairs more chemically coherent than random",
        "parent/product pairings from the same library?",
        "```",
        "",
        "## Result",
        "",
        f"- true mean pathway coherence: `{stats['true_mean_pathway_coherence']:.6f}`",
        f"- shuffled mean pathway coherence: `{stats['shuffle_mean_pathway_coherence']:.6f}`",
        f"- shuffled std: `{stats['shuffle_std_pathway_coherence']:.6f}`",
        f"- permutation p: `{stats['permutation_p']:.6f}`",
        f"- permutations: `{stats['permutations']}`",
        "",
        "## PFAS Boundary Read",
        "",
        f"- rows with any fluorine or C-F bond reduction: `{any_defluorination:.4f}`",
        f"- rows retaining high fluorination / C-F burden: `{retained_high:.4f}`",
        "",
        "The retained-fluorination read is important: a parent disappearing or",
        "transforming is not the same as safe mineralization. The bad-descendant",
        "penalty is the right future lane for PFAS remediation logic.",
        "",
        "## Boundary",
        "",
        "This validates a real PFAS pathway-coherence comparator against a public",
        "reaction library. It does not claim PFAS destruction, remediation success,",
        "or safe byproduct generation.",
        "",
    ]
    (out_dir / "nest2e_pfas_pathway_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    parser.add_argument("--permutations", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=67)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pairs = load_pairs(Path(args.dataset))
    scored = score_pairs(pairs)
    stats = permutation_p(scored, args.permutations, args.seed)
    write_report(scored, stats, out_dir)
    print(
        json.dumps(
            {
                "status": "ok",
                "pairs": int(len(scored)),
                "p": stats["permutation_p"],
                "report": str(out_dir / "nest2e_pfas_pathway_report.md"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
