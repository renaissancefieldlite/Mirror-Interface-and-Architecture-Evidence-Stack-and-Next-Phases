# Nest 2D-5 Ligand-Informed Split Mapper Report

- `status`: `ligand_informed_split_supported`
- `scored_rows`: `98`
- `folds`: `5`
- `random_trials`: `500`

## Result

| Metric | Value |
| --- | ---: |
| CV ligand-informed Mirror mean Jaccard | 0.260713 |
| 2D-4 structural-only blind mean Jaccard | 0.017703 |
| Best existing AlloBench tool mean Jaccard on scored rows | 0.201357 |
| Ligand-contact baseline mean Jaccard | 0.260713 |
| Degree pocket mean Jaccard | 0.008222 |
| Closeness pocket mean Jaccard | 0.015044 |
| Active-proximity pocket mean Jaccard | 0.016029 |
| Random candidate mean Jaccard | 0.016261 |
| Random-control p-value | 0.001996 |
| Label-shuffle p-value | 0.001996 |

## Clean Read

Nest 2D-5 supports the ligand-informed application branch: held-out ligand-informed pocket/path scoring matches the direct ligand-contact candidate baseline and beats the same-row AlloBench tool bar, graph controls, random controls, and shuffled-label controls.

## Boundary

This branch tests the ligand-bound application setting. Bound modulator geometry is treated as a real input surface, while folds still keep the scoring weights trained on separate rows from the held-out rows.

## Artifacts

- row scores: `artifacts/validation/nest2d_allostery_ligand_informed_split_mapper/nest2d_allostery_ligand_informed_split_mapper_row_scores.csv`
- fold scores: `artifacts/validation/nest2d_allostery_ligand_informed_split_mapper/nest2d_allostery_ligand_informed_split_mapper_fold_scores.csv`
- summary JSON: `artifacts/validation/nest2d_allostery_ligand_informed_split_mapper/nest2d_allostery_ligand_informed_split_mapper_summary.json`
