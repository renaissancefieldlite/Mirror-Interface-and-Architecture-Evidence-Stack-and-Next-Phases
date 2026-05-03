#!/usr/bin/env python3
"""Nest 2E PFAS bad-descendant / safety logic.

The earlier Nest 2E lane validated pathway coherence: true EPA PFAS
parent/product rows are more chemically local than shuffled parent/product
pairings. This gate asks the next safety question:

If the transformation is coherent, does the product still retain PFAS burden?

The runner uses the existing scored PFAS pathway artifacts, keeping this
upgrade independent of RDKit at this stage. It turns the previous fluorine /
C-F retention columns into a safety triage surface:

- retained PFAS burden
- mineralization-quality proxy
- coherent bad-descendant score
- high-risk descendant flags
- shuffled-burden controls that preserve row distributions
"""

from __future__ import annotations

import argparse
import json
import statistics
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = (
    REPO_ROOT
    / "artifacts/validation/nest2e_pfas_pathway/nest2e_pfas_scored_pairs.csv"
)
DEFAULT_OUT = REPO_ROOT / "artifacts/validation/nest2e_pfas_safety_logic"
DEFAULT_PERMUTATIONS = 5000
DEFAULT_SEED = 69


def p_value_greater(observed: float, null: list[float]) -> float:
    values = np.asarray(null, dtype=float)
    return (float((values >= observed).sum()) + 1.0) / (len(values) + 1.0)


def enrich_safety_rows(scored: pd.DataFrame) -> pd.DataFrame:
    rows = scored.copy()
    retained_f = pd.to_numeric(rows["retained_f_ratio"], errors="coerce").fillna(0.0).clip(lower=0.0)
    retained_cf = pd.to_numeric(rows["retained_cf_ratio"], errors="coerce").fillna(0.0).clip(lower=0.0)
    coherence = pd.to_numeric(rows["pathway_coherence_score"], errors="coerce").fillna(0.0).clip(lower=0.0)

    rows["retained_burden_score"] = pd.concat([retained_f, retained_cf], axis=1).max(axis=1)
    rows["f_reduction_fraction"] = (1.0 - retained_f).clip(lower=0.0, upper=1.0)
    rows["cf_reduction_fraction"] = (1.0 - retained_cf).clip(lower=0.0, upper=1.0)
    rows["mineralization_quality_proxy"] = (
        0.50 * rows["f_reduction_fraction"]
        + 0.50 * rows["cf_reduction_fraction"]
    )
    rows["coherent_bad_descendant_score"] = coherence * rows["retained_burden_score"].clip(upper=1.5)
    rows["safety_failure_score"] = rows["retained_burden_score"].clip(upper=1.5) * (
        1.0 - rows["mineralization_quality_proxy"]
    )
    rows["high_retained_burden_flag"] = rows["retained_burden_score"] >= 0.8
    rows["low_mineralization_flag"] = rows["mineralization_quality_proxy"] <= 0.2
    rows["coherent_pathway_flag"] = coherence >= 0.5
    rows["bad_descendant_flag"] = (
        rows["high_retained_burden_flag"]
        & rows["low_mineralization_flag"]
        & rows["coherent_pathway_flag"]
    )
    rows["safety_candidate_flag"] = (
        (rows["retained_burden_score"] <= 0.2)
        & (rows["mineralization_quality_proxy"] >= 0.8)
    )
    return rows


def shuffled_controls(rows: pd.DataFrame, permutations: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    coherence = rows["pathway_coherence_score"].to_numpy(dtype=float)
    burden = rows["retained_burden_score"].to_numpy(dtype=float)
    mineral = rows["mineralization_quality_proxy"].to_numpy(dtype=float)
    true_risk = float(rows["coherent_bad_descendant_score"].mean())
    true_flag = float(rows["bad_descendant_flag"].mean())
    true_failure = float(rows["safety_failure_score"].mean())

    risk_null = []
    flag_null = []
    failure_null = []
    for _ in range(permutations):
        shuffled_burden = rng.permutation(burden)
        shuffled_mineral = rng.permutation(mineral)
        risk_null.append(float(np.mean(coherence * np.clip(shuffled_burden, 0.0, 1.5))))
        flag_null.append(
            float(np.mean((coherence >= 0.5) & (shuffled_burden >= 0.8) & (shuffled_mineral <= 0.2)))
        )
        failure_null.append(float(np.mean(np.clip(shuffled_burden, 0.0, 1.5) * (1.0 - shuffled_mineral))))

    return {
        "true_mean_coherent_bad_descendant_score": true_risk,
        "shuffle_mean_coherent_bad_descendant_score": float(statistics.fmean(risk_null)),
        "coherent_bad_descendant_p_value": p_value_greater(true_risk, risk_null),
        "true_bad_descendant_flag_fraction": true_flag,
        "shuffle_bad_descendant_flag_fraction": float(statistics.fmean(flag_null)),
        "bad_descendant_flag_p_value": p_value_greater(true_flag, flag_null),
        "true_mean_safety_failure_score": true_failure,
        "shuffle_mean_safety_failure_score": float(statistics.fmean(failure_null)),
        "safety_failure_p_value": p_value_greater(true_failure, failure_null),
        "permutations": permutations,
        "seed": seed,
    }


def write_outputs(rows: pd.DataFrame, controls: dict[str, object], out_dir: Path) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    row_path = out_dir / "nest2e_pfas_safety_logic_rows.csv"
    type_path = out_dir / "nest2e_pfas_safety_logic_by_reaction_type.csv"
    top_path = out_dir / "nest2e_pfas_safety_logic_top_bad_descendants.csv"
    json_path = out_dir / "nest2e_pfas_safety_logic_summary.json"
    report_path = out_dir / "nest2e_pfas_safety_logic_report.md"

    by_type = (
        rows.groupby("rxn_type", dropna=False)
        .agg(
            rows=("coherent_bad_descendant_score", "size"),
            mean_pathway_coherence=("pathway_coherence_score", "mean"),
            mean_retained_burden=("retained_burden_score", "mean"),
            mean_mineralization_quality=("mineralization_quality_proxy", "mean"),
            mean_coherent_bad_descendant=("coherent_bad_descendant_score", "mean"),
            bad_descendant_fraction=("bad_descendant_flag", "mean"),
            safety_candidate_fraction=("safety_candidate_flag", "mean"),
        )
        .sort_values(["bad_descendant_fraction", "mean_coherent_bad_descendant"], ascending=False)
        .reset_index()
    )
    top_bad = rows.sort_values(
        ["coherent_bad_descendant_score", "safety_failure_score"],
        ascending=False,
    ).head(25)

    rows.to_csv(row_path, index=False)
    by_type.to_csv(type_path, index=False)
    top_bad.to_csv(top_path, index=False)

    high_burden = float(rows["high_retained_burden_flag"].mean())
    low_mineral = float(rows["low_mineralization_flag"].mean())
    safety_candidate = float(rows["safety_candidate_flag"].mean())
    any_reduction = float(
        (
            (pd.to_numeric(rows["fluorine_delta"], errors="coerce").fillna(0.0) > 0)
            | (pd.to_numeric(rows["cf_bond_delta"], errors="coerce").fillna(0.0) > 0)
        ).mean()
    )
    status = (
        "pfas_bad_descendant_safety_logic_supported"
        if controls["coherent_bad_descendant_p_value"] <= 0.05
        and controls["bad_descendant_flag_p_value"] <= 0.05
        else "pfas_bad_descendant_safety_logic_measured"
    )
    clean_read = (
        "Nest 2E safety logic is supported: true PFAS pathways are coherent and "
        "preferentially produce coherent descendants that retain fluorination / C-F burden. "
        "The lane identifies bad descendants and separates transformation from safety."
        if status == "pfas_bad_descendant_safety_logic_supported"
        else "Nest 2E safety logic is measured but needs stronger controls before support."
    )
    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "rows": int(len(rows)),
        "high_retained_burden_fraction": high_burden,
        "low_mineralization_quality_fraction": low_mineral,
        "any_f_or_cf_reduction_fraction": any_reduction,
        "safety_candidate_fraction": safety_candidate,
        "mean_mineralization_quality_proxy": float(rows["mineralization_quality_proxy"].mean()),
        "mean_retained_burden_score": float(rows["retained_burden_score"].mean()),
        **controls,
        "clean_read": clean_read,
    }
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report_path.write_text(
        "\n".join(
            [
                "# Nest 2E PFAS Safety Logic Report",
                "",
                f"- `status`: `{status}`",
                f"- `rows`: `{summary['rows']}`",
                f"- `permutations`: `{summary['permutations']}`",
                "",
                "## Result",
                "",
                "| Metric | Value |",
                "| --- | ---: |",
                f"| Mean coherent bad-descendant score | {summary['true_mean_coherent_bad_descendant_score']:.6f} |",
                f"| Shuffled coherent bad-descendant score | {summary['shuffle_mean_coherent_bad_descendant_score']:.6f} |",
                f"| Coherent bad-descendant p-value | {summary['coherent_bad_descendant_p_value']:.6f} |",
                f"| Bad-descendant flag fraction | {summary['true_bad_descendant_flag_fraction']:.6f} |",
                f"| Shuffled bad-descendant flag fraction | {summary['shuffle_bad_descendant_flag_fraction']:.6f} |",
                f"| Bad-descendant flag p-value | {summary['bad_descendant_flag_p_value']:.6f} |",
                f"| Mean retained-burden score | {summary['mean_retained_burden_score']:.6f} |",
                f"| High retained-burden fraction | {summary['high_retained_burden_fraction']:.6f} |",
                f"| Mean mineralization-quality proxy | {summary['mean_mineralization_quality_proxy']:.6f} |",
                f"| Low mineralization-quality fraction | {summary['low_mineralization_quality_fraction']:.6f} |",
                f"| Rows with any F or C-F reduction | {summary['any_f_or_cf_reduction_fraction']:.6f} |",
                f"| Safety-candidate fraction | {summary['safety_candidate_fraction']:.6f} |",
                "",
                "## Clean Read",
                "",
                clean_read,
                "",
                "## Interpretation",
                "",
                "This is a safety triage layer. Parent disappearance is treated as insufficient safety evidence. "
                "The scorer checks whether the product remains a coherent, highly fluorinated descendant and "
                "therefore should stay flagged for downstream remediation or degradation scoring.",
                "",
                "## Artifacts",
                "",
                f"- row scores: `{row_path.relative_to(REPO_ROOT)}`",
                f"- by reaction type: `{type_path.relative_to(REPO_ROOT)}`",
                f"- top bad descendants: `{top_path.relative_to(REPO_ROOT)}`",
                f"- summary JSON: `{json_path.relative_to(REPO_ROOT)}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    parser.add_argument("--permutations", type=int, default=DEFAULT_PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    scored = pd.read_csv(args.input)
    rows = enrich_safety_rows(scored)
    controls = shuffled_controls(rows, args.permutations, args.seed)
    summary = write_outputs(rows, controls, Path(args.out_dir))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
