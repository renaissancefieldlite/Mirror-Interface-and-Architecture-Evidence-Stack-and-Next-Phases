# Phase 12C B.A.S.I.S. Public-Safe Aggregate Read

Date: `2026-07-15`

Status: `public_safe_aggregate / HRV_Muse_bridge_complete / Thermo_sidecar_open`

## Purpose

This note converts the private B.A.S.I.S. rerun into a public-safe evidence card.
It reports only aggregate counts, lane status, and boundary language. It does not
publish raw biometric exports, private capture paths, device identifiers, local
runtime code, or claim-sensitive mechanics.

## Plain-English Read

B.A.S.I.S. now has a repeated same-clock HRV + Muse capture surface, not just a
dashboard screenshot. The private post-capture gate found `62` same-clock
capture folders and `32` complete HRV + Muse artifact folders across six
represented conditions:

- `breath_paced_calm`
- `drift_control`
- `mirror_coherence`
- `music_movement`
- `music_still_calm`
- `seated_calm`

That means the biology lane has a real paired readout path where heart-rate
variability and Muse-derived signal lanes can be checked against the same
condition windows. The value is not that any single row proves a clinical claim;
the value is that the same pattern can be tested repeatedly with condition,
control, artifact, and quality boundaries preserved.

The July 15 update also inserted two fresh private capture rows into the gate
inventory:

- one full direct Muse capture under the `60 / 120 / 60` Phase 12C timing
  window, with `6,541` packet rows, `652,023` decoded sample rows, `42,038`
  decoded subpacket blocks, and `31,459` decoded EEG-block rows;
- one same-clock HRV + Muse slot with `286` HRV live rows, `6,535` Muse packet
  rows, `650,843` decoded sample rows, `41,952` decoded subpacket blocks, and
  `31,533` decoded EEG-block rows.

Those rows are reported only as aggregate engineering counts. Raw biosignal
files, local capture paths, and device identifiers remain private.

## Aggregate Gate Result

| Surface | Public-safe result | Boundary |
| --- | --- | --- |
| HRV + Muse paired manifest | `62` same-clock folders discovered; `32` complete HRV + Muse artifact folders | raw captures remain private |
| Condition coverage | six condition families represented | not a clinical cohort |
| Direct Muse row | `6,541` packet rows; `652,023` decoded sample rows | aggregate row count only |
| Latest same-clock HRV + Muse row | `286` HRV rows; `6,535` Muse packet rows; `650,843` decoded sample rows | aggregate row count only |
| Thermo lane | API/display sidecar present; `1` temperature link visible in the private audit | sidecar/open, not support-bearing |
| True triple sync | still open | needs same-clock HRV + Muse + temperature capture |
| Masked DE-1 / SPEC-1 / TOPOG rerun | complete over `30` valid private same-clock rows | public summary only |

## Masked Biology Readout

The masked DE-1 / SPEC-1 / TOPOG rerun returned a complete public-safe read over
`30` valid rows: `15` N2 rows and `15` expanded-state rows, across the same six
conditions.

- `DE-1`: supports dynamics-style comparison across condition windows.
- `SPEC-1`: decoded waveform and band-style features exist, but the read stays
  masked because high rail-candidate/artifact rates remain part of the evidence
  discipline.
- `TOPOG`: supports channel-presence, channel-quality, and state-wise difference
  checks; it is not being claimed as final scalp localization.

## What This Supports

This supports B.A.S.I.S. as a live biosignal adapter lane for Mirror Architecture:

1. Real repeated paired physiology rows exist.
2. Conditions and controls are preserved as row structure, not post-hoc story.
3. Artifact and quality masks are part of the evidence path.
4. Public reporting can expose the proof arc without exposing raw personal
   biosignal data.

## What It Does Not Claim

This is not a medical diagnosis, clinical validation, treatment claim, final EEG
brain-state classifier, or medical-device approval claim. It is a public-safe
engineering evidence read showing that the B.A.S.I.S. capture bridge is real,
repeatable, and ready for the next controlled capture gate.

## Next Gate

The clean continuation gate is a true same-clock triple capture:

```text
HRV + Muse + temperature
-> same session clock
-> same condition label
-> artifact and quality masks
-> public-safe aggregate read
```

If Thermo remains unstable as a sidecar, the support-bearing path stays HRV +
Muse while temperature remains an auxiliary lane until a same-clock source can be
captured cleanly.
