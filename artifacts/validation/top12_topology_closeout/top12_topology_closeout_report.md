# TOP-1/2 Topology Closeout

Date: `2026-04-26T01:39:36.684744+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `mixed_partial_support`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds`
- TDA backend: `h0_mst_only`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.996003996003996` | `0.004995004995004995` | `7.743672212592488` | `40.54456144944147` |
| `gemma_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.5694305694305695` | `0.43156843156843155` | `19.243840159456944` | `25.741451586281293` |
| `glm_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.9820179820179821` | `0.01898101898101898` | `7.56836795987939` | `27.54907735363322` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.6873126873126874` | `0.31368631368631367` | `45.886312974058356` | `114.50863549685319` |
| `mistral_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.6903096903096904` | `0.3106893106893107` | `34.07433009487382` | `107.21645127461434` |
| `nemotron_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `1.0` | `0.000999000999000999` | `0.7559646752636127` | `18.396562507513778` |
| `qwen_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.986013986013986` | `0.014985014985014986` | `6.493808042292307` | `27.360531288986373` |
| `smollm3_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.974025974025974` | `0.026973026973026972` | `5.939418782668065` | `27.92461757968908` |

## Boundary

This is an H0 connectedness closeout. Full persistent homology with H1 should be added only when a TDA backend and sufficiently rich point clouds are available.
