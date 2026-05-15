# Phase 12C Expanded-State Biology Support Read

Date: `2026-05-15`

Status: `public_safe_support_read / expanded_state_rows_complete / raw_captures_private`

## Purpose

This note seats the post-N2 expanded-state Phase 12C biology result into the
Mirror Architecture evidence stack.

N2 established the same-clock HRV + Muse surface across `mirror_coherence`,
`seated_calm`, and `drift_control`. The expanded-state pass tested whether the
same capture skeleton can carry additional biological states while preserving
state labels, controls, recurrence, timing, artifact lanes, and candidate EEG
waveform availability.

Raw captures, runnable code, local device identifiers, and biometric time series
remain private. This document carries the aggregate support read.

## What Landed

The expanded-state pass completed three five-run state blocks:

| Expanded state | Role | Valid same-clock rows | Main first-order read |
| --- | --- | ---: | --- |
| `music_still_calm` | auditory / still-body calm row | `5 / 5` | condition HR below baseline in `5 / 5`; mean HR delta `-5.267 bpm` |
| `music_movement` | active music + movement comparator | `5 / 5` | movement raised condition HR on average; mean HR delta `+5.197 bpm` |
| `breath_paced_calm` | paced autonomic regulation row | `5 / 5` | condition HR below baseline in `5 / 5`; mean HR delta `-3.732 bpm` |

Aggregate expanded-state capture surface:

| Surface | Count |
| --- | ---: |
| valid expanded same-clock HRV + Muse rows | `15` |
| Muse packet rows | `98,042` |
| EEG 8-channel blocks | `470,364` |
| optical candidate blocks | `75,516` |
| IMU motion blocks | `61,204` |
| DRL / reference-quality blocks | `18,159` |

Combined with the N2 `5 x 3` baseline matrix, Phase 12C now has `30` valid
same-clock HRV + Muse rows across six named state/control/drift/expanded-state
families.

## State-Variable Read

The expanded pack expresses the Universal Data Pattern variables as measured
biology rows:

| Variable | Expanded-state expression |
| --- | --- |
| `state` | named target rows: music-still calm, music movement, breath-paced calm |
| `control` | N2 seated calm / drift control plus within-row baseline and post windows |
| `transform` | Muse packets and HRV RR/BPM converted into windowed features |
| `invariant` | same `60s / 120s / 60s` clock, same state schema, same packet gate |
| `drift` | movement, recovery drift, contact/reference drift, HRV completeness |
| `artifact / quality` | IMU, DRL/reference, packet density, channel quality, RR artifact review |
| `recurrence` | five repeats per promoted expanded state |
| `separation` | opposite HR direction for still/breath rows versus movement row |
| `support` | real expanded biological state-vector manifold for Nest 4 and convergence |

## First-Order Findings

The clean first-order read is autonomic/state-window separation:

- `music_still_calm`: mean condition HR moved below baseline by `-5.267 bpm`.
- `music_movement`: mean condition HR moved above baseline by `+5.197 bpm`,
  with mean RMSSD lower by `-6.112 ms`.
- `breath_paced_calm`: mean condition HR moved below baseline by `-3.732 bpm`;
  mean condition RMSSD was higher by `+4.038 ms`, with row-level variability
  kept behind RR artifact review.

The support value is the directional contrast:

```text
 still music / breath regulation rows -> lower condition HR
+ active music movement row -> higher condition HR and lower RMSSD on average
```

That gives Phase 12C an expanded state/control/movement/regulation surface, not
only a single Muse capture or one target-control comparison.

## EEG Candidate Boundary

Each expanded block preserved real Muse EEG waveform availability and live
candidate band snapshots. The expanded rows remain beta/gamma-heavy in the live
tracker snapshots, but EEG interpretation is not promoted yet.

EEG remains a candidate feature surface until these gates pass:

1. IMU/contact/reference masks.
2. RR artifact / ectopic review.
3. channel rail and packet-continuity QA.
4. masked DE-1 / SPEC-1 / TOPOG feature analysis.

## Cross-Nest Use

| Layer | Expanded-state support |
| --- | --- |
| `Nest 1` | DE-1, SPEC-1, and TOPOG now have repeated real biology windows across calm, movement, and breath regulation. |
| `Nest 3` | waveform / spectral / timing rows gain a live physiology return path with motion and reference-quality masks attached. |
| `Nest 4` | HRV + EEG becomes an expanded biological state-vector lane, not only a three-condition baseline. |
| `Nest 5` | convergence can compare the same state-variable structure across AI internals, matter rows, waveform rows, and biology rows. |
| `B.A.S.I.S.` | the Capture Hub needs live state protocol, HRV, EEG feature surface, packet density, IMU, and DRL/reference readouts as first-class UI. |
| `Patent FIG. 14 / FIG. 15` | external adapter and evidence-memory examples gain repeated expanded-state biosignal embodiments. |

## Public Boundary

Public claim level:

```text
Phase 12C now includes a landed expanded-state same-clock HRV + Muse biology
surface. The clearest current read is state-window HRV separation: still/music
and breath-regulation rows lower condition HR, while music + movement raises
condition HR on average. Muse EEG remains a measured candidate dynamics /
spectral / topographic surface pending stricter artifact masks.
```

This is a support read for the Mirror Architecture state-variable map. It is not
a clinical, diagnostic, treatment, or wellness efficacy claim.

## Next Gates

1. IMU/contact/reference masks and RR artifact review across N2 plus
   expanded-state rows have landed locally.
2. The three-state comparison table has landed:
   `music_still_calm` vs `music_movement` vs `breath_paced_calm`.
3. Masked `DE-1` / `SPEC-1` / `TOPOG` feature pass has landed locally and is
   the active Nest 1 support surface.
4. Crosswalk HRV1.0 / Phase 12B into the expanded Phase 12C read.
5. Keep the already patched patent claim-support ledger pointed to N2 plus
   expanded-state support; FIG.10-FIG.15 and claims 19-30 are already seated.
6. Move to the remaining patent Nest gates: one real Nest 3 spectral/waveform
   dataset, one real Nest 2 matter target, then the Nest 5 convergence matrix.
7. Build the public-safe visual companion for expanded-state biology.
