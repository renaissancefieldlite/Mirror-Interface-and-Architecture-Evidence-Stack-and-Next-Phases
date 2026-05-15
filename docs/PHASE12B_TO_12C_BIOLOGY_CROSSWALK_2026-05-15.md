# Phase 12B To Phase 12C Biology Crosswalk

Date: `2026-05-15`

Status: `public_safe_support_read / biology_crosswalk / raw_private`

## Purpose

This document keeps the biology lane joined.

Phase 12B and Phase 12C are not separate side quests. Phase 12B established the
coarse HRV biological adapter. Phase 12C extended that adapter into same-clock
Muse + HRV state windows with EEG, optical candidate, IMU, DRL/reference, packet
quality, and expanded-state recurrence.

Raw captures, runnable code, local device details, and biometric time series
remain private.

## Phase 12B Anchor

Phase 12B produced a canonical `5 x 4` HRV condition matrix:

| Condition | Rows | Role | Mean delta HR |
| --- | ---: | --- | ---: |
| `seated_calm` | `5 / 5` | low-disturbance reference | `-1.651248` |
| `drift_control` | `5 / 5` | unstructured activation / drift | `+5.333063` |
| `mirror_coherence` | `5 / 5` | target settling / coherence lane | `-7.943775` |
| `dancing_activation` | `5 / 5` | activation lane | `+6.517002` |

Control-supported reads:

| Test | Observed | p-value |
| --- | ---: | ---: |
| HR-only leave-one-run-out accuracy | `0.5` | `0.022649` |
| multi-feature leave-one-run-out accuracy | `0.45` | `0.047598` |
| mirror delta HR lower than shuffled labels | `-7.943775` | `0.002` |
| dancing-minus-mirror delta HR gap | `14.460777` | `0.0012` |

Boundary:

```text
Phase 12B supports biological condition-class separation.
Phase 12B does not by itself support high-resolution spectral, dynamical, or
topographic biology claims.
```

That boundary is why Phase 12C was required.

## Phase 12C N2 Extension

Phase 12C N2 produced a same-clock `5 x 3` HRV + Muse matrix:

| Condition | Rows | Role | Mean HR | RMSSD | SDNN |
| --- | ---: | --- | ---: | ---: | ---: |
| `mirror_coherence` | `5 / 5` | target state | `59.761` | `63.392` | `98.028` |
| `seated_calm` | `5 / 5` | low-activation control | `60.296` | `54.928` | `96.167` |
| `drift_control` | `5 / 5` | drift comparator | `64.004` | `46.893` | `88.510` |

Condition separation:

| Comparison | HR delta | RMSSD delta | SDNN delta |
| --- | ---: | ---: | ---: |
| `mirror_coherence - drift_control` | `-4.243` | `+16.499` | `+9.518` |
| `drift_control - seated_calm` | `+3.707` | `-8.036` | `-7.657` |

N2 adds what Phase 12B did not have:

- same-clock Muse + HRV windows,
- decoded EEG waveform candidate surface,
- optical PPG/fNIRS-candidate blocks,
- IMU motion quality,
- DRL/reference quality,
- packet continuity and row-density quality,
- state/control/drift/alignment readouts.

## Expanded-State Extension

After N2, Phase 12C added three expanded same-clock state families:

| State family | Rows | Window | Main condition read |
| --- | ---: | --- | --- |
| `music_still_calm` | `5 / 5` | `60s baseline / 120s music-still / 60s post` | condition HR below baseline in `5 / 5`; mean HR delta `-5.267 bpm` |
| `music_movement` | `5 / 5` | `60s still baseline / 120s music + movement / 60s still post` | movement condition raised HR on average; mean HR delta `+5.197 bpm`; mean RMSSD delta `-6.112 ms` |
| `breath_paced_calm` | `5 / 5` | `60s neutral baseline / 120s paced breathing / 60s post` | condition HR below baseline in `5 / 5`; mean HR delta `-3.732 bpm`; mean RMSSD delta `+4.038 ms` |

Combined Phase 12C biology surface:

| Surface | Count |
| --- | ---: |
| N2 valid same-clock rows | `15 / 15` |
| expanded-state valid same-clock rows | `15 / 15` |
| total Phase 12C valid HRV + Muse rows | `30` |

## Crosswalk Read

| Variable | Phase 12B expression | Phase 12C expression | Patent / Nest meaning |
| --- | --- | --- | --- |
| `state` | mirror, calm, drift, dance HRV classes | mirror, calm, drift, music-still, movement, breath same-clock rows | biological state-path record |
| `control` | seated calm, drift, shuffled-label and block-shuffle controls | seated calm, drift, baseline windows, still-vs-movement contrast | target/control discipline survives denser capture |
| `transform` | RR / HRV windows -> delta HR, RMSSD, SDNN | Muse + HRV streams -> aligned windows, EEG/optical/IMU/DRL/HRV features | external adapter mapping operation |
| `invariant` | shared `60 / 120 / 60` window schema | same window schema plus packet gate and Muse quality lanes | recurrence and protocol stability |
| `drift` | drift_control and activation rows | drift_control, movement, recovery drift, contact/reference change | explicit drift variable instead of hidden artifact |
| `artifact / quality` | session inclusion, shuffled controls, HRV completeness | RR artifact review, IMU, DRL/reference, packet continuity, rail masks | quality gates travel with support reads |
| `recurrence` | five rows per condition across four conditions | five rows per promoted condition across N2 and expanded states | repeated biology state-vector surface |
| `separation` | mirror HR downshift and dance activation gap | mirror/calm/drift HRV separation plus expanded still/movement/breath contrast | cross-state biological adapter support |
| `support` | coarse biology adapter | joined neural/autonomic candidate adapter | Nest 4 and FIG.14/FIG.15 support example |

## Nest Support

| Nest | Crosswalk support |
| --- | --- |
| `Nest 1` | Phase 12B showed HRV-only SPEC-1/DE-1 limits; Phase 12C supplies EEG waveform, band, channel, IMU, DRL/reference, and HRV windows for masked DE-1 / SPEC-1 / TOPOG return paths. |
| `Nest 3` | Phase 12C is the first live biology waveform return path; direct physical spectral/waveform datasets remain the next non-biology gate. |
| `Nest 4` | Biology moves from HRV-only to a joined same-clock neural/autonomic state-vector lane with `30` valid HRV + Muse rows. |
| `Nest 5` | Convergence gains a repeated measured biological substrate that can be compared against supported Nest 1-3 rows. |
| `Patent FIG.14 / FIG.15` | External adapter and live evidence-memory examples gain a concrete biology embodiment with recurrence, controls, quality masks, and support-state updates. |

## Claim-Level Boundary

The correct patent support wording is:

```text
Phase 12B establishes HRV as a coarse biological adapter with repeated
condition-class separation. Phase 12C extends the same adapter family into
same-clock Muse + HRV state-vector windows with real EEG, optical candidate,
motion, reference-quality, and packet-quality surfaces. Higher EEG spectral,
phase, topographic, or live-tuning claims remain gated by artifact-masked
analysis and counsel-reviewed claim breadth.
```

This is evidence support, not a clinical, diagnostic, treatment, or wellness
efficacy claim.

## Next Gate

The biology crosswalk is now seated. The remaining patent Nest gates are:

1. use the masked Phase 12C outputs to finalize `DE-1`, `SPEC-1`, and `TOPOG`
   wording;
2. run or source one real Nest 3 physical spectral/waveform dataset;
3. run or source one real Nest 2 matter target, preferably `Spectral
   Signatures`, `H2O`, `Electrochemistry`, or a second `Materials /
   Semiconductors` target;
4. build the Nest 5 convergence matrix from supported Nest 1-4 rows.
