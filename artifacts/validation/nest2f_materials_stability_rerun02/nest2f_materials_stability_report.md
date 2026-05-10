# Nest 2F Materials / Crystal Stability Validation Report

Status: `completed_real_materials_stability_supported`

## Inputs

- Dataset: Matbench `mp_e_form` / Materials Project-derived DFT formation energy
- Rows used after cleaning: `50000`
- Sample cap: `50000`

## Test

Fixed composition / structure descriptors were fit on a train split and
evaluated on a held-out test split against DFT formation energy.

Controls shuffled the formation-energy target while preserving descriptor
rows and the same train/test split.

## Result

- test Pearson: `0.568895`
- test absolute Pearson: `0.568895`
- test RMSE: `0.962665`
- mean-baseline RMSE: `1.170354`
- RMSE improvement fraction: `0.177458`
- shuffled abs Pearson mean: `0.007894`
- Pearson permutation p: `0.000999`
- RMSE-improvement permutation p: `0.000999`
- permutations: `1000`

## Boundary

This validates a real materials-property descriptor lane against DFT
formation energy. It does not claim completed crystal design, synthesis,
or universal materials prediction.
