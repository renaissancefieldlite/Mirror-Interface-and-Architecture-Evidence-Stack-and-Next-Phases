#!/usr/bin/env python3
"""Engine 02V molecule-property validation fork.

This is the concrete Nest 2 validation driver for the RDKit/public-dataset
path. It is intentionally strict: without RDKit and a real molecule dataset, it
writes a blocked report instead of pretending toy rows are validation.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import random
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "engine02v_rdkit_molecule"
PERMUTATIONS = 5000
SEED = 67


def write_report(out_dir: Path, report: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "engine02v_rdkit_molecule_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# Engine 02V RDKit Molecule Validation Fork",
        "",
        f"Status: `{report['status']}`",
        "",
        report["read"],
        "",
        "## Requirements",
        "",
    ]
    for item in report["requirements"]:
        lines.append(f"- {item}")
    if report.get("metrics"):
        lines.extend(["", "## Metrics", ""])
        for key, value in report["metrics"].items():
            lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Boundary", "", report["boundary"], ""])
    (out_dir / "engine02v_rdkit_molecule_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def pearson(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 3 or np.std(left) == 0 or np.std(right) == 0:
        return 0.0
    return float(np.corrcoef(left, right)[0, 1])


def abs_corr_shuffle_p(scores: np.ndarray, targets: np.ndarray, permutations: int, seed: int) -> tuple[float, float]:
    observed = abs(pearson(scores, targets))
    rng = random.Random(seed)
    null_values = []
    target_list = [float(value) for value in targets]
    for _ in range(permutations):
        shuffled = target_list[:]
        rng.shuffle(shuffled)
        null_values.append(abs(pearson(scores, np.array(shuffled, dtype=float))))
    p_value = (sum(value >= observed for value in null_values) + 1) / (len(null_values) + 1)
    return p_value, float(np.mean(null_values))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path)
    parser.add_argument("--smiles-column", default="smiles")
    parser.add_argument("--target-column", default="target")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requirements = [
        "RDKit installed in the active Python environment",
        "real molecule dataset CSV with SMILES and target/property column",
        "declared baseline such as shuffled target or naive descriptor score",
    ]
    if importlib.util.find_spec("rdkit") is None:
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_rdkit",
                "read": "RDKit is not installed, so Engine 02V did not run. This is the correct stop condition for a physical-data validation fork.",
                "requirements": requirements,
                "boundary": "No physical chemistry validation was performed.",
            },
        )
        print(f"Wrote blocked report to {args.out_dir}")
        return
    if not args.input_csv or not args.input_csv.exists():
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_dataset",
                "read": "RDKit is available, but no real molecule dataset was provided.",
                "requirements": requirements,
                "boundary": "No physical chemistry validation was performed.",
            },
        )
        print(f"Wrote blocked report to {args.out_dir}")
        return

    from rdkit import Chem
    from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors

    rows = load_rows(args.input_csv)
    scored = []
    for row in rows:
        smiles = row.get(args.smiles_column, "")
        target_raw = row.get(args.target_column, "")
        try:
            target = float(target_raw)
        except ValueError:
            continue
        mol = Chem.MolFromSmiles(smiles)
        if mol is None or math.isnan(target):
            continue
        descriptor_score = (
            Descriptors.MolWt(mol) * 0.01
            + Crippen.MolLogP(mol)
            + Lipinski.NumHDonors(mol)
            + Lipinski.NumHAcceptors(mol)
            + rdMolDescriptors.CalcNumRings(mol)
        )
        scored.append({"smiles": smiles, "target": target, "descriptor_score": descriptor_score})

    if len(scored) < 10:
        status = "blocked_insufficient_rows"
        read = "Dataset parsed, but fewer than 10 valid molecule rows were available."
        metrics = {"valid_rows": len(scored)}
    else:
        targets = np.array([row["target"] for row in scored], dtype=float)
        scores = np.array([row["descriptor_score"] for row in scored], dtype=float)
        shuffled = np.array(list(reversed(targets)), dtype=float)
        observed_corr = pearson(scores, targets)
        p_value, null_mean_abs_corr = abs_corr_shuffle_p(
            scores, targets, args.permutations, args.seed
        )
        status = (
            "completed_real_molecule_signal_supported"
            if p_value <= 0.05
            else "completed_no_control_support"
        )
        metrics = {
            "valid_rows": len(scored),
            "descriptor_target_pearson": round(observed_corr, 4),
            "descriptor_target_abs_pearson": round(abs(observed_corr), 4),
            "shuffled_baseline_pearson": round(pearson(scores, shuffled), 4),
            "permutation_null_mean_abs_pearson": round(null_mean_abs_corr, 4),
            "abs_pearson_shuffle_p": round(p_value, 6),
            "permutations": args.permutations,
            "seed": args.seed,
        }
        read = (
            "RDKit molecule-property validation completed with descriptor signal "
            "above shuffled-target controls."
            if status == "completed_real_molecule_signal_supported"
            else "RDKit molecule-property validation completed, but descriptor signal did not beat controls."
        )

    write_report(
        args.out_dir,
        {
            "status": status,
            "read": read,
            "requirements": requirements,
            "metrics": metrics,
            "boundary": "This is a cheminformatics validation fork only; interpretation depends on dataset quality and target meaning.",
        },
    )
    print(f"Wrote report to {args.out_dir}")


if __name__ == "__main__":
    main()
