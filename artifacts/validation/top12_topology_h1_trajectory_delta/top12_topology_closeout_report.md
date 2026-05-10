# TOP-1/2 Topology Closeout

Date: `2026-04-26T17:58:49.266443+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `mixed_partial_support`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- TDA backend: `ripser_available`
- TDA mode: `ripser_h1`
- role: `target_mean_layer_delta`
- feature family: `trajectory`
- labels: `lattice, neutral, technical`
- max points per label: `0`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Points | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `81` | `0.9640718562874252` | `0.03792415169660679` | `0.004184507707555603` | `0.6512452489669436` |
| `gemma_v8_hidden_point_cloud.npz` | `not_control_supported` | `123` | `0.5548902195608783` | `0.4471057884231537` | `0.8662792212107405` | `0.8015914111924728` |
| `glm_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `117` | `1.0` | `0.001996007984031936` | `0.02361260329083434` | `2.9919344570394037` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `93` | `0.38323353293413176` | `0.6187624750499002` | `1.0039354011988266` | `0.7248122785395058` |
| `mistral_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `93` | `0.9700598802395209` | `0.031936127744510975` | `0.02283737119360674` | `0.693530850602613` |
| `nemotron_v8_hidden_point_cloud.npz` | `not_control_supported` | `123` | `0.5469061876247505` | `0.4550898203592814` | `1.000140173187061` | `0.8196898965524713` |
| `qwen_v8_hidden_point_cloud.npz` | `not_control_supported` | `105` | `0.5229540918163673` | `0.47904191616766467` | `1.0103487613366127` | `1.0438707976822847` |
| `smollm3_v8_hidden_point_cloud.npz` | `not_control_supported` | `105` | `0.7964071856287425` | `0.2055888223552894` | `0.5314361218051993` | `1.1649805094319154` |

## Boundary

This closeout uses real exported V8 hidden-state point clouds only. `h0_mst` reads connectedness; `ripser_h1` reads loop / persistence profiles. Separation and invariance are both tested against shuffled-label controls.
