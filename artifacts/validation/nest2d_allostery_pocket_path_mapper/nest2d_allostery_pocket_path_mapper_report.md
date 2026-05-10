# Nest 2D-2 Allostery Pocket / Path Mapper Report

- `status`: `allostery_pocket_path_partial_improved`
- `benchmark_rows`: `100`
- `scored_rows`: `98`
- `source_label_overlap_rows`: `98`
- `structures_available`: `98`
- `random_trials`: `500`

## Result

| Metric | Value |
| --- | ---: |
| Mirror pocket/path mean Jaccard | 0.032975 |
| Previous contact-only Mirror mean Jaccard | 0.013452 |
| Best existing AlloBench tool mean Jaccard | 0.197330 |
| Best existing tool | PASSer_Ensemble |
| Degree pocket mean Jaccard | 0.010861 |
| Closeness pocket mean Jaccard | 0.018515 |
| Active-proximity pocket mean Jaccard | 0.014508 |
| Random pocket mean Jaccard | 0.012007 |
| Random pocket p95 Jaccard | 0.079104 |
| Label-shuffle mean Jaccard | 0.017679 |
| Label-shuffle p95 Jaccard | 0.059189 |
| Random-control p-value | 0.001996 |
| Label-shuffle p-value | 0.001996 |

## Clean Read

Nest 2D-2 improves the biological representation: pocket/path scoring beats the first contact-only mapper and graph pocket controls, while the strongest existing AlloBench tool remains the higher closeout bar.

## What This Moves

- Upgrades the 2D object from residue top-k to pocket/path scoring.
- Uses chain-resolved active-site sources instead of matching active-site numbers across every chain.
- Keeps the same AlloBench/PDB benchmark surface, so the comparison is against the previous 2D graph run.
- Establishes whether geometric pocket/path scoring improves the allostery lane before adding external pocket tools.

## Next 2D-3 Upgrade

- add real pocket-tool candidates (`fpocket`, `P2Rank`, or `PrankWeb`) when locally available
- add ligand/contact pocket features from HETATM / binding-site geometry
- compare pocket-cluster recovery and communication-path recovery as separate metrics
- repeat on a second benchmark set if the same-100-PDB pocket/path run clears controls

## Artifacts

- row scores: `artifacts/validation/nest2d_allostery_pocket_path_mapper/nest2d_allostery_pocket_path_mapper_row_scores.csv`
- summary JSON: `artifacts/validation/nest2d_allostery_pocket_path_mapper/nest2d_allostery_pocket_path_mapper_summary.json`
