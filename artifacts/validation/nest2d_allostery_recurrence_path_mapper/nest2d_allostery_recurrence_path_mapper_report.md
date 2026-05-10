# Nest 2D-6 Allostery Recurrence / Path Mapper Report

- `status`: `ligand_informed_recurrence_and_path_supported`
- `scored_rows`: `98`
- `folds`: `5`
- `random_trials`: `500`
- `external_pocket_tools_available`: `{'fpocket': False, 'p2rank': False, 'prankweb': False}`

## Result

| Metric | Value |
| --- | ---: |
| 2D-6 alternate-split pocket Jaccard | 0.249009 |
| 2D-5 pocket Jaccard | 0.260713 |
| Best same-row AlloBench tool Jaccard | 0.201357 |
| Ligand-contact baseline Jaccard | 0.260713 |
| Degree pocket Jaccard | 0.008222 |
| Closeness pocket Jaccard | 0.015044 |
| Active-proximity pocket Jaccard | 0.016029 |
| Random pocket Jaccard | 0.015148 |
| Pocket random-control p-value | 0.001996 |
| Pocket label-shuffle p-value | 0.001996 |
| Mirror path-truth Jaccard | 0.211530 |
| Mirror path-truth recall | 0.345859 |
| Degree path-truth recall | 0.034344 |
| Closeness path-truth recall | 0.051651 |
| Active-proximity path-truth recall | 0.034921 |
| Random path-truth recall | 0.054600 |
| Path random-control p-value | 0.001996 |
| Path label-shuffle p-value | 0.001996 |

## Clean Read

Nest 2D-6 supports recurrence of the ligand-informed allostery branch and separates the mechanism: pocket recovery stays above the same-row tool bar and controls, while active-site to pocket path recovery also beats random and shuffled communication-path controls.

## Boundary

This gate separates two biological claims. Pocket recovery asks whether the predicted residue cluster overlaps known allosteric-site labels. Communication-path recovery asks whether the active-site to predicted-pocket corridor touches those labels more than graph controls. External pocket tools are recorded but not fabricated when unavailable locally.

## Artifacts

- row scores: `artifacts/validation/nest2d_allostery_recurrence_path_mapper/nest2d_allostery_recurrence_path_mapper_row_scores.csv`
- fold scores: `artifacts/validation/nest2d_allostery_recurrence_path_mapper/nest2d_allostery_recurrence_path_mapper_fold_scores.csv`
- summary JSON: `artifacts/validation/nest2d_allostery_recurrence_path_mapper/nest2d_allostery_recurrence_path_mapper_summary.json`
