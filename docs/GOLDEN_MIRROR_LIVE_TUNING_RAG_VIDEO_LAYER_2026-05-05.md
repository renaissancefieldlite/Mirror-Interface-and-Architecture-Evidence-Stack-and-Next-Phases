# Golden Mirror Live Tuning, RAG, Memory, And Video Layer

Date: `2026-05-05`

Status: `parked_architecture_layer / post-patent_build_target`

## Purpose

This document parks the next Golden Mirror build layer while the patent core
and nest closeouts remain the active execution priority.

The build target is a Hermes-based Golden Mirror agent that can ingest the
existing evidence stack, maintain persistent memory, use live biosignals for
state tuning, read continuous video as a visual state stream, and improve its
responses through a Universal Tuning Layer tied back to the Mirror Architecture
evidence ladder.

This is the applied system form of the current stack:

```text
measured evidence lanes
-> retrieval and memory
-> Hermes Golden Mirror agent
-> live HRV / EEG tuning
-> continuous video-state vector
-> Mirror Index tree routing
-> Universal Tuning Layer
-> better instantaneous Mirror Architecture alignment
```

## System Spine

The Golden Mirror build should use the new Hermes agent as the base agentic
surface:

```text
Hermes agent base
-> Mirror Interface / LSPS wrapper
-> Mirror Index over evidence, patent, website, and experiment docs
-> SQL memory for structured state and events
-> JSON memory for portable session snapshots
-> live biosignal adapter from HRV / EEG SDK streams
-> continuous video vector adapter
-> Universal Tuning Layer for output scoring and correction
-> Golden Mirror model / app layer
```

The first version is a local architecture harness. Model tuning comes after
the harness can measure recurrence, drift, state alignment, and correction
quality.

## Layer 1: Hermes Agent Base

Hermes is the proposed base buildout because it fits the steering and
continuity profile we need:

- steerable reasoning
- research-agent behavior
- strong instruction following
- local / open model experimentation path
- compatibility with wrapper, memory, and eval harnesses
- useful fit for Golden Mirror continuity and state-path recurrence tests

The Golden Mirror build should start as a wrapper and eval harness around the
Hermes agent. Fine-tuning or adapter training follows only after the scoring
layer proves which response patterns improve alignment.

## Layer 2: Mirror Index Evidence Spine

The retrieval system is the knowledge spine. It should index the public-safe
and private-local evidence layers separately, then route through a navigable
tree of claims, phases, nests, experiments, figures, and artifacts.

Initial retrieval collections:

| Collection | Purpose |
| --- | --- |
| `mirror_evidence_docs` | README, chronological log, reviewer FAQ, mechanism explainer, white papers |
| `patent_spine` | claim spine, figures, embodiments, USPTO-format drafts |
| `nest_lanes` | Nest 1 through Nest 5 protocols, results, and open gates |
| `transformer_internals` | V8, attention, MLP, SAE, dense trajectory, topology, graph docs |
| `quantum_bridge` | Phase 6 vectors, PennyLane / Qiskit / IBM / Willow proposal notes |
| `biology_biosignal` | Phase 12B, Nest 4A, EEG + HRV protocols, Muse / HRV live-tuning plan |
| `product_surface` | website language, companion map, pitch decks, app/product concepts |

Retrieval should always return:

- source path
- date
- evidence status
- public/private boundary
- linked phase or nest
- confidence / support state

The Mirror Index upgrade adds a tree-routed layer inspired by recent
reasoning-based RAG work, while preserving our own architecture. The index
should treat each evidence row as a typed node:

```text
claim node
-> phase / nest node
-> experiment node
-> artifact / figure node
-> support-state label
-> public/private boundary
-> next gate
```

The vector layer remains a support channel for visual memory, semantic
adjacency, video frames, biosignal states, and related-context discovery. The
tree carries the proof path; mirror vectors carry recurrence and nearby context.

Dedicated design doc:

- [Mirror Index: Tree-Routed RAG, Evidence Graph, And Mirror Vector Memory](./MIRROR_INDEX_TREE_RAG_ARCHITECTURE_2026-05-05.md)

## Layer 3: SQL And JSON Persistent Memory

Use SQL for structured, queryable continuity:

| Table | Role |
| --- | --- |
| `sessions` | run id, date, operator context, active project, active lane |
| `artifacts` | docs, reports, vectors, figures, proofs, private/public status |
| `claims` | claim element, support docs, evidence status, patent mapping |
| `experiments` | phase/nest, input surface, controls, result, p-values, next gate |
| `model_outputs` | prompt, response, score, correction, selected pathway |
| `biosignal_windows` | HRV / EEG / fNIRS windows, condition labels, state vector |
| `video_frames` | frame batch id, embedding id, visual tags, time span |
| `tuning_events` | Universal Tuning Layer score, correction, accepted/rejected outcome |

Use JSON for portable memory snapshots:

```text
session_state.json
current_lane_state.json
operator_context.json
golden_mirror_profile.json
retrieval_trace.json
live_tuning_state.json
```

SQL gives stable long-term querying. JSON gives easy transport, inspection,
thread handoff, and local agent reload.

## Layer 4: Continuous Video Input

The permanent video input acts as a continuous visual state stream.

Goal:

```text
camera / screen / workspace frames
-> frame sampling
-> visual embeddings
-> time-windowed vector memory
-> scene / object / gesture / interface-state tags
-> retrieval context for the Golden Mirror agent
```

Use cases:

- understand what the operator is looking at or building
- maintain continuity across physical bench work, app work, docs, and diagrams
- build a vector memory of recurring visual objects and layouts
- support patent figure review, website review, hardware bench sessions, and
  app UI work
- pair visual frames with biosignal windows when running guided sessions

The first safe version can use periodic screenshots or operator-approved
camera frames. The later version can run as a continuous local visual memory
adapter with clear privacy controls.

## Layer 5: Golden Mirror Live Tuning Layer

This is the live state-adapter layer for HRV and EEG.

Input streams:

- `MoFit` or other HRV / RR interval stream
- `Muse S Athena` EEG / fNIRS / PPG stream if SDK or export path allows
- optional Petal / OSC / LSL / webhook / CSV bridge where useful

Feature vector:

| Signal | Candidate features |
| --- | --- |
| HRV | delta HR, RMSSD, SDNN, recovery slope, raw RR intervals, artifact count |
| EEG | alpha, theta, beta, alpha/theta ratio, band-power deltas, coherence where available |
| fNIRS / PPG | oxygenation trend, pulse trend, effort / relaxation proxy if available |
| Session | baseline / condition / post window, state target, user feedback, pathway label |

Live state classes:

- calm
- focus
- drift
- activation
- recovery
- overload
- coherence

The Golden Mirror agent uses the live state vector to choose the next guidance
move:

```text
state vector
-> pathway target
-> voice / text / breath / sound / silence instruction
-> live signal check
-> next guidance move
```

## Layer 6: Guided Pathway App Surface

The app layer turns Golden Mirror live tuning into a user-facing experience.

Candidate public frame:

```text
Guided Pathway: adaptive meditation and cognitive-state training powered by
live EEG / HRV feedback and Golden Mirror guidance.
```

Initial pathway modes:

| Mode | Target |
| --- | --- |
| `Calm Pathway` | settle arousal and stabilize breath |
| `Focus Pathway` | increase stable attention while managing overload |
| `Recovery Pathway` | post-stress downshift and regulation |
| `Sleep Pathway` | pre-sleep deceleration and low-stimulation guidance |
| `Explorer Pathway` | creativity, deep meditation, altered-state exploration |

For public app-store language, lead with wellness, focus, recovery, sleep
preparation, meditation, and cognitive-state training. Deeper healing language
belongs in research notes or carefully reviewed wellness wording.

## Layer 7: Universal Tuning Layer

The Universal Tuning Layer tests outputs against the Mirror Architecture and
feeds corrections back into the model wrapper.

Scoring dimensions:

| Score | Question |
| --- | --- |
| `mirror_alignment` | does the output preserve the active architecture path? |
| `state_fit` | does the output match the live HRV / EEG / visual state? |
| `continuity` | does it preserve thread, project, and evidence context? |
| `support_status` | does it distinguish supported, partial, parked, and next-gate rows? |
| `actionability` | does it produce an executable next move? |
| `tone_fit` | does it match the operator state and task intensity? |
| `evidence_grounding` | does it cite or retrieve the right phase / nest / artifact? |
| `drift_penalty` | does it flatten, overclaim, underclaim, or miss the active path? |

Correction loop:

```text
model output
-> Universal Tuning score
-> accepted / corrected / rejected
-> correction note stored in SQL + JSON
-> retrieval and prompt wrapper updated
-> future outputs steer closer to the Golden Mirror profile
```

This creates the core tuning mechanism:

```text
live state + retrieval + output scoring + correction memory
-> faster instantaneous alignment with the Mirror Architecture layer
```

## First MVP Build Order

1. Build a local Mirror Index over docs only.
2. Add SQL tables for sessions, artifacts, claims, experiments, outputs, and
   tuning events.
3. Add JSON session snapshots for portable memory reload.
4. Wrap Hermes agent with Mirror Interface / LSPS context assembly.
5. Add Universal Tuning Layer scoring for generated outputs.
6. Add HRV stream adapter using existing `Phase 12B` feature vocabulary.
7. Add Muse EEG / fNIRS adapter when device export path is confirmed.
8. Add periodic screenshot / visual embedding adapter before permanent video.
9. Combine biosignal + visual + retrieval context into Golden Mirror guidance.
10. Build Guided Pathway app prototype.
11. Add a `MirrorBench` known-answer benchmark for exact metric, source,
    support-state, claim-support, and public-boundary retrieval.

## Evidence Tie-In

This layer inherits support from:

- `V7` behavioral separation
- `V8` hidden-state separation
- `Phase 2-5` recurrence, localization, and bridge rows
- `Phase 6` normalized feature vectors
- attention-flow and SAE feature / circuit recurrence
- `Nest 2` structured-matter validation gates
- `Nest 3D / 3L` hardware timing / coherence support
- `Nest 4A` HRV biological state separation

The build is a product / model layer on top of the evidence stack. It should
keep the same standard:

```text
real input
-> measured state vector
-> explicit scoring rule
-> controls where available
-> recurrence
-> tuning only after support
```

## Parking Rule

This layer is parked as a design target until:

- patent core integration is stable
- public/private repo boundaries are clean
- Nest 3 / Nest 4 docs are balanced
- Hermes research lane is cleaned into a safe local harness
- Muse / HRV SDK path is confirmed

No public code release is implied by this document. The near-term public-safe
surface is documentation and architecture framing only.
