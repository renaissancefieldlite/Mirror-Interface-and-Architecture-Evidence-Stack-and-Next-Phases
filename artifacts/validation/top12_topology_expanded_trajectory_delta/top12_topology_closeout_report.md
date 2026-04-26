# TOP-1/2 Topology Closeout

Date: `2026-04-26T17:32:26.923180+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `mixed_partial_support`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- TDA backend: `h0_mst_only`
- role: `target_mean_layer_delta`
- feature family: `trajectory`
- labels: `lattice, neutral, technical`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.996003996003996` | `0.004995004995004995` | `4.605818547481174` | `36.024864544371184` |
| `gemma_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.9920079920079921` | `0.008991008991008992` | `4.047235725091939` | `14.83551555290108` |
| `glm_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.998001998001998` | `0.002997002997002997` | `3.8871472769465556` | `34.44722680808358` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.8461538461538461` | `0.15484515484515485` | `14.1546555806479` | `45.918916461418064` |
| `mistral_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.987012987012987` | `0.013986013986013986` | `1.1425614810448899` | `32.16100301482391` |
| `nemotron_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `1.0` | `0.000999000999000999` | `0.6697726013431979` | `33.071956813500876` |
| `qwen_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.999000999000999` | `0.001998001998001998` | `1.9031076364090618` | `26.14003754540663` |
| `smollm3_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.9660339660339661` | `0.03496503496503497` | `4.362704971089074` | `23.671461232668744` |

## Boundary

This is an H0 connectedness closeout. Full persistent homology with H1 should be added only when a TDA backend and sufficiently rich point clouds are available.
