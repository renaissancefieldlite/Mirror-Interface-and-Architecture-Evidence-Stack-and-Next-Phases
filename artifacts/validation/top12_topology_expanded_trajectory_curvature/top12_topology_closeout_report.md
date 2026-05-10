# TOP-1/2 Topology Closeout

Date: `2026-04-26T17:32:26.923191+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `mixed_partial_support`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- TDA backend: `h0_mst_only`
- role: `target_mean_layer_curvature`
- feature family: `trajectory`
- labels: `lattice, neutral, technical`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.9920079920079921` | `0.008991008991008992` | `4.242544632148924` | `35.544009094263366` |
| `gemma_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.955044955044955` | `0.04595404595404595` | `2.474071128751293` | `10.958898309490722` |
| `glm_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.999000999000999` | `0.001998001998001998` | `2.9054173724791426` | `24.61728360777007` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.8201798201798202` | `0.18081918081918083` | `13.98684990353787` | `43.802665267906356` |
| `mistral_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.981018981018981` | `0.01998001998001998` | `1.5958538358935868` | `32.38607562508275` |
| `nemotron_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.9400599400599401` | `0.060939060939060936` | `7.505190552594493` | `27.44028161726909` |
| `qwen_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.97002997002997` | `0.030969030969030968` | `6.014423634462987` | `23.55231527749207` |
| `smollm3_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.981018981018981` | `0.01998001998001998` | `4.746520726680316` | `17.905411145471707` |

## Boundary

This is an H0 connectedness closeout. Full persistent homology with H1 should be added only when a TDA backend and sufficiently rich point clouds are available.
