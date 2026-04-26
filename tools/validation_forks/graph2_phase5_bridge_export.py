#!/usr/bin/env python3
"""Export Phase 5 internal-bridge data as GRAPH-2 edge/label CSVs.

This is an internal AI bridge-graph validation surface. Edges are derived from
Phase 5 numeric anchor/readout features. Labels are the locked Phase 5 bridge
pairs from the context-to-readout read, not external chemistry/allostery labels.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from itertools import combinations
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = (
    REPO_ROOT
    / "artifacts"
    / "v8"
    / "phase5_internal_bridge"
    / "v8_phase5_internal_bridge_pack_data_2026-04-22.json"
)
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "graph2_phase5_bridge"
FEATURES = [
    "dominant_layer",
    "dominant_delta",
    "anchor_layer_span",
    "context_peak",
    "target_delta",
    "surround_peak",
    "last_delta",
    "target_to_context",
    "target_to_surround",
    "last_to_target",
    "target_layer",
    "last_layer",
    "overlap_count",
    "overlap_jaccard",
]
LOCKED_BRIDGE_PAIRS = {
    tuple(sorted(pair))
    for pair in [
        ("Mistral", "Hermes"),
        ("Qwen", "DeepSeek"),
        ("GLM", "Nemotron"),
    ]
}


def z_vectors(rows: list[dict]) -> dict[str, list[float]]:
    columns = {feature: [float(row.get(feature, 0.0)) for row in rows] for feature in FEATURES}
    means = {feature: sum(values) / len(values) for feature, values in columns.items()}
    stds = {
        feature: math.sqrt(sum((value - means[feature]) ** 2 for value in values) / len(values)) or 1.0
        for feature, values in columns.items()
    }
    return {
        row["display_name"]: [
            (float(row.get(feature, 0.0)) - means[feature]) / stds[feature]
            for feature in FEATURES
        ]
        for row in rows
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-json", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--k", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = json.loads(args.source_json.read_text(encoding="utf-8"))
    rows = data["models"]
    vectors = z_vectors(rows)
    names = list(vectors)
    edge_set: set[tuple[str, str]] = set()
    for source in names:
        neighbors = sorted(
            (
                math.dist(vectors[source], vectors[target]),
                target,
            )
            for target in names
            if target != source
        )[: args.k]
        for _, target in neighbors:
            edge_set.add(tuple(sorted((source, target))))
    edge_rows = [{"source": source, "target": target} for source, target in sorted(edge_set)]
    label_rows = []
    for source, target in combinations(names, 2):
        pair = tuple(sorted((source, target)))
        label_rows.append(
            {
                "source": source,
                "target": target,
                "label": 1 if pair in LOCKED_BRIDGE_PAIRS else 0,
                "label_source": "phase5_locked_context_to_readout_bridge_pairs",
            }
        )
    write_csv(args.out_dir / "graph2_phase5_bridge_edges.csv", edge_rows, ["source", "target"])
    write_csv(
        args.out_dir / "graph2_phase5_bridge_labels.csv",
        label_rows,
        ["source", "target", "label", "label_source"],
    )
    metadata = {
        "source_json": str(args.source_json.relative_to(REPO_ROOT)),
        "edge_rule": f"union k-nearest-neighbor graph over z-scored Phase 5 numeric bridge features, k={args.k}",
        "label_rule": "locked Phase 5 bridge pairs: Mistral/Hermes, Qwen/DeepSeek, GLM/Nemotron",
        "boundary": "internal AI bridge-graph pilot; not external molecular, allostery, grid, or chemistry validation",
        "edge_count": len(edge_rows),
        "label_count": len(label_rows),
        "positive_label_count": sum(int(row["label"]) for row in label_rows),
    }
    (args.out_dir / "graph2_phase5_bridge_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    print(f"Wrote {len(edge_rows)} edges and {len(label_rows)} labels to {args.out_dir}")


if __name__ == "__main__":
    main()
