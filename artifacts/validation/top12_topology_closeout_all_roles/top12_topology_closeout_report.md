# TOP-1/2 Topology Closeout

Date: `2026-04-26T01:39:36.685559+00:00`

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
| `deepseek_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.9660339660339661` | `0.03496503496503497` | `6.678223705986365` | `29.535905779794337` |
| `gemma_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.7382617382617382` | `0.2627372627372627` | `4.811041604256854` | `37.95850327042981` |
| `glm_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `0.986013986013986` | `0.014985014985014986` | `4.8656243231701914` | `21.844083382026867` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.5074925074925075` | `0.4935064935064935` | `28.21915446658121` | `53.97563875677747` |
| `mistral_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.5234765234765235` | `0.4775224775224775` | `23.543420606619215` | `55.43810886222728` |
| `nemotron_v8_hidden_point_cloud.npz` | `not_control_supported` | `0.3156843156843157` | `0.6853146853146853` | `15.204504522844356` | `13.874253460092085` |
| `qwen_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `1.0` | `0.000999000999000999` | `2.183425236035665` | `13.310673912986122` |
| `smollm3_v8_hidden_point_cloud.npz` | `topology_invariance_supported` | `1.0` | `0.000999000999000999` | `2.0381642780170055` | `13.163698288682161` |

## Boundary

This is an H0 connectedness closeout. Full persistent homology with H1 should be added only when a TDA backend and sufficiently rich point clouds are available.
