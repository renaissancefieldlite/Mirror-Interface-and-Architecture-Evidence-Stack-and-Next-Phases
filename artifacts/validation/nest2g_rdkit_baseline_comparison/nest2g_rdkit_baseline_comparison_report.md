# Nest 2G RDKit Stronger Baseline Comparison Report

Status: `completed_multi_dataset_stronger_baseline_supported`

## Purpose

This pass checks whether the molecule-property lane survives stronger
descriptor / baseline comparisons, not just a single hand-built composite.

## Results

| Dataset | Rows | Composite abs r | Multifeature test abs r | RMSE improvement | p(abs r) | p(RMSE improvement) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ESOL` | `1128` | `0.558660` | `0.896224` | `0.552306` | `0.000999` | `0.000999` |
| `Lipophilicity` | `4200` | `0.204180` | `0.524267` | `0.148384` | `0.000999` | `0.000999` |
| `FreeSolv` | `642` | `0.395067` | `0.883146` | `0.534616` | `0.000999` | `0.000999` |
| `QM9_alpha` | `50000` | `0.083271` | `0.911784` | `0.589041` | `0.000999` | `0.000999` |

## Boundary

This is still a descriptor benchmark, not completed chemistry. It strengthens
the Nest 2C molecule-property result by adding held-out prediction and
shuffled-target controls.
