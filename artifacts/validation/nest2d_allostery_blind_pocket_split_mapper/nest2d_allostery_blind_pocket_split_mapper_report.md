# Nest 2D-4 Blind Pocket Split Mapper Report

- `status`: `blind_pocket_split_open`
- `scored_rows`: `98`
- `folds`: `5`
- `random_trials`: `500`

## Result

| Metric | Value |
| --- | ---: |
| CV blind Mirror pocket/path mean Jaccard | 0.017703 |
| 2D-2 untuned pocket/path mean Jaccard | 0.032975 |
| Best existing AlloBench tool mean Jaccard on scored rows | 0.201357 |
| Degree pocket mean Jaccard | 0.008222 |
| Closeness pocket mean Jaccard | 0.015044 |
| Active-proximity pocket mean Jaccard | 0.015651 |
| Random candidate mean Jaccard | 0.014310 |
| Random-control p-value | 0.251497 |
| Label-shuffle p-value | 0.061876 |

## Clean Read

Nest 2D-4 sets the blind-CV boundary. Structural pocket/path features carry directional signal over simple graph controls, and the next closeout needs stronger pocket candidates or ligand-informed features.

## Boundary

This run tunes structural pocket/path feature weights on training folds and evaluates held-out rows using structural features only. It is the first blind split mapper after the ligand-contact feature-source diagnostic.

## Artifacts

- row scores: `artifacts/validation/nest2d_allostery_blind_pocket_split_mapper/nest2d_allostery_blind_pocket_split_mapper_row_scores.csv`
- fold scores: `artifacts/validation/nest2d_allostery_blind_pocket_split_mapper/nest2d_allostery_blind_pocket_split_mapper_fold_scores.csv`
- summary JSON: `artifacts/validation/nest2d_allostery_blind_pocket_split_mapper/nest2d_allostery_blind_pocket_split_mapper_summary.json`
