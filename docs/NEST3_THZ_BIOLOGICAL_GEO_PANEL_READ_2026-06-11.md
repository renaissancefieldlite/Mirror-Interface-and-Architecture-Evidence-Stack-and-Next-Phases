# Nest 3 THz Biological GEO Panel Read

Date: `2026-06-11`

Run ID: `nest3_thz_bio_geo_panel_2026-06-11`

Status: `biological_thz_geo_panel_scored_with_control_gaps`

## Gate State

This is the biology-facing Terahertz gate after the material spectra and
THz-TDS source/reference runs. The goal was simple: stop treating THz biology as
a future phrase and look for real public biological rows where THz exposure is
measured against control or sham biological samples.

The panel found and scored real GEO exposure-response rows. The result is
support-bearing at the panel level, but not a closeout. One source lands cleanly
under held-out biological replicates and exact label-permutation control; three
sources are candidate; three sources are weak or null under this strict read.

Plain English: the bridge now reaches actual biological THz response tables, not
only material spectra. The pattern is real enough to keep the lane open and
stronger than before, but the public sources do not yet provide a complete
heat-matched, off-window, frequency, power, duration, and temperature-control
matrix.

## Public Sources

NCBI GEO / GDS search query: `terahertz`

| Accession | Biological surface | State | Control | Rows | Read |
| --- | --- | --- | --- | ---: | --- |
| `GSE178729` | mouse neural culture | THz exposure | control | `6` samples | support-bearing |
| `GSE248763` | HUVEC cells | THz exposure | sham | `6` samples | candidate |
| `GSE41084` | mouse mesenchymal stem cells | 12h broadband THz | non-irradiated control | `6` samples | candidate |
| `GSE44671` | mouse skin | fs-THz irradiated | sham irradiated | `6` samples | candidate |
| `GSE243842` | C. elegans | 0.26 THz treated | control | `6` samples | weak/null under this scorer |
| `GSE41083` | mouse mesenchymal stem cells | 2h broadband THz | non-irradiated control | `6` samples | weak/null under this scorer |
| `GSE41085` | mouse mesenchymal stem cells | 2h single-frequency THz | non-irradiated control | `6` samples | weak/null under this scorer |

Additional inspected sources:

- `GSE23888`: mammalian stem-cell THz source with one two-channel
  treatment/control pair; useful provenance, not enough independent rows for
  this gate.
- `GSE250026`: HUVEC ATAC-seq THz/CON pair; too few independent rows for this
  gate.
- `GSE151549`: hiPSC THz source with `2` control and `2` THz samples; reserved
  for a later small-n source read, not scored in this 3x3 panel.

Raw GEO files are cached only under ignored local `experiments/**` paths. This
public read stores source names, URLs, row counts, aggregate scores, and control
outcomes only.

## Control Design

- `State`: THz-exposed biological sample rows.
- `Control`: control, sham, or non-irradiated biological sample rows.
- `Primary split`: leave one state sample and one control sample out, train on
  the remaining four samples, then score the held-out pair.
- `Feature discipline`: use expression features only; rank genes/features inside
  each training fold by the training-only effect.
- `Exact label control`: enumerate all balanced `3` vs `3` label assignments.
- `Feature-identity control`: shuffle feature identity within each sample and
  rerun the same score.
- `Gene-block control`: rerun on independent feature blocks to check whether the
  read is carried by one tiny feature slice.

## Result Summary

| Accession | Balanced accuracy | ROC AUC | Exact label p(AUC >= observed) | Feature-shuffle mean AUC | Class |
| --- | ---: | ---: | ---: | ---: | --- |
| `GSE178729` | `0.833333` | `0.950617` | `0.100000` | `0.582469` | support-bearing |
| `GSE248763` | `0.722222` | `0.839506` | `0.200000` | `0.551852` | candidate |
| `GSE41084` | `0.555556` | `0.765432` | `0.200000` | `0.474444` | candidate |
| `GSE44671` | `0.722222` | `0.740741` | `0.300000` | `0.539012` | candidate |
| `GSE243842` | `0.666667` | `0.604938` | `0.500000` | `0.533086` | weak/null |
| `GSE41083` | `0.222222` | `0.160494` | `0.900000` | `0.476296` | weak/null |
| `GSE41085` | `0.277778` | `0.197531` | `0.850000` | `0.473086` | weak/null |

## Support Read

This gate seats real biological THz exposure-response rows. That is the
important advancement. The lane is no longer only NIST spectra, Raman spectra,
or THz-TDS instrument traces; it now includes public biological expression
tables with THz/control or THz/sham rows.

`GSE178729` is the strongest source in this panel. Its THz/control split
survives held-out biological pairs with AUC `0.950617`, while feature-identity
shuffle falls to mean AUC `0.582469`. Exact balanced label permutation is
bounded by the small `3` vs `3` design, but the observed assignment remains at
the strong edge of the permutation set.

`GSE248763`, `GSE41084`, and `GSE44671` remain candidate biological support. They
show above-chance THz/control separation, but exact label controls do not
collapse hard enough to call them closeout evidence.

`GSE243842`, `GSE41083`, and `GSE41085` are weak or null under this particular
held-out expression-score read. That does not prove no biological effect exists
in those studies; it means this public-safe scorer did not recover a stable
held-out state/control separation from those tables.

## Boundary

This is biological source-gate support, not therapeutic proof and not a medical
THz tuning claim.

The public GEO rows do not yet close the exact gate requested by the Nest map:
sham/off-window, heat-matched, frequency, power, duration, and temperature
controls in one harmonized source matrix. Some public metadata includes useful
control details, such as adjacent controls and temperature kept at `26-27 C` in
the mMSC series, but the panel is still incomplete as a full physical-control
matrix.

## Next Gate

1. Build a harmonized THz biology manifest that extracts frequency, power,
   duration, temperature, sham/control type, organism, tissue/cell type, and
   assay type from each GEO source.
2. Run a pathway-level or shared-feature projection so cross-study holdout can
   test whether THz biology separates beyond one platform or one source family.
3. Add local/partner source-on/source-off THz or EMF capture rows with a
   source-disabled baseline, environment temperature, distance, power, duration,
   and instrument-state logging.
