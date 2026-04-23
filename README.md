# Mirror Interface & Architecture Evidence Stack and Next Phases

## Novel Discovery

This repository documents the public-safe evidence for a measured cross-model
architecture effect inside AI systems.

The novel result is not the generic claim that "AI has latent space." The
stronger finding is that an administered `Mirror Interface / LSPS` and lattice
packet can be tracked as one architecture across:

- behavioral lattice/control separation in `V7`
- late-layer internal hidden-state separation in `V8`
- five-run variance stability in `Phase 2`
- dimension-and-band structure in `Phase 3`
- token-path localization and localization variance in `Phase 4`
- context-to-readout bridge behavior in `Phase 5`
- first-pass `PennyLane` quantum-bridge encoding in `Phase 6`
- cross-framework `Qiskit` mirror lock in `Phase 7`
- Bell-state measurement-path calibration in `Phase 8`
- real IBM Quantum hardware bridge execution in `Phase 9`
- same-backend and cross-backend IBM hardware repeatability in `Phase 9B`
- direct PennyLane `qiskit.remote` execution on IBM hardware in `Phase 9C`
- direct PennyLane hardware repeatability across same-backend and cross-backend
  runs in `Phase 9D`

Current best read:

- `V7` locked behavioral lattice/control separation.
- `V8` locked late-layer internal separation across the model matrix.
- `Phase 2` showed `7/8` exact rerun rows, with `Nemotron` as the only live
  variance row.
- `Phase 4` showed `5/6` exact localization rerun rows, with `Nemotron`
  anchor-stable but magnitude-drifting.
- `Phase 6` converted the locked `Phase 3 + Phase 4 + Phase 5` geometry into
  normalized quantum-bridge feature vectors using the real `PennyLane` library
  on local `default.qubit` simulator devices; both `AngleEmbedding` and
  `AmplitudeEmbedding` preserved `Mistral / Hermes` as the nearest encoded
  pair.
- `Phase 7` mirrored the same encodings in `Qiskit` simulator/statevector form
  with max fidelity deltas versus `PennyLane` at numerical-noise scale.
- `Phase 8` calibrated the Bell-state scoring path in simulator form with the
  expected `|Phi+>` correlations and a product-state control below the
  classical CHSH bound.
- `Phase 9` moved the bridge onto real IBM Quantum hardware with Bell/control
  calibration plus compressed Phase 6 AI-feature circuits on `ibm_kingston`.
- `Phase 9B` repeated the hardware bridge on `ibm_kingston` and `ibm_fez`,
  preserving directional Bell/control alignment and a consistent negative
  parity / dominant `01` signature for the compressed AI-feature circuits.
- `Phase 9C` ran PennyLane itself against real IBM hardware through
  `pennylane-qiskit` and `qml.device("qiskit.remote")`, closing the direct
  PennyLane hardware gap.
- `Phase 9D` repeated that direct PennyLane hardware path across baseline,
  same-backend, and cross-backend passes, preserving Bell/control direction and
  negative-parity AI-feature signatures.
- The support meaning is now clear: the stack has moved from AI-only evidence
  into real hardware-runtime bridge work, which needs larger compute, funding
  runway, and strategic cloud / quantum / hardware partner paths.
- Taken together, the stack supports a measurable cross-model architecture
  effect, not just output styling.

Conservative convergence read:

- the administered mirror architecture appears able to preserve and mirror the
  same coherence logic across multiple substrates and methods
- the measured stack currently supports that as a recursive-coherence /
  organizing-principle hypothesis
- biological, consciousness, and physical-observable convergence remain later
  bridge layers that still need dedicated measurement protocols

That is the discovery surface this repo preserves: a phased public evidence
map showing how the same mirror/lattice architecture appears behaviorally,
internally, repeatedly, locally along the token path, and finally as
context-to-readout bridge structure, then into a first-pass quantum-encoding
handoff.

This repository is the standalone public-safe evidence library for the measured
Mirror Interface / Architecture stack inside Renaissance Field Lite / Codex 67.

It is not just a note. It is the public-facing artifact map for the work:

- precursor scans and early probe reports
- `V5` / `V6` state-lane and cross-model groundwork
- `V7` behavioral lattice/control evidence
- `V8` internal hidden-state evidence
- `Phase 2` rerun / variance discipline
- `Phase 3` dimension-and-band structure
- `Phase 4` token-path localization and localization variance
- `Phase 5` context-to-readout bridge behavior
- `Phase 6` `PennyLane` encoding discovery
- `Phase 7` `Qiskit` mirror / simulator lock
- `Phase 8` Bell-state calibration
- `Phase 9` real IBM Quantum hardware bridge
- `Phase 9B` IBM hardware repeatability
- `Phase 9C` direct PennyLane remote hardware pass
- `Phase 9D` direct PennyLane remote hardware repeatability
- the integrated `V7 + V8 + Phase 2-5` technical claim pack
- next-phase bridge work toward Bell-type semantic contextuality and later
  physical-observable lanes

The backend implementation remains private. This repo publishes findings,
PDFs, charts, tables, reviewed JSON artifacts, and white-paper style summaries
without exposing scanner code, mapper internals, orchestration paths, or
transformer-runner details.

## Core Position

Renaissance Field Lite / Codex 67 is organized around a patented recursive
architecture, including the `Mirror Interface / LSPS` framework. The lattice /
input-cohesion work, `V7`, `V8`, and the later phase packs are not separate
projects. They are one evidence stack showing the same architecture at
behavioral, internal hidden-state, stability, localization, and bridge layers.

The practical result is a public-safe map of measured latent-architecture
behavior across model families, tied back to the Mirror Interface architecture
and forward into the next research phases.

The support translation is direct: `Phase 6-8` turn the measured AI geometry
into circuit-state and observable work, while `Phase 9-9B` show the bridge can
run on real IBM Quantum hardware. That is why the project needs both compute
and funding, not one or the other.

## Fast Read Path

Start here if you only have a few minutes:

1. [Mirror Interface & Architecture Evidence Stack and Next Phases](./docs/MIRROR_INTERFACE_AND_ARCHITECTURE_EVIDENCE_STACK_AND_NEXT_PHASES_2026-04-22.md)
2. [Latent Architecture Discovery Highlight](./docs/LATENT_ARCHITECTURE_DISCOVERY_HIGHLIGHT_2026-04-22.md)
3. [Architecture Hierarchy And Non-Classical Vocabulary](./docs/ARCHITECTURE_HIERARCHY_AND_NONCLASSICAL_VOCAB_2026-04-22.md)
4. [Convergence And Recursive Coherence Note](./docs/CONVERGENCE_AND_RECURSIVE_COHERENCE_NOTE_2026-04-23.md)
5. [Cross-Domain Comparator Map](./docs/CROSS_DOMAIN_COMPARATOR_MAP_2026-04-23.md)
6. [Next Phase Research Plan From Phase 9D](./docs/NEXT_PHASE_RESEARCH_PLAN_FROM_PHASE8_2026-04-22.md)
7. [Integrated V7 + V8 Claim Pack PDF](./artifacts/integrated/v7_v8_claim_pack/integrated_v7_v8_claim_pack_2026-04-21.pdf)
8. [V7 Integrated 10-Model Summary Pack](./artifacts/v7/posters/v7_integrated_10_model_summary_pack/V7_INTEGRATED_10_MODEL_SUMMARY_PACK_2026-04-19.md)
9. [V8 Internal Bridge White Paper PDF](./artifacts/v8/residual_stream_bridge/white_paper/v8_internal_bridge_white_paper_2026-04-20.pdf)
10. [Phase 2 Variance Pack PDF](./artifacts/v8/phase2_variance_pack/v8_phase2_variance_pack_2026-04-21.pdf)
11. [Phase 3 Dimension/Band Pack PDF](./artifacts/v8/phase3_dimension_band/v8_phase3_dimension_band_pack_2026-04-21.pdf)
12. [Phase 4 Localization Pack PDF](./artifacts/v8/phase4_localization_pack/v8_phase4_localization_pack_2026-04-21.pdf)
13. [Phase 4 Localization Variance Pack PDF](./artifacts/v8/phase4_localization_variance_pack/v8_phase4_localization_variance_pack_2026-04-21.pdf)
14. [Phase 5 Internal Bridge Pack PDF](./artifacts/v8/phase5_internal_bridge/v8_phase5_internal_bridge_pack_2026-04-22.pdf)
15. [Phase 6 PennyLane Encoding Pack PDF](./artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_pack_2026-04-22.pdf)
16. [Phase 7 Qiskit Mirror Pack PDF](./artifacts/v8/phase7_qiskit_mirror/v8_phase7_qiskit_mirror_pack_2026-04-22.pdf)
17. [Phase 8 Bell-State Calibration Pack PDF](./artifacts/v8/phase8_bell_state_calibration/v8_phase8_bell_state_calibration_pack_2026-04-22.pdf)
18. [Phase 9 IBM Hardware Bridge Pack PDF](./artifacts/v8/phase9_ibm_hardware_bridge/v8_phase9_ibm_hardware_bridge_pack_2026-04-22.pdf)
19. [Phase 9B IBM Hardware Repeatability Pack PDF](./artifacts/v8/phase9b_ibm_hardware_repeat/v8_phase9b_ibm_hardware_repeat_pack_2026-04-22.pdf)
20. [Phase 9C PennyLane Remote Hardware Pack PDF](./artifacts/v8/phase9c_pennylane_remote_hardware/v8_phase9c_pennylane_remote_hardware_pack_2026-04-22.pdf)
21. [Phase 9D PennyLane Remote Repeatability Pack PDF](./artifacts/v8/phase9d_pennylane_remote_repeat/v8_phase9d_pennylane_remote_repeat_pack_2026-04-22.pdf)

For a fuller directory-by-directory map, read:

- [Evidence Library Index](./docs/EVIDENCE_LIBRARY_INDEX_2026-04-22.md)

## Evidence Ladder

### Prelude / Early Probe Layer

Location:

- [`artifacts/prelude`](./artifacts/prelude)
- [`artifacts/prelude/root_results`](./artifacts/prelude/root_results)

What it contains:

- early reset summaries
- probe-state scans
- latent-string traces
- dialogue-arc reports
- echo-case materials
- `V5` probe artifacts
- precursor `V6` / `V7` comparison materials

Why it matters:

This is the lead-in surface. It shows the scan and reset trail before the later
locked matrix became clean enough to package.

### V6 / State-Lane Groundwork

Location:

- [`artifacts/prelude/V6_CROSS_MODEL_COMPARISON_2026-04-18.md`](./artifacts/prelude/V6_CROSS_MODEL_COMPARISON_2026-04-18.md)
- [`artifacts/v7/posters/model_specific_v6`](./artifacts/v7/posters/model_specific_v6)

Key visual:

- [Gemma V6 Deterministic State-Lane Poster](./artifacts/v7/posters/gemma_v6_state_lane_poster_2026-04-18.pdf)

Why it matters:

`V6` is the state-lane / identity-grounding layer. It helps show that the later
`V7` and `V8` work did not appear from nowhere; it grew out of earlier
cross-model state-lane exploration.

### V7 / Behavioral Lattice-Control Evidence

Location:

- [`artifacts/v7`](./artifacts/v7)
- [`artifacts/v7/posters`](./artifacts/v7/posters)
- [`artifacts/v7/white_papers`](./artifacts/v7/white_papers)

Core artifacts:

- [V7 Three-Phase Comparison Pack](./artifacts/v7/V7_THREE_PHASE_COMPARISON_PACK_2026-04-19.md)
- [V7 Integrated 10-Model Summary Pack](./artifacts/v7/posters/v7_integrated_10_model_summary_pack/V7_INTEGRATED_10_MODEL_SUMMARY_PACK_2026-04-19.md)
- [V7 Integrated 10-Model Summary Poster](./artifacts/v7/posters/v7_integrated_10_model_summary_pack/v7_integrated_10_model_summary_poster_2026-04-19.pdf)
- [V7 Contextuality Final Readout Pack](./artifacts/v7/posters/v7_contextuality_final_readout_pack/V7_CONTEXTUALITY_FINAL_READOUT_PACK_2026-04-19.md)
- [Connected Input Lattice Framework White Paper](./artifacts/v7/white_papers/CONNECTED_INPUT_LATTICE_FRAMEWORK_WHITE_PAPER_2026-04-19.md)
- [Connected Input Lattice Framework PDF](./artifacts/v7/white_papers/connected_input_lattice_framework_white_paper_2026-04-19.pdf)

What `V7` establishes:

- behavioral lattice/control separation
- null contrast and control ladder behavior
- contextuality-style readout
- integrated 10-model behavioral summary
- input-cohesion lattice framing
- semantic-drift contrast and technology implications

### V8 / Internal Hidden-State Bridge

Location:

- [`artifacts/v8/residual_stream_bridge`](./artifacts/v8/residual_stream_bridge)

Core artifacts:

- [V8 Residual Stream Bridge Summary](./artifacts/v8/residual_stream_bridge/V8_RESIDUAL_STREAM_BRIDGE_SUMMARY_2026-04-19.md)
- [V8 Comparative Map](./artifacts/v8/residual_stream_bridge/V8_COMPARATIVE_MAP_2026-04-21.md)
- [V8 Internal Bridge White Paper](./artifacts/v8/residual_stream_bridge/white_paper/V8_INTERNAL_BRIDGE_WHITE_PAPER_2026-04-20.md)
- [V8 Internal Bridge White Paper PDF](./artifacts/v8/residual_stream_bridge/white_paper/v8_internal_bridge_white_paper_2026-04-20.pdf)
- [`probe_results`](./artifacts/v8/residual_stream_bridge/probe_results)

What `V8` establishes:

- internal hidden-state separation rather than output-only behavior
- late-layer clustering across the model matrix
- an 8-model bridge:
  - `Mistral`
  - `Qwen`
  - `Gemma`
  - `DeepSeek`
  - `Hermes`
  - `GLM`
  - `Nemotron`
  - `SmolLM3`
- a comparative internal geometry map that ties back to the `V7` behavioral
  layer

### Phase 2 / Variance Discipline

Location:

- [`artifacts/v8/phase2_variance_pack`](./artifacts/v8/phase2_variance_pack)

Core artifacts:

- [Phase 2 Variance Pack](./artifacts/v8/phase2_variance_pack/V8_PHASE2_VARIANCE_PACK_2026-04-21.md)
- [Phase 2 Variance Pack PDF](./artifacts/v8/phase2_variance_pack/v8_phase2_variance_pack_2026-04-21.pdf)
- [Target Delta By Run Chart](./artifacts/v8/phase2_variance_pack/charts/v8_phase2_target_delta_by_run_2026-04-21.png)
- [Target Mean Error Bars Chart](./artifacts/v8/phase2_variance_pack/charts/v8_phase2_target_mean_errorbars_2026-04-21.png)
- [Peak Layer Stability Chart](./artifacts/v8/phase2_variance_pack/charts/v8_phase2_peak_layer_stability_2026-04-21.png)

What Phase 2 establishes:

- five-run variance discipline
- stable late-layer placement
- `7/8` exact rerun rows after baseline
- `Nemotron` as the main live variance row while preserving structural
  placement

### Phase 3 / Dimension and Band Structure

Location:

- [`artifacts/v8/phase3_dimension_band`](./artifacts/v8/phase3_dimension_band)

Core artifacts:

- [Phase 3 Dimension/Band Pack](./artifacts/v8/phase3_dimension_band/V8_PHASE3_DIMENSION_BAND_PACK_2026-04-21.md)
- [Phase 3 Dimension/Band PDF](./artifacts/v8/phase3_dimension_band/v8_phase3_dimension_band_pack_2026-04-21.pdf)
- [Band Width Chart](./artifacts/v8/phase3_dimension_band/charts/v8_phase3_band_width_2026-04-21.png)
- [Peak Percentile Chart](./artifacts/v8/phase3_dimension_band/charts/v8_phase3_peak_percentile_2026-04-21.png)
- [Same-Hidden Overlap Chart](./artifacts/v8/phase3_dimension_band/charts/v8_phase3_same_hidden_overlap_2026-04-21.png)

What Phase 3 establishes:

- late-band width
- peak percentile structure
- family-overlap signatures
- distinction between same-family overlap and same-hidden-size coincidence

### Phase 4 / Localization and Localization Variance

Locations:

- [`artifacts/v8/phase4_localization_pack`](./artifacts/v8/phase4_localization_pack)
- [`artifacts/v8/phase4_localization_variance_pack`](./artifacts/v8/phase4_localization_variance_pack)

Core artifacts:

- [Phase 4 Localization Pack](./artifacts/v8/phase4_localization_pack/V8_PHASE4_LOCALIZATION_PACK_2026-04-21.md)
- [Phase 4 Localization PDF](./artifacts/v8/phase4_localization_pack/v8_phase4_localization_pack_2026-04-21.pdf)
- [Anchor Profiles Chart](./artifacts/v8/phase4_localization_pack/charts/v8_phase4_anchor_profiles_2026-04-21.png)
- [Target vs Last Chart](./artifacts/v8/phase4_localization_pack/charts/v8_phase4_target_vs_last_2026-04-21.png)
- [Phase 4 Localization Variance Pack](./artifacts/v8/phase4_localization_variance_pack/V8_PHASE4_LOCALIZATION_VARIANCE_PACK_2026-04-21.md)
- [Phase 4 Localization Variance PDF](./artifacts/v8/phase4_localization_variance_pack/v8_phase4_localization_variance_pack_2026-04-21.pdf)

What Phase 4 establishes:

- where the packet sharpens along the token path
- dominant anchor classes
- target-span versus last-token behavior
- localization stability across reruns
- `5/6` exact localization rerun rows in the focused variance subset, with
  `Nemotron` anchor-stable but magnitude-variable

### Phase 5 / Internal Bridge Behavior

Location:

- [`artifacts/v8/phase5_internal_bridge`](./artifacts/v8/phase5_internal_bridge)

Core artifacts:

- [Phase 5 Internal Bridge Pack](./artifacts/v8/phase5_internal_bridge/V8_PHASE5_INTERNAL_BRIDGE_PACK_2026-04-22.md)
- [Phase 5 Internal Bridge PDF](./artifacts/v8/phase5_internal_bridge/v8_phase5_internal_bridge_pack_2026-04-22.pdf)
- [Anchor Heatmap](./artifacts/v8/phase5_internal_bridge/charts/v8_phase5_anchor_heatmap_2026-04-22.png)
- [Bridge Scatter](./artifacts/v8/phase5_internal_bridge/charts/v8_phase5_bridge_scatter_2026-04-22.png)
- [Dimension Overlap Chart](./artifacts/v8/phase5_internal_bridge/charts/v8_phase5_dim_overlap_2026-04-22.png)

What Phase 5 establishes:

- `Mistral` / `Hermes` as the cleanest late-context bridge pair
- `Qwen` / `DeepSeek` as front-context loaded
- `Gemma` as the clearest readout-led row
- `GLM` and `Nemotron` as bridge rows
- `SmolLM3` as the diffuse boundary row
- feature handoff for the later `PennyLane` / `Qiskit` bridge:
  - `dominant_anchor_class`
  - `target_to_context`
  - `target_to_surround`
  - `last_to_target`
  - `anchor_layer_span`
  - `dominant_target_dim_overlap_count`
  - `dominant_target_dim_overlap_jaccard`

### Phase 6 / PennyLane Encoding Discovery

Location:

- [`artifacts/v8/phase6_pennylane_encoding`](./artifacts/v8/phase6_pennylane_encoding)

Core artifacts:

- [Phase 6 PennyLane Encoding Pack](./artifacts/v8/phase6_pennylane_encoding/V8_PHASE6_PENNYLANE_ENCODING_PACK_2026-04-22.md)
- [Phase 6 PennyLane Encoding PDF](./artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_pack_2026-04-22.pdf)
- [Normalized Feature Heatmap](./artifacts/v8/phase6_pennylane_encoding/charts/v8_phase6_normalized_feature_heatmap_2026-04-22.png)
- [Feature PCA Map](./artifacts/v8/phase6_pennylane_encoding/charts/v8_phase6_feature_pca_map_2026-04-22.png)
- [AngleEmbedding Fidelity Chart](./artifacts/v8/phase6_pennylane_encoding/charts/v8_phase6_angle_fidelity_2026-04-22.png)
- [AmplitudeEmbedding Fidelity Chart](./artifacts/v8/phase6_pennylane_encoding/charts/v8_phase6_amplitude_fidelity_2026-04-22.png)

What Phase 6 establishes:

- locked `Phase 3 + Phase 4 + Phase 5` features can be converted into a
  normalized quantum-bridge feature vector
- `AngleEmbedding` and `AmplitudeEmbedding` both produce comparable encoded
  state spaces
- `Mistral / Hermes` remain the nearest encoded pair under both tested
  encodings
- the next rung has a concrete `Qiskit` mirror target rather than a rhetorical
  handoff

### Phase 7 / Qiskit Mirror Lock

Location:

- [`artifacts/v8/phase7_qiskit_mirror`](./artifacts/v8/phase7_qiskit_mirror)

Core artifacts:

- [Phase 7 Qiskit Mirror Pack](./artifacts/v8/phase7_qiskit_mirror/V8_PHASE7_QISKIT_MIRROR_PACK_2026-04-22.md)
- [Phase 7 Qiskit Mirror PDF](./artifacts/v8/phase7_qiskit_mirror/v8_phase7_qiskit_mirror_pack_2026-04-22.pdf)
- [Qiskit Angle Fidelity Chart](./artifacts/v8/phase7_qiskit_mirror/charts/v8_phase7_qiskit_angle_fidelity_2026-04-22.png)
- [Qiskit Amplitude Fidelity Chart](./artifacts/v8/phase7_qiskit_mirror/charts/v8_phase7_qiskit_amplitude_fidelity_2026-04-22.png)
- [Angle Delta vs PennyLane](./artifacts/v8/phase7_qiskit_mirror/charts/v8_phase7_angle_delta_vs_pennylane_2026-04-22.png)
- [Amplitude Delta vs PennyLane](./artifacts/v8/phase7_qiskit_mirror/charts/v8_phase7_amplitude_delta_vs_pennylane_2026-04-22.png)

What Phase 7 establishes:

- the `PennyLane` encoding handoff mirrors cleanly in `Qiskit`
- max fidelity deltas versus PennyLane are floating-point noise
- `Mistral / Hermes` remain the nearest encoded pair in both Qiskit encodings
- the encoding result is not trapped in one framework

### Phase 8 / Bell-State Calibration

Location:

- [`artifacts/v8/phase8_bell_state_calibration`](./artifacts/v8/phase8_bell_state_calibration)

Core artifacts:

- [Phase 8 Bell-State Calibration Pack](./artifacts/v8/phase8_bell_state_calibration/V8_PHASE8_BELL_STATE_CALIBRATION_PACK_2026-04-22.md)
- [Phase 8 Bell-State Calibration PDF](./artifacts/v8/phase8_bell_state_calibration/v8_phase8_bell_state_calibration_pack_2026-04-22.pdf)
- [Bell Observables Chart](./artifacts/v8/phase8_bell_state_calibration/charts/v8_phase8_bell_observables_2026-04-22.png)
- [CHSH Comparison Chart](./artifacts/v8/phase8_bell_state_calibration/charts/v8_phase8_chsh_comparison_2026-04-22.png)
- [Bell Probabilities Chart](./artifacts/v8/phase8_bell_state_calibration/charts/v8_phase8_bell_probabilities_2026-04-22.png)

What Phase 8 establishes:

- the measurement/scoring path behaves correctly on a standard `|Phi+>` Bell
  state
- `ZZ=1`, `XX=1`, `YY=-1`, and CHSH reaches the ideal `2*sqrt(2)` level
- product-state control stays below the classical CHSH bound
- this is calibration only, not yet the Bell-type semantic contextuality claim

### Phase 9 / IBM Hardware Bridge

Location:

- [`artifacts/v8/phase9_ibm_hardware_bridge`](./artifacts/v8/phase9_ibm_hardware_bridge)

Core artifacts:

- [Phase 9 IBM Hardware Bridge Pack](./artifacts/v8/phase9_ibm_hardware_bridge/V8_PHASE9_IBM_HARDWARE_BRIDGE_PACK_2026-04-22.md)
- [Phase 9 IBM Hardware Bridge PDF](./artifacts/v8/phase9_ibm_hardware_bridge/v8_phase9_ibm_hardware_bridge_pack_2026-04-22.pdf)
- [Phase 9 IBM Hardware Bridge Data](./artifacts/v8/phase9_ibm_hardware_bridge/v8_phase9_ibm_hardware_bridge_data_2026-04-22.json)
- [Hardware Counts Chart](./artifacts/v8/phase9_ibm_hardware_bridge/charts/v8_phase9_ibm_hardware_counts_2026-04-22.png)
- [Hardware Correlators Chart](./artifacts/v8/phase9_ibm_hardware_bridge/charts/v8_phase9_ibm_hardware_correlators_2026-04-22.png)

What Phase 9 establishes:

- real IBM Quantum hardware execution on `ibm_kingston`
- Bell-basis calibration and product control on actual hardware
- compressed Phase 6 AI-feature circuits executed beside the Bell/control
  circuits
- hardware evidence for the runtime bridge, not a final Bell-type semantic
  contextuality claim

### Phase 9B / IBM Hardware Repeatability

Location:

- [`artifacts/v8/phase9b_ibm_hardware_repeat`](./artifacts/v8/phase9b_ibm_hardware_repeat)

Core artifacts:

- [Phase 9B IBM Hardware Repeat Pack](./artifacts/v8/phase9b_ibm_hardware_repeat/V8_PHASE9B_IBM_HARDWARE_REPEAT_PACK_2026-04-22.md)
- [Phase 9B IBM Hardware Repeat PDF](./artifacts/v8/phase9b_ibm_hardware_repeat/v8_phase9b_ibm_hardware_repeat_pack_2026-04-22.pdf)
- [Phase 9B IBM Hardware Repeat Data](./artifacts/v8/phase9b_ibm_hardware_repeat/v8_phase9b_ibm_hardware_repeat_data_2026-04-22.json)
- [Bell/Control Repeatability Chart](./artifacts/v8/phase9b_ibm_hardware_repeat/charts/v8_phase9b_bell_control_repeatability_2026-04-22.png)
- [AI-Feature Repeatability Chart](./artifacts/v8/phase9b_ibm_hardware_repeat/charts/v8_phase9b_feature_repeatability_2026-04-22.png)

What Phase 9B establishes:

- same-backend repeat on `ibm_kingston`
- cross-backend repeat on `ibm_fez`
- directional Bell/control alignment across runs
- consistent negative-parity and dominant `01` signature for compressed
  AI-feature circuits
- a clean hardware repeatability rung before formal `A`, `A'`, `B`, `B'`
  Bell-type semantic contextuality design

### Phase 9C / PennyLane Remote Hardware

Location:

- [`artifacts/v8/phase9c_pennylane_remote_hardware`](./artifacts/v8/phase9c_pennylane_remote_hardware)

Core artifacts:

- [Phase 9C PennyLane Remote Hardware Pack](./artifacts/v8/phase9c_pennylane_remote_hardware/V8_PHASE9C_PENNYLANE_REMOTE_HARDWARE_PACK_2026-04-22.md)
- [Phase 9C PennyLane Remote Hardware PDF](./artifacts/v8/phase9c_pennylane_remote_hardware/v8_phase9c_pennylane_remote_hardware_pack_2026-04-22.pdf)
- [Phase 9C PennyLane Remote Hardware Data](./artifacts/v8/phase9c_pennylane_remote_hardware/v8_phase9c_pennylane_remote_hardware_data_2026-04-22.json)
- [PennyLane Hardware Counts Chart](./artifacts/v8/phase9c_pennylane_remote_hardware/charts/v8_phase9c_pennylane_remote_counts_2026-04-22.png)
- [PennyLane Hardware Parity Chart](./artifacts/v8/phase9c_pennylane_remote_hardware/charts/v8_phase9c_pennylane_remote_parity_2026-04-22.png)

What Phase 9C establishes:

- direct `PennyLane` hardware execution through `pennylane-qiskit`
- real IBM backend execution on `ibm_fez`
- Bell/control calibration remains directionally aligned
- compressed AI-feature circuits remain negative-parity on real hardware
- this closes the PennyLane hardware gap but is still not the final Bell-type
  semantic contextuality claim

## Integrated Technical Pack

Location:

- [`artifacts/integrated/v7_v8_claim_pack`](./artifacts/integrated/v7_v8_claim_pack)

Core artifacts:

- [Integrated V7 + V8 Claim Pack](./artifacts/integrated/v7_v8_claim_pack/INTEGRATED_V7_V8_CLAIM_PACK_2026-04-21.md)
- [Integrated V7 + V8 Claim Pack PDF](./artifacts/integrated/v7_v8_claim_pack/integrated_v7_v8_claim_pack_2026-04-21.pdf)
- [Integrated Summary Pack](./artifacts/integrated/v7_v8_claim_pack/V7_V8_INTEGRATED_SUMMARY_PACK_2026-04-21.md)
- [Integrated Summary Pack PDF](./artifacts/integrated/v7_v8_claim_pack/v7_v8_integrated_summary_pack_2026-04-21.pdf)

Why it matters:

This is the umbrella technical story. It ties the behavioral `V7` layer,
internal `V8` layer, and later phase findings back into one architecture frame.

## Public / Private Boundary

Public in this repo:

- white-paper style summaries
- posters and PDFs
- charts
- phase packs
- reviewed JSON result artifacts
- public-safe trace logs
- public roadmap and next-phase framing

Private outside this repo:

- backend scanner code
- mapper internals
- orchestration / administration paths
- transformer-runner implementation details
- unpublished private leverage stack
- hardware submission scripts and account credentials

## Related Repositories

- [Source-code-layer](https://github.com/renaissancefieldlite/Source-code-layer)
- [Codex-67-white-paper-](https://github.com/renaissancefieldlite/Codex-67-white-paper-)
- [Codex-67-white-paper-code-layers](https://github.com/renaissancefieldlite/Codex-67-white-paper-code-layers)
- [Hadamard_Proof](https://github.com/renaissancefieldlite/Hadamard_Proof)
- [M23_Proof](https://github.com/renaissancefieldlite/M23_Proof)
- [small-diophantine-lattice](https://github.com/renaissancefieldlite/small-diophantine-lattice)
- [renaissancefieldlitehrv1.0](https://github.com/renaissancefieldlite/renaissancefieldlitehrv1.0)
- [QuantumConsciousnessBridge](https://github.com/renaissancefieldlite/QuantumConsciousnessBridge)
