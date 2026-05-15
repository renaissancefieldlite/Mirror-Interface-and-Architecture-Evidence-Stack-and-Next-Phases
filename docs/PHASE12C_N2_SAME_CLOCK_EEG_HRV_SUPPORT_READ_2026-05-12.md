# Phase 12C N2 Same-Clock EEG + HRV Support Read

Date: `2026-05-12`

Status: `public_safe_support_read / N2_same_clock_complete / raw_captures_private`

## Purpose

This note seats the Phase 12C N2 result into the Mirror Architecture public
evidence stack.

N1 proved that the existing Muse S Athena captures could be exported into real
waveform and artifact-mask surfaces. N2 is the next step: HRV and Muse were
captured inside the same operator clock across the same state / control / drift
window schema.

The private analysis pack, raw captures, runnable scripts, device identifiers,
and biometric time series remain local. This document carries the public-safe
support read.

## What Landed

The N2 same-clock pack produced a complete `5 x 3` biology matrix:

| Condition | Role | Same-clock rows |
| --- | --- | ---: |
| `mirror_coherence` | target state | `5 / 5` |
| `seated_calm` | low-activation control | `5 / 5` |
| `drift_control` | unstructured drift comparator | `5 / 5` |

Aggregate capture surface:

| Surface | Count |
| --- | ---: |
| valid same-clock HRV + Muse rows | `15` |
| Muse packet rows | `98,027` |
| Athena sensor rows | `96,992` |
| decoded sample rows | `9,750,684` |
| EEG channel blocks | `469,489` |
| HRV RR / BPM samples | `3,980` |

## Universal Data Pattern Map

N2 expresses the public Universal Data Pattern variables in a live biology
surface:

| Variable | N2 expression |
| --- | --- |
| `state` | `mirror_coherence` same-clock HRV + Muse rows |
| `control` | `seated_calm` comparator rows |
| `drift` | `drift_control`, IMU motion, reference instability, recovery drift |
| `transform` | Muse BLE packets -> decoded EEG / optical / IMU / DRL + HRV RR/BPM windows |
| `invariant` | same `60s / 120s / 60s` window clock across all rows |
| `artifact / quality` | packet continuity, IMU, DRL/reference, rail-channel QA, HRV completeness |
| `recurrence` | five repeats per condition |
| `separation` | HRV and candidate EEG feature differences by condition |
| `support` | real same-clock biological state-vector surface for Nest 4 and convergence rows |

## First-Order HRV Finding

The strongest N2 finding is the HRV state/control/drift separation. Across the
same-clock condition windows, `drift_control` showed higher average heart rate
and lower HRV than `mirror_coherence` and `seated_calm`.

| Condition | Mean HR | RMSSD | SDNN |
| --- | ---: | ---: | ---: |
| `mirror_coherence` | `59.761` | `63.392` | `98.028` |
| `seated_calm` | `60.296` | `54.928` | `96.167` |
| `drift_control` | `64.004` | `46.893` | `88.510` |

Condition separation:

| Comparison | HR delta | RMSSD delta | SDNN delta |
| --- | ---: | ---: | ---: |
| `mirror_coherence - drift_control` | `-4.243` | `+16.499` | `+9.518` |
| `drift_control - seated_calm` | `+3.707` | `-8.036` | `-7.657` |

Read:

```text
N2 strengthens the Phase 12B biology lane because the same-clock pack preserves
the mirror / calm / drift condition separation while Muse is running in the
same state window.
```

## Candidate EEG Feature Read

The EEG read is now real measured support, but it stays at candidate status
until stricter channel masks and artifact weighting are applied. N2 deliberately
keeps high-rail primary channels in the QA boundary rather than promoting them
as final spectral proof.

Low-rail / QA-clean feature surface:

| Condition | EEG std | Theta rel | Alpha rel | Beta rel | Alpha / theta | Gyro norm |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `mirror_coherence` | `97.757` | `0.025` | `0.028` | `0.493` | `1.201` | `3.392` |
| `seated_calm` | `95.066` | `0.030` | `0.038` | `0.506` | `1.287` | `3.072` |
| `drift_control` | `99.929` | `0.027` | `0.034` | `0.517` | `1.332` | `5.897` |

The candidate EEG read is most useful for the next gate:

- `DE-1`: continuous dynamics can now use same-clock HRV + EEG windows.
- `SPEC-1`: bandpower / phase can now be run against measured EEG windows after
  stricter masks.
- `TOPOG`: Muse channel layout gives the first biology topographic route, with
  contact/reference QA carried forward.
- `STAT-1 / CTRL-1`: IMU and DRL/reference are now attached as artifact and
  control variables rather than after-the-fact notes.

## Architecture Support

| Layer | N2 support |
| --- | --- |
| `Nest 1` | DE-1 / SPEC-1 / TOPOG now have same-clock biology input instead of HRV-only coarse support. |
| `Nest 3` | waveform / timing / spectral lanes gain a real biology return path. |
| `Nest 4` | HRV + EEG becomes a joined state-vector lane with recurrence. |
| `Nest 5` | convergence gets another repeated measured substrate class. |
| `B.A.S.I.S.` | same-clock capture proves the Capture Hub needs visible timing, quality, and state readouts. |
| `Patent FIG. 14 / FIG. 15` | external adapter and live evidence-memory examples gain a concrete same-clock biosignal embodiment. |

## Public Boundary

This support read does not publish raw captures, runnable code, local device
identifiers, or biometric time series. It also does not promote a clinical
claim.

Public claim level:

```text
Phase 12C N2 landed a real same-clock HRV + Muse matrix. The strongest current
read is HRV condition separation with Muse running in the same state window.
EEG adds a measured candidate dynamics / spectral / topographic surface, with
stricter artifact masks required before higher EEG claims are promoted.
```

## Next Gates

1. Apply stricter channel masks and artifact weighting to the N2 EEG feature
   table.
2. Run expanded state packs: breath-paced calm, guided coherence, eyes-open /
   eyes-closed, cognitive load, motion, and recovery. Emotion-linked rows stay
   private / optional unless separately cleared.
3. HRV1.0 / Phase 12B is now crosswalked into Phase 12C so the coarse HRV
   adapter and same-clock Muse + HRV adapter stay joined instead of parallel.
4. Patch B.A.S.I.S. Capture Hub around live readouts: HRV, EEG feature bands,
   IMU, DRL/reference, packet density, and state timer.
5. Use the expanded same-clock packs to rerun DE-1, SPEC-1, TOPOG, and the
   Nest 4 / Nest 5 convergence summaries.

Expanded-state protocol:

```text
docs/PHASE12C_POST_N2_EXPANDED_STATE_CAPTURE_PROTOCOL_2026-05-12.md
```
