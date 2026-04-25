#!/usr/bin/env python3
"""GRAPH-1/2 pathway validation fork.

This runner turns the graph-theory Nest 1 bridge into a falsifiable test:
given a real graph and known positive/negative pathway labels, compare a
mirror-style path-preservation score against a naive degree baseline.

Without real graph + label files it writes a blocked report. No toy rows.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict, deque
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "graph12_pathway"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_report(out_dir: Path, report: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "graph12_pathway_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    lines = [
        "# GRAPH-1/2 Pathway Validation Fork",
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
    (out_dir / "graph12_pathway_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def auc(scores: list[float], labels: list[int]) -> float:
    positives = [score for score, label in zip(scores, labels) if label == 1]
    negatives = [score for score, label in zip(scores, labels) if label == 0]
    if not positives or not negatives:
        return 0.0
    wins = 0.0
    total = len(positives) * len(negatives)
    for pos in positives:
        for neg in negatives:
            if pos > neg:
                wins += 1.0
            elif pos == neg:
                wins += 0.5
    return wins / total


def shortest_path_length(adjacency: dict[str, set[str]], source: str, target: str) -> int | None:
    if source == target:
        return 0
    seen = {source}
    queue: deque[tuple[str, int]] = deque([(source, 0)])
    while queue:
        node, distance = queue.popleft()
        for neighbor in adjacency.get(node, set()):
            if neighbor == target:
                return distance + 1
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, distance + 1))
    return None


def build_graph(edge_rows: list[dict[str, str]]) -> tuple[dict[str, set[str]], dict[str, int]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for row in edge_rows:
        source = row.get("source") or row.get("from") or row.get("node_a")
        target = row.get("target") or row.get("to") or row.get("node_b")
        if not source or not target:
            continue
        adjacency[source].add(target)
        adjacency[target].add(source)
    degrees = {node: len(neighbors) for node, neighbors in adjacency.items()}
    return adjacency, degrees


def score_pairs(
    adjacency: dict[str, set[str]],
    degrees: dict[str, int],
    label_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    rows = []
    max_degree = max(degrees.values()) if degrees else 1
    for row in label_rows:
        source = row.get("source") or row.get("from") or row.get("node_a")
        target = row.get("target") or row.get("to") or row.get("node_b")
        label_raw = row.get("label") or row.get("known_pathway") or row.get("positive")
        if not source or not target or label_raw is None:
            continue
        try:
            label = int(float(label_raw))
        except ValueError:
            continue
        path_length = shortest_path_length(adjacency, source, target)
        if path_length is None:
            mirror_score = 0.0
        else:
            mirror_score = 1.0 / (1.0 + path_length)
        degree_score = (degrees.get(source, 0) + degrees.get(target, 0)) / (2.0 * max_degree)
        rows.append(
            {
                "source": source,
                "target": target,
                "label": label,
                "path_length": path_length,
                "mirror_path_score": mirror_score,
                "degree_baseline_score": degree_score,
            }
        )
    return rows


def write_scored_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edge-csv", type=Path, help="CSV with source,target graph edges.")
    parser.add_argument(
        "--label-csv",
        type=Path,
        help="CSV with source,target,label rows where label is 1 for known pathway and 0 for control.",
    )
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requirements = [
        "real graph edge CSV with source,target columns",
        "known pathway/control label CSV with source,target,label columns",
        "declared baseline such as degree centrality or random labels",
    ]
    if not args.edge_csv or not args.edge_csv.exists():
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_edge_csv",
                "read": "No real graph edge file was provided, so GRAPH-1/2 did not run.",
                "requirements": requirements,
                "boundary": "No graph/allostery validation was performed.",
            },
        )
        print(f"Wrote blocked report to {args.out_dir}")
        return
    if not args.label_csv or not args.label_csv.exists():
        write_report(
            args.out_dir,
            {
                "status": "blocked_missing_label_csv",
                "read": "Graph edges were provided, but no real pathway/control labels were provided.",
                "requirements": requirements,
                "boundary": "No graph/allostery validation was performed.",
            },
        )
        print(f"Wrote blocked report to {args.out_dir}")
        return

    adjacency, degrees = build_graph(read_csv(args.edge_csv))
    scored = score_pairs(adjacency, degrees, read_csv(args.label_csv))
    labels = [int(row["label"]) for row in scored]
    mirror_scores = [float(row["mirror_path_score"]) for row in scored]
    degree_scores = [float(row["degree_baseline_score"]) for row in scored]
    metrics = {
        "node_count": len(adjacency),
        "edge_count": sum(len(neighbors) for neighbors in adjacency.values()) // 2,
        "labeled_pair_count": len(scored),
        "mirror_path_auc": round(auc(mirror_scores, labels), 4),
        "degree_baseline_auc": round(auc(degree_scores, labels), 4),
    }
    if len(scored) < 10 or len(set(labels)) < 2:
        status = "blocked_insufficient_labeled_pairs"
        read = "Graph files parsed, but there are not enough positive/control labels for a validation read."
    else:
        status = "completed"
        read = "GRAPH-1/2 pathway validation completed against the provided graph and labels."

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_scored_csv(args.out_dir / "graph12_pathway_scored_pairs.csv", scored)
    write_report(
        args.out_dir,
        {
            "status": status,
            "read": read,
            "requirements": requirements,
            "metrics": metrics,
            "boundary": "This validates graph pathway recovery only; it does not validate chemistry, biology, or allostery without domain-correct labels.",
        },
    )
    print(f"Wrote report to {args.out_dir}")


if __name__ == "__main__":
    main()
