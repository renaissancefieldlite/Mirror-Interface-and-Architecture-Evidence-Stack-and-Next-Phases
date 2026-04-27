# GRAPH-2 Quantum-Label Crosswalk

Status: `completed_internal_crosswalk_soft_positive_only`

Quantum-derived labels produced at least one soft-positive internal GRAPH-2 crosswalk, but no mode cleanly beat both degree baseline and shuffled-label controls.

## Best Mode

- `mode`: `phase6_amplitude_top3`
- `status`: `completed_soft_positive_no_shuffle_support`
- `positive_labels`: `3`
- `control_labels`: `25`
- `labeled_pair_count`: `28`
- `mirror_path_auc`: `0.74`
- `degree_baseline_auc`: `0.66`
- `mirror_minus_degree_auc`: `0.08`
- `mirror_path_auc_label_shuffle_p`: `0.177482`
- `degree_baseline_auc_label_shuffle_p`: `0.231277`

## Mode Summary

- `phase6_angle_top1`: status `completed_no_control_support`, mirror AUC `0.722222`, degree AUC `0.907407`, shuffle p `0.577642`
- `phase6_angle_top2`: status `completed_no_control_support`, mirror AUC `0.730769`, degree AUC `0.971154`, shuffle p `0.315968`
- `phase6_angle_top3`: status `completed_no_control_support`, mirror AUC `0.74`, degree AUC `0.773333`, shuffle p `0.168383`
- `phase6_angle_top4`: status `completed_no_control_support`, mirror AUC `0.75`, degree AUC `0.765625`, shuffle p `0.090591`
- `phase6_angle_top5`: status `completed_soft_positive_no_shuffle_support`, mirror AUC `0.63913`, degree AUC `0.626087`, shuffle p `0.270973`
- `phase6_amplitude_top1`: status `completed_no_control_support`, mirror AUC `0.722222`, degree AUC `0.907407`, shuffle p `0.577642`
- `phase6_amplitude_top2`: status `completed_no_control_support`, mirror AUC `0.730769`, degree AUC `0.807692`, shuffle p `0.324068`
- `phase6_amplitude_top3`: status `completed_soft_positive_no_shuffle_support`, mirror AUC `0.74`, degree AUC `0.66`, shuffle p `0.177482`
- `phase6_amplitude_top4`: status `completed_soft_positive_no_shuffle_support`, mirror AUC `0.75`, degree AUC `0.677083`, shuffle p `0.090591`
- `phase6_amplitude_top5`: status `completed_no_control_support`, mirror AUC `0.76087`, degree AUC `0.765217`, shuffle p `0.046895`
- `phase7_angle_top1`: status `completed_no_control_support`, mirror AUC `0.722222`, degree AUC `0.907407`, shuffle p `0.577642`
- `phase7_angle_top2`: status `completed_no_control_support`, mirror AUC `0.730769`, degree AUC `0.971154`, shuffle p `0.315968`
- `phase7_angle_top3`: status `completed_no_control_support`, mirror AUC `0.74`, degree AUC `0.773333`, shuffle p `0.168383`
- `phase7_angle_top4`: status `completed_no_control_support`, mirror AUC `0.75`, degree AUC `0.765625`, shuffle p `0.090591`
- `phase7_angle_top5`: status `completed_soft_positive_no_shuffle_support`, mirror AUC `0.63913`, degree AUC `0.626087`, shuffle p `0.270973`
- `phase7_amplitude_top1`: status `completed_no_control_support`, mirror AUC `0.722222`, degree AUC `0.907407`, shuffle p `0.577642`
- `phase7_amplitude_top2`: status `completed_no_control_support`, mirror AUC `0.730769`, degree AUC `0.807692`, shuffle p `0.324068`
- `phase7_amplitude_top3`: status `completed_soft_positive_no_shuffle_support`, mirror AUC `0.74`, degree AUC `0.66`, shuffle p `0.177482`
- `phase7_amplitude_top4`: status `completed_soft_positive_no_shuffle_support`, mirror AUC `0.75`, degree AUC `0.677083`, shuffle p `0.090591`
- `phase7_amplitude_top5`: status `completed_no_control_support`, mirror AUC `0.76087`, degree AUC `0.765217`, shuffle p `0.046895`
- `phase9_hardware_subset_mistral_hermes`: status `completed_no_control_support`, mirror AUC `0.722222`, degree AUC `0.907407`, shuffle p `0.577642`

## Boundary

This tests whether quantum bridge pair order can serve as an independent internal label source for the Phase 5 bridge graph. It does not validate external graph domains such as allostery, chemistry, grid flow, logistics, or molecular pathways.

## Next Requirement

GRAPH-2 still needs stronger independent labels from a real external or domain graph, or a richer attention-flow graph where labels are locked before scoring.
