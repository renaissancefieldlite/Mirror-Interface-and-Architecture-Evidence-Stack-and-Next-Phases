# Nest 1 Remaining Lane Closeout

Status: `completed_remaining_lane_closeout`

Remaining Nest 1 lanes are now separated into real support, small-N partial transfer, and true data blockers. No remaining lane is left as vague pending real-data validation language.

## Lane Summary

| Lane | Status | Read |
| --- | --- | --- |
| `GEO-2` | `control_supported` | Expected bridge-pair relation is preserved above controls in the full, Phase 3, and Phase 5 subspaces; narrower context/overlap subspaces are weaker. |
| `DYN-2` | `control_supported` | The target/control trajectory does not merely peak late; its threshold crossing and center-of-mass are late relative to within-model random layer-order controls. |
| `OPT-1` | `limited_small_n_partial` | A real artifact selection objective can be evaluated over the three hardware-executed Phase 6 feature circuits, and Phase 6 selects the same best pair as hardware parity similarity. The sample is only three models, so this is a limited benchmark, not a closed optimization lane. |
| `CAT-1` | `limited_small_n_transfer_partial` | The Phase 6 feature relation transfers directionally into the Phase 9D hardware parity-vector relation for the three executed feature circuits, but the sample is too small to close CAT-1. |
| `TOP-1/2` | `blocked_raw_point_clouds_required` | export raw hidden-state vectors / point clouds, not only layer summaries and scalar deltas |
| `GRAPH-2` | `blocked_domain_graph_labels_required` | provide real pathway, attention-flow, allostery, grid, molecular, or other domain graph labels |
| `CTRL-1` | `blocked_lsps_transition_trace_required` | export LSPS / Oracle transition trace CSV with observed mode, expected mode, stability score, and drift/error columns |
| `GAME-1` | `blocked_adversarial_protocol_required` | define a real multi-agent, adversarial, or decision-theory benchmark artifact before scoring |

## GEO-2 Subspace Preservation

| Group | Status | Mean Expected Score | Expected Rank Avg | p(score >= obs) | p(rank <= obs) |
| --- | --- | ---: | ---: | ---: | ---: |
| `all` | `control_supported` | `0.271292` | `7.333333` | `0.007143` | `0.038095` |
| `phase3` | `control_supported` | `0.404831` | `7.333333` | `0.007143` | `0.019048` |
| `phase5` | `control_supported` | `0.305842` | `7.666667` | `0.030952` | `0.05` |
| `context_ratio` | `partial` | `0.43324` | `9.666667` | `0.054762` | `0.104762` |
| `overlap_anchor` | `partial` | `0.349374` | `9.333333` | `0.207143` | `0.12381` |

## DYN-2 Threshold / Regime Closeout

- Mean target center-of-mass fraction: `0.785372`
- Mean 75% threshold crossing fraction: `0.951439`
- Late 75% crossing count: `8/8`
- p(center >= observed): `5e-05`
- p(cross75 >= observed): `5e-05`
- p(late cross75 >= observed): `5e-05`

## OPT-1 / CAT-1 Limited Transfer

- OPT Phase 6 best pair: `Hermes/Mistral`
- OPT hardware best pair: `Hermes/Mistral`
- OPT random pair baseline probability: `0.333333`
- CAT Phase6-to-hardware similarity correlation: `0.893921`

These are real artifact transfer reads, but they are limited by the three-model hardware feature-circuit sample.

## Boundary

This closeout does not pretend blocked lanes are validated. It records the exact data surfaces needed to complete `TOP`, `GRAPH-2`, `CTRL`, and `GAME` later.