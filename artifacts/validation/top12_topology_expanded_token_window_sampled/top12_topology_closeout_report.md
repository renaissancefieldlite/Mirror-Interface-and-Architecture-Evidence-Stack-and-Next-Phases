# TOP-1/2 Topology Closeout

Date: `2026-04-26T17:38:48.831328+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `mixed_partial_support`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- TDA backend: `h0_mst_only`
- role: `target_window_token`
- feature family: `token_window`
- labels: `lattice, neutral, technical`
- max points per label: `120`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Points | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `not_control_supported` | `360` | `0.2217782217782218` | `0.7792207792207793` | `23.974022413246082` | `17.636618919030212` |
| `gemma_v8_hidden_point_cloud.npz` | `not_control_supported` | `360` | `0.7962037962037962` | `0.2047952047952048` | `7.319356691476803` | `16.121965564896534` |
| `glm_v8_hidden_point_cloud.npz` | `not_control_supported` | `360` | `0.8671328671328671` | `0.13386613386613386` | `5.124937518485384` | `8.814892071889965` |
| `hermes_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `360` | `0.962037962037962` | `0.03896103896103896` | `5.515382478023212` | `29.32565307801953` |
| `mistral_v8_hidden_point_cloud.npz` | `not_control_supported` | `360` | `0.7782217782217782` | `0.22277722277722278` | `14.188230390185089` | `22.049594297493744` |
| `nemotron_v8_hidden_point_cloud.npz` | `not_control_supported` | `360` | `0.3516483516483517` | `0.6493506493506493` | `25.175201458248512` | `22.18068775183522` |
| `qwen_v8_hidden_point_cloud.npz` | `not_control_supported` | `360` | `0.17682317682317683` | `0.8241758241758241` | `24.932440467875264` | `16.900380527101596` |
| `smollm3_v8_hidden_point_cloud.npz` | `not_control_supported` | `360` | `0.8301698301698301` | `0.17082917082917082` | `3.9971667173300767` | `6.4481390791610025` |

## Boundary

This is an H0 connectedness closeout. Full persistent homology with H1 should be added only when a TDA backend and sufficiently rich point clouds are available.
