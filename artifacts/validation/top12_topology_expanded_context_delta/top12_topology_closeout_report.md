# TOP-1/2 Topology Closeout

Date: `2026-04-26T17:32:26.923179+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `mixed_partial_support`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- TDA backend: `h0_mst_only`
- role: `target_mean_context_delta`
- feature family: `context_delta`
- labels: `lattice_minus_neutral, lattice_minus_technical, technical_minus_neutral`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `1.0` | `0.000999000999000999` | `3.2510156622404613` | `33.8028326687993` |
| `gemma_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.98001998001998` | `0.02097902097902098` | `3.5864679119967424` | `12.828061998329229` |
| `glm_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.962037962037962` | `0.03896103896103896` | `8.774593781269536` | `22.872228873301204` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.7892107892107892` | `0.21178821178821178` | `14.906320400650845` | `29.408172806505323` |
| `mistral_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.7612387612387612` | `0.23976023976023977` | `23.451001937666163` | `30.254067892218448` |
| `nemotron_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.955044955044955` | `0.04595404595404595` | `5.9743687258698355` | `16.430500332093477` |
| `qwen_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.999000999000999` | `0.001998001998001998` | `3.106546191590773` | `21.878022349213037` |
| `smollm3_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.5934065934065934` | `0.4075924075924076` | `18.11079113956072` | `21.19012776723276` |

## Boundary

This is an H0 connectedness closeout. Full persistent homology with H1 should be added only when a TDA backend and sufficiently rich point clouds are available.
