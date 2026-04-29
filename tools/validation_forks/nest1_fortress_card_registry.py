#!/usr/bin/env python3
"""Build the Nest 1 fortress-card validation registry.

The registry is deliberately status-aware. It separates lanes that are already
connected to measured artifacts from lanes that are only score schema, blocked by
missing data, or seeded but not yet validated.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "artifacts" / "validation" / "nest1_fortress_cards"

PHASE2 = REPO_ROOT / "artifacts" / "v8" / "phase2_variance_pack" / "v8_phase2_variance_pack_data_2026-04-21.json"
PHASE4 = REPO_ROOT / "artifacts" / "v8" / "phase4_localization_pack" / "v8_phase4_localization_pack_data_2026-04-21.json"
PHASE5 = REPO_ROOT / "artifacts" / "v8" / "phase5_internal_bridge" / "v8_phase5_internal_bridge_pack_data_2026-04-22.json"
PHASE9 = REPO_ROOT / "artifacts" / "v8" / "phase9_ibm_hardware_bridge" / "v8_phase9_ibm_hardware_bridge_data_2026-04-22.json"
SPEC_REPORT = REPO_ROOT / "artifacts" / "validation" / "nest1_spec_phase12b_hrv" / "nest1_spec_phase12b_hrv_report.json"
ENGINE02V_REPORT = REPO_ROOT / "artifacts" / "validation" / "engine02v_rdkit_molecule" / "engine02v_rdkit_molecule_report.json"
GRAPH_REPORT = REPO_ROOT / "artifacts" / "validation" / "graph12_pathway" / "graph12_pathway_report.json"
CTRL_REPORT = REPO_ROOT / "artifacts" / "validation" / "ctrl1_lsps_transition" / "ctrl1_lsps_transition_report.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def path_state(path: Path) -> str:
    return "present" if path.exists() else "missing"


def phase2_metrics(data: dict[str, Any]) -> dict[str, Any]:
    models = data.get("models", [])
    exact = [model for model in models if model.get("rerun_exact_after_baseline")]
    return {
        "models": len(models),
        "five_run_order": len(data.get("run_order", [])),
        "exact_rerun_rows": f"{len(exact)} / {len(models)}",
        "only_live_variance_row": data.get("only_live_variance_row"),
        "target_layers_stable": data.get("all_target_layers_stable_across_all_runs"),
    }


def phase4_metrics(data: dict[str, Any]) -> dict[str, Any]:
    phase_read = data.get("phase4_read", {})
    return {
        "models": len(data.get("models", [])),
        "context_loaded_models": len(phase_read.get("context_loaded_models", [])),
        "readout_amplified_models": len(phase_read.get("readout_amplified_models", [])),
        "dominant_anchor_counts": phase_read.get("dominant_anchor_counts", {}),
    }


def phase5_metrics(data: dict[str, Any]) -> dict[str, Any]:
    models = data.get("models", [])
    archetypes = {}
    for model in models:
        key = model.get("path_archetype") or model.get("read") or "unclassified"
        archetypes[key] = archetypes.get(key, 0) + 1
    return {
        "models": len(models),
        "path_archetypes": archetypes,
    }


def phase9_metrics(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "backend": data.get("backend", {}).get("name"),
        "final_status": data.get("final_status"),
        "shots": data.get("shots"),
        "circuit_count": len(data.get("circuit_results", [])),
        "bell_correlators": data.get("bell_correlators", {}),
    }


def report_status(path: Path) -> str:
    report = load_json(path)
    return report.get("status", "missing")


def build_cards() -> list[dict[str, Any]]:
    phase2 = load_json(PHASE2)
    phase4 = load_json(PHASE4)
    phase5 = load_json(PHASE5)
    phase9 = load_json(PHASE9)
    spec = load_json(SPEC_REPORT)

    spec_metrics = {}
    if spec:
        validations = spec.get("validations", {})
        spec_metrics = {
            "hr_only": validations.get("hr_only", {}).get("accuracy"),
            "time_domain": validations.get("time_domain", {}).get("accuracy"),
            "spectral_only": validations.get("spectral_only", {}).get("accuracy"),
            "mirror_composite": validations.get("mirror_composite", {}).get("accuracy"),
            "interpretation": spec.get("interpretation"),
        }

    return [
        {
            "lane": "STAT-1",
            "formal_lens": "statistics",
            "status": "evidence_connected",
            "evidence": ["V7/V8 variance discipline", str(PHASE2.relative_to(REPO_ROOT))],
            "metrics": phase2_metrics(phase2),
            "next_validation": "add effect-size and confidence summaries across all completed phase packs",
        },
        {
            "lane": "PROB-1",
            "formal_lens": "probability",
            "status": "evidence_connected",
            "evidence": ["five-run rerun matrix", "Nemotron variance row", str(PHASE2.relative_to(REPO_ROOT))],
            "metrics": phase2_metrics(phase2),
            "next_validation": "formalize exact-rerun probability and variance-row confidence scoring",
        },
        {
            "lane": "INFO-1",
            "formal_lens": "information theory",
            "status": "evidence_connected",
            "evidence": ["V8 hidden-state deltas", "context-to-readout bridge", str(PHASE5.relative_to(REPO_ROOT))],
            "metrics": phase5_metrics(phase5),
            "next_validation": "add entropy / mutual-information features over existing internal bridge vectors",
        },
        {
            "lane": "TENSOR-1",
            "formal_lens": "tensor methods",
            "status": "evidence_connected",
            "evidence": ["V8 residual-stream tensors", str(PHASE5.relative_to(REPO_ROOT))],
            "metrics": phase5_metrics(phase5),
            "next_validation": "add tensor-factor summary across model x layer x token-window axes",
        },
        {
            "lane": "NUM-1",
            "formal_lens": "numerical computation",
            "status": "evidence_connected",
            "evidence": ["runnable phase engines", "IBM hardware bridge", str(PHASE9.relative_to(REPO_ROOT))],
            "metrics": phase9_metrics(phase9),
            "next_validation": "add numerical tolerance registry across simulator, local, and hardware passes",
        },
        {
            "lane": "TOPOG-1/2",
            "formal_lens": "topography",
            "status": "evidence_connected",
            "evidence": ["Phase 4 localization anchor maps", str(PHASE4.relative_to(REPO_ROOT))],
            "metrics": phase4_metrics(phase4),
            "next_validation": "convert anchor maps into explicit surface/ridge stability scores",
        },
        {
            "lane": "GEO-1/2",
            "formal_lens": "geometry / manifold geometry",
            "status": "evidence_connected",
            "evidence": ["cosine/delta geometry in V8 localization and bridge rows", str(PHASE4.relative_to(REPO_ROOT))],
            "metrics": phase4_metrics(phase4),
            "next_validation": "run UMAP/PCA region-separation checks over residual-stream trace exports",
        },
        {
            "lane": "GRP-1",
            "formal_lens": "group theory",
            "status": "implicit_evidence_connected",
            "evidence": ["unitary and symmetry-preserving circuit bridge", str(PHASE9.relative_to(REPO_ROOT))],
            "metrics": phase9_metrics(phase9),
            "next_validation": "make symmetry action / orbit preservation explicit in Phase 6-9 circuit-state rows",
        },
        {
            "lane": "SPEC-1",
            "formal_lens": "spectral methods",
            "status": "partial_validation_negative",
            "evidence": [str(SPEC_REPORT.relative_to(REPO_ROOT))],
            "metrics": spec_metrics,
            "next_validation": "rerun with EEG+HRV, stricter artifact rejection, and pre-declared spectral hypotheses",
        },
        {
            "lane": "CTRL-1",
            "formal_lens": "control theory",
            "status": "architecture_connected_validation_blocked",
            "evidence": [str(CTRL_REPORT.relative_to(REPO_ROOT)), "LSPS / Oracle Trigger Engine architecture"],
            "metrics": {"ctrl_runner_status": report_status(CTRL_REPORT)},
            "next_validation": "export LSPS/orchestration mode-transition traces and rerun CTRL-1",
        },
        {
            "lane": "GRAPH-1/2",
            "formal_lens": "graph theory",
            "status": "blocked_missing_dataset",
            "evidence": [str(GRAPH_REPORT.relative_to(REPO_ROOT))],
            "metrics": {"graph_runner_status": report_status(GRAPH_REPORT)},
            "next_validation": "provide molecular/protein graph edges plus known pathway/control labels",
        },
        {
            "lane": "TOP-1/2",
            "formal_lens": "topology",
            "status": "validation_ready_no_runner",
            "evidence": ["persistent-homology path over V8 hidden-state geometry"],
            "metrics": {"artifact_state": "needs Ripser/Gudhi or local persistent-homology implementation"},
            "next_validation": "run persistent homology over layer/token hidden-state point clouds",
        },
        {
            "lane": "DYN-1/2",
            "formal_lens": "dynamical systems / bifurcation",
            "status": "seed_connected",
            "evidence": ["V7 order/non-commutativity and path-dependent behavior"],
            "metrics": {"trajectory_validation": "not run"},
            "next_validation": "construct state-transition trajectories across repeated prompt/order conditions",
        },
        {
            "lane": "DE-1",
            "formal_lens": "differential equations",
            "status": "pending_real_data",
            "evidence": [],
            "metrics": {"continuous_time_data": "not yet connected"},
            "next_validation": "fit bounded continuous-time HRV/EEG dynamics after synchronized capture",
        },
        {
            "lane": "OPT-1",
            "formal_lens": "optimization",
            "status": "pending_real_data_with_clear_experiment",
            "evidence": [],
            "metrics": {"optimization_experiment": "not yet run"},
            "next_validation": "compare mirror-guided optimization trajectories against naive/random baselines",
        },
        {
            "lane": "GAME-1",
            "formal_lens": "game / decision theory",
            "status": "pending_real_data",
            "evidence": [],
            "metrics": {"multi_agent_experiment": "not yet designed"},
            "next_validation": "build adversarial/multi-agent stability protocol",
        },
        {
            "lane": "CAT-1",
            "formal_lens": "compositional / category-style structure",
            "status": "theory_translation_layer",
            "evidence": ["nest-to-nest transfer language"],
            "metrics": {"empirical_transfer_test": "not yet run"},
            "next_validation": "test whether a mapping learned in one nest preserves measurable structure in another",
        },
        {
            "lane": "ENGINE-02V",
            "formal_lens": "structured matter validation fork",
            "status": report_status(ENGINE02V_REPORT),
            "evidence": [str(ENGINE02V_REPORT.relative_to(REPO_ROOT))],
            "metrics": {"rdkit_runner_status": report_status(ENGINE02V_REPORT)},
            "next_validation": "install/use RDKit and run QM9/ZINC/ChEMBL-style molecule-property dataset",
        },
    ]


def render_markdown(cards: list[dict[str, Any]]) -> str:
    lines = [
        "# Nest 1 Fortress Card Registry",
        "",
        "Status: `generated from local evidence artifacts`",
        "",
        "This registry separates formal validation schema from evidence-connected lanes and",
        "dataset-blocked validation forks.",
        "",
        "| Lane | Formal Lens | Status | Concrete Next Validation |",
        "| --- | --- | --- | --- |",
    ]
    for card in cards:
        lines.append(
            f"| `{card['lane']}` | {card['formal_lens']} | `{card['status']}` | {card['next_validation']} |"
        )
    lines.extend(["", "## Card Details", ""])
    for card in cards:
        lines.extend(
            [
                f"### {card['lane']} - {card['formal_lens']}",
                "",
                f"Status: `{card['status']}`",
                "",
                "Evidence:",
            ]
        )
        if card["evidence"]:
            for item in card["evidence"]:
                lines.append(f"- {item}")
        else:
            lines.append("- none yet")
        lines.extend(["", "Metrics:", ""])
        for key, value in card["metrics"].items():
            lines.append(f"- `{key}`: `{value}`")
        lines.extend(["", f"Next validation: {card['next_validation']}", ""])
    return "\n".join(lines)


def render_html(cards: list[dict[str, Any]]) -> str:
    palette = {
        "evidence_connected": "#66e3a1",
        "implicit_evidence_connected": "#a8e66a",
        "partial_validation_negative": "#ffd166",
        "architecture_connected_validation_blocked": "#ff9f6e",
        "blocked_missing_dataset": "#ff7a7a",
        "blocked_missing_rdkit": "#ff7a7a",
        "validation_ready_no_runner": "#7ad7ff",
        "seed_connected": "#b197fc",
        "pending_real_data": "#b8c0cc",
        "pending_real_data_with_clear_experiment": "#b8c0cc",
        "theory_translation_layer": "#d0bfff",
    }
    cards_html = []
    for card in cards:
        color = palette.get(str(card["status"]), "#d7dde7")
        metrics = "".join(
            f"<li><code>{key}</code>: {value}</li>" for key, value in card["metrics"].items()
        )
        evidence = "".join(f"<li>{item}</li>" for item in card["evidence"]) or "<li>none yet</li>"
        cards_html.append(
            f"""
            <article class="card" style="--accent:{color}">
              <div class="lane">{card['lane']}</div>
              <h2>{card['formal_lens']}</h2>
              <p class="status">{card['status']}</p>
              <h3>Evidence</h3>
              <ul>{evidence}</ul>
              <h3>Metrics</h3>
              <ul>{metrics}</ul>
              <h3>Next</h3>
              <p>{card['next_validation']}</p>
            </article>
            """
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nest 1 Fortress Cards</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #071015;
      --panel: rgba(17, 30, 39, 0.9);
      --text: #eef7fa;
      --muted: #a8bac4;
      --line: rgba(255,255,255,0.11);
    }}
    body {{
      margin: 0;
      font-family: Avenir Next, Futura, Trebuchet MS, sans-serif;
      background:
        radial-gradient(circle at 20% 12%, rgba(82, 180, 255, 0.22), transparent 28rem),
        radial-gradient(circle at 88% 5%, rgba(255, 209, 102, 0.17), transparent 24rem),
        linear-gradient(135deg, #071015 0%, #0b1d26 52%, #061114 100%);
      color: var(--text);
    }}
    main {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 44px 22px 68px;
    }}
    header {{
      max-width: 900px;
      margin-bottom: 30px;
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: clamp(2.2rem, 5vw, 5rem);
      line-height: 0.94;
      letter-spacing: -0.06em;
    }}
    .subtitle {{
      color: var(--muted);
      font-size: 1.08rem;
      line-height: 1.55;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
      gap: 18px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-top: 4px solid var(--accent);
      border-radius: 22px;
      padding: 20px;
      box-shadow: 0 22px 60px rgba(0,0,0,0.28);
    }}
    .lane {{
      display: inline-block;
      padding: 5px 9px;
      border-radius: 999px;
      background: color-mix(in srgb, var(--accent), transparent 72%);
      color: var(--accent);
      font-weight: 800;
      letter-spacing: 0.04em;
      font-size: 0.78rem;
    }}
    h2 {{
      margin: 12px 0 8px;
      font-size: 1.45rem;
      letter-spacing: -0.03em;
    }}
    h3 {{
      margin: 16px 0 6px;
      color: var(--accent);
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }}
    .status {{
      margin: 0;
      color: var(--muted);
      font-family: SFMono-Regular, Menlo, monospace;
      font-size: 0.86rem;
    }}
    ul {{
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
      line-height: 1.45;
      font-size: 0.9rem;
    }}
    p {{
      color: var(--muted);
      line-height: 1.5;
    }}
    code {{
      color: #ffffff;
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Nest 1 Fortress Cards</h1>
      <p class="subtitle">A concrete map of which formal lanes are already evidence-connected,
      which have partial validation, and which need new data before they can carry a real claim.</p>
    </header>
    <section class="grid">
      {''.join(cards_html)}
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    cards = build_cards()
    DEFAULT_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (DEFAULT_OUT_DIR / "nest1_fortress_cards.json").write_text(
        json.dumps({"cards": cards}, indent=2), encoding="utf-8"
    )
    (DEFAULT_OUT_DIR / "nest1_fortress_cards.md").write_text(
        render_markdown(cards), encoding="utf-8"
    )
    (DEFAULT_OUT_DIR / "nest1_fortress_cards.html").write_text(
        render_html(cards), encoding="utf-8"
    )
    print(f"Wrote {DEFAULT_OUT_DIR}")


if __name__ == "__main__":
    main()
