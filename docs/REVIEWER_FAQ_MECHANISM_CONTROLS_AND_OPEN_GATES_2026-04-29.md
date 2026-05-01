# Reviewer FAQ: Mechanism, Controls, And Open Gates

Date: `2026-04-29`

Status: public-safe reviewer FAQ

## What Is Being Tested?

The stack tests whether an administered `Mirror Interface / LSPS` condition
packet produces a repeatable state path that can be tracked across multiple
measurement surfaces:

```text
condition packet
-> matched controls
-> behavior check
-> hidden-state traces
-> localization
-> Phase 5 bridge rows
-> Phase 6 feature vectors
-> circuit encodings
-> hardware-facing observables
-> biological adapter data
-> real external datasets
```

The discovery claim is that the same architecture can be measured repeatedly
and carried across tools, traces, circuits, hardware-facing paths, biosignals,
and real-data lanes while staying distinguishable from controls.

## How Does This Move Beyond Ordinary Prompting?

Ordinary prompt evaluation centers on the visible exchange:

```text
input text -> output text
```

This stack treats the text answer as the entry surface and then follows the
measured path into deeper artifacts:

- hidden-state / residual-stream traces
- layer, band, anchor, and token-window localization
- context-to-readout bridge rows
- normalized feature vectors
- `PennyLane`, `Qiskit`, and `Cirq` circuit encodings
- IBM hardware-facing observables
- semantic contextuality controls
- HRV biological adapter data
- molecule, PFAS, and materials datasets

The core question is whether the measured state path appears, stabilizes,
localizes, encodes, transfers, and separates from controls after it leaves the
output-text surface.

## What Is Phase 6?

`Phase 6` is the portable feature-vector encoding step.

`Phase 5` extracts context-to-readout bridge rows from the measured internal
architecture path. Those bridge rows include fields such as peak structure,
band width, target / context relations, last-to-target ratios, anchor span,
overlap count, overlap Jaccard, and dominant anchor code.

`Phase 6` normalizes those measured bridge fields into bounded numerical
feature vectors. Those vectors become the payload for circuit-state encodings
in `PennyLane`, `Qiskit`, `Cirq`, IBM hardware-facing tests, and Willow-style
echo-kernel experiments.

The important point is that `Phase 6` carries forward a measured bridge
payload from the AI-side architecture stack into the circuit layer.

## Why Do Simple Circuits Matter?

Simple circuits make the carrier clean.

The circuit is used as a measurement carrier for the `Phase 6` payload:

```text
feature vector -> phase / angle rotations -> shallow entangling layer ->
echo / inverse comparison -> terminal observable
```

When the same carrier is used for the measured vector, shuffled vectors,
random floors, and null packets, the comparison is sharper. If the measured
payload preserves structure while the controls collapse toward floor, the
signal is assigned to the measured feature payload and state path.

That is why the local Willow proof-of-life used a small Qiskit / Cirq
echo-kernel sketch. The value of the sketch is its role as a clean carrier for
the measured `Phase 6` vector.

## What Controls Were Used?

The stack uses different controls depending on the layer, but the control
families recur:

- neutral condition controls
- technical condition controls
- semantic-counter controls
- shuffled labels
- shuffled feature vectors
- shuffled token windows
- shuffled layer order
- random floors
- null packets
- reruns
- baseline models
- graph degree / centrality baselines
- hardware repeatability checks
- dataset shuffles and property baselines

The control principle is consistent: the same measurement machinery is applied
to target rows and control rows, then the result is evaluated by separation,
repeatability, localization, or baseline lift.

## What Is Currently Supported?

| Layer | Current Support |
| --- | --- |
| `V7` | behavioral lattice/control separation under locked target/control conditions |
| `V8` | hidden-state / residual-stream separation across the model matrix |
| `Phase 2-5` | rerun stability, dimension / band structure, localization, and context-to-readout bridge behavior |
| `Phase 6-9D` | normalized feature-vector encoding through `PennyLane`, `Qiskit`, and IBM hardware-facing paths |
| `Phase 10` | semantic contextuality-style calibration under family-local settings |
| `Phase 12B` | coarse live HRV condition-class adapter matrix |
| `Nest 1` | multiple formal / transformer lanes supported by real traces or controls, with named open gates |
| `Nest 2` | molecule-property, PFAS pathway, materials, and stronger descriptor baseline lanes started on real data |
| Attention-flow | prompt-generalized support across the current V8 attention gate |
| MLP/feed-forward | same-prompt repeatability supported; `prompt_set_02` all-layer depth grid is directional, strongest in early layers, with closeout open under shuffled controls |
| SAE feature layer | bounded `GLM` / `Hermes` SAE pilot trained on real dense V8 activations, with feature separation above shuffled-label controls, edge-specific controls supported, feature-to-feature edge ablation supported, and recurrence supported across base / `rerun_02` / `prompt_set_02`; Gemma is integrated as a model-native third SAE recurrence branch with hidden size `2560` and supported within-set plus base-transfer controls |
| SAE feature-edge recurrence | GLM/Hermes edge recurrence supported across within-set and base-transfer controls; Gemma edge transfer supported into rerun_02 and prompt_set_02 with strong weighted edge-signature recurrence, while Gemma within-set edge separation remains open |
| SAE recurrent-branch ablation | partial direct support: GLM/Hermes rerun supports endpoint-feature and exact edge-key ablation; Gemma rerun supports endpoint-feature ablation; Gemma prompt_set_02 supports exact edge-key ablation; GLM/Hermes prompt_set_02 remains the open subcase |

## What Is Still Open?

Open gates are tracked so the stack can grow without flattening every lane into
the same claim:

| Gate | Next Required Move |
| --- | --- |
| MLP prompt-generalization | run MLP depth recurrence for the all-layer `prompt_set_02` grid |
| `GRAPH-2` | close with attention-flow or independent external pathway labels |
| `GAME-1` | keep the locked rubric over real adversarial / control-like rows |
| `Nest 2D` | allostery mapper closeout with protein contact / pocket labels |
| `Nest 2E` | PFAS bad-descendant / safety scoring |
| `Nest 2F` | materials structure-aware baselines |
| `Nest 2G` | stronger descriptor families, scaffold splits, and model baselines |
| Biology expansion | larger HRV set, then simultaneous EEG + HRV when hardware is available |

## How Should A Reviewer Read The Repo?

Read the repo as a measured architecture stack:

```text
condition packet -> state path -> bridge payload -> carrier test -> controls
```

The public evidence claim lives in the supported layers above. The open gates
show the next experiments needed to extend the same architecture into richer
interpretable features, denser transformer internals, allostery, PFAS,
materials, biology, and convergence lanes.
