#!/usr/bin/env python3
"""First local model engine for the Lattice Model Node Companion.

This engine is intentionally small and dependency-free. It demonstrates the
Nest 1 score grammar with linear algebra transforms:

state -> control -> transform -> invariant -> drift -> coherence -> score
"""

from __future__ import annotations

import json
import math
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
JSON_OUT = OUTPUT_DIR / "nest1_formal_engine_report.json"
MD_OUT = OUTPUT_DIR / "nest1_formal_engine_report.md"

VECTORS = {
    "axis_x": (1.0, 0.0),
    "axis_y": (0.0, 1.0),
    "diagonal": (1.0, 1.0),
}

TRANSFORMS = {
    "identity": ((1.0, 0.0), (0.0, 1.0)),
    "rotate_90": ((0.0, -1.0), (1.0, 0.0)),
    "reflect_x": ((1.0, 0.0), (0.0, -1.0)),
    "scale_control": ((1.35, 0.0), (0.0, 0.65)),
    "shear_control": ((1.0, 0.42), (0.0, 1.0)),
}


def matmul(matrix: tuple[tuple[float, float], tuple[float, float]], vector: tuple[float, float]) -> tuple[float, float]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]


def norm(vector: tuple[float, float]) -> float:
    return math.sqrt(dot(vector, vector))


def pairwise_dots(vectors: dict[str, tuple[float, float]]) -> dict[str, float]:
    names = list(vectors)
    values: dict[str, float] = {}
    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            values[f"{left}:{right}"] = dot(vectors[left], vectors[right])
    return values


def score_transform(name: str, matrix: tuple[tuple[float, float], tuple[float, float]]) -> dict:
    transformed = {label: matmul(matrix, vector) for label, vector in VECTORS.items()}
    base_norms = {label: norm(vector) for label, vector in VECTORS.items()}
    transformed_norms = {label: norm(vector) for label, vector in transformed.items()}
    base_dots = pairwise_dots(VECTORS)
    transformed_dots = pairwise_dots(transformed)

    norm_error = sum(abs(base_norms[label] - transformed_norms[label]) for label in VECTORS)
    dot_error = sum(abs(base_dots[label] - transformed_dots[label]) for label in base_dots)
    drift_penalty = norm_error + dot_error
    coherence = max(0.0, 1.0 - drift_penalty / 4.0)

    if coherence >= 0.95:
        read = "invariant-preserving"
    elif coherence >= 0.75:
        read = "mostly stable"
    else:
        read = "control drift"

    return {
        "transform": name,
        "matrix": matrix,
        "transformed_vectors": transformed,
        "norm_error": round(norm_error, 6),
        "dot_error": round(dot_error, 6),
        "drift_penalty": round(drift_penalty, 6),
        "coherence_score": round(coherence, 6),
        "read": read,
    }


def build_report() -> dict:
    rows = [score_transform(name, matrix) for name, matrix in TRANSFORMS.items()]
    return {
        "engine": "Engine 01: Nest 1 Formal Invariant Model",
        "schema": "state / control / transform / invariant / drift / coherence / score",
        "state": VECTORS,
        "invariants": ["norm", "pairwise dot product", "relative geometry"],
        "rows": rows,
        "claim_boundary": "Toy local model engine. Demonstrates the comparator grammar; it is not a physics or biology result.",
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Engine 01: Nest 1 Formal Invariant Model",
        "",
        f"Schema: `{report['schema']}`",
        "",
        "This is the first local model engine behind the Lattice Model Node Companion.",
        "It scores whether simple linear transforms preserve formal invariants.",
        "",
        "| Transform | Coherence Score | Drift Penalty | Read |",
        "| --- | ---: | ---: | --- |",
    ]
    for row in report["rows"]:
        lines.append(
            f"| `{row['transform']}` | {row['coherence_score']} | {row['drift_penalty']} | {row['read']} |"
        )
    lines.extend(
        [
            "",
            "Boundary:",
            "",
            report["claim_boundary"],
            "",
        ]
    )
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

