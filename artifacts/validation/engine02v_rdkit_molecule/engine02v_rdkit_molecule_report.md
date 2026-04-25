# Engine 02V RDKit Molecule Validation Fork

Status: `blocked_missing_rdkit`

RDKit is not installed, so Engine 02V did not run. This is the correct stop condition for a physical-data validation fork.

## Requirements

- RDKit installed in the active Python environment
- real molecule dataset CSV with SMILES and target/property column
- declared baseline such as shuffled target or naive descriptor score

## Boundary

No physical chemistry validation was performed.
