#!/usr/bin/env python3
"""Extract the AlloBench 100-protein Jaccard benchmark table from the SI PDF.

This creates a real allostery benchmark surface, but it does not pretend to
validate the Mirror mapper yet. The next missing input is a residue/contact
graph plus known allosteric-site labels for scoring our own pathway graph.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF = ROOT / "artifacts" / "validation" / "datasets" / "allobench_si_001.pdf"
DEFAULT_ARTICLE = ROOT / "artifacts" / "validation" / "datasets" / "allobench_article.json"
DEFAULT_OUT = ROOT / "artifacts" / "validation" / "nest2d_allostery_benchmark"

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


def parse_number(token: str) -> float | None:
    token = token.replace("*", "").strip()
    if token.upper() == "FAILED":
        return None
    try:
        return float(token)
    except ValueError:
        return None


def extract_table(pdf_path: Path) -> pd.DataFrame:
    reader = PdfReader(str(pdf_path))
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    start = text.find("Table S3: Jaccard")
    end = text.find("Table S4:", start)
    if start == -1 or end == -1:
        raise RuntimeError("Could not locate Table S3 boundaries in AlloBench supplement.")
    section = text[start:end]
    matches = re.findall(
        r"(?:^|\s)(\d{1,3})\s+([0-9][A-Z0-9]{3})\s+(.+?)(?=\s+\d{1,3}\s+[0-9][A-Z0-9]{3}\s+|$)",
        section,
        flags=re.S,
    )
    rows: list[dict[str, object]] = []
    for index, pdb_id, rest in matches:
        values = rest.replace("\n", " ").split()
        values = values[: len(TOOLS)]
        if len(values) < len(TOOLS):
            values = values + ["FAILED"] * (len(TOOLS) - len(values))
        row: dict[str, object] = {"row": int(index), "pdb_id": pdb_id}
        for tool, token in zip(TOOLS, values, strict=True):
            row[tool] = parse_number(token)
            row[f"{tool}_raw"] = token
        rows.append(row)
    return pd.DataFrame(rows)


def write_report(df: pd.DataFrame, article_path: Path, out_dir: Path) -> None:
    article = json.loads(article_path.read_text(encoding="utf-8")) if article_path.exists() else {}
    numeric = df[TOOLS]
    tool_summary = pd.DataFrame(
        {
            "tool": TOOLS,
            "valid_rows": [int(numeric[t].notna().sum()) for t in TOOLS],
            "mean_jaccard": [float(numeric[t].mean(skipna=True)) for t in TOOLS],
            "fraction_positive": [float((numeric[t].fillna(0) > 0).mean()) for t in TOOLS],
            "fraction_ge_0_2": [float((numeric[t].fillna(0) >= 0.2).mean()) for t in TOOLS],
            "fraction_ge_0_5": [float((numeric[t].fillna(0) >= 0.5).mean()) for t in TOOLS],
        }
    ).sort_values("mean_jaccard", ascending=False)
    df.to_csv(out_dir / "nest2d_allobench_table_s3_extracted.csv", index=False)
    tool_summary.to_csv(out_dir / "nest2d_allobench_tool_summary.csv", index=False)
    status = "completed_real_allostery_benchmark_extracted_mapper_not_scored"
    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "article_title": article.get("title"),
        "article_doi": article.get("doi"),
        "rows_extracted": int(len(df)),
        "tool_count": len(TOOLS),
        "best_mean_jaccard_tool": str(tool_summary.iloc[0]["tool"]) if len(tool_summary) else None,
        "best_mean_jaccard": float(tool_summary.iloc[0]["mean_jaccard"]) if len(tool_summary) else None,
        "boundary": "benchmark surface extracted; Mirror mapper not yet scored because residue/contact graph labels are still needed",
    }
    (out_dir / "nest2d_allostery_benchmark_report.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Nest 2D Allostery Benchmark Extraction Report",
        "",
        f"Status: `{status}`",
        "",
        "## Inputs",
        "",
        "- Source: AlloBench supporting-information PDF",
        f"- Article: `{summary['article_title']}`",
        f"- DOI: `{summary['article_doi']}`",
        "- Extracted table: Table S3, topmost allosteric-site prediction Jaccard index",
        "",
        "## Result",
        "",
        f"- extracted PDB rows: `{len(df)}`",
        f"- prediction-tool columns: `{len(TOOLS)}`",
        f"- best mean Jaccard tool in extracted table: `{summary['best_mean_jaccard_tool']}`",
        f"- best mean Jaccard: `{summary['best_mean_jaccard']:.6f}`",
        "",
        "## Clean Read",
        "",
        "This is a real allostery benchmark surface, not a synthetic table.",
        "",
        "It does not yet validate the Mirror mapper because the current extracted",
        "table reports existing tool Jaccard scores. To score our own pathway",
        "mapper, the next input must be a residue/contact graph plus known",
        "allosteric-site residue labels or pocket membership labels.",
        "",
        "## Next Missing Input",
        "",
        "- protein contact graph or pocket graph per PDB row",
        "- known allosteric-site residue / pocket labels",
        "- mapper score for candidate communication path",
        "- controls against degree / centrality / shuffled-site labels",
        "",
    ]
    (out_dir / "nest2d_allostery_benchmark_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default=str(DEFAULT_PDF))
    parser.add_argument("--article", default=str(DEFAULT_ARTICLE))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = extract_table(Path(args.pdf))
    write_report(df, Path(args.article), out_dir)
    print(
        json.dumps(
            {
                "status": "ok",
                "rows": int(len(df)),
                "report": str(out_dir / "nest2d_allostery_benchmark_report.md"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
