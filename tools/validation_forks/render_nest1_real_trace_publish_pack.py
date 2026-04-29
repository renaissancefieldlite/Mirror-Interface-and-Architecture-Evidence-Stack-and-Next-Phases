#!/usr/bin/env python3
"""Render the Nest 1 real-trace foundation visuals and PDF pack.

This script is intentionally downstream of `nest1_real_trace_foundation.py`.
It reads the generated real-data CSV/JSON outputs and renders charts plus a
compact PDF evidence pack. No synthetic rows are generated here.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("MPLCONFIGDIR", str(REPO_ROOT / ".matplotlib-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PACK_ROOT = REPO_ROOT / "artifacts" / "validation" / "nest1_real_trace_foundation"
CHART_ROOT = PACK_ROOT / "charts"
PDF_PATH = PACK_ROOT / "nest1_real_trace_foundation_pack_2026-04-25.pdf"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def f(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def save_fig(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()


def chart_pca(feature_rows: list[dict[str, str]]) -> Path:
    path = CHART_ROOT / "nest1_phase6_pca_geometry.png"
    xs = [f(row["pc1"]) for row in feature_rows]
    ys = [f(row["pc2"]) for row in feature_rows]
    labels = [row["model"] for row in feature_rows]

    plt.figure(figsize=(7.5, 5.5))
    plt.scatter(xs, ys, s=95, c="#1f77b4", edgecolor="#0b1720", linewidth=0.8)
    for x, y, label in zip(xs, ys, labels, strict=True):
        plt.annotate(label, (x, y), xytext=(6, 5), textcoords="offset points", fontsize=9)
    plt.axhline(0, color="#d0d7de", linewidth=0.8)
    plt.axvline(0, color="#d0d7de", linewidth=0.8)
    plt.title("Nest 1 Phase 6 Feature Geometry: PCA Projection")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    save_fig(path)
    return path


def chart_bridge_pairs(report: dict[str, Any]) -> Path:
    path = CHART_ROOT / "nest1_expected_bridge_pair_distances.png"
    rows = report["bridge_pair_checks"]
    labels = [row["pair"] for row in rows]
    distances = [f(row.get("distance")) for row in rows]
    colors_ = ["#2ca02c" if row.get("mutual_nearest") else "#d62728" for row in rows]

    plt.figure(figsize=(7.5, 4.8))
    bars = plt.bar(labels, distances, color=colors_, alpha=0.86)
    plt.title("Expected Bridge Pair Recovery Over Real Feature Geometry")
    plt.ylabel("Z-scored feature distance")
    plt.xticks(rotation=12, ha="right")
    for bar, row in zip(bars, rows, strict=True):
        label = "mutual nearest" if row.get("mutual_nearest") else "not recovered"
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label, ha="center", va="bottom", fontsize=8)
    save_fig(path)
    return path


def chart_topography(topography_rows: list[dict[str, str]]) -> Path:
    path = CHART_ROOT / "nest1_phase5_anchor_topography.png"
    anchors: dict[str, int] = {}
    for row in topography_rows:
        anchors[row["dominant_anchor"]] = anchors.get(row["dominant_anchor"], 0) + 1

    labels = list(anchors)
    counts = [anchors[label] for label in labels]
    plt.figure(figsize=(7.5, 4.8))
    plt.bar(labels, counts, color=["#17becf", "#ff7f0e", "#9467bd"][: len(labels)])
    plt.title("Phase 5 Internal Topography: Dominant Anchor Counts")
    plt.ylabel("Model count")
    plt.xlabel("Dominant anchor")
    for i, count in enumerate(counts):
        plt.text(i, count, str(count), ha="center", va="bottom", fontsize=10)
    save_fig(path)
    return path


def chart_dynamics(layer_rows: list[dict[str, str]]) -> Path:
    path = CHART_ROOT / "nest1_layer_dynamics_peaks.png"
    rows = sorted(layer_rows, key=lambda row: f(row["target_peak_layer_fraction"]))
    labels = [row["model"] for row in rows]
    fractions = [f(row["target_peak_layer_fraction"]) for row in rows]
    peaks = [f(row["target_peak_value"]) for row in rows]

    x = np.arange(len(labels))
    fig, ax1 = plt.subplots(figsize=(8.5, 5.2))
    ax1.bar(x, fractions, color="#1f77b4", alpha=0.82)
    ax1.set_ylabel("Peak layer fraction")
    ax1.set_ylim(0, 1.08)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=35, ha="right")
    ax2 = ax1.twinx()
    ax2.plot(x, peaks, color="#d62728", marker="o", linewidth=1.8)
    ax2.set_ylabel("Target peak delta")
    plt.title("V8 Residual Dynamics: Target Peak Layer Position and Magnitude")
    fig.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()
    return path


def chart_hardware(hardware_rows: list[dict[str, str]]) -> Path:
    path = CHART_ROOT / "nest1_phase9d_hardware_sign_stability.png"
    labels = [row["circuit"] for row in hardware_rows]
    means = [f(row["mean_parity"]) for row in hardware_rows]
    stds = [f(row["std_parity"]) for row in hardware_rows]
    colors_ = ["#2ca02c" if row["sign_stable"] == "True" else "#d62728" for row in hardware_rows]

    plt.figure(figsize=(9, 5.2))
    plt.bar(labels, means, yerr=stds, capsize=4, color=colors_, alpha=0.86)
    plt.axhline(0, color="#202428", linewidth=1.0)
    plt.title("Phase 9D Real Hardware: Parity Sign Stability")
    plt.ylabel("Mean parity expectation +/- std")
    plt.xticks(rotation=35, ha="right")
    save_fig(path)
    return path


def relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def build_pdf(report: dict[str, Any], chart_paths: list[Path]) -> None:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0b1720"),
            fontSize=20,
            leading=24,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallNote",
            parent=styles["BodyText"],
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#39424e"),
        )
    )

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )
    story: list[Any] = []
    story.append(Paragraph("Nest 1 Real-Trace Foundation Evidence Pack", styles["TitleCenter"]))
    story.append(Paragraph("Generated from real exported AI and hardware artifacts. No synthetic rows are used in this pack.", styles["BodyText"]))
    story.append(Spacer(1, 0.14 * inch))

    branch_table = [["Branch", "Status", "Key read"]]
    for item in report["branch_results"]:
        branch_table.append(
            [
                item["branch"],
                item["status"],
                item["read"],
            ]
        )
    table = Table(branch_table, colWidths=[1.45 * inch, 1.35 * inch, 4.5 * inch], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b1720")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d0d7de")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.6),
                ("LEADING", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7f9fb")),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.16 * inch))

    summary = (
        "Clean read: Nest 1 now has a real foundation pass over the existing "
        "AI/hardware stack. Linear algebra/geometry, tensor/information, "
        "statistics/probability, topography, layer dynamics, and hardware "
        "sign stability are grounded in real artifacts. Optimization, control, "
        "deeper topology, and composition remain explicit next-runner lanes."
    )
    story.append(Paragraph(summary, styles["BodyText"]))
    story.append(Spacer(1, 0.12 * inch))
    story.append(Paragraph(report["boundary"], styles["SmallNote"]))

    for chart in chart_paths:
        story.append(Spacer(1, 0.18 * inch))
        story.append(Image(str(chart), width=6.6 * inch, height=4.1 * inch, kind="proportional"))

    doc.build(story)


def patch_markdown(report_path: Path, chart_paths: list[Path]) -> None:
    text = report_path.read_text(encoding="utf-8")
    marker = "## Visual Evidence Pack"
    visual_section = [
        marker,
        "",
        f"- PDF pack: [`{PDF_PATH.name}`](./{PDF_PATH.name})",
    ]
    for chart in chart_paths:
        visual_section.append(f"- Chart: [`{chart.name}`](./charts/{chart.name})")
    visual_section.extend(["", ""])

    if marker in text:
        before = text.split(marker, 1)[0].rstrip()
        boundary = "## Boundary" + text.split("## Boundary", 1)[1]
        text = before + "\n\n" + "\n".join(visual_section) + boundary
    else:
        text = text.replace("## Boundary\n", "\n".join(visual_section) + "## Boundary\n")
    report_path.write_text(text, encoding="utf-8")


def main() -> None:
    CHART_ROOT.mkdir(parents=True, exist_ok=True)
    report = read_json(PACK_ROOT / "nest1_real_trace_foundation_report.json")
    feature_rows = read_csv(PACK_ROOT / "nest1_real_trace_feature_matrix.csv")
    topography = read_csv(PACK_ROOT / "nest1_real_trace_topography_bridge.csv")
    dynamics = read_csv(PACK_ROOT / "nest1_real_trace_layer_dynamics.csv")
    hardware = read_csv(PACK_ROOT / "nest1_real_trace_hardware_signs.csv")

    charts = [
        chart_pca(feature_rows),
        chart_bridge_pairs(report),
        chart_topography(topography),
        chart_dynamics(dynamics),
        chart_hardware(hardware),
    ]
    build_pdf(report, charts)
    patch_markdown(PACK_ROOT / "nest1_real_trace_foundation_report.md", charts)

    result = {
        "status": "rendered",
        "pdf": relative(PDF_PATH),
        "charts": [relative(chart) for chart in charts],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
