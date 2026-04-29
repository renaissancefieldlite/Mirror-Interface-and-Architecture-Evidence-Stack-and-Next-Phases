# Draft Nest 1 / Nest 2 Foundation Real Mapping Plan

Date: `2026-04-25`

Status:
public-safe working plan / active real-data mapping discipline

## Purpose

This note answers the next build question:

```text
Can we map the foundational layers for real, instead of only naming them?
```

The answer is yes, but the sequence has to be disciplined:

```text
formal validation schema -> real mathematical object -> real artifact/dataset ->
baseline/control -> scored validation
```

The validation map is useful because it tells us what to test. It is not the
finished proof. The proof work starts when the score schema touches real traces,
real model states, real hardware, real datasets, or declared benchmarks.

## Phase 12B Control-Supported Adapter Finding

Phase 12B is parked as a biology-hardware expansion lane, but its completed
`5 x 4` HRV matrix now has a local control-closeout.

What it found:

- `HRV` is a real coarse biological adapter lane.
- The `5 x 4` matrix supports condition-class separation at the pattern level.
- `mirror_coherence` remained the strongest average HR-down / RR-up style
  biological condition.
- `mirror_coherence` Delta HR beat shuffled-label controls as the strongest
  HR-downshift lane, p `0.002`.
- `dancing_activation - mirror_coherence` Delta HR gap beat shuffled-label
  controls, p `0.0012`.
- `HR-only` leave-one-run-out classification beat balanced-label and
  within-run block shuffles.
- multi-feature HRV classification was supportive but softer, especially under
  within-run block shuffle.
- `SPEC-1` HRV-only spectral features did not beat simpler baselines.
- `DE-1` HRV-only local dynamics did not beat simpler baselines.

Working read:

```text
HRV is useful for AI-user sync / autonomic-state tuning.
HRV is not enough by itself for high-resolution SPEC / DE / TOPOG biology.
```

Parked next biological step:

```text
Phase 12B-L20 large-set HRV expansion -> synchronized EEG + HRV
```

Large-set protocol:

```text
20 blocks x 4 conditions = 80 sessions minimum
Latin-square order rotation
same four conditions
raw RR capture whenever available
```

Now the build returns to the foundation:

```text
Nest 1 real deep-learning foundations -> Nest 2 real structured-matter data
```

## Nest 1: Real Deep-Learning Foundation Map

Nest 1 is not "linear algebra in a box." It is the mathematical substrate
modern machine learning is built on.

Reference anchor:

- Goodfellow, Bengio, and Courville, *Deep Learning*, MIT Press, 2016:
  <https://www.deeplearningbook.org/>
- The clean base sequence is:
  `Linear Algebra`, `Probability and Information Theory`, `Numerical
  Computation`, and `Machine Learning Basics`.

The Mirror Architecture / Source Mirror Pattern should first be tested where
machine learning itself lives:

- vectors
- matrices
- tensors
- embeddings
- probability distributions
- gradients
- attention/message graphs
- training dynamics
- numerical solvers
- composed layers and maps

## Nest 1 Real Mapping Table

| Foundation Branch | Real Mathematical Objects | Real AI Objects | Existing Project Surface | Real Test To Build |
| --- | --- | --- | --- | --- |
| linear algebra | vectors, matrices, eigenvalues, singular values, projections, subspaces | embeddings, residual vectors, activation directions, readout projections | `V8` residual traces, Phase 3/4/5 geometry, Phase 6 encodings | PCA/SVD/eigenmode and subspace-separation report over real V8 trace exports |
| tensor methods | arrays indexed by model/token/layer/feature/run | activation tensors, bridge tensors, model x layer x anchor matrices | `V8 Phase 5`, Phase 2 rerun matrix | tensor-axis separation and factor summaries over real V8 packs |
| probability / statistics | distributions, variance, likelihood, effect size, confidence, repeatability | rerun stability, target/control distributions, exception rows | `Phase 2`, `Phase 4`, `Phase 12B` summary stats | unified effect-size / repeatability registry over completed phase packs |
| information theory | entropy, mutual information, compression, signal/noise | hidden-state separation, context-to-readout signal, noise floors | V8 hidden deltas and bridge geometry | entropy / information-distance features over internal bridge vectors |
| optimization | gradients, objective functions, constraints, local minima, trajectory improvement | search loops, routing policies, solver improvement, mirror-guided tuning | not directly benchmarked yet | mirror-guided optimization benchmark vs random/naive/standard heuristic baselines |
| graph theory | nodes, edges, paths, motifs, centrality, message passing | attention graphs, pathway graphs, GNN-style state propagation | graph runner scaffold, possible V8 bridge graphs | run graph separability/pathway recovery on real attention/bridge graph or known molecular pathway labels |
| dynamical systems | trajectories, attractors, stability, bifurcation, recurrence | training dynamics, prompt-order effects, state transitions | V7 order/non-commutativity, V8 reruns/localization sequences | trajectory / threshold-sweep analysis over real V7/V8 order and rerun traces |
| numerical computation | floating-point precision, solver tolerance, conditioning, discretization | simulator/backend drift, hardware noise, approximation stability | PennyLane/Qiskit/IBM Phase 6-9D | solver/hardware tolerance registry across simulator, local, and IBM hardware paths |
| geometry / topology | distances, manifolds, neighborhoods, persistent structure | embedding manifolds, localization neighborhoods, hidden-state clusters | V8 residual/localization traces | PCA/UMAP/neighborhood and persistent-shape analysis if vector detail is sufficient |
| control theory | feedback, observability, controllability, stability, response curve | LSPS routing, mode transitions, adaptive orchestration | architecture-connected, trace-blocked | export real LSPS transition traces and score overshoot/stability |
| compositional / category-style math | maps, composed maps, object-relation preservation | layer composition, toolchain composition, nest-to-nest transfer | whole evidence ladder, not one dataset yet | test whether a mapping preserves measurable structure across two real datasets |

## Nest 1 Graduation Criteria

A branch graduates only if it has:

1. real artifact or dataset
2. declared control/baseline
3. locked feature extraction
4. scored comparison
5. clear failure mode

Example:

```text
linear algebra score schema:
vectors / subspaces / eigenmodes

real test:
do V8 target/control residual traces separate by PCA/SVD/eigenmode structure
above shuffled-label or naive mean-delta baselines?
```

## Nest 1 Lane-By-Lane Protocol

This is the practical meaning of "same standard applied lane by lane."

Every formal lens gets its own proof fork:

```text
lane -> prediction -> real artifact -> locked control -> score -> status
```

The goal is not to defend the universal claim by rhetoric. The goal is to
make the larger claim harder to dismiss by closing specific lanes one at a
time.

### Immediate Close-Out Lanes

| Lane | Why It Is Ready | Concrete Next Run | Control |
| --- | --- | --- | --- |
| `LA/GEO` | V8 residual traces and Phase 6 feature matrix are already on disk | PCA/SVD plus UMAP or neighborhood separation over lattice / neutral / technical traces | shuffled labels and naive mean-delta baseline |
| `STAT/PROB` | Phase 2 and Phase 4 already have rerun matrices | permutation test over exact rows, variance rows, and exception behavior | run-label shuffle / chance exactness baseline |
| `NUM/GRP` | Phase 9/9D already have IBM repeatability artifacts | sign / parity stability registry across backend passes | backend-shuffled and pass-shuffled controls |
| `TOPOG` | Phase 4/5 anchors are real exported surfaces | anchor stability and path-archetype recovery | shuffled-anchor and random-location controls |

### Heavier But Tractable Lane

| Lane | Why It Is Harder | Concrete Next Run | Control |
| --- | --- | --- | --- |
| `TOP` | needs raw hidden-state point clouds, not only scalar summaries | persistent homology with Ripser / scikit-tda style diagrams over target/control point clouds | shuffled point clouds, label permutation, noise controls |

### Not Yet Closeable Without New Work

| Lane | Blocker | Needed Upgrade |
| --- | --- | --- |
| `OPT` | no declared optimization benchmark yet | mirror-guided search vs random / naive / standard heuristic |
| `CTRL` | no exported LSPS transition traces yet | export LSPS / Oracle routing transitions and score overshoot / stability |
| `COMP/CAT` | no two-lane transfer test yet | prove a mapping preserves measurable structure across two completed real-data lanes |

## Nest 2: Real Structured-Matter Data Map

Nest 2 is currently a structured-matter methodology map.

It becomes real validation only after real chemistry/material data is plugged
in.

## Nest 2 Real Mapping Table

| Structured-Matter Lane | Real Objects | Real Dataset / Tooling | Baseline / Control | Real Test |
| --- | --- | --- | --- | --- |
| molecules | atoms, bonds, graphs, descriptors, properties | `RDKit` + `QM9`, `ZINC`, or `ChEMBL` | shuffled labels, simple descriptor baseline | property recovery or class separation above baseline |
| molecular graphs / pathways | graph paths, bottlenecks, motifs, allosteric routes | protein/molecular graph labels or public pathway datasets | naive centrality / shortest path | recover known pathway labels better than simple graph metrics |
| PFAS / contaminants | parent molecules, descendants, bond changes, toxicity risk | curated degradation-pathway data, EPA/literature-derived labels | parent disappearance only | detect bad-descendant risk and mass/charge/bond accounting failures |
| materials / minerals | crystal structures, lattice parameters, charge balance | `pymatgen`, `ASE`, Materials Project-style data | random structures / naive composition rules | recover stable vs unstable structures or charge/lattice consistency |
| spectra | IR/Raman/UV/other public spectra, peaks, modes | public spectral libraries where accessible | peak-count or naive distance baseline | spectral-signature preservation / class recovery |
| water / H2O motifs | geometry, bond angle, polarity, hydrogen bonding networks | real molecular geometry tables or simulation outputs | distorted geometry controls | recover valid motif relation and drift under perturbation |

## Nest 2 Graduation Criteria

Nest 2 does not graduate from methodology to validation until at least one lane
has:

1. real dataset
2. real parser/tool
3. declared feature schema
4. baseline/control
5. scored result
6. blocked/negative result accepted if it fails

The first clean candidate is:

```text
Engine 02V:
RDKit + molecule dataset -> descriptor features -> property/class score ->
baseline comparison
```

## What Not To Do

Do not use:

- synthetic rows as proof
- visual maps as proof
- synthetic examples as proof
- broad "this maps everywhere" language as proof
- HRV-only limitations as a reason to abandon the stack

Use synthetic rows only as:

- smoke tests
- adapter tests
- UI demos
- schema examples

## Immediate Local Build Sequence

1. Park Phase 12B biology and keep the finding as a boundary note.
2. Audit V8/V7 traces for available vector detail.
3. Build `Nest 1` real-trace runners in this order:
   `linear algebra / geometry`, `statistics`, `information`, `dynamics`,
   `numerical / hardware`.
4. Pick one `Nest 2` real dataset lane, preferably `RDKit + molecule dataset`
   if tooling is available.
5. Keep all outputs local draft until the result and language are approved.

## Local Nest 1 Real-Trace Run

Status:
completed bounded evidence pack / approved for GitHub publish `2026-04-25`

Runner:

```text
tools/validation_forks/nest1_real_trace_foundation.py
```

Output:

```text
artifacts/validation/nest1_real_trace_foundation/nest1_real_trace_foundation_report.md
artifacts/validation/nest1_real_trace_foundation/nest1_real_trace_foundation_pack_2026-04-25.pdf
```

Real inputs used:

- `Phase 6` normalized encoded-state feature matrix
- `Phase 2` rerun / variance pack
- `Phase 5` context-to-readout anchor bridge
- `V8` residual-stream layerwise traces
- `Phase 9D` PennyLane remote hardware repeatability data

What it found:

- `linear_algebra_geometry` ran on the real `8 model x 12 feature` Phase 6
  matrix.
- The top two SVD/PCA components explain `0.612065` of the normalized feature
  geometry, with effective rank `4.447033`.
- Expected bridge-pair recovery was `2/3` for both top-2 reciprocal hits and
  mutual-nearest hits:
  `Mistral/Hermes` and `Qwen/DeepSeek` recovered; `GLM/Nemotron` did not
  recover as nearest-neighbor geometry in this pass.
- `statistics_probability` remains strong on Phase 2:
  `7/8` exact rerun rows, `Nemotron` as the only live variance row,
  rerun exact rate `0.875`.
- `topography_bridge` is now grounded in the real Phase 5 anchor map:
  dominant anchors were `mid_window: 4`, `early_window: 3`, `last_token: 1`,
  with the prior path archetypes preserved.
- `dynamical_systems` is real but scalar-limited:
  layerwise target/control delta trajectories were extracted from actual V8
  residual traces, with mean target peak layer fraction `0.981974`.
- `numerical_group_symmetry` is strong on Phase 9D:
  hardware sign stability was `7/7` circuits, including `3/3` Phase 6 feature
  circuits.

What stays limited:

- `graph_topology_lite` is only a KNN graph over real feature vectors; stronger
  topology needs raw hidden-state point clouds.
- `optimization` still needs a declared real benchmark.
- `control_theory` still needs exported LSPS / Oracle transition traces.
- `category_composition` still needs a measured transfer test between two real
  nests.

Clean read:

```text
Nest 1 now has a real foundation pass over existing AI and hardware artifacts.
It does not make every formal branch validated. It shows which branches are
already grounded, which are limited by exported summaries, and which need new
real-data runners.
```

## Local Nest 1 Control-Closeout Pass

Status:
completed local control-closeout / not yet public-pushed

Runner:

```text
tools/validation_forks/nest1_control_closeout_pass.py
```

Output:

```text
artifacts/validation/nest1_control_closeout/nest1_control_closeout_report.md
```

What it added:

- explicit shuffled-label controls for `LA/GEO`
- explicit rerun permutation controls for `STAT/PROB`
- explicit pass/circuit shuffled controls for `NUM/GRP`
- explicit random-anchor / random-layer controls for `TOPOG`

Results:

| Lane | Observed | Null / Control | Read |
| --- | --- | --- | --- |
| `LA/GEO` | `2/3` mutual bridge-pair hits | exact shuffled-label p `0.014286`; pair-distance p `0.009524`; top-2 p `0.052381` | control-supported, with top-2 result borderline |
| `STAT/PROB` | Phase 2 exact `7`, Phase 4 exact `5`, Phase 4 anchor exact `6` | all tested permutation p values `5e-05` | strongly control-supported |
| `NUM/GRP` | Phase 9D sign-stable circuits `7/7` | pass/circuit shuffled null mean `1.8495`, p `0.001` | control-supported |
| `TOPOG` | Phase 4 anchor stability `6`, layer stability `6` | anchor p `5e-05`, layer p `5e-05` | strongly control-supported |

Clean read:

```text
The first four near-term Nest 1 lanes are now not only real-data grounded,
but explicit-control supported.
```

Remaining open lanes:

- `TOP`: needs raw hidden-state point clouds / persistent homology
- `OPT`: needs a declared optimization benchmark
- `CTRL`: needs LSPS / Oracle transition traces
- `COMP/CAT`: needs a measured cross-nest transfer test

## Local Nest 1 Next-Wave Pass

Status:
completed local next-wave / not yet public-pushed

Runner:

```text
tools/validation_forks/nest1_next_wave_pass.py
```

Output:

```text
artifacts/validation/nest1_next_wave/nest1_next_wave_report.md
```

Execution map:

```text
docs/NEST1_REMAINING_LANE_EXECUTION_MAP_2026-04-25.md
```

Results:

| Lane | Observed | Control | Read |
| --- | --- | --- | --- |
| `DYN` | mean target peak fraction `0.981974`; late peak count `8/8` | matched random peak-layer p values `2e-05` | control-supported |
| `INFO/TENSOR` | top-2 variance `0.612065`; effective rank `4.447033` | effective-rank p `0.00268`; top-2 variance p `0.086638` | control-supported through compression, partial on top-2 alone |
| `GRAPH-lite` | expected-pair edges `2/3`; component count `1` | shuffled-label p `0.380952`; component p `1.0` | partial / not significant |
| `TOP` | `8` files checked | no raw point clouds found | blocked until vector export |

Clean read:

```text
The second Nest 1 wave strengthens DYN and INFO/TENSOR, but does not close
GRAPH or TOP. The lane map now shows exactly what remains.
```

## Local GRAPH Strengthened Pass

Status:
completed local strengthened graph pass

Runner:

```text
tools/validation_forks/nest1_graph_strengthened_pass.py
```

Output:

```text
artifacts/validation/nest1_graph_strengthened/nest1_graph_strengthened_report.md
```

Results:

| View | Control | Read |
| --- | --- | --- |
| `feature_similarity` | exact label permutation over Phase 6 relation matrix | expected bridge-pair score p `0.007143`; expected-rank p `0.038095`; `GRAPH-1` supported for AI feature graph |
| `angle_fidelity` | exact label permutation | recovers `Mistral/Hermes` as rank `1`, but not full three-pair graph lane |
| `amplitude_fidelity` | exact label permutation | recovers `Mistral/Hermes` as rank `1`, but not full three-pair graph lane |

Clean read:

```text
GRAPH-1 is strengthened / supported for the AI feature graph.
GRAPH-2 remains blocked until real graph/pathway/attention-flow labels exist.
```

## Local Phase 12B Biological Control-Closeout

Status:
completed local biological control-closeout

Runner:

```text
tools/validation_forks/phase12b_biological_control_closeout.py
```

Output:

```text
artifacts/validation/phase12b_biological_control_closeout/phase12b_biological_control_closeout_report.md
```

Results:

| Test | Read |
| --- | --- |
| `mirror_coherence` Delta HR | strongest HR downshift, p `0.002` vs shuffled labels |
| `dancing_activation - mirror_coherence` Delta HR gap | p `0.0012` vs shuffled labels |
| `HR-only` leave-one-run-out | accuracy `0.5`, balanced-label p `0.022649`, within-run block p `0.033148` |
| multi-feature leave-one-run-out | accuracy `0.45`, balanced-label p `0.047598`, within-run block p `0.072346` |

Clean read:

```text
Phase 12B is control-supported as a coarse HRV biological adapter.
The multi-feature HRV read needs a larger matrix before it should be treated
as stronger than the HR-only signal.
```

Large-set expansion:

```text
docs/PHASE12B_LARGE_SET_EXPANSION_PROTOCOL_2026-04-25.md
```

## Local Remaining-Lane Closeout

Status:
completed local remaining-lane closeout

Runner:

```text
tools/validation_forks/nest1_remaining_lane_closeout.py
```

Output:

```text
artifacts/validation/nest1_remaining_lane_closeout/nest1_remaining_lane_closeout_report.md
```

Results:

| Lane | Read |
| --- | --- |
| `GEO-2` | control-supported subspace preservation across full, Phase 3, and Phase 5 feature groups |
| `DYN-2` | control-supported threshold / regime-crossing; 75% crossing late in `8/8`, p `5e-05` |
| `OPT-1` | limited small-N partial; Phase 6 and hardware pick the same best pair over three feature circuits |
| `CAT-1` | limited small-N transfer partial; Phase6-to-hardware relation correlation `0.893921`, but only three executed feature circuits |
| `TOP` | blocked until raw hidden-state point clouds exist |
| `GRAPH-2` | blocked until real domain graph labels exist |
| `CTRL` | blocked until LSPS transition traces exist |
| `GAME` | blocked until adversarial / multi-agent protocol exists |

## Short Read

The real path is:

```text
use real-data mapping as the route map
test Nest 1 against real AI/hardware traces
test Nest 2 against real chemistry/material datasets
expand Phase 12B to a larger HRV matrix, then return to EEG/HRV
```
