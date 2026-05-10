# Phase 12C Waveform QA Public Read

Date: `2026-05-10`

Status: `N1_waveform_QA_complete / existing_captures_only / no_recapture`

## Execution Lock

Phase N1 used the five direct Phase 12C Muse S Athena decoded captures already
on disk. It did not start Bluetooth, did not recapture the headset, and did
not use toy data.

The private output pack remains local and is not uploaded. Raw wide waveform
tables remain local/private. This public document is the support readout.

## What N1 Adds

| Layer | N1 result |
| --- | --- |
| `DE-1` | EEG waveform rows were exported per run and per channel from real decoded Athena packets. |
| `SPEC-1` | Spectral / bandpower work is now queued against measured waveform QA instead of HRV-only coarse spectral data. |
| `TOPOG` | Muse channel layout is present across `TP9`, `AF7`, `AF8`, `TP10`, `FPz`, `AUX_R`, `AUX_L`, `AUX`. |
| `STAT / CTRL` | IMU, DRL/reference, optical candidate, and battery/status masks are attached at the window level. |
| `Nest 4` | The Muse side is ready to be joined into the HRV + Muse synchronized manifest. |

## Five-Run QA Surface

| Run | Condition | Sensor packets | Waveform rows | Channels | Packet rate | Max packet gap |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| `phase12c_direct_mirror_coherence_20260509T004420Z` | `mirror_coherence` | `6469` | `62254` | `8/8` | `26.95` | `n/a` |
| `phase12c_direct_mirror_coherence_20260509T054300Z` | `mirror_coherence` | `6471` | `62496` | `8/8` | `26.42` | `0.186s` |
| `phase12c_direct_mirror_coherence_20260509T054802Z` | `mirror_coherence` | `6472` | `63052` | `8/8` | `26.42` | `0.134s` |
| `phase12c_direct_seated_calm_20260509T052412Z` | `seated_calm` | `6468` | `62314` | `8/8` | `26.41` | `0.147s` |
| `phase12c_direct_drift_control_20260509T052930Z` | `drift_control` | `6467` | `63046` | `8/8` | `26.40` | `0.176s` |

Continuity note: the first direct run has a header-only `muse_ble_packets.csv`
but populated decoded output and `muse_ble_summary.json`, so packet count/rate
are taken from the BLE summary while max-gap continuity remains unavailable for
that one run.

## Channel QA Read

All expected EEG channels are present in all five runs. Mean decoded density is
about `255.69` samples/sec per channel.

| Channel | Rail-candidate pattern | N1 status |
| --- | --- | --- |
| `TP9` | `high` | `present_high_rail_candidate_load` |
| `AF7` | `high` | `present_high_rail_candidate_load` |
| `AF8` | `high` | `present_high_rail_candidate_load` |
| `TP10` | `high` | `present_high_rail_candidate_load` |
| `FPz` | `low` | `present_low_rail_candidate_load` |
| `AUX_R` | `low` | `present_low_rail_candidate_load` |
| `AUX_L` | `low` | `present_low_rail_candidate_load` |
| `AUX` | `moderate` | `present_moderate_rail_candidate_load` |

The main QA flag is rail-candidate load on the outer EEG channels. That is the
point of this pass: it tells the next run pack exactly where contact/reference
calibration and artifact masking tighten before bandpower, phase, topographic,
or live tuning reads are promoted.

## Window Artifact Masks

N1 generated a per-run, per-window artifact table with:

- max EEG rail-candidate rate,
- IMU acceleration and gyro norms,
- DRL/reference raw-count statistics,
- optical candidate row counts,
- battery/status row counts.

This is the bridge into Phase N2: every HRV window can now be joined to Muse
waveform, motion, reference-quality, optical, and status masks.

## Cross-Nest Support

| Parked lane | N1 support |
| --- | --- |
| `DE-1` | continuous EEG waveform export exists; next step is artifact-masked dynamics. |
| `SPEC-1` | measured EEG substrate exists; next step is bandpower/phase only after QA masks are applied. |
| `TOPOG` | Muse electrode/channel structure supplies the first biology topography path. |
| `Nest 3 waves / spectra` | live waveform row now has a measured biology return path. |
| `Nest 4 HRV + EEG` | N2 manifest can join HRV state windows with Muse waveform/quality masks. |
| `Nest 5 convergence` | biology now has HRV coarse state separation plus EEG waveform QA as the denser substrate. |

## Next

```text
N1 waveform QA complete
-> N2 HRV + Muse manifest surface
-> same-clock 5 x 3 synchronized capture pack
-> 10 x 3 recurrence extension
-> full lane expansion from lattice-companion.html
```
