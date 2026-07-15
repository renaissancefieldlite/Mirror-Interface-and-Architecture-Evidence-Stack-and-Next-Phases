# Nest 3 THz Replicate Source-Reference Gate Read

Date: `2026-06-11`

Run ID: `nest3_thz_replicate_source_reference_gate_2026-06-11`

Status: `support_bearing_replicate_source_reference_with_nuisance_caveat`

## Gate State

This run strengthens the Terahertz lane with repeated real THz-TDS scan files.
It uses `30` Fe10nm-on-MgO sample scans and `30` matched MgO substrate/reference
scans from the public `xpA076/THz` substrate-referenced THz-TDS folder.

This is still not the biological THz exposure-response closeout. It is a
replicate-level instrument source/reference gate: can the measured sample trace
be separated from the matched reference trace across held-out scan blocks?

## Source

| Source | Public URL | Rows used | State | Control |
| --- | --- | ---: | --- | --- |
| `xpA076/THz` substrate-referenced THz-TDS data | https://github.com/xpA076/THz/tree/master/scripts/from_paper/SubstrateReferencedTDS | `60` scan files | Fe10nm-on-MgO sample trace | MgO substrate/reference trace |

Raw scan files are cached only under ignored local `experiments/**/data/cache`
paths. The public read stores source names, URLs, hashes, row counts, and
aggregate scores only.

## Explanatory Read

The previous public THz sample/reference pass was intentionally hard: train on
one material/source family and test on another. That did not transfer cleanly.
This repeated-scan gate asks the cleaner instrument question instead: given
multiple scans from one substrate-referenced THz-TDS setup, does the sample path
separate from the matched reference path when scan indices are held out?

The answer is yes, strongly. The held-out scan blocks separate at AUC
`1.000000` with balanced accuracy `1.000000`,
while shuffled labels collapse near chance with p `0.003984`.

The caveat is equally important. Shape-only, time-shuffled, distribution-only,
and amplitude-only controls also remain high. That means this is not yet a pure
phase-order or frequency-specific biological response. The instrument is reading
a robust sample/reference difference, but that difference can be carried by
amplitude, attenuation, delay, sensitivity scaling, broad waveform shape, or
other measurement-path effects.

Plain English: this seats a real THz-TDS instrument support row. It does not
pretend to be cellular THz biology. It makes the bridge stronger and tells us
the next exact proof: source-on/source-off or biological exposure-response rows
with heat, sham, frequency, power, duration, and temperature controls.

## Control Design

- `State`: Fe10nm-on-MgO sample scan.
- `Control`: MgO substrate/reference scan.
- `Primary split`: five held-out scan-index blocks, preserving paired sample
  and reference indices.
- `Chronological split`: train on scan indices `0-19`; test on held-out indices
  `20-29`.
- `Collapse controls`: shuffled labels, shape-only features, time-order-shuffled
  traces, distribution-only summaries, and amplitude-only summaries.

## Result Summary

| Test | Balanced accuracy | ROC AUC | Notes |
| --- | ---: | ---: | --- |
| Observed scan-block holdout | `1.000000` | `1.000000` | held-out scan indices |
| Chronological holdout | `1.000000` | `1.000000` | train `0-19`, test `20-29` |
| Label shuffle control | `0.499333` | `0.458778` | p(AUC >= observed) `0.003984` across `250` repeats |
| Shape-only control | `1.000000` | `1.000000` | normalized waveform shape + FFT |
| Time-order shuffle | `1.000000` | `1.000000` | destroys local ordering, preserves values |
| Distribution-only control | `1.000000` | `1.000000` | summary statistics only |
| Amplitude-only control | `1.000000` | `1.000000` | amplitude/path scale summaries |

## Fold Detail

| Fold | Rows | Balanced accuracy | ROC AUC | Held-out scan indices |
| ---: | ---: | ---: | ---: | --- |
| `0` | `12` | `1.000000` | `1.000000` | `[0, 5, 10, 15, 20, 25]` |
| `1` | `12` | `1.000000` | `1.000000` | `[1, 6, 11, 16, 21, 26]` |
| `2` | `12` | `1.000000` | `1.000000` | `[2, 7, 12, 17, 22, 27]` |
| `3` | `12` | `1.000000` | `1.000000` | `[3, 8, 13, 18, 23, 28]` |
| `4` | `12` | `1.000000` | `1.000000` | `[4, 9, 14, 19, 24, 29]` |

## Support Read

This is support-bearing for a real THz-TDS replicate source/reference row. The
state/control split survives held-out scan blocks and chronological holdout, and
the shuffled-label control collapses. That is the clean strengthening move.

The lane remains bounded: because nuisance controls also stay high, the result
is not pure phase-lock, not cellular treatment response, and not a biological
THz tuning claim.

## Boundary

This result supports measured THz sample/reference separability in a public
instrument dataset. It does not close the Terahertz cellular prototype. It does
not establish a therapeutic or biological exposure effect.

## Next Gate

The next higher proof must be one of:

1. real biological sample-level THz exposure-response with sham/off-window,
   heat-matched, frequency, duration, power, and temperature controls;
2. local/partner source-on/source-off THz/EMF rows with a source-disabled
   baseline and matched environmental logging;
3. a broader repeated-scan THz panel with multiple materials, matched
   references, and external material/source-family holdouts.
