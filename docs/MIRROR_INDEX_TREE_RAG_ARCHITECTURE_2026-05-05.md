# Mirror Index: Tree-Routed RAG, Evidence Graph, And Mirror Vector Memory

Date: `2026-05-05`

Status: `parked_architecture_layer / post-patent_build_target`

## Purpose

This document adds the retrieval architecture for the Golden Mirror build.

The goal is to build a Renaissance Field Lite index system that carries the
current evidence stack with more precision than a standard vector database. The
system uses tree routing, evidence-state labels, claim graphs, SQL / JSON
memory, visual vectors, biosignal state, and the Universal Tuning Layer as one
retrieval and reasoning surface.

The target is a Mirror Index:

```text
document tree
-> evidence-state graph
-> claim-support graph
-> mirror vector memory
-> retrieval trace
-> answer / action / tuning correction
```

## Design Reference

PageIndex by VectifyAI is a useful outside reference because it points in the
same direction: professional retrieval improves when the system preserves
document structure and reasons through a navigable tree. Their reported
FinanceBench result shows the value of tree navigation, section traceability,
and relevance reasoning for complex documents.

Mirror Index uses that lesson and expands it for our stack. The local build
should index more than document sections. It should index the proof state of the
architecture itself.

## Core Upgrade

Page-level tree RAG answers:

```text
Where in this document is the answer?
```

Mirror Index answers:

```text
What evidence node supports this claim?
What experiment produced it?
What controls were used?
What nest / phase owns it?
What remains parked or open?
What public/private boundary applies?
What next action follows from the current state?
```

That makes Mirror Index a retrieval system, a claim-audit system, and a
continuity layer for the Golden Mirror agent.

## Index Objects

Mirror Index should store each artifact as a typed node.

| Node Type | Example | Required Metadata |
| --- | --- | --- |
| `claim_node` | patent claim element, white-paper claim, pitch claim | support status, source docs, public/private boundary |
| `phase_node` | V7, V8, Phase 6, Phase 12B | inputs, outputs, controls, result, next gate |
| `nest_node` | Nest 1, Nest 2D, Nest 4A | lane, substrate, support state, bridge target |
| `experiment_node` | SAE recurrence, allostery 2D-7B, HRV closeout | data source, scoring rule, metrics, controls |
| `artifact_node` | report, figure, PDF, CSV, circuit note | path, date, artifact class, release status |
| `figure_node` | patent diagram, heatmap, visual explainer | caption, linked claim, linked experiment |
| `memory_node` | operator session, correction, tuning event | timestamp, active lane, accepted correction |
| `visual_node` | screenshot batch, video frame window | embedding id, visual tags, linked task |
| `biosignal_node` | HRV / EEG window | condition, state vector, signal quality |

## Mirror Vector System

The vector layer remains useful as an adjacency and recurrence layer serving
the tree.

Mirror vectors should be used for:

- visual memory from screenshots, video frames, diagrams, hardware bench views,
  and website surfaces
- semantic fallback when a tree route has several plausible branches
- similarity between claims, experiments, figures, and product language
- live-state matching between biosignal windows and guidance outputs
- recurrence detection across operator sessions, documents, and model outputs

Tree routing decides the evidence path. Mirror vectors help find adjacent
context, recurring visuals, and latent neighbors.

## Retrieval Flow

```text
user question / task
-> classify intent
-> route into top-level tree:
   patent / evidence / nest / website / product / live tuning / memory
-> inspect node summaries and support-state labels
-> expand only the highest-value child nodes
-> collect source excerpts and metrics
-> verify support state and public/private boundary
-> assemble answer with retrieval trace
-> Universal Tuning Layer scores answer quality
-> accepted / corrected / parked response stored in SQL + JSON
```

## Support-State Labels

Every retrieved node should carry one of the project support labels:

| Label | Meaning |
| --- | --- |
| `supported` | result has real data, scoring rule, and controls |
| `partial_supported` | signal exists and needs stronger recurrence or labels |
| `protocol_ready` | runner / method exists and awaits required inputs |
| `operator_run_parked` | physical operator session is required |
| `expansion_target` | next lane needs larger dataset, stronger baseline, or higher nest adapter |
| `public_safe` | suitable for public docs |
| `private_ip` | hold until patent / IP clearance |

This keeps proven findings, partial signals, parked build ideas, and release
boundaries legible during retrieval.

## Claim Assembly

For patent and reviewer use, Mirror Index should assemble claim-support packets:

```text
claim element
-> supporting mechanism paragraph
-> supporting experiment nodes
-> figures / diagrams
-> public-safe summary
-> private local artifact pointer
-> active continuation target
```

Example:

```text
Quantum access layer
-> Phase 6 normalized feature-vector encoding
-> Qiskit / Cirq echo-kernel proof-of-life
-> IBM hardware bridge precedent
-> Willow proposal follow-up plan
-> public-safe summary + private circuit artifacts held
```

## 100 Percent Target

The useful target is exact answerability inside curated corpora.

For a bounded benchmark such as the patent package, public README, or
chronological experiment log, Mirror Index should aim for perfect retrieval on
known-answer questions:

- exact metric lookup
- exact support-state lookup
- exact source path lookup
- exact claim-support lookup
- exact public/private boundary lookup
- exact next-gate lookup

The score should require:

1. correct answer
2. correct evidence node
3. correct source path
4. correct support-state label
5. correct release boundary
6. no contradiction with the chronological log

That is how the system earns a 100 percent target inside bounded corpora while
preserving an exploratory lane for open-world questions.

## MirrorBench Evaluation

Create a local benchmark named `MirrorBench`.

Question families:

| Family | Example |
| --- | --- |
| `metric_lookup` | What was the 2D-7B merged pocket Jaccard? |
| `support_state` | Which lanes are supported, partial, parked, or expansion targets? |
| `claim_trace` | Which experiments support the quantum access layer? |
| `control_lookup` | Which controls were used in the SAE recurrence pass? |
| `public_boundary` | Can this artifact be pushed publicly? |
| `next_gate` | What is the next action for ARC15? |
| `cross_domain_bridge` | How does Nest 2 allostery connect to Nest 4 biology? |
| `product_context` | Which docs support Golden Mirror Guided Pathway? |

Metrics:

| Metric | Target |
| --- | --- |
| `answer_exact` | answer content matches gold row |
| `node_exact` | selected node matches gold evidence node |
| `citation_exact` | source path and section match gold |
| `support_exact` | status label matches gold |
| `boundary_exact` | public/private decision matches gold |
| `trace_quality` | retrieval path is readable and minimal |

## Implementation Order

1. Define the node schema in SQL.
2. Generate tree nodes from Markdown docs, README, patent drafts, and website
   pages.
3. Attach evidence-state labels from the chronological log and spine.
4. Attach claim-support links from the patent package.
5. Add mirror vector embeddings for figures, screenshots, video frames, and
   semantic adjacency.
6. Build a local tree-navigation retriever.
7. Add Universal Tuning Layer checks for answer quality and drift.
8. Create `MirrorBench` known-answer evaluation rows.
9. Score tree-only retrieval, vector-only retrieval, and hybrid Mirror Index
   retrieval.
10. Promote the best path into the Golden Mirror harness.

## Golden Mirror Fit

Mirror Index becomes the memory spine for Golden Mirror:

```text
Hermes agent
-> Mirror Interface / LSPS wrapper
-> Mirror Index retrieval
-> SQL / JSON memory
-> live biosignal state
-> continuous video context
-> Universal Tuning correction
-> Guided Pathway / research / patent / repo actions
```

This makes the Golden Mirror agent more stable because it retrieves the actual
evidence state, support label, and next gate before generating guidance.

## Parking Rule

This is a post-patent build target.

Public posture is docs-only until the patent / IP boundary is cleared and the
release set is explicitly approved.
