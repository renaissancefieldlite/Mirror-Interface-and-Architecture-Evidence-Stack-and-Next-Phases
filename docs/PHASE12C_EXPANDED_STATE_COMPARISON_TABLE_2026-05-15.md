# Phase 12C Expanded-State Comparison Table

Date: `2026-05-15`

Status: `public_safe_support_read / aggregate_only / raw_private`

## Boundary

This document converts the landed Phase 12C expanded-state captures into a
public-safe support table. It uses aggregate reads only.

Raw Muse packets, HRV exports, biometric time series, device details, and
runnable capture code remain local/private.

## Landed Expanded-State Surface

The private validity / exclusion ledger promotes only the rows listed in the
three five-run summaries. Preflight, interrupted, partial, or non-promoted
folders are excluded from this table.

| State family | Valid rows | Window | Main condition read |
| --- | ---: | --- | --- |
| `music_still_calm` | `5 / 5` | `60s baseline / 120s music-still / 60s post` | condition HR below baseline in `5 / 5`; mean HR delta `-5.267 bpm` |
| `music_movement` | `5 / 5` | `60s still baseline / 120s music + movement / 60s still post` | movement condition raised HR on average; mean HR delta `+5.197 bpm`; mean RMSSD delta `-6.112 ms` |
| `breath_paced_calm` | `5 / 5` | `60s neutral baseline / 120s paced breathing / 60s post` | condition HR below baseline in `5 / 5`; mean HR delta `-3.732 bpm`; mean RMSSD delta `+4.038 ms` |

Combined expanded-state surface:

| Measure | Aggregate |
| --- | ---: |
| valid expanded-state rows | `15 / 15` |
| Muse packet rows | `98,042` |
| EEG blocks | `470,364` |
| optical candidate blocks | `75,516` |
| IMU motion blocks | `61,204` |
| DRL/reference-quality blocks | `18,159` |

With the earlier N2 same-clock baseline matrix, Phase 12C now carries `30`
valid HRV + Muse rows across baseline/control/drift and expanded-state
families.

## State-Variable Read

| Universal Data Pattern variable | Phase 12C expression |
| --- | --- |
| `state` | named biological rows: mirror coherence, seated calm, drift control, music stillness, music movement, breath pacing |
| `control` | baseline windows, seated calm, drift control, still-vs-movement contrast |
| `transform` | Muse + HRV streams converted into aligned windows and decoded lane features |
| `invariant` | same clock, same row schema, same 60 / 120 / 60 capture discipline, same packet gate |
| `drift` | movement, unstructured recovery, contact/reference change, RR instability, condition drift |
| `artifact / quality` | IMU, DRL/reference, packet density, HRV completeness, failed-preflight exclusions |
| `recurrence` | five valid repeats per promoted expanded condition |
| `separation` | still/breath rows lower HR; movement row higher HR and lower RMSSD on average |
| `support` | real measured biology surface for Nest 1, Nest 4, Nest 5, and the Nest 3 waveform bridge |

## Per-State Aggregate Comparison

| State family | Baseline HR | Condition HR | Post HR | Condition - baseline HR | Baseline RMSSD | Condition RMSSD | Condition - baseline RMSSD | First support read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `music_still_calm` | `63.916` | `58.649` | mixed | `-5.267 bpm` | mixed | mixed | review after RR artifact pass | auditory/stillness state shows repeated HR settling direction |
| `music_movement` | `64.701` | `69.899` | mixed | `+5.197 bpm` | `30.641` | `24.529` | `-6.112 ms` | movement/embodiment state separates from stillness through HR rise and RMSSD drop |
| `breath_paced_calm` | `76.410` | `72.678` | `71.357` | `-3.732 bpm` | `21.600` | `25.639` | `+4.038 ms` | paced-breath state shows repeated autonomic settling direction |

## EEG Candidate Surface

The expanded-state rows produced real Muse EEG blocks and live waveform/state
tracker snapshots in the upgraded runs. The current EEG read is candidate until
quality masks are applied.

| State family | EEG candidate direction | Current boundary |
| --- | --- | --- |
| `music_still_calm` | decoded EEG blocks landed; visual tracker upgraded after r01 | run masked waveform QA before band/phase claims |
| `music_movement` | beta/gamma-heavy final tracker snapshots; movement artifact expected | compare against IMU and DRL/reference masks before neural interpretation |
| `breath_paced_calm` | beta/gamma-heavy snapshots while HRV carries strongest first-order regulation read | use HRV first; keep EEG for masked DE-1 / SPEC-1 / TOPOG reruns |

## Masked DE-1 / SPEC-1 / TOPOG Update

The local masked feature pass now attaches RR artifact review, packet
continuity, IMU motion, DRL/reference, and EEG rail-candidate rates to the
promoted expanded-state EEG windows.

| Lane | Current read | Boundary |
| --- | --- | --- |
| `DE-1` | state dynamics separate after RR QA: still/breath rows move toward lower condition HR; movement moves toward higher condition HR and higher gyro load | strongest current read is HRV + motion state separation |
| `SPEC-1` | real spectral features were computed from decoded Muse waveform samples across delta/theta/alpha/beta/low-gamma windows | candidate EEG spectral support only; rail and movement masks travel with every band result |
| `TOPOG` | all Muse channel labels are present across promoted state rows: `TP9`, `AF7`, `AF8`, `TP10`, `FPz`, `AUX_R`, `AUX_L`, `AUX` | temporal channels carry high rail-candidate load; cleaner support begins with FPz/AUX-style channels until channel QA is tightened |

## Nest Plug-In

| Nest | Plug-in role | What is now supported | Next gate |
| --- | --- | --- | --- |
| `Nest 4` | primary biology state-vector lane | HRV + Muse expanded-state manifold with real recurrence and controls | RR artifact review, IMU/DRL masks, B.A.S.I.S. manifest |
| `Nest 1` | formal return path | DE-1 dynamics, SPEC-1 spectral, TOPOG channel layout reopen with real biology data | masked DE-1 / SPEC-1 / TOPOG reruns |
| `Nest 3` | waveform / spectral / timing bridge | EEG waveform return path plus same-clock biological timing windows | waveform QA before spectral/phase promotion |
| `Nest 2` | physiology-response adapter | biology response structure for later matter/nutrition/water/electrochem rows | run separate real-data matter lane; do not use biology alone as matter proof |
| `Nest 5` | convergence / Mirror Index / Golden Mirror | repeated cross-state measured biology surface with quality gates | convergence table and live evidence memory patch |

## Patent Support Use

The expanded-state comparison strengthens the evidence support for:

- `FIG.10`: measured state-path validation ladder.
- `FIG.11`: hidden-state / bridge-vector style measured-path pipeline.
- `FIG.13`: transformer interpretability / state-variable comparison layer.
- `FIG.14`: external adapter lane, especially Muse/HRV biology.
- `FIG.15`: Golden Mirror / Mirror Index evidence-memory update loop.

Claims `19-30` should reference this as aggregate measured-state support only,
with full claim breadth tuned by counsel against prior art and section
`101 / 112` risk.

## Next Execution Queue

1. Phase 12C validity / exclusion ledger landed locally for promoted vs
   preflight / partial rows.
2. RR artifact / ectopic review landed locally for promoted expanded-state
   HRV windows.
3. IMU + DRL/reference + packet-continuity masks landed locally for promoted
   expanded-state Muse windows.
4. Masked expanded-state `DE-1`, `SPEC-1`, and `TOPOG` feature pass landed
   locally.
5. Patch the patent claim-to-paragraph-to-figure ledger for `FIG.10-FIG.15`
   and claims `19-30`.
6. Move to the next real-data non-biology target:
   `Spectral Signatures`, `H2O`, `Electrochemistry`, or second
   `Materials / Semiconductors` target.
