#!/usr/bin/env python3
"""Nest 2D allostery label/readiness bridge.

The current Nest 2D artifact has a real AlloBench Jaccard benchmark table.
This gate turns that extraction into a concrete scoring bridge: it reports the
measurement surface available now and writes the exact residue/contact label
manifest required before the Mirror mapper scoring pass.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TABLE = (
    ROOT
    / "artifacts"
    / "validation"
    / "nest2d_allostery_benchmark"
    / "nest2d_allobench_table_s3_extracted.csv"
)
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "nest2d_allostery_label_bridge"
TOOLS = [
    "APOP",
    "PASSer_Rank",
    "PASSer_AutoML",
    "PASSer_Ensemble",
    "Ohm",
    "ALLO",
    "AllositePro",
    "STRESS",
    "AlloPred",
    "Allosite",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Nest 2D allostery label bridge/readiness report.")
    parser.add_argument("--table", default=str(DEFAULT_TABLE))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    return parser.parse_args()


def require_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"AlloBench extracted table missing: {path}")
    df = pd.read_csv(path)
    required = {"row", "pdb_id", *TOOLS}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"AlloBench table missing columns: {sorted(missing)}")
    return df


def summarize(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    numeric = df[TOOLS].copy()
    best_tool = numeric.idxmax(axis=1)
    best_jaccard = numeric.max(axis=1, skipna=True)
    tool_summary = []
    for tool in TOOLS:
        values = pd.to_numeric(numeric[tool], errors="coerce")
        tool_summary.append(
            {
                "tool": tool,
                "valid_rows": int(values.notna().sum()),
                "mean_jaccard": float(values.mean(skipna=True)),
                "median_jaccard": float(values.median(skipna=True)),
                "fraction_positive": float((values.fillna(0.0) > 0.0).mean()),
                "fraction_ge_0_2": float((values.fillna(0.0) >= 0.2).mean()),
                "fraction_ge_0_5": float((values.fillna(0.0) >= 0.5).mean()),
            }
        )
    summary_df = pd.DataFrame(tool_summary).sort_values("mean_jaccard", ascending=False)
    row_summary = pd.DataFrame(
        {
            "row": df["row"],
            "pdb_id": df["pdb_id"],
            "best_tool": best_tool,
            "best_jaccard": best_jaccard,
            "tool_mean_jaccard": numeric.mean(axis=1, skipna=True),
            "tool_positive_count": (numeric.fillna(0.0) > 0.0).sum(axis=1),
            "tool_ge_0_2_count": (numeric.fillna(0.0) >= 0.2).sum(axis=1),
            "tool_ge_0_5_count": (numeric.fillna(0.0) >= 0.5).sum(axis=1),
        }
    )
    stats = {
        "rows": int(len(df)),
        "tool_count": len(TOOLS),
        "best_mean_tool": str(summary_df.iloc[0]["tool"]),
        "best_mean_jaccard": round(float(summary_df.iloc[0]["mean_jaccard"]), 9),
        "median_best_jaccard": round(float(best_jaccard.median(skipna=True)), 9),
        "mean_best_jaccard": round(float(best_jaccard.mean(skipna=True)), 9),
        "rows_any_tool_ge_0_2": int((best_jaccard.fillna(0.0) >= 0.2).sum()),
        "rows_any_tool_ge_0_5": int((best_jaccard.fillna(0.0) >= 0.5).sum()),
        "rows_all_tools_zero_or_failed": int((numeric.fillna(0.0).max(axis=1) == 0.0).sum()),
        "mean_tool_pair_correlation": round(float(numeric.corr().where(~np.eye(len(TOOLS), dtype=bool)).stack().mean()), 9),
    }
    return row_summary, {"tool_summary": summary_df, "stats": stats}


def write_template(out_dir: Path, pdb_ids: list[str]) -> Path:
    template = pd.DataFrame(
        {
            "pdb_id": pdb_ids,
            "protein_structure_uri": "",
            "contact_graph_uri": "",
            "pocket_graph_uri": "",
            "known_allosteric_residue_labels_uri": "",
            "known_active_site_residue_labels_uri": "",
            "candidate_mapper_score_uri": "",
            "label_source": "AlloBench/ASD/PDB/UniProt/M-CSA residue-synchronized labels",
            "evidence_uri": "",
            "ready_for_mapper_scoring": False,
        }
    )
    path = out_dir / "nest2d_allostery_label_manifest_template.csv"
    template.to_csv(path, index=False)
    return path


def write_outputs(df: pd.DataFrame, row_summary: pd.DataFrame, summary: dict[str, Any], out_dir: Path, table_path: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    tool_summary = summary["tool_summary"]
    stats = summary["stats"]
    row_summary_path = out_dir / "nest2d_allobench_proxy_row_summary.csv"
    tool_summary_path = out_dir / "nest2d_allobench_proxy_tool_summary.csv"
    manifest_path = write_template(out_dir, [str(x) for x in df["pdb_id"].tolist()])
    row_summary.to_csv(row_summary_path, index=False)
    tool_summary.to_csv(tool_summary_path, index=False)

    status = "allostery_label_bridge_ready_mapper_awaiting_contact_pocket_labels"
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "input_table": str(table_path),
        "proxy_row_summary": str(row_summary_path),
        "proxy_tool_summary": str(tool_summary_path),
        "label_manifest_template": str(manifest_path),
        "stats": stats,
        "available_now": [
            "100 real PDB benchmark rows",
            "10 existing allosteric-site prediction tool Jaccard columns",
            "per-row benchmark difficulty and tool consensus summaries",
        ],
        "required_before_mapper_scoring": [
            "protein contact graph or pocket graph per PDB row",
            "known allosteric-site residue or pocket labels",
            "known active-site residue labels when pathway direction is scored",
            "candidate Mirror mapper path or pocket score for the same graph units",
            "degree/centrality/shuffled-site controls",
        ],
        "clean_read": (
            "Nest 2D has a real AlloBench benchmark surface and a concrete label manifest. "
            "The current local data supports benchmark readiness and baseline characterization; "
            "Mirror mapper validation is the next pass once residue/contact/pocket labels are attached."
        ),
    }
    (out_dir / "nest2d_allostery_label_bridge_report.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Nest 2D Allostery Label Bridge Report",
        "",
        f"Status: `{status}`",
        "",
        "## What Ran",
        "",
        "This pass reads the extracted AlloBench Table S3 benchmark and converts it",
        "into a mapper-readiness bridge. The Mirror mapper scoring pass starts",
        "once the contact / pocket / residue-label handoff is attached.",
        "",
        "## Benchmark Surface",
        "",
        f"- real PDB benchmark rows: `{stats['rows']}`",
        f"- allosteric-site prediction tool columns: `{stats['tool_count']}`",
        f"- best mean Jaccard tool: `{stats['best_mean_tool']}`",
        f"- best mean Jaccard: `{stats['best_mean_jaccard']}`",
        f"- mean best-per-protein Jaccard: `{stats['mean_best_jaccard']}`",
        f"- median best-per-protein Jaccard: `{stats['median_best_jaccard']}`",
        f"- rows with any tool >= 0.2 Jaccard: `{stats['rows_any_tool_ge_0_2']}`",
        f"- rows with any tool >= 0.5 Jaccard: `{stats['rows_any_tool_ge_0_5']}`",
        f"- rows where all tools are zero / failed: `{stats['rows_all_tools_zero_or_failed']}`",
        f"- mean pairwise tool-score correlation: `{stats['mean_tool_pair_correlation']}`",
        "",
        "## Why This Matters",
        "",
        "Allostery is the first Nest 2 lane where the mapper needs real biological",
        "graph structure alongside molecule descriptors. The extracted table proves",
        "we have a real benchmark family and exposes the baseline difficulty: even",
        "the best existing table-level mean Jaccard is low, so a future path mapper",
        "must be scored carefully against degree, centrality, and shuffled-site",
        "controls.",
        "",
        "## Available Now",
        "",
        "- PDB IDs for the `100` AlloBench test proteins",
        "- existing tool Jaccard scores against known allosteric sites",
        "- per-row difficulty summaries and best-tool baselines",
        "- a label manifest template for the next contact / pocket graph handoff",
        "",
        "## Required Before Mapper Validation",
        "",
        "- protein structure file per PDB row",
        "- contact graph or pocket graph per PDB row",
        "- known allosteric-site residue / pocket labels",
        "- known active-site residue labels for communication-path direction",
        "- Mirror mapper candidate path / pocket score on the same graph units",
        "- controls against degree, centrality, shuffled-site labels, and random pockets",
        "",
        "## Combined Closeout Design",
        "",
        "The next Nest 2D mapper run uses the same `100` PDB rows and compares:",
        "",
        "- Mirror mapper candidate path / pocket score",
        "- existing AlloBench tools: `APOP`, `PASSer_Rank`, `PASSer_AutoML`,",
        "  `PASSer_Ensemble`, `Ohm`, `ALLO`, `AllositePro`, `STRESS`,",
        "  `AlloPred`, and `Allosite`",
        "- added pocket tools where available: `fpocket`, `P2Rank`, and `PrankWeb`",
        "- graph-naive controls: degree, centrality, shortest active-site path,",
        "  random pocket, and shuffled allosteric labels",
        "",
        "Closeout target:",
        "",
        "```text",
        "Mirror mapper > PASSer_Ensemble mean Jaccard baseline",
        "and",
        "Mirror mapper > graph-naive controls",
        "and",
        "repeat holds on a second seed / split or second allostery benchmark",
        "```",
        "",
        "## Clean Read",
        "",
        report["clean_read"],
        "",
        "## Outputs",
        "",
        f"- row summary: `{row_summary_path}`",
        f"- tool summary: `{tool_summary_path}`",
        f"- label manifest template: `{manifest_path}`",
        "",
    ]
    (out_dir / "nest2d_allostery_label_bridge_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    table_path = Path(args.table).resolve()
    out_dir = Path(args.out_dir).resolve()
    df = require_table(table_path)
    row_summary, summary = summarize(df)
    write_outputs(df, row_summary, summary, out_dir, table_path)
    print(
        json.dumps(
            {
                "status": "ok",
                "report": str(out_dir / "nest2d_allostery_label_bridge_report.md"),
                "rows": int(len(df)),
                "best_mean_tool": summary["stats"]["best_mean_tool"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
