# OPT-1 Perspective-Nest Benchmark

Status: `completed_condition_optimization_supported_hardware_partial`

OPT-1 is no longer pending real-data validation: the V7 perspective condition-selection objective is control-supported, while the Phase 6 -> Phase 9D hardware pair-selection objective agrees but remains small-N partial.

## Behavioral Condition Optimization

- `source`: `artifacts/validation/game1_v7_locked_rubric/game1_v7_locked_rubric_report.json`
- `declared_selector`: `lattice`
- `observed_mean_composite`: `1.6758`
- `shuffle_mean_composite`: `0.7754`
- `shuffle_p_ge_observed`: `0.02178`
- `status`: `completed_v7_rubric_control_supported`

## Hardware Pair Optimization

- `source_phase6`: `artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_data_2026-04-22.json`
- `source_phase9d`: `artifacts/v8/phase9d_pennylane_remote_repeat/v8_phase9d_pennylane_remote_repeat_data_2026-04-22.json`
- `hardware_models`: `Hermes, Mistral, Nemotron`
- `phase6_best_pair`: `Hermes/Mistral`
- `hardware_best_pair`: `Hermes/Mistral`
- `best_pair_agreement`: `1`
- `random_pair_baseline_probability`: `0.333333`
- `status`: `small_n_partial`

| pair | phase6 feature similarity | hardware parity similarity |
|---|---:|---:|
| `Hermes/Mistral` | 0.432328 | 0.855954 |
| `Hermes/Nemotron` | 0.121684 | 0.673342 |
| `Mistral/Nemotron` | 0.119611 | 0.756579 |

## Boundary

This validates a real optimization benchmark over existing artifacts. The condition-selection objective is supported; the hardware pair-selection objective is useful but limited by the three hardware-executed feature circuits.

## Next Step

Use this OPT-1 result as condition-optimization support, then expand the hardware pair objective with more executed feature circuits or move to CAT-1 composition / transfer scoring.
