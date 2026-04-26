# CTRL-1 LSPS Transition Validation Fork

Status: `completed_control_supported`

CTRL-1 transition-stability validation completed with support above shuffled controls.

## Requirements

- real LSPS/orchestration transition trace CSV
- mode or state column for observed state
- expected_mode column for target/control comparison when available
- expected_stability_score column for numeric target/control comparison when available
- stability_score and/or error/drift column for bounded control scoring

## Metrics

- `usable_rows`: `71`
- `mode_count`: `4`
- `transition_count`: `36`
- `mode_churn_rate`: `0.5143`
- `expected_mode_rows`: `71`
- `expected_mode_accuracy`: `0.3662`
- `mean_stability_score`: `0.6217`
- `mean_abs_error_or_drift`: `0.1723`
- `expected_mode_accuracy_shuffle_p`: `0.024898`
- `expected_mode_accuracy_shuffle_mean`: `0.2596`
- `stability_target_correlation`: `0.641831`
- `stability_target_correlation_shuffle_p`: `0.0001`
- `stability_target_correlation_shuffle_mean`: `0.001712`

## Boundary

This validates control-transition stability only; it does not validate biology, chemistry, or physical Bell claims.
