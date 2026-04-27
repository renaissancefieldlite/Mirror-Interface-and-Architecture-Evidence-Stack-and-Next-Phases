#!/usr/bin/env python3
"""GRAPH-2 independent-label gate.

This gate does not score GRAPH-2 by itself. It checks whether a graph + label
pack is eligible for the existing pathway validator without pretending that
internally inferred labels are independent domain evidence.

Run with no inputs to write templates and a blocked report. That is the
correct state until real labels exist.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "graph2_independent_label_gate"

EDGE_FIELDS = ["source", "target", "edge_weight", "edge_type", "edge_source", "evidence_uri"]
LABEL_FIELDS = [
    "source",
    "target",
    "label",
    "label_class",
    "label_source",
    "label_method",
    "evidence_uri",
    "label_lock_date",
    "notes",
]
MANIFEST_TEMPLATE = {
    "status": "template_only",
    "graph_domain": "attention_flow | allostery | molecular_pathway | grid_flow | logistics | other",
    "edge_source": "Where the graph edges came from.",
    "label_source": "Where the positive/control pathway labels came from.",
    "label_independence_rule": "Labels must not be derived from the same mirror path score being tested.",
    "positive_label_rule": "What makes label=1.",
    "control_label_rule": "What makes label=0.",
    "locked_before_scoring": False,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv_header(path: Path, fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()


def write_report(out_dir: Path, report: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "graph2_independent_label_gate_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GRAPH-2 Independent Label Gate",
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
    if report.get("issues"):
        lines.extend(["", "## Issues", ""])
        for issue in report["issues"]:
            lines.append(f"- {issue}")
    lines.extend(["", "## Boundary", "", report["boundary"], ""])
    (out_dir / "graph2_independent_label_gate_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_templates(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv_header(out_dir / "graph2_edges_template.csv", EDGE_FIELDS)
    write_csv_header(out_dir / "graph2_labels_template.csv", LABEL_FIELDS)
    (out_dir / "graph2_manifest_template.json").write_text(
        json.dumps(MANIFEST_TEMPLATE, indent=2), encoding="utf-8"
    )


def validate_pack(edge_csv: Path, label_csv: Path) -> tuple[dict, list[str]]:
    edge_rows = read_csv(edge_csv)
    label_rows = read_csv(label_csv)
    issues: list[str] = []
    if not edge_rows:
        issues.append("edge CSV has no rows")
    if not label_rows:
        issues.append("label CSV has no rows")

    edge_nodes = set()
    for row in edge_rows:
        source = (row.get("source") or "").strip()
        target = (row.get("target") or "").strip()
        if source and target:
            edge_nodes.add(source)
            edge_nodes.add(target)

    positive = 0
    control = 0
    labels_with_evidence = 0
    labels_with_source = 0
    labels_missing_nodes = 0
    label_methods = set()
    label_sources = set()
    for row in label_rows:
        source = (row.get("source") or "").strip()
        target = (row.get("target") or "").strip()
        label_raw = (row.get("label") or "").strip()
        if source not in edge_nodes or target not in edge_nodes:
            labels_missing_nodes += 1
        if row.get("evidence_uri"):
            labels_with_evidence += 1
        if row.get("label_source"):
            labels_with_source += 1
            label_sources.add(row["label_source"].strip())
        if row.get("label_method"):
            label_methods.add(row["label_method"].strip())
        try:
            label = int(float(label_raw))
        except ValueError:
            issues.append(f"invalid label for pair {source}->{target}: {label_raw!r}")
            continue
        if label == 1:
            positive += 1
        elif label == 0:
            control += 1
        else:
            issues.append(f"label must be 0 or 1 for pair {source}->{target}")

    if labels_missing_nodes:
        issues.append(f"{labels_missing_nodes} label rows reference nodes missing from edge CSV")
    if positive < 10:
        issues.append("need at least 10 positive pathway labels")
    if control < 10:
        issues.append("need at least 10 control / negative pathway labels")
    if labels_with_evidence < len(label_rows):
        issues.append("every label row needs evidence_uri")
    if labels_with_source < len(label_rows):
        issues.append("every label row needs label_source")
    if not label_methods:
        issues.append("label_method is required so label independence can be audited")

    metrics = {
        "edge_rows": len(edge_rows),
        "edge_node_count": len(edge_nodes),
        "label_rows": len(label_rows),
        "positive_labels": positive,
        "control_labels": control,
        "labels_with_evidence_uri": labels_with_evidence,
        "unique_label_sources": len(label_sources),
        "unique_label_methods": len(label_methods),
    }
    return metrics, issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edge-csv", type=Path, help="Real GRAPH-2 edge CSV.")
    parser.add_argument("--label-csv", type=Path, help="Independent pathway/control label CSV.")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--write-templates", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requirements = [
        "real graph edge CSV with source,target columns",
        "independent pathway/control label CSV with label_source and evidence_uri",
        "at least 10 positive and 10 control pathway labels",
        "label_method declared before scoring",
        "labels not derived from the same mirror path score being tested",
    ]
    if args.write_templates or not args.edge_csv or not args.label_csv:
        write_templates(args.out_dir)
    if not args.edge_csv or not args.edge_csv.exists():
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_edge_csv",
                "read": "GRAPH-2 independent-label gate did not run because no real edge CSV was provided. Templates were written for the next data collection pass.",
                "requirements": requirements,
                "boundary": "No GRAPH-2 validation was performed.",
            },
        )
        print(f"Wrote blocked report and templates to {args.out_dir}")
        return
    if not args.label_csv or not args.label_csv.exists():
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_independent_label_csv",
                "read": "GRAPH-2 edges exist, but no independent pathway/control label CSV was provided.",
                "requirements": requirements,
                "boundary": "No GRAPH-2 validation was performed.",
            },
        )
        print(f"Wrote blocked report and templates to {args.out_dir}")
        return

    metrics, issues = validate_pack(args.edge_csv, args.label_csv)
    status = "eligible_for_graph12_pathway_validation" if not issues else "blocked_label_pack_not_eligible"
    read = (
        "GRAPH-2 label pack passed the independence gate and can be sent to graph12_pathway_validation.py."
        if not issues
        else "GRAPH-2 label pack was audited but is not eligible for validation yet."
    )
    write_report(
        args.out_dir,
        {
            "status": status,
            "read": read,
            "requirements": requirements,
            "metrics": metrics,
            "issues": issues,
            "boundary": "This gate audits label eligibility only; it does not score pathway recovery.",
        },
    )
    print(f"Wrote report to {args.out_dir}")


if __name__ == "__main__":
    main()
