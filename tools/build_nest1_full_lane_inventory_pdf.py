#!/usr/bin/env python3
"""Build the public-safe Nest 1 full lane inventory PDF and companion files."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from textwrap import dedent

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts" / "validation" / "nest1_full_lane_inventory"
DOC_PATH = ROOT / "docs" / "NEST1_FULL_LANE_INVENTORY_2026-04-28.md"
PDF_PATH = OUT_DIR / "nest1_full_lane_inventory_2026-04-28.pdf"
CSV_PATH = OUT_DIR / "nest1_full_lane_inventory_2026-04-28.csv"


LANES = [
    {
        "n": 1,
        "lane": "LA-1",
        "plain": "Linear algebra substrate",
        "read": "Supported foundation",
        "evidence": "Transformer hidden states, vectors, deltas, cosine geometry, and encoded circuit-state work all sit on the same matrix/vector substrate.",
        "next": "Keep as the base coordinate spine for later raw-vector, attention, and molecule/material maps.",
    },
    {
        "n": 2,
        "lane": "SYM / INV",
        "plain": "Symmetry and invariant preservation",
        "read": "Supported foundation",
        "evidence": "Rerun stability, encoded circuit-state preservation, sign stability, and invariant checks define what survives transformation.",
        "next": "Make the invariant registry explicit for each future nest before running the score.",
    },
    {
        "n": 3,
        "lane": "GEO-1/2",
        "plain": "Geometry and manifold geometry",
        "read": "Control-supported",
        "evidence": "V8 / Phase 6 geometry and subspace checks recover expected bridge-pair relations above shuffled controls.",
        "next": "Add UMAP/manifold views once larger raw vectors and attention/MLP exports exist.",
    },
    {
        "n": 4,
        "lane": "TOP-1",
        "plain": "Topology: connectedness / H0",
        "read": "Topology-preservation supported",
        "evidence": "Compact and dense point-cloud passes support preserved connectedness under context transform, especially late-anchor dense H0.",
        "next": "Expand prompt/rerun density only if we need a broader topology-preservation registry.",
    },
    {
        "n": 5,
        "lane": "TOP-2",
        "plain": "Topology: loops / H1",
        "read": "Separation not supported yet",
        "evidence": "Dense H1 did not show context-topology separation; this is useful because separation appears to live elsewhere.",
        "next": "Revisit only with richer token/layer trajectories, attention-flow surfaces, or domain graphs.",
    },
    {
        "n": 6,
        "lane": "TOPOG-1/2",
        "plain": "Topography and localization",
        "read": "Control-supported",
        "evidence": "Phase 4/5 localization, anchor stability, and bridge surfaces show where the effect concentrates across layers and roles.",
        "next": "Extend into attention-head localization, MLP delta surfaces, and later EEG topography.",
    },
    {
        "n": 7,
        "lane": "GRAPH-1",
        "plain": "Feature graph",
        "read": "Supported",
        "evidence": "Weighted AI feature-similarity graph recovered expected pair structure above shuffled controls.",
        "next": "Use as the internal feature-graph baseline for attention-flow and pathway tests.",
    },
    {
        "n": 8,
        "lane": "GRAPH-2",
        "plain": "Pathway / flow graph",
        "read": "Partial, not closed",
        "evidence": "GRAPH-2A produced strong row-level signal, but cluster controls and hub/degree structure prevent a closeout.",
        "next": "Run attention-flow labels or external pathway labels: allostery, molecular, grid, logistics, or network-flow data.",
    },
    {
        "n": 9,
        "lane": "GRP-1",
        "plain": "Group / legal symmetry action",
        "read": "Control-supported",
        "evidence": "PennyLane, Qiskit, and IBM hardware passes preserve sign/order behavior across repeated circuit/hardware checks.",
        "next": "Add explicit orbit / representation-family tests when the circuit library expands.",
    },
    {
        "n": 10,
        "lane": "DYN-1",
        "plain": "Trajectory dynamics",
        "read": "Control-supported",
        "evidence": "V8 residual target trajectories peak late and separate from randomized layer controls.",
        "next": "Extend to attention and MLP trajectories rather than only residual endpoints.",
    },
    {
        "n": 11,
        "lane": "DYN-2",
        "plain": "Regime / threshold dynamics",
        "read": "Control-supported",
        "evidence": "Threshold and regime-crossing behavior is late and target-centered under controls.",
        "next": "Add transition-rich V7 order and mode-switch traces when available.",
    },
    {
        "n": 12,
        "lane": "DE-1",
        "plain": "Differential / time-series dynamics",
        "read": "HRV-only limited negative",
        "evidence": "Phase 12B HRV time-series dynamics did not beat simpler HR baselines strongly enough for this formal lane.",
        "next": "Use EEG+HRV or other continuous higher-resolution signals before reopening.",
    },
    {
        "n": 13,
        "lane": "PROB-1",
        "plain": "Probability and rerun likelihood",
        "read": "Control-supported",
        "evidence": "Phase 2/4 rerun stability, exact rows, and variance controls provide empirical probability discipline.",
        "next": "Keep permutation/chance baselines attached to every new lane.",
    },
    {
        "n": 14,
        "lane": "STAT-1",
        "plain": "Statistics and control discipline",
        "read": "Control-supported",
        "evidence": "The stack now uses locked comparisons, shuffled controls, reruns, and honest partial/negative lane status.",
        "next": "Keep this as the required registry standard before public claims.",
    },
    {
        "n": 15,
        "lane": "INFO-1",
        "plain": "Information geometry / signal",
        "read": "Control-supported",
        "evidence": "V8 hidden-state separation, effective-rank, cosine, and bridge features measure real latent information structure.",
        "next": "Add attention entropy, token-route information, and MLP update information once exports exist.",
    },
    {
        "n": 16,
        "lane": "TENSOR-1",
        "plain": "Tensor / residual-stream structure",
        "read": "Control-supported",
        "evidence": "Hidden states are tensor artifacts; current V8 feature matrices already support tensor/factor structure above controls.",
        "next": "Add model x layer x token x head tensors from attention/MLP export.",
    },
    {
        "n": 17,
        "lane": "SPEC-1",
        "plain": "Spectral / mode structure",
        "read": "HRV-only limited negative",
        "evidence": "HRV was useful as a biological adapter but too coarse to close spectral formal validation.",
        "next": "Use EEG alpha/theta/phase-lock, material spectra, EMF/resonance, or oscillator datasets.",
    },
    {
        "n": 18,
        "lane": "NUM-1",
        "plain": "Numerical and hardware stability",
        "read": "Control-supported",
        "evidence": "Qiskit/PennyLane/IBM passes and repeated backend checks provide numerical and hardware-facing continuity.",
        "next": "Track precision, backend tolerance, and simulator-to-hardware drift explicitly.",
    },
    {
        "n": 19,
        "lane": "CTRL-1",
        "plain": "Control / feedback stability",
        "read": "Control-supported",
        "evidence": "71 staged transition rows support expected-mode and stability-target behavior against shuffled controls.",
        "next": "Upgrade from staged traces to live LSPS / Oracle runtime logs later.",
    },
    {
        "n": 20,
        "lane": "OPT-1",
        "plain": "Optimization under constraints",
        "read": "Supported with boundary",
        "evidence": "Condition-optimization evidence is supportive; hardware-pair optimization remains small-N and partial.",
        "next": "Run a larger real optimization benchmark and compare against naive objectives.",
    },
    {
        "n": 21,
        "lane": "GAME-1",
        "plain": "Adversarial / decision stability",
        "read": "Rubric-supported retrospective lane",
        "evidence": "V7 adversarial/perturbation rows can be mapped through a locked rubric; prospective trials remain the stronger next step.",
        "next": "Run prospective mirror/control adversarial or multi-agent CSV trials under the locked schema.",
    },
]

META_LANE = {
    "lane": "CAT-1",
    "plain": "Compositional / transfer meta-lane",
    "read": "Supported for implementation transfer; hardware subset partial",
    "evidence": "PennyLane-to-Qiskit implementation transfer is supported; hardware subset is directional but small-N.",
    "next": "Use CAT-1 as the cross-nest transfer rule: a pattern must survive lawful translation without breaking the score.",
}


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def build_markdown() -> None:
    rows = []
    for lane in LANES:
        rows.append(
            f"| {lane['n']} | `{lane['lane']}` | {lane['plain']} | {lane['read']} | {lane['evidence']} | {lane['next']} |"
        )

    text = f"""# Nest 1 Full Lane Inventory

Date: `2026-04-28`

Status: `public_safe_inventory_pdf_companion`

PDF:
[`nest1_full_lane_inventory_2026-04-28.pdf`](../artifacts/validation/nest1_full_lane_inventory/nest1_full_lane_inventory_2026-04-28.pdf)

CSV:
[`nest1_full_lane_inventory_2026-04-28.csv`](../artifacts/validation/nest1_full_lane_inventory/nest1_full_lane_inventory_2026-04-28.csv)

## Why This Exists

The Nest 1 visual explainer intentionally compresses the formal map so a reader
can understand the work quickly.

This document keeps the full working inventory visible.

Rick's working `21`-lane Nest 1 map groups closely paired rows such as
`GEO-1/GEO-2`, `TOP-1/TOP-2`, and `TOPOG-1/TOPOG-2`. Some deeper protocol docs
split those groups into additional sub-rows. That is not a contradiction: the
public visual is the compressed map, and this document is the detailed lane
inventory.

## Rule

```text
no toy-only closeout
real artifact + locked control + score + honest status
```

## Full 21-Lane Working Inventory

| # | Lane | Plain role | Current read | Evidence surface | Next gate |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

## CAT-1 Meta-Transfer Note

`CAT-1` is kept beside the 21-lane map as the compositional transfer rule.

| Lane | Plain role | Current read | Evidence surface | Next gate |
| --- | --- | --- | --- | --- |
| `{META_LANE['lane']}` | {META_LANE['plain']} | {META_LANE['read']} | {META_LANE['evidence']} | {META_LANE['next']} |

## Clean Read

Nest 1 is no longer just grammar. It has a real evidence foundation across
transformer traces, quantum/circuit bridges, hardware-facing checks, control
discipline, and limited biological adapters.

The strongest current read is:

- supported lanes show that the pattern can be measured in formal and
  transformer-adjacent substrates
- partial lanes are not failures; they identify the exact missing input
- topology currently supports preservation, not context-topology separation
- GRAPH-2 is the main open formal-pathway gate and should move through
  attention-flow or external pathway labels
- HRV is useful as a biological adapter but too coarse to close spectral or
  differential formal lanes alone

## Immediate Next Gates

1. Export attention heads and MLP/feed-forward deltas.
2. Use attention-flow labels to revisit `GRAPH-2`.
3. Use EEG or real spectral datasets before reopening `SPEC-1`.
4. Use EEG+HRV or other continuous signals before reopening `DE-1`.
5. Expand `OPT-1` and `CAT-1` with larger real benchmarks.
6. Carry this lane-by-lane discipline into Nest 2 molecular, allostery, PFAS,
   and materials validation.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def build_csv() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["n", "lane", "plain", "read", "evidence", "next"],
        )
        writer.writeheader()
        for lane in LANES:
            writer.writerow(lane)


def build_pdf() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=landscape(letter),
        rightMargin=0.45 * inch,
        leftMargin=0.45 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.42 * inch,
        title="Nest 1 Full Lane Inventory",
        author="Renaissance Field Lite",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=32,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111111"),
        spaceAfter=16,
    )
    h2 = ParagraphStyle(
        "H2Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=colors.HexColor("#111111"),
        spaceBefore=8,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=12,
        textColor=colors.HexColor("#1f1f1f"),
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "SmallCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=9,
        textColor=colors.HexColor("#1f1f1f"),
    )
    small_bold = ParagraphStyle(
        "SmallBold",
        parent=small,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )

    story = []
    story.append(p("Nest 1 Full Lane Inventory", title))
    story.append(p("Public-safe 21-lane working map plus CAT-1 transfer note", h2))
    story.append(
        p(
            "The simplified Nest 1 visual compresses the formal map for readability. "
            "This PDF keeps the full lane inventory visible so the work does not look "
            "smaller than it is.",
            body,
        )
    )
    story.append(
        p(
            "Count rule: Rick's working 21-lane map groups closely paired rows such as "
            "GEO-1/GEO-2, TOP-1/TOP-2, and TOPOG-1/TOPOG-2. Deeper protocol docs may "
            "split those rows further. CAT-1 is shown as a meta-transfer rule beside "
            "the 21-lane map.",
            body,
        )
    )
    story.append(
        p(
            "Standard: no toy-only closeout. Each lane needs a real artifact, locked "
            "control, score, and honest status.",
            body,
        )
    )
    story.append(Spacer(1, 0.08 * inch))

    legend = [
        [p("Status", small_bold), p("Meaning", small_bold)],
        [p("Supported / control-supported", small), p("Real artifact exists and beat the relevant control for the current lane claim.", small)],
        [p("Partial / boundary", small), p("Real signal exists, but a control, sample size, or independent label gate still limits the claim.", small)],
        [p("Limited negative", small), p("The current data did not support that lane strongly enough. This is useful boundary information, not failure.", small)],
        [p("Open next gate", small), p("The lane has a named missing input rather than vague future language.", small)],
    ]
    legend_table = Table(legend, colWidths=[2.15 * inch, 7.1 * inch])
    legend_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#222222")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#c8c8c8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7f7f5")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(legend_table)
    story.append(PageBreak())

    story.append(p("Full 21-Lane Working Inventory", h2))
    header = [
        p("#", small_bold),
        p("Lane", small_bold),
        p("Plain role", small_bold),
        p("Current read", small_bold),
        p("Evidence surface", small_bold),
        p("Next gate", small_bold),
    ]
    table_data = [header]
    for lane in LANES:
        table_data.append(
            [
                p(str(lane["n"]), small),
                p(lane["lane"], small),
                p(lane["plain"], small),
                p(lane["read"], small),
                p(lane["evidence"], small),
                p(lane["next"], small),
            ]
        )

    table = Table(
        table_data,
        colWidths=[0.32 * inch, 0.82 * inch, 1.4 * inch, 1.25 * inch, 3.35 * inch, 2.75 * inch],
        repeatRows=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111111")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bdbdbd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f4f2")]),
            ]
        )
    )
    story.append(table)
    story.append(PageBreak())

    story.append(p("CAT-1 Meta-Transfer Note", h2))
    story.append(
        p(
            "CAT-1 is kept beside the 21-lane map because it is the composition rule: "
            "a pattern must survive lawful translation between artifacts without "
            "breaking the score.",
            body,
        )
    )
    meta_table = Table(
        [
            [p("Lane", small_bold), p("Plain role", small_bold), p("Current read", small_bold), p("Evidence surface", small_bold), p("Next gate", small_bold)],
            [
                p(META_LANE["lane"], small),
                p(META_LANE["plain"], small),
                p(META_LANE["read"], small),
                p(META_LANE["evidence"], small),
                p(META_LANE["next"], small),
            ],
        ],
        colWidths=[0.85 * inch, 1.6 * inch, 1.8 * inch, 3.2 * inch, 2.55 * inch],
    )
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111111")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#bdbdbd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f4f4f2")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 0.16 * inch))
    story.append(p("Clean Read", h2))
    clean_read = dedent(
        """
        Nest 1 is no longer just grammar. It has a real evidence foundation across
        transformer traces, quantum/circuit bridges, hardware-facing checks, control
        discipline, and limited biological adapters. The supported lanes show the
        pattern can be measured in formal and transformer-adjacent substrates. The
        partial lanes identify exact missing inputs instead of vague future language.
        """
    ).strip()
    story.append(p(clean_read, body))
    story.append(
        p(
            "The current topology read is especially important: topology preservation "
            "is supported, but context-topology separation is not. Separation is "
            "showing up in geometry, magnitude, trajectory, topography, and feature "
            "graph structure.",
            body,
        )
    )
    story.append(p("Immediate Next Gates", h2))
    next_items = [
        "Export attention heads and MLP/feed-forward deltas.",
        "Use attention-flow labels to revisit GRAPH-2.",
        "Use EEG or real spectral datasets before reopening SPEC-1.",
        "Use EEG+HRV or other continuous signals before reopening DE-1.",
        "Expand OPT-1 and CAT-1 with larger real benchmarks.",
        "Carry this lane-by-lane discipline into Nest 2 molecular, allostery, PFAS, and materials validation.",
    ]
    for item in next_items:
        story.append(p(f"- {item}", body))

    doc.build(story)


def main() -> None:
    build_markdown()
    build_csv()
    build_pdf()
    print(f"wrote {DOC_PATH.relative_to(ROOT)}")
    print(f"wrote {PDF_PATH.relative_to(ROOT)}")
    print(f"wrote {CSV_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
