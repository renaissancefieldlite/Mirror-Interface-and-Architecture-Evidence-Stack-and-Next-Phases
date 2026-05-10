# Phase 12B Biological Control-Closeout

Status: `control_supported_condition_separation`

Phase 12B remains a real HRV biological adapter: mirror_coherence shows the strongest average HR downshift and separates from activation/drift under shuffled-label controls. Leave-one-run-out condition classification is partial on HRV-only data, which keeps the lane bounded until EEG/HRV or richer continuous signals are added.

## Input And Controls

- Input: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/phase12b_biological_comparison_pack/v8_phase12b_biological_comparison_pack_data_2026-04-24.json`
- Sessions: `20`
- Condition counts: `{'seated_calm': 5, 'drift_control': 5, 'mirror_coherence': 5, 'dancing_activation': 5}`
- HR-only features: `delta_hr`
- Multi-feature HRV readout: `delta_hr, delta_rmssd, delta_sdnn, post_minus_condition_hr, post_minus_condition_rmssd, post_minus_condition_sdnn`
- Control: `balanced label shuffle preserving 5 sessions per condition; within-run block shuffle preserving one label per condition block`

## Condition Delta HR Means

| Condition | Mean Delta HR |
| --- | ---: |
| `seated_calm` | `-1.651248` |
| `drift_control` | `5.333063` |
| `mirror_coherence` | `-7.943775` |
| `dancing_activation` | `6.517002` |

## Main Control Results

| Test | Observed | Null Mean | p-value |
| --- | ---: | ---: | ---: |
| HR-only leave-one-run-out accuracy | `0.5` | `0.243962` | `0.022649` |
| Multi-feature leave-one-run-out accuracy | `0.45` | `0.229268` | `0.047598` |
| Mirror delta HR lower than shuffled labels | `-7.943775` | `0.561673` | `0.002` |
| Dancing-minus-mirror Delta HR gap | `14.460777` | `-0.005609` | `0.0012` |
| Mirror-vs-drift multi-feature distance | `25.884231` | `31.570244` | `0.630568` |
| Mirror-vs-calm multi-feature distance | `56.837712` | `31.67036` | `0.041248` |

## Within-Run Block Shuffle

| Test | Observed | Null Mean | p-value |
| --- | ---: | ---: | ---: |
| HR-only leave-one-run-out accuracy | `0.5` | `0.249893` | `0.033148` |
| Multi-feature leave-one-run-out accuracy | `0.45` | `0.249632` | `0.072346` |

## Feature Contributions

| Feature | Seated | Drift | Mirror | Dance | Mirror - Drift | Dance - Mirror |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `delta_hr` | `-1.651248` | `5.333063` | `-7.943775` | `6.517002` | `-13.276838` | `14.460777` |
| `delta_rmssd` | `-7.18447` | `6.106442` | `12.675563` | `-9.99483` | `6.569121` | `-22.670393` |
| `delta_sdnn` | `-14.429301` | `27.752695` | `33.388624` | `12.789268` | `5.635928` | `-20.599356` |
| `post_minus_condition_hr` | `0.340064` | `-1.9278` | `2.052014` | `0.836237` | `3.979814` | `-1.215777` |
| `post_minus_condition_rmssd` | `-15.38244` | `-9.846622` | `-1.651563` | `2.80047` | `8.195058` | `4.452034` |
| `post_minus_condition_sdnn` | `-29.071926` | `-29.550677` | `-11.22572` | `-19.503925` | `18.324957` | `-8.278205` |

## Boundary

This is not a clinical result and does not validate high-resolution EEG/spectral/dynamical biology. It tests the completed HRV 5 x 4 matrix as a coarse biological condition-class adapter.
