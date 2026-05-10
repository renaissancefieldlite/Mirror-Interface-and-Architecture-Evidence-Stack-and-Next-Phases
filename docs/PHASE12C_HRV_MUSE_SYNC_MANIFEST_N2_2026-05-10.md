# Phase N2 HRV + Muse Synchronized Manifest

Date: `2026-05-10`

Status: `N2_manifest_surface_complete / condition_aligned_existing_rows / same_clock_slots_defined`

## Read

N1 waveform QA is complete. The Muse side now has exported waveform rows,
packet / continuity checks, and per-window artifact masks.

N2 now has a two-layer manifest:

1. existing Phase 12B HRV rows mapped to existing Phase 12C Muse rows by
   condition,
2. real same-clock HRV + Muse capture slots for the next `5 x 3` and `10 x 3`
   packs.

The existing 12B and 12C rows are condition-aligned support rows. The live
synchronized manifest becomes complete when HRV and Muse are captured in the
same operator session with the same baseline / condition / post clock.

The private output pack remains local and is not uploaded.

## Existing Overlap

| Condition | HRV canonical rows | Existing Muse rows | Current status |
| --- | ---: | ---: | --- |
| `mirror_coherence` | `5` | `3` | `in_N2_sync_plan` |
| `seated_calm` | `5` | `1` | `in_N2_sync_plan` |
| `drift_control` | `5` | `1` | `in_N2_sync_plan` |
| `dancing_activation` | `5` | `0` | `phase12b_supported_optional_muse_extension` |

## Same-Clock Capture Plan

| Pack | Conditions | Slots | Window structure |
| --- | --- | ---: | --- |
| `5 x 3` | `mirror_coherence`, `seated_calm`, `drift_control` | `15` | `60s baseline / 120s condition / 60s post` |
| `10 x 3` | `mirror_coherence`, `seated_calm`, `drift_control` | `30` | same clock, same masks, recurrence extension |

Every sync slot must carry:

- HRV: RR/BPM export, RMSSD, SDNN, mean HR by window,
- Muse: EEG waveform, optical candidate lane, IMU, DRL/reference quality,
  battery/status,
- shared timing: UTC start/end plus relative seconds and baseline / condition /
  post labels,
- artifact masks: N1 rail-candidate, IMU, DRL/reference, optical, and packet QA
  fields.

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
| `recurrence` | `5 x 3` first synchronized pack, then `10 x 3` recurrence extension |
| `score / support` | joined biological state-vector surface for Nest 4 and convergence rows |

## Next

The next execution move is the same-clock `5 x 3` pack:

```text
mirror_coherence x 5
seated_calm x 5
drift_control x 5
each row = HRV + Muse in one shared baseline / condition / post session
```

After N2 same-clock slots are populated, the full lane expansion uses:

```text
renaissancefieldlite.github.io/lattice-companion.html
```
