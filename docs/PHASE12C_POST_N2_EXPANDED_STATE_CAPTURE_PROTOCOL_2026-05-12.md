# Phase 12C Post-N2 Expanded State Capture Protocol

Date: `2026-05-12`

Status: `expanded_state_rows_landed / public_safe_protocol / analysis_gates_active`

## Purpose

N2 landed the first same-clock HRV + Muse `5 x 3` support surface. The next
move is not another copy of the same three states. The next move is to expand
the state manifold so the Universal Data Pattern can be tested across a wider
biology state space while keeping the same controls, clock, and artifact masks.

This protocol started as the next execution map. As of `2026-05-15`, three
expanded-state five-run blocks have landed and now move into masking and
analysis:

| State | Valid rows | First read |
| --- | ---: | --- |
| `music_still_calm` | `5 / 5` | condition HR below baseline in `5 / 5`; mean HR delta `-5.267 bpm` |
| `music_movement` | `5 / 5` | movement raised condition HR on average; mean HR delta `+5.197 bpm` |
| `breath_paced_calm` | `5 / 5` | condition HR below baseline in `5 / 5`; mean HR delta `-3.732 bpm` |

The aggregate expanded-state surface is `15` valid same-clock HRV + Muse rows,
`98,042` Muse packet rows, and `470,364` EEG 8-channel blocks. Raw captures and
biometric time series remain private.

## Fixed Capture Clock

Every expanded-state row keeps the same clock:

```text
60s baseline
120s condition
60s post / recovery
```

Every row uses the same joined capture surface:

```text
MoFit HRV / RR / BPM
+ Muse EEG / optical candidate / IMU / DRL-reference / battery-status
+ state label
+ artifact and quality masks
```

## State Pack A: Low-Motion Calibration

| State | Purpose | Control value |
| --- | --- | --- |
| `seated_calm` | existing low-activation reference | preserves N2 continuity |
| `breath_paced_calm` | paced autonomic regulation | separates intentional breath pacing from ordinary calm |
| `music_still_calm` | music-on, body-still calm row | separates auditory/music state from motion artifact |
| `eyes_open_rest` | visual-input baseline | separates eye / visual artifact from state effects |
| `eyes_closed_rest` | reduced visual-input baseline | helps EEG alpha/topography gates after masks |

## State Pack B: AI-Guided / Cognitive States

| State | Purpose | Control value |
| --- | --- | --- |
| `mirror_coherence` | existing target state | preserves N2 continuity |
| `ai_guided_coherence` | B.A.S.I.S. prototype: AI guides the operator toward a named state | tests guided-state surface |
| `cognitive_load_math` | structured cognitive effort | separates effort/load from drift |
| `language_focus` | reading/listening or verbal focus | tests AI-interface relevance without heavy motion |

## State Pack C: Drift / Artifact / Recovery

| State | Purpose | Control value |
| --- | --- | --- |
| `drift_control` | existing unstructured thought comparator | preserves N2 continuity |
| `motion_control` | deliberate movement / posture shift | calibrates IMU and artifact masks |
| `music_movement` | music-guided movement / active embodiment row | tests guided active state while IMU protects EEG interpretation |
| `blink_jaw_artifact` | eye / jaw / facial artifact calibration | prevents artifact from masquerading as EEG state |
| `recovery_only` | post-effort recovery row | tests return-to-baseline structure |

## Minimum First Expansion

The first expansion should be small enough to run cleanly:

```text
3 repeats x 6 states = 18 joined HRV + Muse rows
```

Recommended first six:

1. `seated_calm`
2. `breath_paced_calm`
3. `mirror_coherence`
4. `ai_guided_coherence`
5. `cognitive_load_math`
6. `drift_control`

After the first six-state expansion lands, add artifact and topology states:

```text
eyes_open_rest
eyes_closed_rest
motion_control
music_movement
blink_jaw_artifact
recovery_only
language_focus
```

## Executed First Expansion Status

The first executed expansion landed as three high-value five-run blocks:

1. `music_still_calm`
2. `music_movement`
3. `breath_paced_calm`

This differs from the original six-state recommendation because the live
capture path prioritized a clean contrast set:

```text
auditory stillness
-> active movement artifact / embodiment comparator
-> paced autonomic regulation
```

The remaining planned states stay queued:

- `ai_guided_coherence`
- `cognitive_load_math`
- `eyes_open_rest`
- `eyes_closed_rest`
- `blink_jaw_artifact`
- `language_focus`
- `recovery_only`

## Music Still-Calm Row

`music_still_calm` is an auditory / music-state row, not a movement row. Music
stays present while the body stays still.

Recommended operator instruction:

```text
Baseline: music on, still body, normal breath.
Condition: music stays on, still body, let the music-calm state settle.
Post: music may stay on or lower, still body, recovery.
```

Primary read:

- HRV / RR and recovery,
- IMU-stillness as a quality guardrail,
- Muse packet density,
- DRL/reference quality,
- EEG candidate bands after masks.

## Music + Movement Row

`music_movement` is an active guided-state row, not a clean stillness row. It
should be interpreted through the active-state lens:

- HRV / RR / recovery are primary.
- IMU movement is primary and expected.
- DRL/reference quality is a guardrail.
- EEG is candidate only after motion-aware masks.
- The post window matters because recovery is part of the state read.

Recommended operator instruction:

```text
Baseline: still, no music or music paused.
Condition: play the selected music and move naturally at low-to-moderate
intensity while keeping the headset seated.
Post: stop movement, music off or lowered, stay still for recovery.
```

## Universal Data Pattern Variables

| Variable | Expanded-state expression |
| --- | --- |
| `state` | named target state: mirror, guided coherence, paced calm, cognitive load, recovery |
| `control` | seated calm, drift, eyes open/closed, motion, artifact calibration |
| `transform` | HRV + Muse raw streams into windowed features |
| `invariant` | same clock, devices, masks, and state schema |
| `drift` | unstructured thought, motion, recovery drift, contact/reference drift |
| `artifact / quality` | IMU, DRL/reference, rail channels, packet continuity, HRV completeness |
| `recurrence` | at least three repeats per new state, then five repeats for promoted states |
| `separation` | condition differences across HRV, EEG features, motion, and quality masks |
| `support` | candidate state-vector manifold for B.A.S.I.S., Nest 4, and convergence |

## Analysis Gates

1. Lock row validity: same clock, complete windows, packet density, HRV samples.
2. Apply stricter EEG masks: channel rails, IMU, DRL/reference, packet gaps.
3. Compare condition-window HRV: HR, RMSSD, SDNN, recovery.
4. Compare EEG features only after masks: alpha, theta, beta, alpha/theta,
   channel/topography, and dynamics.
5. Separate state signal from artifact signal: motion, jaw/blink, reference
   quality, and device status stay attached.
6. Promote only repeated, control-separated effects.

## B.A.S.I.S. Product Translation

This is the bridge from experiment to product console:

```text
AI gives a state protocol
-> Capture Hub shows timer and live quality
-> HRV + EEG features update during the row
-> artifact masks protect the read
-> the session saves as a state-vector record
-> Mirror Architecture analysis reads the state/control/drift surface
```

The product goal is guided state navigation and research capture. Clinical,
diagnostic, or treatment claims remain later validation layers.

## HRV1.0 Crosswalk

Before promoting the expanded-state pack, crosswalk it against the HRV1.0 first
biological matrix:

```text
HRV1.0 / Phase 12B 5 x 4
-> seated_calm / drift_control / mirror_coherence / dancing_activation
-> N2 5 x 3 same-clock HRV + Muse
-> expanded-state HRV + Muse manifold
```

This keeps the biological ladder continuous instead of treating Phase 12B,
Phase 12C, and B.A.S.I.S. as disconnected experiments.
