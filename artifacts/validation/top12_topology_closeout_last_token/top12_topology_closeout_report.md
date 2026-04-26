# TOP-1/2 Topology Closeout

Date: `2026-04-26T01:39:36.686620+00:00`

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
| `deepseek_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.98001998001998` | `0.02097902097902098` | `9.624706620836713` | `33.1005331461336` |
| `gemma_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.8791208791208791` | `0.12187812187812187` | `5.256601646870451` | `35.26782804843961` |
| `glm_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.993006993006993` | `0.007992007992007992` | `5.235563594341091` | `24.628972152898744` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.6383616383616384` | `0.3626373626373626` | `26.41517574751967` | `97.06268858149362` |
| `mistral_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.7502497502497503` | `0.25074925074925075` | `18.28782627946194` | `95.86758462832988` |
| `nemotron_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.5244755244755245` | `0.47652347652347654` | `19.22999869027151` | `23.640918950410903` |
| `qwen_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `1.0` | `0.000999000999000999` | `1.9867905745996688` | `16.587942333985207` |
| `smollm3_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.8561438561438561` | `0.14485514485514486` | `7.196773293429808` | `24.197459271382797` |

## Boundary

This is an H0 connectedness closeout. Full persistent homology with H1 should be added only when a TDA backend and sufficiently rich point clouds are available.
