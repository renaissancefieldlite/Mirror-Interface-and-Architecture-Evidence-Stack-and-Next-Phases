# Engine 02V RDKit Molecule Validation Fork

Status: `completed_real_molecule_signal_supported`

RDKit molecule-property validation completed with descriptor signal above shuffled-target controls.

## Requirements

- RDKit installed in the active Python environment
- real molecule dataset CSV with SMILES and target/property column
- declared baseline such as shuffled target or naive descriptor score

## Metrics

- `valid_rows`: `1128`
- `descriptor_target_pearson`: `-0.5587`
- `descriptor_target_abs_pearson`: `0.5587`
- `shuffled_baseline_pearson`: `-0.0007`
- `permutation_null_mean_abs_pearson`: `0.0243`
- `abs_pearson_shuffle_p`: `0.0002`
- `permutations`: `5000`
- `seed`: `67`

## Boundary

This is a cheminformatics validation fork only; interpretation depends on dataset quality and target meaning.
