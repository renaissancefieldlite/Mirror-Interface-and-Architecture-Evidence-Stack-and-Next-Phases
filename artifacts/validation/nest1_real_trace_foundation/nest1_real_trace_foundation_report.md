# Nest 1 Real-Trace Foundation Report

Status: `completed_bounded_evidence_pack`

Bounded Nest 1 foundation pass over existing AI and hardware artifacts; not a final universal-claim layer.

## Inputs

- `phase6`: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_data_2026-04-22.json`
- `phase2`: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/phase2_variance_pack/v8_phase2_variance_pack_data_2026-04-21.json`
- `phase5`: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/phase5_internal_bridge/v8_phase5_internal_bridge_pack_data_2026-04-22.json`
- `phase9d`: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/phase9d_pennylane_remote_repeat/v8_phase9d_pennylane_remote_repeat_data_2026-04-22.json`
- `residual_root`: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/v8/residual_stream_bridge/probe_results`

## Branch Results

| Branch | Status | Read | Key Metrics |
| --- | --- | --- | --- |
| `linear_algebra_geometry` | `real_trace_run` | Phase 6 normalized feature matrix supports PCA/SVD, pairwise distance, cosine, and bridge-pair checks. | models=8; features=12; top2_variance_ratio=0.612065; effective_rank=4.447033; expected_pairs_top2_hits=2/3; expected_pairs_mutual_nearest_hits=2/3 |
| `tensor_information` | `real_trace_run` | Model x feature matrix gives a real tensor/information summary, but raw activation tensors would strengthen this lane. | matrix_shape=[8, 12]; coordinates_basis_note=PCA coordinates written in feature matrix CSV. |
| `statistics_probability` | `real_trace_run` | Phase 2 rerun matrix remains the strongest real STAT/PROB surface. | model_count=8; exact_after_baseline_count=7; exact_after_baseline_models=['Mistral', 'Qwen', 'Gemma', 'DeepSeek', 'Hermes', 'GLM', 'SmolLM3']; only_live_variance_row=Nemotron; mean_target_std=1.222201; mean_last_std=4.584119; all_target_layers_stable=True; rerun_exact_rate=0.875 |
| `graph_topology_lite` | `real_trace_run_limited` | KNN graph over real feature vectors is a topology-lite pass; stronger topology needs raw hidden-state point clouds. | k=2; edge_count=12; component_count=1 |
| `topography_bridge` | `real_trace_run` | Phase 5 context-to-readout anchors give a real topographic bridge over internal model traces. | models=8; dominant_anchor_counts={'mid_window': 4, 'early_window': 3, 'last_token': 1}; path_archetype_counts={'late-context supported target': 3, 'front-context loaded': 2, 'readout-led': 1, 'late-context to readout bridge': 1, 'front-context to readout bridge': 1}; mean_overlap_jaccard=0.096703; mean_target_to_context=0.711626 |
| `dynamical_systems` | `real_trace_run` | Layerwise target/control delta trajectories provide a real dynamics-over-depth pass. | models=8; target_peak_layers={'DeepSeek': 26, 'Gemma': 41, 'GLM': 38, 'Hermes': 31, 'Mistral': 31, 'Nemotron': 40, 'Qwen': 34, 'SmolLM3': 34}; mean_target_peak_layer_fraction=0.981974 |
| `numerical_group_symmetry` | `real_hardware_run` | Phase 9D hardware repeatability gives a real numerical/backend and sign-symmetry surface. | circuits=7; sign_stable_circuits=7/7; phase6_feature_sign_stable=3/3 |
| `optimization` | `blocked_new_benchmark_needed` | Needs a declared mirror-guided optimization benchmark against naive/random/standard baselines. |  |
| `control_theory` | `blocked_trace_needed` | Needs exported real LSPS/Oracle transition traces. |  |
| `category_composition` | `design_lane` | Needs a measured transfer test showing structure preserved between two real nests. |  |

## Expected Bridge Pair Checks

| Pair | Distance | Rank L->R | Rank R->L | Mutual Nearest | Top-2 Both Ways |
| --- | ---: | ---: | ---: | --- | --- |
| Mistral/Hermes | 1.334634 | 1 | 1 | True | True |
| Qwen/DeepSeek | 3.367389 | 1 | 1 | True | True |
| GLM/Nemotron | 5.386827 | 5 | 4 | False | False |

## Phase 5 Topographic Bridge

| Model | Dominant Anchor | Dominant Layer | Archetype | Top-3 Sequence | Overlap Jaccard |
| --- | --- | ---: | --- | --- | ---: |
| Mistral | `mid_window` | 31 | late-context supported target | mid > pre > target | 0.230769 |
| Qwen | `early_window` | 34 | front-context loaded | early > pre > mid | 0.0 |
| Gemma | `last_token` | 41 | readout-led | last > mid > target | 0.0 |
| DeepSeek | `early_window` | 25 | front-context loaded | early > pre > mid | 0.066667 |
| Hermes | `mid_window` | 31 | late-context supported target | mid > pre > target | 0.333333 |
| GLM | `mid_window` | 38 | late-context to readout bridge | mid > pre > early | 0.142857 |
| Nemotron | `early_window` | 39 | front-context to readout bridge | early > mid > last | 0.0 |
| SmolLM3 | `mid_window` | 35 | late-context supported target | mid > early > pre | 0.0 |

## Hardware Sign Stability

| Circuit | Passes | Backends | Mean Parity | Std Parity | Sign Stable | Dominant Mode |
| --- | ---: | --- | ---: | ---: | --- | --- |
| `bell_phi_plus_xx` | 3 | ibm_fez,ibm_kingston | 0.979167 | 0.014731 | True | `11` |
| `bell_phi_plus_yy` | 3 | ibm_fez,ibm_kingston | -0.895833 | 0.038976 | True | `01` |
| `bell_phi_plus_zz` | 3 | ibm_fez,ibm_kingston | 0.927083 | 0.058926 | True | `11` |
| `phase6_feature_hermes` | 3 | ibm_fez,ibm_kingston | -0.677083 | 0.145087 | True | `10` |
| `phase6_feature_mistral` | 3 | ibm_fez,ibm_kingston | -0.6875 | 0.051031 | True | `10` |
| `phase6_feature_nemotron` | 3 | ibm_fez,ibm_kingston | -0.666667 | 0.145087 | True | `10` |
| `product_00_zz` | 3 | ibm_fez,ibm_kingston | 0.927083 | 0.014731 | True | `00` |

## Visual Evidence Pack

- PDF pack: [`nest1_real_trace_foundation_pack_2026-04-25.pdf`](./nest1_real_trace_foundation_pack_2026-04-25.pdf)
- Chart: [`nest1_phase6_pca_geometry.png`](./charts/nest1_phase6_pca_geometry.png)
- Chart: [`nest1_expected_bridge_pair_distances.png`](./charts/nest1_expected_bridge_pair_distances.png)
- Chart: [`nest1_phase5_anchor_topography.png`](./charts/nest1_phase5_anchor_topography.png)
- Chart: [`nest1_layer_dynamics_peaks.png`](./charts/nest1_layer_dynamics_peaks.png)
- Chart: [`nest1_phase9d_hardware_sign_stability.png`](./charts/nest1_phase9d_hardware_sign_stability.png)

## Boundary

This uses real exported V8 and hardware artifacts. Some lanes are limited by the currently exported scalar summaries and still need raw hidden-state point clouds, LSPS traces, or new benchmarks before stronger claims.

## Next Real Nest 1 Steps

1. If raw hidden-state vectors are available, rerun `GEO/TOP` on actual point clouds.
2. Build the unified `STAT/PROB/INFO/TENSOR` registry from completed phase packs.
3. Build a real `OPT-1` benchmark instead of treating optimization as mapped-only.
4. Export LSPS transition traces before claiming `CTRL-1` validation.
