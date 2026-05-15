# Phase N2 HRV + Muse Synchronized Manifest

Date: `2026-05-10`

Status: `N2_same_clock_complete / 15_valid_rows / public_safe_support_read_linked`

## Read

N1 waveform QA is complete. The Muse side has exported waveform rows, packet /
continuity checks, and per-window artifact masks.

N2 has now advanced from manifest surface to completed same-clock support read.

The completed `5 x 3` same-clock pack landed:

- `5` `mirror_coherence` target rows,
- `5` `seated_calm` control rows,
- `5` `drift_control` comparator rows,
- one shared `60s baseline / 120s condition / 60s post` timing structure,
- HRV RR/BPM windows joined to Muse EEG / optical / IMU / DRL / status lanes.

The private output pack remains local and is not uploaded.

Public support read:

```text
docs/PHASE12C_N2_SAME_CLOCK_EEG_HRV_SUPPORT_READ_2026-05-12.md
```

## Completed Same-Clock Surface

| Condition | Same-clock rows | Current status |
| --- | ---: | --- |
| `mirror_coherence` | `5 / 5` | `target_state_landed` |
| `seated_calm` | `5 / 5` | `control_landed` |
| `drift_control` | `5 / 5` | `drift_comparator_landed` |

Aggregate private-analysis read:

| Surface | Count |
| --- | ---: |
| valid same-clock HRV + Muse rows | `15` |
| Muse packet rows | `98,027` |
| Athena sensor rows | `96,992` |
| decoded sample rows | `9,750,684` |
| EEG channel blocks | `469,489` |
| HRV RR / BPM samples | `3,980` |

## N2 Finding

The strongest current N2 finding is HRV state/control/drift separation with Muse
running in the same state window.

| Condition | Mean HR | RMSSD | SDNN |
| --- | ---: | ---: | ---: |
| `mirror_coherence` | `59.761` | `63.392` | `98.028` |
| `seated_calm` | `60.296` | `54.928` | `96.167` |
| `drift_control` | `64.004` | `46.893` | `88.510` |

The EEG feature table is real measured support, but remains a candidate
dynamics / spectral / topographic surface until stricter channel masks and
artifact weighting are applied.

## State-Variable Bridge

| Variable | N2 expression |
| --- | --- |
| `state` | `mirror_coherence` HRV + Muse same-clock condition rows |
| `control` | `seated_calm` and `drift_control` same-clock comparator rows |
| `transform` | HRV RR/BPM windows + Muse EEG/optical/IMU/DRL decoded windows |
| `invariant` | same baseline / condition / post schema across both devices |
| `drift` | motion, contact/reference instability, condition drift, HRV recovery drift |
| `artifact / quality` | N1 Muse masks plus HRV RR-count/window completeness |
| `coherence / alignment` | mirror-minus-control read across HRV and Muse vectors |
| `recurrence` | completed `5 x 3` same-clock pack, then expanded state and `10 x 3` recurrence extension |
| `score / support` | joined biological state-vector surface for Nest 4 and convergence rows |

## Next

The next execution move is expanded-state capture and stricter EEG QA:

```text
N2 same-clock complete
-> stricter EEG channel masks / artifact weighting
-> expanded state packs
-> HRV1.0 first-matrix crosswalk
-> DE-1 / SPEC-1 / TOPOG reruns
```

The full lane expansion uses:

```text
renaissancefieldlite.github.io/lattice-companion.html
```
