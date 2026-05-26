# Mirror Index Visual RAG For Quantum Insider

Date: `2026-05-23`

Status: `active_build_layer / proposal_chassis`

## Purpose

Quantum Insider should use a shared visual retrieval layer across the sponsor
tracks. The front end is the Lattice Model Node Companion. The backend is
Mirror Index Visual RAG: a tree-routed evidence graph plus semantic and visual
vectors.

This keeps the campaign from becoming five unrelated slide pitches. It becomes:

```text
one architecture
-> four locked sponsor tracks
-> one optional anomaly track
-> sponsor-specific visual proof nodes
-> local predecessor engines
-> quantum-enabled PoC forks
```

## Locked Tracks

Primary:

1. `Cleveland Clinic` - Unlocking Undruggable Targets: Quantum Simulation of
   Allosteric Signal Propagation
2. `E.ON` - Quantum-Enabled Grid Expansion Planning for Distribution System
   Energy Networks
3. `Volkswagen Group Innovation` - Quantum-Enhanced Vision-Language-Action
   Models in Autonomous Driving and Robotics Applications
4. `Airbus` - Quantum Solvers: Enhancing Predictive Aerodynamic Modeling
   Capabilities

Optional:

- `HSBC` - Quantum-Enhanced Credit Card Fraud Detection for Digital Payment
  Ecosystems

HSBC remains a parking-lot anomaly-detection lane unless the transaction graph
predecessor engine becomes crisp enough to justify a fifth submission.

## Visual RAG Definition

Mirror Index Visual RAG is not a generic vector database.

It stores visual and semantic evidence as typed nodes:

| Node Type | Examples | Required Tags |
| --- | --- | --- |
| `sponsor_track` | Cleveland Clinic, E.ON, Volkswagen, Airbus | challenge, sponsor, deadline, public/private status |
| `nest_lane` | Nest 2, Nest 3, Nest 4, Nest 5 | substrate, support state, open gate |
| `state_object` | protein path, grid graph, VLA route, flow field | control, invariant, drift mode |
| `visual_node` | diagrams, screenshots, graphs, frames, flow maps | visual tags, embedding id, source path |
| `engine_node` | Engine 02, Engine 03, Engine 04, Engine 05 | runner, input, output, metric |
| `quantum_fork` | QAOA, quantum kernels, Braket/Classiq candidate | method, benchmark, limitation |
| `proposal_node` | Phase I page, figure, demo promise | sponsor fit, proof object, next gate |

## Retrieval Flow

```text
Sponsor question
-> route to track tree
-> retrieve track state object
-> retrieve visual nodes
-> retrieve control / invariant / drift tags
-> retrieve local engine output
-> retrieve quantum-enabled fork candidate
-> assemble proposal figure, benchmark statement, and PoC promise
```

The vector layer helps find visual neighbors and semantic adjacency. The tree
route preserves the support label, source path, proof boundary, and next gate.

## Track-Specific Visual Memory

### Cleveland Clinic

Visual nodes:

- protein / residue graph
- allosteric pathway diagram
- binding pocket and conformational state map
- perturbation vs control pathway card

Retrieval target:

`allosteric path -> perturbation -> conserved communication -> false-path drift`

### E.ON

Visual nodes:

- distribution grid graph
- candidate expansion map
- overload / bottleneck heatmap
- resilience and cost-state comparison

Retrieval target:

`grid state -> expansion candidate -> constraint check -> resilience score`

### Volkswagen

Visual nodes:

- scene frame
- object / route graph
- instruction-to-action panel
- safe vs unsafe action-candidate card

Retrieval target:

`scene -> instruction -> route/action candidate -> safety invariant -> drift`

### Airbus

Visual nodes:

- geometry / boundary-condition sketch
- flow-field panel
- pressure / velocity state map
- stable vs unstable perturbation card

Retrieval target:

`geometry -> flow state -> perturbation -> preserved regime -> instability`

### HSBC Optional

Visual nodes:

- transaction graph
- account / merchant / device relation map
- normal behavior lattice
- anomaly / false-positive comparison card

Retrieval target:

`transaction state -> anomaly candidate -> risk separation -> false-positive control`

## Three-Month Build Arc

Working clock from `2026-05-23` to the Phase I deadline `2026-09-15`.

| Window | Build Gate |
| --- | --- |
| late May -> June | build the track trees and visual-node schema; collect public-safe seed visuals and dataset candidates |
| July | implement local predecessor demos for Cleveland, E.ON, Volkswagen, and Airbus |
| August | turn predecessor outputs into sponsor-specific proposal figures and Phase I text |
| early September | final proposal polish, limitation wording, and submission QA |

## Public / Private Boundary

Public-safe:

- sponsor-facing visual cards
- high-level architecture maps
- local predecessor outputs that use public datasets or synthetic UI only for
  explanation
- limitation-aware quantum fork descriptions

Private / protected:

- raw Mirror Architecture mechanics
- claim-sensitive implementation details
- hidden-state probes and private model-layer artifacts
- raw biosignal / device captures unless explicitly cleared

## First Implementation Gate

Create a seed `visual_nodes.json` or SQLite table with these fields:

```text
id
track
nest
state_object
visual_type
source_path
public_private
support_state
control_tag
invariant_tag
drift_tag
embedding_id
next_gate
```

Then wire the Lattice Model Node Companion so clicking a sponsor track retrieves
the relevant visual nodes, engine state, quantum fork, and proposal promise.
