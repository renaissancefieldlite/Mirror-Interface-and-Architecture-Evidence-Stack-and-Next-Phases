# TOP-1/2 Topology Closeout

Date: `2026-04-26T17:59:20.703530+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `mixed_partial_support`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- TDA backend: `ripser_available`
- TDA mode: `ripser_h1`
- role: `target_window_token`
- feature family: `token_window`
- labels: `lattice, neutral, technical`
- max points per label: `80`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Points | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `not_control_supported` | `240` | `0.654485049833887` | `0.3488372093023256` | `3.38780758656243` | `4.771785908666731` |
| `gemma_v8_hidden_point_cloud.npz` | `not_control_supported` | `240` | `0.6378737541528239` | `0.3654485049833887` | `3.1074058196431307` | `3.868520296056815` |
| `glm_v8_hidden_point_cloud.npz` | `not_control_supported` | `240` | `0.3687707641196013` | `0.6345514950166113` | `5.905849751528688` | `5.461703563870515` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `240` | `0.5182724252491694` | `0.4850498338870432` | `2.35662385812707` | `2.6628655547690063` |
| `mistral_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `240` | `0.9867109634551495` | `0.016611295681063124` | `0.21648513344505144` | `2.010020857664374` |
| `nemotron_v8_hidden_point_cloud.npz` | `not_control_supported` | `240` | `0.8970099667774086` | `0.10631229235880399` | `2.1412581162590922` | `5.164671462810841` |
| `qwen_v8_hidden_point_cloud.npz` | `not_control_supported` | `240` | `0.7873754152823921` | `0.2159468438538206` | `1.3741893133923746` | `2.950067063347387` |
| `smollm3_v8_hidden_point_cloud.npz` | `not_control_supported` | `240` | `0.5813953488372093` | `0.4219269102990033` | `4.7545273022104935` | `5.683704617944718` |

## Boundary

This closeout uses real exported V8 hidden-state point clouds only. `h0_mst` reads connectedness; `ripser_h1` reads loop / persistence profiles. Separation and invariance are both tested against shuffled-label controls.
