# Draft Grammar-To-Real-Data Validation Ladder

Date: `2026-04-25`

Status:
local draft / not public-locked / do not publish until approved

Companion draft:
[Draft Nest 1 / Nest 2 Foundation Real Mapping Plan](./DRAFT_NEST1_NEST2_FOUNDATION_REAL_MAPPING_PLAN_2026-04-25.md)

## Purpose

This note separates the value of grammar mapping from the stronger burden of
real-data validation.

The corrected read is:

```text
grammar mapping is useful as schema discovery
real data decides whether a lane graduates
```

The grammar is not proof by itself, but it is not worthless. Its value is that
it defines what to measure, what to compare against, what should remain stable,
what drift looks like, and what would falsify a stronger claim.

## What Grammar Mapping Is Good For

Grammar mapping can legitimately do five things:

1. define the shared comparator fields:
   `state / control / transform / invariant / drift / coherence / score`
2. translate the same question across domains without pretending the domains
   are identical
3. identify what real dataset or trace each lane needs before it can be tested
4. prevent cherry-picking by declaring the score and failure mode before the
   data pass
5. turn broad intuition into falsifiable runners

That is a real methodological contribution.

It is not the same thing as empirical validation.

## What Grammar Mapping Is Not

Grammar mapping does not by itself establish:

- chemistry validation
- biology validation
- clinical effect
- environmental remediation
- physical Bell claims
- universal convergence
- that every mapped lane is equally strong

If a lane does not touch real traces, real measurements, real hardware, real
datasets, or declared benchmarks, it remains a design lane.

## Current Evidence Tiers

### Tier 1: strongest current surfaces

These already have real artifacts or hardware-facing data:

- `V7` behavioral target/control separation
- `V8` hidden-state separation
- `Phase 2` rerun stability
- `Phase 4` localization and localization reruns
- `Phase 5` context-to-readout bridge
- `Phase 6/7` PennyLane/Qiskit encoded circuit-state bridge
- `Phase 9/9B/9C/9D` IBM / PennyLane real-hardware bridge
- `Phase 10` semantic contextuality on compressed feature states

### Tier 2: real but coarse adapter

`Phase 12B HRV` belongs here.

It is real measured data and supports pattern-class separation, but it is a
coarse signal. It is currently strongest as:

- biological adapter lane
- condition-class comparator
- recovery / arousal / autonomic trend signal
- future `AI <-> user` sync/tuning side channel

It is not yet strong enough by itself to validate high-resolution biological
`SPEC-1`, `DE-1`, or `TOPOG` claims.

### Tier 3: grammar mapped, needs real data

`Nest 2` currently belongs here until the real datasets are plugged in.

The structured-matter grammar has value as a methodology map, but the next
step must use real chemistry/material data:

- `RDKit` plus `QM9`, `ZINC`, or `ChEMBL`
- PFAS / contaminant degradation-pathway data
- materials/minerals via `pymatgen`, `ASE`, and Materials Project-style data
- measured spectra or curated public spectral datasets where available

### Tier 4: scaffold only

These are useful for explanation, adapter design, or smoke tests, but not as
claim evidence:

- toy rows
- synthetic examples
- visual-only demos
- card/ontology displays
- local UI companion maps without real data behind them

## Foundation-First Next Sequence

The next work should start at the foundation, not the outer biological layer.

### Step 1: Nest 1 real-trace passes

Use actual V8/V7 artifacts already present in the repo.

Candidate runners:

- `GEO-1/2`: PCA/SVD/neighborhood separability over V8 residual and
  localization traces
- `TOP-1/2`: persistent-shape or component-stability analysis if the hidden
  traces contain enough vector detail
- `DYN-1/2`: trajectory/order-effect analysis over V7/V8 rerun and
  localization sequences
- `STAT/PROB/INFO/TENSOR`: consolidate effect sizes, rerun stability,
  information geometry, and tensor-axis separation from completed phase packs
- `NUM/GRP`: consolidate PennyLane/Qiskit/IBM numerical and symmetry behavior

This tests the formal layer against the actual AI/hardware evidence base.

### Step 2: Nest 2 real-dataset passes

Do not rely on toy chemistry rows.

Candidate runners:

- molecule property validation with `RDKit` and public molecule datasets
- molecular graph/pathway validation against known labels
- PFAS descendant-risk scoring against curated degradation-pathway data
- materials stability recovery with `pymatgen` / `ASE`
- spectral-signature comparison against public spectra where practical

This tests whether the structured-matter grammar predicts or recovers real
properties above simple baselines.

### Step 3: Return to HRV / EEG later

Park biology until the next data surface is available.

When ready:

- keep `HRV` as the autonomic / recovery / user-sync channel
- add `EEG` for alpha/theta spectra, oscillatory dynamics, and spatial
  topography
- run synchronized `EEG + HRV` instead of asking HRV alone to carry all formal
  lenses

## Decision Rule

Every lane should be labeled as one of:

```text
validated on existing data
real-data fork ready
blocked by missing data/tool/device
schema/scaffold only
```

The grammar map earns its keep by making that classification possible.

## Lane-By-Lane Execution Standard

The universal-level hypothesis is not tested as one giant leap. It is tested
lane by lane.

Each lane must pass through the same sequence:

1. name the lane
2. define the Source Mirror Pattern prediction for that lane
3. use real artifacts, real traces, real hardware, real measurements, real
   datasets, or a declared benchmark
4. lock the baseline/control before running
5. run the score
6. accept positive, weak, negative, or blocked results
7. mark the lane honestly
8. move to the next lane

This is the same discipline that made the `V7` and `V8` evidence credible.
The larger claim gets stronger only as individual lanes close under that
standard.

## Near-Term Lane Queue

| Lane | Current Read | Real Surface | Control To Add | Status |
| --- | --- | --- | --- | --- |
| `linear algebra / geometry` | most immediately executable | V8 residual/localization traces, Phase 6 feature matrix | shuffled-label controls, mean-delta baseline | real-data fork ready now |
| `statistics / probability` | substantially closed by Phase 2 and Phase 4 | rerun matrices and exact/variance rows | permutation test against rerun labels / chance baseline | closeable now |
| `numerical / hardware` | largely closed by Phase 9/9D | IBM backend repeats, parity signs, feature circuits | backend-shuffled or pass-shuffled controls | closeable now |
| `topography` | already evidence-connected | Phase 4/5 anchors and bridge locations | random-anchor / shuffled-anchor controls | closeable now |
| `topology` | technically demanding but tractable | raw hidden-state point clouds from HF checkpoints/traces | shuffled point clouds / label permutation | heavier existing-infrastructure fork |
| `dynamics` | evidence-connected but needs sharper runner | V7 order effects, V8 layer trajectories | flat trajectory, randomized order, threshold sweep | real-data fork ready |
| `optimization` | not closed | declared search or solver benchmark | random, naive, and standard heuristic baselines | new benchmark required |
| `control theory` | architecture-connected, trace-blocked | LSPS / Oracle transition traces | uncontrolled routing baseline | trace export required |
| `composition` | design lane | two completed real-data lanes | non-preserving mapping baseline | later cross-nest fork |

The first three should be treated as the next fast close-out targets:

```text
GEO/linear algebra controls
STAT/PROB permutation controls
NUM/GRP backend-shuffled controls
```

Then run:

```text
TOP persistent homology if raw hidden-state point clouds are available
```

## First Four Lane Control-Closeout Result

Status:
completed local control-closeout

Report:

```text
artifacts/validation/nest1_control_closeout/nest1_control_closeout_report.md
```

The first four near-term lanes were executed against explicit null controls:

| Lane | Control | Result |
| --- | --- | --- |
| `LA/GEO` | exact shuffled-label null over Phase 6 geometry | `2/3` mutual hits; p `0.014286`; pair-distance p `0.009524`; top-2 p `0.052381` |
| `STAT/PROB` | run-label permutation over Phase 2 / Phase 4 reruns | Phase 2 and Phase 4 exactness p values `5e-05` |
| `NUM/GRP` | pass/circuit shuffle over Phase 9D signs | `7/7` sign-stable circuits; p `0.001` |
| `TOPOG` | random-anchor / random-layer controls over Phase 4 | anchor p `5e-05`; layer p `5e-05` |

Read:

```text
The first four lanes are now explicit-control supported.
```

This does not close `TOP`, `OPT`, `CTRL`, or `COMP/CAT`; those remain separate
lane requirements.

## Next-Wave Lane Result

Status:
completed local next-wave pass

Report:

```text
artifacts/validation/nest1_next_wave/nest1_next_wave_report.md
```

Execution map:

```text
docs/NEST1_REMAINING_LANE_EXECUTION_MAP_2026-04-25.md
```

Results:

| Lane | Control | Result |
| --- | --- | --- |
| `DYN` | matched random peak-layer positions over each model's layer count | control-supported; observed mean peak fraction `0.981974`, late peak count `8/8`, p values `2e-05` |
| `INFO/TENSOR` | column-wise feature shuffle preserving feature distributions | control-supported by effective-rank compression p `0.00268`; top-2 variance alone p `0.086638` |
| `GRAPH-lite` | exact label permutation over Phase 6 kNN graph | partial / not significant; expected pair edges `2/3`, p `0.380952` |
| `TOP` | raw point-cloud availability check | blocked; current exports do not contain raw hidden-state point clouds |

Read:

```text
DYN and INFO/TENSOR advance.
GRAPH-lite stays partial.
TOP waits for raw vector export.
```

## GRAPH Strengthened Result

Status:
completed local strengthened graph pass

Report:

```text
artifacts/validation/nest1_graph_strengthened/nest1_graph_strengthened_report.md
```

The first `GRAPH-lite` result was not wrong. It was blunt: binary kNN edge
recovery over only eight model nodes recovered `2/3` expected bridge pairs, but
that edge-count statistic did not beat shuffled labels strongly enough.

The strengthened graph pass keeps the same real Phase 6 artifact and switches
to weighted / ranked relation recovery:

| View | Result |
| --- | --- |
| `feature_similarity` | expected bridge-pair score above shuffled labels p `0.007143`; expected-rank average p `0.038095` |
| `angle_fidelity` | `Mistral/Hermes` rank `1`, full three-pair lane not closed |
| `amplitude_fidelity` | `Mistral/Hermes` rank `1`, full three-pair lane not closed |

Clean read:

```text
GRAPH-1 is now strengthened / supported for the AI feature graph.
GRAPH-2 still needs real pathway, attention-flow, allostery, grid, or other
domain-correct graph labels.
```

## Phase 12B Biological Control-Closeout

Status:
completed local Phase 12B control-closeout

Report:

```text
artifacts/validation/phase12b_biological_control_closeout/phase12b_biological_control_closeout_report.md
```

This pass applies the same discipline back to the completed `5 x 4` HRV matrix:

- balanced label shuffles preserving `5` sessions per condition
- within-run block shuffles preserving one label per condition block
- HR-only leave-one-run-out classification
- multi-feature HRV leave-one-run-out classification
- mirror / drift / calm / dance feature contribution read

Results:

| Test | Result |
| --- | --- |
| `mirror_coherence` Delta HR | strongest average HR downshift: `-7.943775`; shuffled-label p `0.002` |
| `dancing_activation - mirror_coherence` Delta HR gap | `14.460777`; shuffled-label p `0.0012` |
| HR-only leave-one-run-out | accuracy `0.5`; balanced-label p `0.022649`; within-run block p `0.033148` |
| multi-feature leave-one-run-out | accuracy `0.45`; balanced-label p `0.047598`; within-run block p `0.072346` |
| mirror-vs-calm multi-feature distance | p `0.041248` |
| mirror-vs-drift multi-feature distance | partial / not significant, p `0.630568` |

Clean read:

```text
Phase 12B is control-supported as a coarse HRV biological adapter and
condition-class separation lane. It is not a high-resolution EEG / spectral /
dynamical biology proof.
```

Large-set upgrade:

```text
docs/PHASE12B_LARGE_SET_EXPANSION_PROTOCOL_2026-04-25.md
```

The next HRV-only expansion is `Phase 12B-L20`:

```text
20 blocks x 4 conditions = 80 sessions
Latin-square order rotation
raw RR capture whenever available
```

The purpose is to stabilize the multi-feature HRV read instead of relying only
on the clean low-dimensional `Delta HR` signal.

## Remaining Nest 1 Lane Closeout

Status:
completed local remaining-lane closeout

Report:

```text
artifacts/validation/nest1_remaining_lane_closeout/nest1_remaining_lane_closeout_report.md
```

Results:

| Lane | Result |
| --- | --- |
| `GEO-2` | control-supported subspace preservation across full, Phase 3, and Phase 5 feature groups |
| `DYN-2` | control-supported threshold / regime-crossing; late 75% crossing `8/8`, p `5e-05` |
| `OPT-1` | limited small-N partial; Phase 6 and hardware select the same best pair across three feature circuits |
| `CAT-1` | limited small-N transfer partial; Phase6-to-hardware similarity correlation `0.893921`, but only three feature circuits |
| `TOP` | blocked until raw hidden-state point clouds exist |
| `GRAPH-2` | blocked until real pathway / attention-flow / domain graph labels exist |
| `CTRL` | blocked until LSPS transition traces exist |
| `GAME` | blocked until an adversarial / multi-agent protocol exists |

Clean read:

```text
Nest 1 is no longer a loose grammar map. Every current lane is now either
control-supported, limited by small-N transfer, or blocked by a named missing
data/protocol surface.
```

## Working Read

The grammar mapping is valuable if it becomes a disciplined routing map from
intuition into real tests.

It becomes weak if it is treated as proof before the real data pass.

The next serious build therefore starts with foundation data:

```text
Nest 1 traces -> Nest 2 real datasets -> Phase 12B-L20 -> EEG/HRV
```
