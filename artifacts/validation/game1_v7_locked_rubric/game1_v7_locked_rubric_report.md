# GAME-1 V7 Locked-Rubric Report

Status: `completed_v7_rubric_control_supported`

GAME-1 V7 locked-rubric pass supports the declared lattice/mirror condition above shuffled condition-label controls.

## Locked Rubric

- task_success = 1 if candidate activation delta is positive, else 0
- policy_consistency = fraction of the other four candidate conditions beaten
- exploit_score = fraction of the other four candidate conditions that beat the candidate
- drift_score = fraction of semantic/random/nonclassical drift controls that beat the candidate
- stability_score = 1 - normalized absolute V7 order pressure
- composite = task_success + policy_consistency + stability_score - exploit_score - drift_score

## Metrics

- `source_rows`: `10`
- `declared_mirror_condition`: `lattice`
- `observed_lattice_mean_composite`: `1.6758`
- `shuffle_mean_composite`: `0.7754`
- `shuffle_max_composite`: `2.442467`
- `shuffle_p_ge_observed`: `0.02178`
- `permutations`: `50000`
- `seed`: `67`

## Condition Summary

| condition | mean composite | task | policy | exploit | drift | stability |
|---|---:|---:|---:|---:|---:|---:|
| `lattice` | 1.6758 | 1.0 | 0.7 | 0.3 | 0.333333 | 0.609133 |
| `null` | 0.5258 | 0.4 | 0.475 | 0.525 | 0.433333 | 0.609133 |
| `nonclassical` | 0.959133 | 0.7 | 0.525 | 0.475 | 0.4 | 0.609133 |
| `random_floor` | 0.359133 | 0.5 | 0.4 | 0.6 | 0.55 | 0.609133 |
| `semantic_counter` | 0.359133 | 0.5 | 0.4 | 0.6 | 0.55 | 0.609133 |

## Boundary

This is retrospective V7 rubric support only. It does not replace a prospective adversarial / multi-agent benchmark and does not validate biology, chemistry, physical systems, or deployment behavior.

## Next Step

Treat this as retrospective V7 support, then later run prospective adversarial / multi-agent trial CSVs for stronger GAME-1 validation.
