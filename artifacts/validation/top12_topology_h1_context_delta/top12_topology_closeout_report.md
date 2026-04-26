# TOP-1/2 Topology Closeout

Date: `2026-04-26T17:59:20.701200+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `mixed_partial_support`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- TDA backend: `ripser_available`
- TDA mode: `ripser_h1`
- role: `target_mean_context_delta`
- feature family: `context_delta`
- labels: `lattice_minus_neutral, lattice_minus_technical, technical_minus_neutral`
- max points per label: `0`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Points | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `not_control_supported` | `84` | `1.0` | `0.34331337325349304` | `0.0` | `2.6716413106711836` |
| `gemma_v8_hidden_point_cloud.npz` | `not_control_supported` | `126` | `0.36726546906187624` | `0.6347305389221557` | `3.6393446060779913` | `3.369767749705026` |
| `glm_v8_hidden_point_cloud.npz` | `not_control_supported` | `120` | `1.0` | `0.2435129740518962` | `0.0` | `2.2510880377123224` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `96` | `1.0` | `0.21756487025948104` | `0.0` | `1.4576220424795039` |
| `mistral_v8_hidden_point_cloud.npz` | `not_control_supported` | `96` | `1.0` | `0.24550898203592814` | `0.0` | `1.3109148927191654` |
| `nemotron_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `126` | `1.0` | `0.033932135728542916` | `0.0` | `6.415346041440496` |
| `qwen_v8_hidden_point_cloud.npz` | `not_control_supported` | `108` | `0.16367265469061876` | `0.8383233532934131` | `2.2475585842194725` | `1.1219155045894305` |
| `smollm3_v8_hidden_point_cloud.npz` | `not_control_supported` | `108` | `1.0` | `0.46706586826347307` | `0.0` | `1.1639473129588724` |

## Boundary

This closeout uses real exported V8 hidden-state point clouds only. `h0_mst` reads connectedness; `ripser_h1` reads loop / persistence profiles. Separation and invariance are both tested against shuffled-label controls.
