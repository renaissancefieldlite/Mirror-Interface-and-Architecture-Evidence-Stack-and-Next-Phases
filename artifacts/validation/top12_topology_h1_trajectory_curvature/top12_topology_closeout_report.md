# TOP-1/2 Topology Closeout

Date: `2026-04-26T17:59:20.698479+00:00`

## Purpose

This runner tests the missing Nest 1 topology lane only when real V8 hidden-state point clouds exist.

## Status

- overall status: `not_control_supported_or_blocked`
- point-cloud directory: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/point_clouds_expanded`
- TDA backend: `ripser_available`
- TDA mode: `ripser_h1`
- role: `target_mean_layer_curvature`
- feature family: `trajectory`
- labels: `lattice, neutral, technical`
- max points per label: `0`
- score read: `separation_p_value` tests real topology distances above shuffled labels; `invariance_p_value` tests real topology distances below shuffled labels

## Model Results

| Point Cloud | Status | Points | Separation p | Invariance p | Real Score | Null Mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `deepseek_v8_hidden_point_cloud.npz` | `not_control_supported` | `78` | `0.48502994011976047` | `0.5169660678642715` | `0.3349332500959489` | `0.5205397193277004` |
| `gemma_v8_hidden_point_cloud.npz` | `not_control_supported` | `120` | `0.3073852295409182` | `0.6946107784431138` | `1.0359888199211313` | `0.7524098963428673` |
| `glm_v8_hidden_point_cloud.npz` | `not_control_supported` | `114` | `0.0658682634730539` | `0.936127744510978` | `3.1153858349649464` | `1.256343785132208` |
| `hermes_v8_hidden_point_cloud.npz` | `not_control_supported` | `90` | `1.0` | `0.39520958083832336` | `0.0` | `0.2636343138650157` |
| `mistral_v8_hidden_point_cloud.npz` | `not_control_supported` | `90` | `0.5229540918163673` | `0.47904191616766467` | `0.014710177360969258` | `0.24134068225353789` |
| `nemotron_v8_hidden_point_cloud.npz` | `not_control_supported` | `120` | `0.5169660678642715` | `0.48502994011976047` | `0.04794850403507243` | `0.2828195930904364` |
| `qwen_v8_hidden_point_cloud.npz` | `not_control_supported` | `102` | `0.7684630738522954` | `0.23353293413173654` | `0.26662011302740957` | `0.850715128168669` |
| `smollm3_v8_hidden_point_cloud.npz` | `not_control_supported` | `102` | `0.7085828343313373` | `0.2934131736526946` | `0.06962929113830164` | `0.8268970041044994` |

## Boundary

This closeout uses real exported V8 hidden-state point clouds only. `h0_mst` reads connectedness; `ripser_h1` reads loop / persistence profiles. Separation and invariance are both tested against shuffled-label controls.
