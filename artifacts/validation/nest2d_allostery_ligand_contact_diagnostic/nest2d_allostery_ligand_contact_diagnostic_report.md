# Nest 2D-3 Allostery Ligand-Contact Diagnostic

- `status`: `ligand_contact_mapping_supported`
- `source_rows_in_benchmark`: `98`
- `scored_rows`: `94`
- `contact_cutoff_angstrom`: `5.0`

## Result

| Metric | Value |
| --- | ---: |
| Mean ligand-contact Jaccard | 0.263504 |
| Median ligand-contact Jaccard | 0.230952 |
| Rows >= 0.2 Jaccard | 56 |
| Rows >= 0.5 Jaccard | 12 |
| Best existing AlloBench tool mean Jaccard | 0.197330 |

## Clean Read

Bound-ligand contact geometry recovers the AlloBench allosteric labels above the strongest mean-Jaccard tool bar, confirming that the labels and structures align as real pocket/contact objects. This is a feature-source diagnostic for the next blind allosteric prediction closeout.

## Boundary

This diagnostic uses bound ligand/contact geometry present in the PDB files. It validates that the allosteric labels map onto real pocket/contact structure and supplies a strong feature source for the next blind allosteric-site mapper.

## Artifacts

- row scores: `artifacts/validation/nest2d_allostery_ligand_contact_diagnostic/nest2d_allostery_ligand_contact_diagnostic_row_scores.csv`
- summary JSON: `artifacts/validation/nest2d_allostery_ligand_contact_diagnostic/nest2d_allostery_ligand_contact_diagnostic_summary.json`
