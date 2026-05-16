# Phase 12C Masked DE-1 / SPEC-1 / TOPOG Public Read

Date: `2026-05-15`

Status: `public_safe_aggregate / private_raw_retained / no_capture_code`

## What Ran

The masked formal-return analysis ran over the full Phase 12C same-clock
biology surface:

```text
30 / 30 valid HRV + Muse rows
= 15 N2 mirror/calm/drift rows
+ 15 expanded-state music/movement/breath rows
```

The run used private HRV window summaries, decoded Muse EEG waveform features,
IMU motion summaries, DRL/reference summaries, packet continuity, and channel
rail masks. Raw waveform, raw RR, local device, and runnable capture materials
remain private.

## DE-1 Dynamics Result

DE-1 moved from "reopened candidate" to `masked candidate dynamics pass
complete`.

| Set | Condition | Rows | Condition HR delta | Condition RMSSD delta | Condition gyro |
| --- | --- | ---: | ---: | ---: | ---: |
| expanded | `breath_paced_calm` | `5` | `-3.732` | `+4.038` | `4.695` |
| expanded | `music_movement` | `5` | `+5.197` | `-6.112` | `13.986` |
| expanded | `music_still_calm` | `5` | `-5.267` | `-5.954` | `2.609` |
| N2 | `drift_control` | `5` | `-0.478` | `-0.977` | `5.897` |
| N2 | `mirror_coherence` | `5` | `-0.148` | `+14.342` | `3.392` |
| N2 | `seated_calm` | `5` | `-2.422` | `-9.690` | `3.072` |

Read:

```text
The 30-row surface separates state families through HRV trajectory and motion
masks. Movement is the clearest activation row: HR rises, RMSSD falls, and gyro
load is highest. Breath shows autonomic settling: HR falls and RMSSD rises.
Mirror coherence holds the strongest N2 RMSSD lift against its baseline window.
```

Boundary:

```text
DE-1 is now a masked candidate dynamics result. It supports continuous
state-trajectory analysis, while stronger formal promotion still depends on
larger recurrence and tighter artifact controls.
```

## SPEC-1 Spectral Result

SPEC-1 moved from "candidate spectral surface landed" to `masked candidate
spectral pass complete`.

The spectral pass used low/moderate-rail channels only. High-rail temporal
electrode channels remain visible in private QA tables but are not promoted.

| Set | Condition | Window | Channels | Delta | Theta | Alpha | Beta | Low gamma |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| expanded | `breath_paced_calm` | condition | `4` | `0.027` | `0.023` | `0.028` | `0.518` | `0.394` |
| expanded | `music_movement` | condition | `4` | `0.092` | `0.025` | `0.023` | `0.485` | `0.365` |
| expanded | `music_still_calm` | condition | `4` | `0.025` | `0.023` | `0.027` | `0.527` | `0.390` |
| N2 | `drift_control` | condition | `4` | `0.026` | `0.027` | `0.031` | `0.521` | `0.386` |
| N2 | `mirror_coherence` | condition | `5` | `0.076` | `0.028` | `0.028` | `0.489` | `0.368` |
| N2 | `seated_calm` | condition | `6` | `0.088` | `0.039` | `0.039` | `0.466` | `0.355` |

Read:

```text
The decoded Muse waveform yields a real EEG spectral feature surface across all
six state families. The strongest safe claim is feature availability plus
state-wise masked spectral separation, not final brain-state interpretation.
```

Boundary:

```text
SPEC-1 remains candidate spectral support because elevated rail/contact burden
persists in the temporal electrode lanes. The next improvement is stricter
contact control and recurrence, not a broader claim.
```

## TOPOG-1/2 Channel Result

TOPOG moved from "biology channel topology queued" to `channel topology pass
complete with quality boundary`.

All eight Muse channel labels were present across promoted rows:

```text
TP9, AF7, AF8, TP10, FPz, AUX_R, AUX_L, AUX
```

The channel-quality read is the important result:

| Channel group | Current quality read | Role |
| --- | --- | --- |
| `FPz`, `AUX_R`, `AUX_L` | low rail | strongest current masked EEG feature surface |
| `AUX` | moderate rail | usable with caution as auxiliary channel |
| `TP9`, `AF7`, `AF8`, `TP10` | high rail / contact burden | topology present, but not promoted for clean neural interpretation |

Read:

```text
TOPOG now has a real biology channel-layout surface. The support is channel
presence, channel quality, and state-wise channel comparison under masks. It is
not yet a final scalp-localization claim.
```

## Universal Data Pattern Support

| Variable | 30-row masked result |
| --- | --- |
| `state` | six named state families produced valid windows |
| `control` | seated calm, drift control, stillness, movement, breath, baseline, and post windows remained separable |
| `transform` | HRV + Muse streams became masked feature vectors |
| `drift` | motion and channel/contact burden became explicit variables |
| `artifact / quality` | IMU, DRL/reference, packet density, RR review, and rail masks controlled promotion |
| `recurrence` | five valid rows per promoted condition family |
| `support` | Nest 1 DE-1 / SPEC-1 / TOPOG now have real masked candidate passes instead of only queued wording |

## Patent / Nest Use

This result strengthens:

- `FIG.10`: measured state-path ladder;
- `FIG.14`: external biological adapter lane;
- `FIG.15`: evidence-memory / support-state update loop;
- claims `19`, `21`, `26`, `27`, `28`, `29`, and `30` as implementation
  examples using real physiology feature vectors and masks.

## Next Gate

```text
First real Nest 3 spectral / waveform dataset run:
USGS Spectral Library Version 7 ASTER subset
-> complete as first Waves / Spectra and Spectral Signatures support pass
-> next: Nest 5 convergence matrix
-> then: native spectra / H2O extraction / second spectral family / materials target
```
