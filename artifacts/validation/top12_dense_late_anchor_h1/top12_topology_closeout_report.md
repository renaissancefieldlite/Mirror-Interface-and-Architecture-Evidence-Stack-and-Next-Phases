# TOP-1/2 Topology Closeout

Date: `2026-04-26T19:13:03.191425+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `not_control_supported_or_blocked`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_dense_trajectory`
- TDA backend: `ripser_available`
- TDA mode: `ripser_h1`
- role: `dense_prompt_token`
- feature family: `dense_trajectory`
- layer depth: `late`
- token region: `anchor_phrase`
- labels: `lattice, neutral, technical`
- max points per label: `0`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Points | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `glm_v8_hidden_point_cloud.npz` | `not_control_supported` | `378` | `0.8403193612774451` | `0.16167664670658682` | `4.608172173684546` | `9.369668287572301` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `297` | `0.13373253493013973` | `0.8682634730538922` | `17.00424398100229` | `9.714947478545849` |

## Boundary

This closeout uses real exported V8 hidden-state point clouds only. `h0_mst` reads connectedness; `ripser_h1` reads loop / persistence profiles. Separation and invariance are both tested against shuffled-label controls.
