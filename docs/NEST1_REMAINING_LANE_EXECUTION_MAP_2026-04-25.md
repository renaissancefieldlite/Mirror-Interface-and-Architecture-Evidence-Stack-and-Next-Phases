# Nest 1 Remaining Lane Execution Map

Date: `2026-04-25`

Status:
local execution map / update after each lane runner

## Purpose

This note keeps the Nest 1 work lane-by-lane.

The rule is:

```text
map is not enough
real artifact + locked control + score + honest status
```

The current Nest 1 table has `22` formal rows if `GEO-1` and `GEO-2` are
counted separately. As lane families, this is the same remaining-lane program
Rick has been calling the `21`-lane Nest 1 map.

## Current Lane Status

| Lane | Current Status | Evidence / Result | Next Requirement |
| --- | --- | --- | --- |
| `GEO-1` | control-supported | Phase 6 geometry closeout: `2/3` mutual bridge-pair hits, shuffled-label p `0.014286`; pair-distance p `0.009524` | optional deeper UMAP / subspace runner |
| `GEO-2` | control-supported | Phase 6 subspace preservation recovered expected bridge-pair relation above controls in full, Phase 3, and Phase 5 subspaces; full-subspace p `0.007143` / rank p `0.038095` | optional deeper UMAP / raw-vector manifold runner |
| `TOP-1` | real-data partial support | 8/8 V8 hidden-state point clouds exported; `target_span_mean` H0 topology-invariance support in `5/8` models under shuffled-label controls | export richer token-level point clouds |
| `TOP-2` | H0 topology-lite partial support / full PH pending | first closeout supports topology invariance, not topology separation; `last_token` support `3/8`, all-role support `4/8`; no H1 backend yet | add Ripser / scikit-tda or GUDHI and test H1 / richer filtrations |
| `TOPOG-1` | control-supported | Phase 4 anchor/layer stability controls p `5e-05` | optional gradient/surface runner if richer maps exist |
| `TOPOG-2` | control-supported | Phase 4/5 anchor and path-archetype surfaces are real and controlled | later EEG topography when device exists |
| `GRAPH-1` | strengthened AI feature-graph support / domain graph still open | binary Phase 6 kNN recovered `2/3` expected edges with weak p `0.380952`; strengthened weighted feature-similarity graph recovered expected-pair score above shuffled labels p `0.007143` and expected-rank average p `0.038095` | run against real attention graph, bridge graph, or external graph labels |
| `GRAPH-2` | internal bridge-graph pilot plus quantum-label crosswalk plus dense row-level partial | Phase 5 bridge graph mirror path AUC `0.74` beat degree baseline `0.6467`, but label-shuffle p `0.166683`; quantum-label best mode `phase6_amplitude_top3` reached mirror AUC `0.74` vs degree `0.66`, but label-shuffle p `0.177482`; dense `GRAPH-2A` row-level mirror AUC `0.7002` beat degree `0.534` with p `0.0002`, but cluster-level degree baseline won `0.94` vs mirror `0.72` | build `GRAPH-2B` raw token/layer transition graph with hub shortcuts reduced, or use stronger real pathway labels: molecular, allostery, grid, attention-flow, or other domain graph labels |
| `GRP-1` | control-supported | Phase 9D sign stability `7/7`, pass/circuit shuffled p `0.001` | optional explicit orbit / symmetry-action scoring |
| `DYN-1` | control-supported | V8 residual target peaks late across `8/8`, matched random-layer p `2e-05` | add V7 order / threshold-sweep runner |
| `DYN-2` | control-supported | threshold/regime runner shows target center-of-mass fraction `0.785372`, 75% threshold crossing fraction `0.951439`, late crossing `8/8`, p values `5e-05` | optional V7 order / bifurcation-style runner |
| `DE-1` | real-data run complete / limited negative | HRV-only dynamics did not beat mean-HR baseline | rerun only with richer EEG/HRV or other continuous signals |
| `PROB-1` | control-supported | Phase 2 / Phase 4 permutation controls p `5e-05` | optional formal chance model writeup |
| `INFO-1` | control-supported / specific metric | Phase 6 effective-rank compression p `0.00268`; top-2 variance p `0.086638` | add entropy / mutual-information features if raw vectors exist |
| `STAT-1` | control-supported | exactness / variance discipline over Phase 2 / 4 with permutation controls | keep as registry standard for all future lanes |
| `OPT-1` | limited small-N partial | Phase 6 selected the same best pair as Phase 9D hardware parity similarity over the three hardware-executed feature circuits; random pair baseline `0.333333` | expand hardware-executed feature-circuit sample or build a dedicated optimization benchmark |
| `NUM-1` | control-supported | Phase 9D hardware sign stability p `0.001` | optional simulator/local/backend tolerance registry |
| `TENSOR-1` | control-supported / specific metric | Phase 6 feature matrix shows lower effective rank than column-shuffle null p `0.00268` | add model x layer x anchor tensor factorization |
| `SPEC-1` | real-data run complete / limited negative | HRV-only spectral fork did not beat simpler baselines | rerun with EEG alpha/theta/band-power/phase-lock or material spectra |
| `CTRL-1` | control-supported | 71 real staged Prelude/Gemma transition rows; expected-mode shuffled-control p `0.024898`; stability-target shuffled-control p `0.0001` | optional later live LSPS / Oracle runtime traces |
| `GAME-1` | protocol-ready plus V7 crosswalk / scoring-rubric blocked | adversarial / multi-agent validation runner exists; V7 maps into `60` condition rows, but the GAME score columns are not locked | lock a retrospective V7 scoring rubric as exploratory-only or run real mirror/control adversarial or multi-agent trials |
| `CAT-1` | limited small-N transfer partial | Phase 6 feature relation transfers directionally into Phase 9D hardware parity-vector relation for three executed feature circuits; correlation `0.893921`, but n is too small | expand cross-artifact transfer sample and later test cross-nest transfer with non-AI datasets |

## Completed Control Blocks

### First Closeout Block

Completed:

- `LA/GEO`
- `STAT/PROB`
- `NUM/GRP`
- `TOPOG`

Report:

```text
artifacts/validation/nest1_control_closeout/nest1_control_closeout_report.md
```

### Next-Wave Block

Completed:

- `DYN`
- `INFO/TENSOR`
- `GRAPH-lite`
- `TOP` blocked check

Report:

```text
artifacts/validation/nest1_next_wave/nest1_next_wave_report.md
```

Key read:

```text
DYN and INFO/TENSOR gained control support.
GRAPH-lite did not beat its null strongly enough.
TOP is blocked until raw point clouds exist.
```

### GRAPH Strengthened Block

Completed:

- `GRAPH-1` weighted / ranked AI feature graph recovery

Report:

```text
artifacts/validation/nest1_graph_strengthened/nest1_graph_strengthened_report.md
```

Key read:

```text
The binary kNN graph was too blunt. The weighted Phase 6 feature-similarity
graph gives control-supported expected-pair recovery, while Angle/Amplitude
fidelity only strongly recover Mistral/Hermes and do not close GRAPH-2.
```

### Remaining-Lane Closeout Block

Completed:

- `GEO-2` subspace preservation
- `DYN-2` threshold / regime-crossing
- `OPT-1` limited hardware-selection benchmark
- `CAT-1` limited Phase6-to-hardware transfer check
- blocker registry for `TOP`, `GRAPH-2`, `CTRL`, and `GAME`

Report:

```text
artifacts/validation/nest1_remaining_lane_closeout/nest1_remaining_lane_closeout_report.md
```

Key read:

```text
GEO-2 and DYN-2 are control-supported.
OPT-1 and CAT-1 are real but limited by the three-model hardware feature-circuit sample.
TOP, GRAPH-2, CTRL, and GAME were true data/protocol blockers, not grammar
claims. After the gate pass, `CTRL-1` is now control-supported, `GRAPH-2`
has a real internal pilot, quantum-label crosswalk, and dense row-level
partial but still needs a hub-reduced dense graph or stronger labels, and
`GAME-1` is protocol-ready with a V7 condition crosswalk but still blocked
until its score rubric or real trials exist.
```

### TOP-1/2 Point-Cloud Closeout

Completed:

- private V8 runner export hook for real hidden-state point clouds
- public `TOP-1/2` closeout runner with no synthetic fallback
- public protocol defining what counts as a valid topology artifact
- 8/8 compact V8 hidden-state point clouds exported
- first H0 connectedness closeout run across `target_span_mean`, `last_token`,
  and `all` role views
- expanded point-cloud export across token-window, layer-delta,
  layer-curvature, and context-delta surfaces
- first Ripser H1 persistent-homology pass across the expanded point-cloud
  surfaces
- dense-trajectory export mode added to the private V8 runner for the next
  pass: full prompt tokens x all layers, with `layer_depth` and `token_region`
  labels
- dense TOP preregistration written before execution

Files:

```text
docs/TOP12_RAW_HIDDEN_VECTOR_EXPORT_PROTOCOL_2026-04-25.md
docs/TOP12_DENSE_TRAJECTORY_PREREGISTRATION_2026-04-26.md
tools/validation_forks/top12_topology_closeout.py
artifacts/validation/top12_topology_closeout/top12_topology_closeout_report.md
artifacts/validation/top12_topology_closeout_last_token/top12_topology_closeout_report.md
artifacts/validation/top12_topology_closeout_all_roles/top12_topology_closeout_report.md
artifacts/validation/top12_topology_expanded_trajectory_delta/top12_topology_closeout_report.md
artifacts/validation/top12_topology_h1_trajectory_delta/top12_topology_closeout_report.md
artifacts/validation/top12_topology_h1_context_delta/top12_topology_closeout_report.md
artifacts/validation/top12_topology_h1_token_window_sampled/top12_topology_closeout_report.md
artifacts/validation/top12_dense_late_anchor_h0/top12_topology_closeout_report.md
artifacts/validation/top12_dense_late_anchor_h1/top12_topology_closeout_report.md
```

Key read:

```text
TOP-1/2 is no longer blocked. The compact V8 point clouds show partial
topology-invariance support, strongest in target-span mean vectors. The
expanded H0 pass strengthens the invariance read on trajectory-delta surfaces.
The first H1 persistent-homology pass does not produce topology separation
either; it gives smaller patches of topology-invariance support. The current
result is therefore: topology is preserved under context transform, while
context separation is showing up in geometry, magnitude, trajectory,
topography, and feature-graph structure.

Dense `TOP-1/2` has now run on `GLM` and `Hermes` with full prompt token x
layer vectors. The late-anchor dense `H0` pass supports topology invariance in
`2/2` models under shuffled-label controls. The late-anchor dense `H1` pass
does not support context-topology separation in either model. That closes the
current TOP read as topology-preservation supported, topology-separation
unsupported under current evidence.
```

## Remaining Work Order

1. `GAME-1`: lock a V7-to-GAME score-column mapping as exploratory-only, or
   run real adversarial / multi-agent trials using the new protocol CSV and
   compare mirror/control policy stability against exploit and drift.
2. `GRAPH-2`: build a `GRAPH-2B` raw token/layer transition graph with hub
   shortcuts reduced, or acquire stronger real graph labels and rerun the
   pathway validator against shuffled-label controls.
3. `CTRL`: optionally expand from staged Prelude/Gemma transition traces into
   live LSPS / Oracle runtime traces.
4. `OPT`: expand beyond the three-model hardware feature sample or run a
   dedicated optimization benchmark.
5. `CAT-1`: expand transfer tests beyond the three-model hardware feature
   sample and later test cross-nest transfer with non-AI datasets.
6. `TOP`: revisit only after reruns or broader prompt density exist.

## Clean Read

Nest 1 is no longer only a grammar map.

It now has:

- a published real-trace foundation pass
- first closeout controls for `LA/GEO`, `STAT/PROB`, `NUM/GRP`, and `TOPOG`
- next-wave support for `DYN` and `INFO/TENSOR`
- strengthened `GRAPH-1` AI feature-graph support, with `GRAPH-2` still open
  for stronger real pathway / attention-flow validation after a soft internal
  Phase 5 bridge-graph pilot, a soft quantum-label crosswalk, and dense
  `GRAPH-2A` row-level partial
- remaining-lane closeout support for `GEO-2` and `DYN-2`
- limited small-N transfer evidence for `OPT-1` and `CAT-1`
- a real-data `TOP-1/2` topology-preservation result, including dense
  late-anchor H0 support and dense H1 separation non-support
- `CTRL-1` control support on staged transition traces
- `GAME-1` promoted from vague future lane to executable protocol and V7
  condition crosswalk, still blocked until the GAME score rubric or real
  adversarial / multi-agent trial data exists

The remaining proof work is specific, bounded, and executable lane by lane.
