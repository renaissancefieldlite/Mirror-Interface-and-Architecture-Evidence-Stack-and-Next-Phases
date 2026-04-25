# Nest 1 Control-Closeout Pass

Status: `completed_local_control_closeout`

Explicit controls for the first four Nest 1 lanes. This strengthens the real-data evidence ladder but does not close every Nest 1 lane.

## Lane Summary

| Lane | Status | Headline |
| --- | --- | --- |
| `LA/GEO` | `control_supported` | Observed 2/3 mutual bridge-pair hits against exact shuffled-label null p=0.014286. |
| `STAT/PROB` | `control_supported` | Phase 2 / Phase 4 exact rerun structure tested against run-label permutation controls. |
| `NUM/GRP` | `control_supported` | Observed 7/7 sign-stable circuits against pass-shuffled null p=0.001. |
| `TOPOG` | `control_supported` | Phase 4 anchor/layer stability tested against random-anchor controls. |

## LA/GEO Shuffled-Label Control

- Observed mutual bridge-pair hits: `2/3`
- Observed top-2 reciprocal hits: `2/3`
- Exact permutations: `40320`
- Null mean mutual hits: `0.214286`
- p(mutual hits >= observed): `0.014286`
- p(top-2 hits >= observed): `0.052381`
- p(total pair distance <= observed): `0.009524`

| Pair | Distance | Rank L->R | Rank R->L | Mutual | Top-2 Both |
| --- | ---: | ---: | ---: | --- | --- |
| Mistral/Hermes | 1.334634 | 1 | 1 | True | True |
| Qwen/DeepSeek | 3.367389 | 1 | 1 | True | True |
| GLM/Nemotron | 5.386827 | 5 | 4 | False | False |

## STAT/PROB Rerun Permutation Controls

| Pack | Observed Exact Count | Null Mean | Null Max | p >= Observed |
| --- | ---: | ---: | ---: | ---: |
| Phase 2 target values | 7 | 0.01375 | 2 | 5e-05 |
| Phase 2 target layers | 8 | 0.07035 | 2 | 5e-05 |
| Phase 4 target values | 5 | 0.02245 | 2 | 5e-05 |
| Phase 4 dominant anchors | 6 | 0.4593 | 4 | 5e-05 |

## NUM/GRP Hardware Sign-Shuffle Control

- Observed sign-stable circuits: `7/7`
- Null mean stable sign circuits: `1.8495`
- Null max stable sign circuits: `7`
- p(stable signs >= observed): `0.001`

| Circuit | Signs | Mean Parity | Std Parity | Sign Stable |
| --- | --- | ---: | ---: | --- |
| `bell_phi_plus_xx` | `[1, 1, 1]` | 0.979167 | 0.014731 | True |
| `bell_phi_plus_yy` | `[-1, -1, -1]` | -0.895833 | 0.038976 | True |
| `bell_phi_plus_zz` | `[1, 1, 1]` | 0.927083 | 0.058926 | True |
| `phase6_feature_hermes` | `[-1, -1, -1]` | -0.677083 | 0.145087 | True |
| `phase6_feature_mistral` | `[-1, -1, -1]` | -0.6875 | 0.051031 | True |
| `phase6_feature_nemotron` | `[-1, -1, -1]` | -0.666667 | 0.145087 | True |
| `product_00_zz` | `[1, 1, 1]` | 0.927083 | 0.014731 | True |

## TOPOG Random-Anchor Controls

| Control | Observed Stable Count | Null Mean | Null Max | p >= Observed |
| --- | ---: | ---: | ---: | ---: |
| Phase 4 dominant anchors | 6 | 0.4488 | 4 | 5e-05 |
| Phase 4 dominant layers | 6 | 0.092 | 3 | 5e-05 |

Phase 5 context:

- dominant anchor counts: `{'mid_window': 4, 'early_window': 3, 'last_token': 1}`
- path archetype counts: `{'late-context supported target': 3, 'front-context loaded': 2, 'readout-led': 1, 'late-context to readout bridge': 1, 'front-context to readout bridge': 1}`

## Boundary

This pass closes explicit controls for the first four near-term Nest 1 lanes. `TOP`, `OPT`, `CTRL`, and `COMP/CAT` remain separate lanes with their own requirements.
