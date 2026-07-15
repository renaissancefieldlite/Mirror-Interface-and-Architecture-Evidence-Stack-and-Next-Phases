# Nest 3 Cross-Spectral Family Panel Read

Date: `2026-06-11`

Run ID: `nest3_cross_spectral_family_panel_2026-06-11`

Status: `real_data / public_spectral_sources / backup panel after THz exposure source gate`

## Purpose

The parked primary gate was a real Terahertz exposure-response dataset with
sham, off-window, and heat-matched controls. No such public source is seated in
this run. The exposure-response lane stays open.

This runner executes the backup lane: a larger public spectral panel using the
already seated NIST THz, NIST gas-phase IR, and NASA Ames Ramdb Raman evidence
rows, plus a new family-heldout IR check.

## Sources

| Source | Local basis | Public source surface |
| --- | --- | --- |
| NIST gas-phase IR | `nest3_second_spectral_nist_ir` | `https://webbook.nist.gov/chemistry/` |
| NIST THz Spectral Database | `nest3_terahertz_nist_thz` | `https://webbook.nist.gov/chemistry/thz-ir/` |
| NASA Ames Ramdb Raman | `nest3_ramdb_raman_udp` | `https://ramdb.spectra.tools/` |

Raw JCAMP / transition / source files remain in ignored local experiment data
folders. This public read records source hashes, scores, and controls only.

## New IR Family-Heldout Check

| Metric | Value |
| --- | ---: |
| Records | 32 |
| Observed AUC | 0.797619 |
| Observed balanced accuracy | 0.746032 |
| Shuffled-label mean AUC | 0.491647 |
| Shuffled-label p | 0.004975 |
| Band-position shuffle AUC | 0.611111 |
| Distribution-only AUC | 0.829365 |

Family-heldout folds:

| Heldout target | Heldout control | Records | Target / control | AUC | Balanced accuracy |
| --- | --- | ---: | ---: | ---: | ---: |
| `alcohol` | `alkane` | 12 | 6 / 6 | 0.638889 | 0.500000 |
| `aldehyde` | `aromatic` | 9 | 3 / 6 | 0.666667 | 0.833333 |
| `ketone` | `halocarbon` | 11 | 5 / 6 | 0.866667 | 0.900000 |

Read: the family-heldout IR contrast stays above shuffled labels, but
distribution-only features remain high. Treat this as spectral-family
continuation support, not pure band-position / phase-lock closeout.

## Cross-Panel Evidence Rows

| Lane | Row | Records | Score | Shuffle/control | p | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `NIST gas IR` | `six-family functional IR` | 32 | 0.588889 | 0.174944 | 0.004975 | support |
| `NIST THz` | `pharma vs non-pharma main-family THz` | 32 | 0.851852 | 0.519481 | 0.039801 | partial support |
| `NASA Ames Ramdb Raman` | `amino_acid_vs_mineral_405nm` | 22 | 0.950000 | 0.485733 | 0.003984 | support |
| `NASA Ames Ramdb Raman` | `pah_vs_amino_acid_405nm` | 12 | 1.000000 | 0.535222 | 0.035857 | support |


## Interpretation

This panel strengthens `Nest 3 / Waves / Spectra / Phase-Lock` as a
multi-source physical spectral lane:

- NIST gas-phase IR supports functional-family structure.
- NIST THz gives partial material-family support through a pharma-vs-non-pharma
  row while broad multiclass THz remains candidate.
- NASA Ames Ramdb Raman supports same-laser class-level transition-structure
  rows.
- The new IR family-heldout check tests generalization across heldout
  functional families and remains above label-shuffle controls.

## Boundary

This is not Terahertz biological exposure-response evidence. It is not medical
THz tuning and not cellular response. It is a larger public spectral-source
panel for the physical spectra lane.

The next clean THz-specific gate remains a real exposure-response dataset with
sham/off-window/heat-matched controls, or a local/partner instrument run with
source-on/source-off rows.

## Artifact Hashes

| Artifact | SHA-256 |
| --- | --- |
| `nest3_second_spectral_nist_gas_ir_functional_family_2026-05-27.json` | `531a348f2a6222b8b31d28a14c31a6377ce7e2c49a97ee72b7be8cf75bd950ec` |
| `nest3_terahertz_nist_material_family_2026-05-27.json` | `3aed368ee5f897e6ee96400e425fced8ed26baf39c67134c73ad528917a0e4c5` |
| `nest3_ramdb_raman_hard_controls_2026-05-24.json` | `9314aa7884c995f2800e830c86613198c747d81eca0b19e8d65598c40e4ea48e` |
