# OPT-1 Perspective-Nest Benchmark

Date: 2026-04-27

## Purpose

`OPT-1` should not be claimed from score schema alone. The lane needs a real
objective, a declared selector, and a baseline.

This benchmark treats optimization through the perspective-nest lens:

- behavioral / condition perspective: choose the condition that optimizes the
  locked V7 decision-stability composite
- hardware bridge perspective: choose the encoded model pair that transfers
  from Phase 6 feature geometry into Phase 9D hardware parity similarity

## Benchmark A: V7 Condition Selection

Source:

`artifacts/validation/game1_v7_locked_rubric/game1_v7_locked_rubric_report.json`

Objective:

maximize the locked composite:

`task_success + policy_consistency + stability_score - exploit_score - drift_score`

Declared Mirror selector:

`lattice`

Control:

shuffled condition-label null over the same V7 model rows.

Closure:

supported if the declared `lattice` selector beats shuffled condition labels at
`p <= 0.05`.

## Benchmark B: Phase 6 -> Phase 9D Hardware Pair Selection

Source:

- `artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_data_2026-04-22.json`
- `artifacts/v8/phase9d_pennylane_remote_repeat/v8_phase9d_pennylane_remote_repeat_data_2026-04-22.json`

Objective:

select the model pair whose Phase 6 feature similarity predicts the strongest
Phase 9D hardware parity-vector similarity among hardware-executed feature
circuits.

Boundary:

this remains small-N because only three feature circuits were executed on the
Phase 9D hardware path. Agreement is useful, but it cannot close `OPT-1` alone.

## Status Rule

If Benchmark A closes and Benchmark B agrees only at small-N, `OPT-1` is marked:

`completed_condition_optimization_supported_hardware_partial`

That means optimization is no longer pending real-data validation, but the hardware-transfer
optimization lane still needs a larger executed sample.
