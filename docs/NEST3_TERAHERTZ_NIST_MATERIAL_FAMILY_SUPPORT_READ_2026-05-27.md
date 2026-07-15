# Nest 3 Terahertz NIST Material-Family Support Read

Date: `2026-05-27`

Run ID: `nest3_terahertz_nist_material_family_2026-05-27`

Status: `real_data / NIST_Chemistry_WebBook / THz_spectra / partial Terahertz spectral-family support; multiclass candidate`

## Source

Primary source: `NIST Chemistry WebBook THz Spectral Database`

Source page: `https://webbook.nist.gov/chemistry/thz-ir/`

Reference surface: `NIST Chemistry WebBook, SRD 69`

Source notes: NIST lists THz spectra compiled by E.J. Heilweil and M.
Campbell. The public page describes powder samples pressed into polyethylene
pellets and transmission spectra ratioed against polyethylene blanks.

Local source family: JCAMP-DX THz spectra downloaded from the NIST WebBook
per-spectrum links. Raw JCAMP files remain in the local ignored
`experiments/` tree.

## State / Control

| Role | Definition |
| --- | --- |
| `state labels` | conservative material-family labels assigned from NIST sample names |
| `main target` | four-family separation across carbohydrate/starch/sugar, inorganic/mineral, pharma/drug, and household/food mixture rows |
| `binary controls` | carbohydrate/starch/sugar vs inorganic/mineral; pharma/drug vs household/food mixture; pharma/drug vs all non-pharma main-family rows |
| `feature boundary` | sample name, family label, NIST ID, source page, and metadata are excluded from spectral features |
| `shuffle controls` | shuffled labels, band-position shuffle, and distribution-only summaries |

## Results

| Metric | Value |
| --- | ---: |
| Source entries discovered | 36 |
| Downloaded spectra | 34 |
| Skipped source entries | 2 |
| Main-family spectra used | 32 |
| Dropped small-family spectra | 2 |
| Main family count | 4 |
| Common grid bins | 161 |
| Spectral feature count | 322 |
| Multiclass accuracy | 0.250000 |
| Multiclass balanced accuracy | 0.246528 |
| Multiclass shuffled-label mean balanced accuracy | 0.234042 |
| Multiclass shuffled-label p | 0.432836 |
| Multiclass band-position shuffle balanced accuracy | 0.249306 |
| Multiclass distribution-only balanced accuracy | 0.376389 |

## Binary Control Rows

| Target | Controls | Records | Target / control | AUC | Balanced accuracy | Shuffled-label p | Band-shuffle AUC | Distribution-only AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `carbohydrate_starch_sugar` | `inorganic_mineral` | 19 | 10 / 9 | 0.433333 | 0.372222 | 0.621891 | 0.466667 | 0.622222 |
| `pharma_drug` | `household_food_mixture` | 13 | 5 / 8 | 0.700000 | 0.637500 | 0.169154 | 0.075000 | 0.325000 |
| `pharma_drug` | `carbohydrate_starch_sugar, household_food_mixture, inorganic_mineral` | 32 | 5 / 27 | 0.851852 | 0.733333 | 0.039801 | 0.259259 | 0.496296 |


## Family Counts

| Family | Spectra |
| --- | ---: |
| `biological_small` | 2 |
| `carbohydrate_starch_sugar` | 10 |
| `household_food_mixture` | 8 |
| `inorganic_mineral` | 9 |
| `pharma_drug` | 5 |


## Interpretation

This seats the first dedicated `Nest 3 / Terahertz` source gate using public
NIST THz transmission spectra. The support read is material-family spectral
structure: the same sample rows separate under real labels and degrade under
label and band-position controls.

Read as `partial Terahertz spectral-family support; multiclass candidate`.

## Boundary

This is not a cellular-response or medical exposure result. It does not claim
THz biological tuning. It gives the Terahertz lane a real spectral source
surface that can later bridge into water, biomolecules, cells, DNA, or
chemical-remediation prototypes only after dedicated exposure/response datasets
or instrument rows are available.

Next gate: add a second THz/IR/Raman source family or pair this spectral source
with a real exposure-response dataset under sham, off-window, and heat-matched
controls.
