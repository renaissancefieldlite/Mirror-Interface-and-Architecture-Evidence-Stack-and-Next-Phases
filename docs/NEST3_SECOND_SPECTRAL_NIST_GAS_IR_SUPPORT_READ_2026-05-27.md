# Nest 3 Second Spectral NIST Gas IR Support Read

Date: `2026-05-27`

Run ID: `nest3_second_spectral_nist_gas_ir_functional_family_2026-05-27`

Status: `real_data / NIST_Chemistry_WebBook / gas_phase_IR_spectra / second spectral-family functional IR support`

## Source

Primary source: `NIST Chemistry WebBook gas-phase infrared spectra`

Source page: `https://webbook.nist.gov/chemistry/`

Reference surface: `NIST Chemistry WebBook, SRD 69` and NIST/EPA Gas-Phase Infrared Database
rows exposed through public WebBook JCAMP-DX spectrum links.

Local source family: public NIST IR JCAMP-DX spectra downloaded from WebBook
per-compound pages. Raw JCAMP files remain in the local ignored
`experiments/` tree.

## State / Control

| Role | Definition |
| --- | --- |
| `state labels` | conservative functional-family labels assigned from selected NIST compounds |
| `main target` | six-family separation across alcohol, aldehyde, ketone, alkane, aromatic, and halocarbon gas-phase rows |
| `binary controls` | oxygenated vs hydrocarbon/halocarbon; carbonyl vs alcohol; halocarbon vs hydrocarbon |
| `feature boundary` | compound name, family label, NIST ID, formula, source URL, and metadata are excluded from spectral features |
| `spectral grid` | `720-3700 cm^-1` common grid with absorbance bins plus first-derivative bins |
| `shuffle controls` | shuffled labels, band-position shuffle, and distribution-only summaries |

## Results

| Metric | Value |
| --- | ---: |
| Source compounds requested | 34 |
| Downloaded spectra | 32 |
| Skipped compounds | 2 |
| Functional families | 6 |
| Common grid bins | 299 |
| Spectral feature count | 598 |
| Multiclass accuracy | 0.625000 |
| Multiclass balanced accuracy | 0.588889 |
| Multiclass shuffled-label mean balanced accuracy | 0.174944 |
| Multiclass shuffled-label p | 0.004975 |
| Multiclass band-position shuffle balanced accuracy | 0.277778 |
| Multiclass distribution-only balanced accuracy | 0.500000 |

## Binary Control Rows

| Contrast | Target families | Control families | Records | Target / control | AUC | Balanced accuracy | Shuffled-label p | Band-shuffle AUC | Distribution-only AUC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `oxygenated_vs_nonoxygenated` | `alcohol, aldehyde, ketone` | `alkane, aromatic, halocarbon` | 32 | 14 / 18 | 0.928571 | 0.936508 | 0.004975 | 0.876984 | 0.853175 |
| `carbonyl_vs_alcohol` | `aldehyde, ketone` | `alcohol` | 14 | 8 / 6 | 0.770833 | 0.583333 | 0.084577 | 0.312500 | 0.520833 |
| `halocarbon_vs_hydrocarbon` | `halocarbon` | `alkane, aromatic` | 18 | 6 / 12 | 0.888889 | 0.875000 | 0.009950 | 0.541667 | 1.000000 |


## Family Counts

| Family | Spectra |
| --- | ---: |
| `alcohol` | 6 |
| `aldehyde` | 3 |
| `alkane` | 6 |
| `aromatic` | 6 |
| `halocarbon` | 6 |
| `ketone` | 5 |


## Interpretation

This seats a second physical spectral-family source gate for `Nest 3` using
public NIST gas-phase IR spectra. It is independent from the prior NIST THz
gate and tests whether a different spectral measurement family carries
functional-state structure under label and band-position controls.

Read as `second spectral-family functional IR support`.

## Boundary

This is not a Terahertz exposure-response result and not biological-response
support. It strengthens the `Native spectra / IR / Raman / THz` lane as a
spectral-source layer. The binary rows show useful contrasts but also preserve
some distribution-level separability, so the strongest read stays on the
multiclass functional IR support row. Terahertz cellular or medical claims
remain behind a dedicated exposure-response dataset with sham, off-window, and
heat-matched controls.

Next gate: either source a real THz exposure-response dataset or harden this IR
row with a larger NIST panel and family-heldout / scaffold-heldout controls.
