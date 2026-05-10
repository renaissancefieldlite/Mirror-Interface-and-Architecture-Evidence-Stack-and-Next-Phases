# TOP-1/2 Topology Closeout

Date: `2026-04-26T19:13:03.191426+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `control_supported`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_dense_trajectory`
- TDA backend: `ripser_available`
- TDA mode: `h0_mst`
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
| `glm_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `378` | `1.0` | `0.001996007984031936` | `0.6506058067744295` | `4.6536637250448525` |
| `hermes_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `297` | `0.9700598802395209` | `0.031936127744510975` | `3.025801787066807` | `19.74686226211736` |

## Boundary

This closeout uses real exported V8 hidden-state point clouds only. `h0_mst` reads connectedness; `ripser_h1` reads loop / persistence profiles. Separation and invariance are both tested against shuffled-label controls.
