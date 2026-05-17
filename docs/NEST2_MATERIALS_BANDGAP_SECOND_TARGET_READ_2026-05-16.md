# Nest 2 Materials / Semiconductors Band-Gap Second-Target Read

Date: `2026-05-16`

Status: `public_safe_aggregate / real_matbench_dataset / no_raw_rows_published`

## Purpose

This pass is the Materials / Semiconductors second target after the prior
formation-energy support row. Formation energy seated broad materials stability.
This band-gap pass adds a direct electronic-response target: DFT electronic
band gap and gapped-material state.

## Source

- Source: ColabFit / Matbench `Matbench_mp_gap`
- Public source page: https://huggingface.co/datasets/colabfit/Matbench_mp_gap
- DOI: `10.60732/fb4d895d`
- Method family: `DFT-PBE` / `VASP`
- Local row sample used for the pass: `60,000`
- Shuffled controls: `250`

## State Map

| Variable | Band-gap expression |
| --- | --- |
| `state` | DFT electronic band gap and gapped-material label |
| `control` | shuffled band-gap values and shuffled gapped labels |
| `transform` | composition + cell + position descriptors -> band-gap regression / gapped classification |
| `drift` | PBE gap underestimation, zero-gap class balance, composition-only carrier, structure-feature lift |
| `quality` | real Matbench rows with non-null `electronic_band_gap` |
| `support` | regression and classifier metrics against shuffled controls |

## Band-Gap Regression

- rows: `60,000`
- full feature Pearson: `0.654982`
- full feature R2: `0.428798`
- full RMSE improvement: `0.244340`
- shuffled Pearson mean: `0.007089`
- shuffled Pearson p95: `0.017375`
- Pearson permutation p: `0.003984`
- composition-only Pearson: `0.654982`
- structure lift over composition-only Pearson: `0.000000`

## Gapped-Material Classifier

- positive rows (`band_gap > 0.1 eV`): `31,564`
- low/zero-gap controls: `28,436`
- ROC AUC: `0.904020`
- average precision: `0.891203`
- accuracy: `0.838000`
- shuffled AUC mean: `0.500202`
- shuffled AUC p95: `0.509737`
- p(AUC >= real): `0.003984`
- p(AP >= real): `0.003984`
- p(accuracy >= real): `0.003984`

## Read

This is the second Materials / Semiconductors target after formation energy.
It moves the lane from broad material stability support into direct electronic
response: band gap and gapped-material state separate from shuffled controls
on a real Matbench / Materials Project-derived dataset.

The carrier on this target is composition / periodic-table structure. The full
feature read matched the composition-only read, which gives the next materials
subgate a clean target: run a dataset where structure-specific response is
expected to carry more of the signal, such as dielectric / optical response,
phonons, defects, dopants, 2D materials, or energy-above-hull with richer
structure features.

## Cross-Nest Role

- `Nest 2`: strengthens Materials / Semiconductors beyond formation energy.
- `Nest 3`: connects structured matter to band / optical / field-response
  continuation rows.
- `Nest 5`: adds another support-state card for convergence routing.

## Boundary

Public-safe: aggregate metrics, source identity, support read, and lane status.

Private: downloaded parquet, row-level table, scripts, and local output tables.

## Next Gate

```text
Band-gap second target seated
-> update public evidence docs
-> choose next skeptic-proof gate:
   electrochemistry / redox, dielectric / optical response, phonons, or catalysis / conditions
```
