# Nest 3 THz Source-Reference Gate Read

Date: `2026-06-11`

Run ID: `nest3_thz_source_reference_gate_2026-06-11`

Status: `weak_or_null`

## Gate State

This is the strengthening pass after the same-family spectral panel. The clean
target remains a real Terahertz biological exposure-response matrix with sham,
off-window, and heat-matched controls. That target is still open.

This run seats the next honest layer: real THz time-domain spectroscopy
sample/reference traces. A sample trace is a pulse that has passed through a
material or sample geometry; a reference trace is the matched baseline/reference
pulse for that measurement. That gives the lane real source/reference rows,
without pretending they are cellular treatment rows.

## Sources

| Pair | Source | Measurement label | Reference rows | Sample rows | Windows per role |
| --- | --- | --- | ---: | ---: | ---: |
| `sfeir_cp` | SfeirLab/MTMM-THz-TDS | CP carbon film / substrate example | `151` | `151` | `12` |
| `sfeir_h2o` | SfeirLab/MTMM-THz-TDS | H2O cuvette example | `1421` | `1422` | `28` |
| `sfeir_pa6` | SfeirLab/MTMM-THz-TDS | PA6 polymer example | `750` | `750` | `28` |
| `sfeir_ptfe` | SfeirLab/MTMM-THz-TDS | PTFE polymer example | `550` | `550` | `28` |
| `sfeir_sio2` | SfeirLab/MTMM-THz-TDS | SiO2 example | `1791` | `1791` | `28` |
| `sfeir_sno2` | SfeirLab/MTMM-THz-TDS | SnO2 example | `1260` | `1260` | `28` |
| `yale_pellet` | YaleTHz/nelly | Nelly figure 4 pellet pulse | `2838` | `4421` | `28` |
| `yale_two_layer_photo` | YaleTHz/nelly | Nelly figure 4 two-layer photo pulse | `2861` | `2861` | `28` |
| `yale_water_cuvette` | YaleTHz/nelly | Nelly figure 4 water-in-cuvette pulse | `5526` | `5528` | `28` |

Public source links:

- SfeirLab MTMM-THz-TDS: https://github.com/SfeirLab/MTMM-THz-TDS
- YaleTHz Nelly: https://github.com/YaleTHz/nelly

Raw payloads are cached only under ignored local `experiments/**/data/cache`
paths. The public read stores source names, URLs, row counts, hashes, and
aggregate scores only.

## Explanatory Read

This gate strengthens the THz bridge in the right order. The earlier same-family
spectral run showed that public physical spectra still carry state structure,
but it did not prove source-on/source-off response. Here we move one step closer
to that missing proof by using matched THz sample and reference traces from real
instrument workflows.

In plain English: the question is whether the instrument can tell when the THz
pulse went through the sample instead of the reference path. If that separation
survives material holdout and collapses under label shuffle, the source/reference
surface is real. If distribution-only or time-shuffled controls also stay high,
then the signal is not yet pure phase-order; it may still be carried by amplitude,
delay, attenuation, or broad waveform shape. That is still useful, but it stays
bounded.

The arc is preserved: physical spectra support is stronger; real THz
sample/reference support is now tested; biological THz exposure-response remains
the next proof gate rather than a claimed result.

## Control Design

- `State`: THz sample trace window.
- `Control`: matched THz reference trace window.
- `Primary split`: leave one material/sample pair out, train on the other pairs,
  test on the held-out pair.
- `Repository holdout`: train on one public source family and test on the other.
- `Collapse controls`: shuffled labels, time-order-shuffled windows,
  sorted/distribution-only windows, and distribution-only summary features.

## Result Summary

| Test | Balanced accuracy | ROC AUC | Notes |
| --- | ---: | ---: | --- |
| Observed leave-pair-out | `0.459746` | `0.474720` | held-out material/sample pair |
| Label shuffle control | `0.500992` | `0.494143` | p(AUC >= observed) `0.713147` across `250` repeats |
| Time-order shuffle | `0.542373` | `0.511670` | destroys local waveform ordering |
| Sorted distribution control | `0.550847` | `0.514184` | preserves value distribution, removes time order |
| Distribution-only control | `0.540254` | `0.510144` | summary statistics only |
| Cross-repository holdout | `0.529661` | `0.533378` | source-family holdout |

## Pair-Holdout Detail

| Held-out pair | Rows | Balanced accuracy | ROC AUC |
| --- | ---: | ---: | ---: |
| `sfeir_cp` | `24` | `0.500000` | `0.500000` |
| `sfeir_h2o` | `56` | `0.571429` | `0.515306` |
| `sfeir_pa6` | `56` | `0.303571` | `0.220663` |
| `sfeir_ptfe` | `56` | `0.267857` | `0.255102` |
| `sfeir_sio2` | `56` | `0.500000` | `0.441327` |
| `sfeir_sno2` | `56` | `0.571429` | `0.665816` |
| `yale_pellet` | `56` | `0.392857` | `0.448980` |
| `yale_two_layer_photo` | `56` | `0.500000` | `0.516582` |
| `yale_water_cuvette` | `56` | `0.553571` | `0.584184` |

## Cross-Repository Detail

| Held-out source | Rows | Balanced accuracy | ROC AUC |
| --- | ---: | ---: | ---: |
| `SfeirLab/MTMM-THz-TDS` | `304` | `0.536184` | `0.543066` |
| `YaleTHz/nelly` | `168` | `0.517857` | `0.523243` |

## Support Read

This cross-material / cross-repository source-reference pass is weak/null under
the hard transfer test. The observed leave-pair-out result did not beat the
shuffled-label control, and the repository-holdout result stayed near chance.

That is useful boundary information. It says there is not yet a universal
sample/reference signature that transfers cleanly across unrelated public THz-TDS
materials and repositories. The right follow-up is a repeated-scan
source/reference gate where the state/control rows come from matched instrument
replicates rather than unrelated material families.

## Boundary

This is not a biological exposure-response result. It is not a medical THz
tuning result. It is not a cellular demethylation claim. It is a public,
real-data THz-TDS source/reference support gate using matched sample and
reference traces.

## Next Gate

To promote the Terahertz cellular bridge, the next proof still needs one of:

1. sample-level biological THz exposure-response rows with sham, off-window,
   heat-matched, power, duration, frequency, and temperature controls;
2. local/partner source-on/source-off THz or EMF instrument captures with
   matched baseline and temperature logging;
3. a larger raw THz panel with external material/source-family holdouts and
   stronger phase/frequency controls.
