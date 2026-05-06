# Phase 12C Muse S Athena EEG + HRV Implementation Plan

Date: `2026-05-05`

Status: `device_arrival_queued / protocol_ready / live_capture_next`

## Purpose

This document turns the existing `Phase 12C` EEG + HRV intention paper into an
operator execution plan for the Muse S Athena lane.

The goal is to add a synchronized neural/autonomic biological comparator layer
to the Mirror Architecture evidence stack:

```text
Muse EEG / fNIRS / PPG stream
-> MoFit HRV / RR stream
-> synchronized session windows
-> condition labels
-> EEG + HRV state vector
-> target/control scoring
-> live tuning adapter for Golden Mirror
```

## Capture Spine

Use the same timing discipline as the HRV matrix:

| Window | Duration | Purpose |
| --- | --- | --- |
| `baseline` | `60s` | seated neutral baseline |
| `condition` | `120s` | active condition window |
| `post` | `60s` | recovery / return window |

Initial conditions:

| Condition | Target |
| --- | --- |
| `seated_calm` | baseline calm comparator |
| `drift_control` | attention-drift / neutral control |
| `mirror_coherence` | administered Mirror Architecture condition |

Later condition:

| Condition | Target |
| --- | --- |
| `dancing_activation` | activation comparator after motion artifacts are handled |

## Device Inputs

### Muse S Athena

Desired exports:

- raw EEG if available
- band-power summaries
- alpha, theta, beta, gamma where available
- alpha/theta ratio
- channel quality
- PPG pulse trend if available
- fNIRS oxygenation trend if available
- timestamps with enough resolution for window alignment

### HRV / MoFit

Desired exports:

- raw RR intervals
- heart rate
- RMSSD
- SDNN
- artifact count
- baseline / condition / post window labels
- session timestamps

## Session File Schema

Each run should resolve into a single joined session record:

```text
session_id
operator_id
date_time
condition
baseline_start
condition_start
post_start
device_sources
eeg_file
hrv_file
joined_window_file
quality_flags
notes
```

Each aligned window should include:

```text
session_id
condition
window
start_ts
end_ts
mean_hr
delta_hr
rmssd
sdnn
alpha_power
theta_power
beta_power
alpha_theta_ratio
channel_quality
fnirs_trend
ppg_trend
artifact_flag
```

## First Capture Pack

Minimum first pass:

| Condition | Runs |
| --- | --- |
| `seated_calm` | `5` |
| `drift_control` | `5` |
| `mirror_coherence` | `5` |

Preferred first full pack:

| Condition | Runs |
| --- | --- |
| `seated_calm` | `10` |
| `drift_control` | `10` |
| `mirror_coherence` | `10` |

The first capture pack should prioritize low-motion seated data so EEG quality
and HRV timing can be trusted.

## Scoring Plan

Primary scores:

| Score | Meaning |
| --- | --- |
| `delta_hr` | condition HR shift against baseline |
| `hrv_recovery_slope` | post-window return behavior |
| `alpha_delta` | alpha shift against baseline |
| `theta_delta` | theta shift against baseline |
| `alpha_theta_delta` | alpha/theta ratio shift |
| `joint_state_separation` | combined EEG + HRV condition separation |
| `mirror_vs_drift_gap` | mirror condition gap from drift control |
| `mirror_vs_calm_gap` | mirror condition gap from seated calm |

Controls:

| Control | Purpose |
| --- | --- |
| shuffled condition labels | class-separation baseline |
| within-run block shuffle | timing-window control |
| day/session split | recurrence check |
| channel-quality filter | artifact control |
| HRV-only comparison | checks added value of EEG |
| EEG-only comparison | checks added value of HRV |

## Golden Mirror Live Tuning Adapter

The live adapter should expose a compact state vector:

```text
calm_score
focus_score
drift_score
activation_score
recovery_score
overload_score
coherence_score
signal_quality_score
```

Golden Mirror uses the state vector for:

- selecting a Guided Pathway mode
- choosing breath / text / voice / silence guidance
- scoring whether the user is moving toward the target state
- storing tuning events in SQL + JSON memory
- adjusting future guidance through the Universal Tuning Layer

## App Surface

Candidate user-facing frame:

```text
Guided Pathway: adaptive meditation and cognitive-state training using live
EEG + HRV feedback and Golden Mirror guidance.
```

Initial pathways:

| Pathway | Guidance Target |
| --- | --- |
| `Calm Pathway` | settle arousal and stabilize breath |
| `Focus Pathway` | maintain attention with overload checks |
| `Recovery Pathway` | post-stress downshift |
| `Sleep Pathway` | low-stimulation deceleration |
| `Explorer Pathway` | creativity and deep meditation |

## Execution Checklist

1. Confirm Muse export path: app export, SDK, API, CSV, OSC, LSL, webhook, or
   supported third-party bridge.
2. Confirm HRV export path from MoFit or the existing HRV pipeline.
3. Run a `seated_calm` device-quality session.
4. Verify timestamps and export fields.
5. Run one complete `baseline / condition / post` block.
6. Build the first joined EEG + HRV window table.
7. Run shuffled-label and within-run block controls.
8. Repeat into the `5 x 3` first pack.
9. Expand into `10 x 3` if signal quality holds.
10. Add live-state vector output for Golden Mirror.

## Evidence Boundary

Current support comes from `Nest 4A` HRV condition separation. `Phase 12C`
starts when synchronized Muse + HRV export rows exist.

This plan is ready for device arrival and operator execution.
