# MirrorBench Retrieval Evaluation Spec

Date: `2026-05-05`

Status: `benchmark_design_locked / implementation_after_patent_core`

## Purpose

`MirrorBench` is the retrieval benchmark for Golden Mirror and Mirror Index.

The benchmark measures whether the system can retrieve exact evidence from the
curated Renaissance Field Lite corpus:

```text
question
-> Mirror Index tree route
-> evidence node
-> source path
-> support-state label
-> public/private boundary
-> answer
-> retrieval trace
```

The target is exact answerability inside curated corpora. This is the practical
route toward a `100%` internal retrieval target for known-answer questions.

## Core Corpus

Initial corpus:

| Corpus | Source |
| --- | --- |
| `evidence_readme` | public-safe README |
| `chronological_log` | chronological experiment log |
| `spine` | Rick continuity spine |
| `patent_core` | non-provisional claim spine, support table, integration maps |
| `nest_docs` | Nest 1 through Nest 4 docs |
| `transformer_docs` | attention, MLP, SAE, topology, graph docs |
| `quantum_docs` | Phase 6-9D and Willow follow-up docs |
| `golden_mirror_docs` | Golden Mirror, Mirror Index, Guided Pathway docs |
| `website_docs` | public companion and architecture pages |

## Question Families

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
| `patent_mapping` | Which claims cover external adapter subsystems? |
| `device_plan` | What is the Muse EEG + HRV capture protocol? |

## Gold Row Schema

Each benchmark row should carry:

```text
question_id
question
expected_answer
expected_node_id
expected_source_path
expected_section
expected_support_state
expected_public_boundary
expected_next_gate
allowed_aliases
contradiction_checks
```

## Scoring

| Metric | Target |
| --- | --- |
| `answer_exact` | answer content matches the gold row |
| `node_exact` | selected evidence node matches the gold row |
| `source_exact` | source path matches the gold row |
| `section_exact` | source section matches the gold row |
| `support_exact` | support-state label matches the gold row |
| `boundary_exact` | public/private boundary matches the gold row |
| `next_gate_exact` | next action matches the gold row |
| `trace_quality` | retrieval path is short, readable, and faithful |
| `contradiction_free` | answer agrees with chronological log and support table |

Pass condition for curated rows:

```text
answer_exact
+ node_exact
+ source_exact
+ support_exact
+ boundary_exact
+ contradiction_free
```

## Retrieval Modes To Compare

Run three retrieval modes:

| Mode | Description |
| --- | --- |
| `tree_only` | Mirror Index tree routing through typed nodes |
| `vector_only` | semantic / visual vector retrieval |
| `hybrid_mirror_index` | tree route with vector adjacency and Universal Tuning check |

Expected direction:

```text
hybrid_mirror_index >= tree_only >= vector_only
```

The useful proof is a retrieval system that finds the correct evidence state,
not just similar text.

## Initial Gold Questions

Seed the first set with `100` rows:

| Bucket | Rows |
| --- | --- |
| Nest 1 / transformer internal evidence | `15` |
| Nest 2 structured matter and allostery | `20` |
| Nest 3 resonance / hardware / ARC15 | `10` |
| Nest 4 HRV / EEG + HRV plan | `10` |
| quantum access / Phase 6-9D / Willow | `10` |
| patent claim support | `15` |
| public/private release boundary | `10` |
| Golden Mirror / Mirror Index / app layer | `10` |

## First Build Order

1. Build gold rows from the chronological log and claim-support table.
2. Assign node ids to the main README, spine, patent, and nest docs.
3. Implement tree route selection in the local harness.
4. Add vector adjacency after tree retrieval is stable.
5. Add Universal Tuning Layer checks for support status, public boundary, and
   contradiction.
6. Score tree-only, vector-only, and hybrid retrieval.
7. Promote the best route into Golden Mirror.

## Parking Rule

`MirrorBench` is a post-patent implementation target. This spec can remain
public-safe as an architecture/evaluation document. Runnable code, private
source corpora, raw artifacts, and hidden vectors stay local until patent/IP
clearance.
