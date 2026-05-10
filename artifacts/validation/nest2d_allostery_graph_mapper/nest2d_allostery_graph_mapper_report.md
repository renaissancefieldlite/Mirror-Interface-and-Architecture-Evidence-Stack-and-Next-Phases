# Nest 2D Allostery Graph Mapper Report

- `status`: `allostery_mapper_open`
- `benchmark_rows`: `100`
- `source_label_overlap_rows`: `98`
- `structures_available`: `98`
- `scored_rows`: `98`
- `contact_cutoff_angstrom`: `8.0`
- `random_trials`: `500`

## Result

| Metric | Value |
| --- | ---: |
| Mirror mean Jaccard | 0.013452 |
| Best existing AlloBench tool mean Jaccard | 0.197330 |
| Best existing tool | PASSer_Ensemble |
| Degree mean Jaccard | 0.006597 |
| Closeness mean Jaccard | 0.017282 |
| Active-proximity mean Jaccard | 0.031329 |
| Random mean Jaccard | 0.014990 |
| Random p95 Jaccard | 0.052545 |
| Label-shuffle mean Jaccard | 0.017916 |
| Label-shuffle p95 Jaccard | 0.058513 |
| Random-control p-value | 0.722555 |
| Label-shuffle p-value | 1.000000 |

## Clean Read

Nest 2D remains open on this pass: graph controls and the best AlloBench tool stay above the current contact-only mapper. The useful result is that real AlloBench labels are now joined to real PDB contact graphs, so the next run can add pocket/pathway features without changing the benchmark surface.

## What This Proves

- The AlloBench source labels are now joined to the same `100` benchmark PDB rows used by the prior tool table.
- The run resolved `98` real PDB structures into residue-contact graphs and scored the mapper against independent allosteric-site labels.
- The current contact-only residue scorer leaves the Nest 2D closeout target at pocket, chain-mapped active-site, and pathway-level features.

## Next 2D-2 Upgrade

- add sequence-to-structure mapping so active-site residues are chain-resolved instead of broad residue-number matches
- build pocket candidates from local pocket tools or geometric residue clusters
- score active-site to allosteric-site communication paths instead of exact residue top-k only
- rerun against the same `100` PDB rows, the `PASSer_Ensemble` `0.19733` mean-Jaccard bar, and graph controls

## Method

The run joins the existing 100-row AlloBench benchmark table to the public `AlloBench.csv` residue labels. Each resolved PDB structure is parsed into a residue-contact graph using coordinate contacts. The mapper scores candidate allosteric residues by communication distance from active-site residues, local contact density, non-hub bridge position, and graph centrality. The same rows are compared against degree, closeness, active-proximity, random residue, and shuffled-label controls.

This is the Nest 2D mechanics pass: the Mirror Architecture rule is converted into an applied protein graph score, and the external allosteric labels decide whether that score has support.

## Artifacts

- row scores: `artifacts/validation/nest2d_allostery_graph_mapper/nest2d_allostery_graph_mapper_row_scores.csv`
- summary JSON: `artifacts/validation/nest2d_allostery_graph_mapper/nest2d_allostery_graph_mapper_summary.json`

## Source Data

- AlloBench source CSV: `artifacts/validation/datasets/allobench_source/AlloBench.csv`
- PDB structures: downloaded from RCSB into the ignored local cache `artifacts/validation/datasets/rcsb_pdb/`
