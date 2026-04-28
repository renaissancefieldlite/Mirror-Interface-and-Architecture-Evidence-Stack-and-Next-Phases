# V8 Attention / MLP Nest 1 Bridge Protocol

Date: `2026-04-28`

Status: `protocol_locked_missing_exports`

Companion gate:

- [V8 Attention / MLP Nest 1 Bridge Gate Report](../artifacts/validation/v8_attention_mlp_bridge_gate/v8_attention_mlp_bridge_gate_report.md)

## Purpose

The V8 stack already measures hidden-state / residual-stream separation.

That is not the same thing as measuring attention heads or feed-forward / MLP
blocks.

The clean transformer-internal split is:

- hidden states / residual stream: where the representation lands
- multi-head attention: how token-to-token routing and context flow are formed
- feed-forward / MLP blocks: how the representation is transformed after routing

This protocol locks those missing internals as a Nest 1 validation bridge.

## Why This Belongs In Nest 1

Nest 1 is the smallest formal system layer and the real mathematical substrate
of machine learning.

Attention and MLP blocks are not extra metaphor. They are actual transformer
objects:

| Transformer object | Nest 1 lane |
| --- | --- |
| attention matrices / top-k attention edges | `GRAPH-2`, `INFO-1`, `SPEC-1`, `DYN-1` |
| head entropy / head specialization | `SPEC-1`, `INFO-1`, `STAT` |
| layer-by-layer attention-flow changes | `DYN-1`, `CTRL-1` |
| MLP block deltas | `TENSOR`, `GEO`, `DYN-2`, `OPT-1` |

So yes: these should be run against Nest 1.

## What We Have Now

Current evidence:

- V8 hidden-state / residual-stream geometry
- V8 point-cloud exports
- TOP-1/2 dense topology pilots
- GRAPH-2B raw token/layer pathway graph

Current missing exports:

- per-layer / per-head attention matrices
- top-k token-to-token attention-flow edges
- head entropy and anchor-flow summaries
- MLP/feed-forward block intermediate activations or block-delta summaries

## GRAPH-2 Connection

`GRAPH-2B` did not close because raw token/layer geometry alone did not beat
degree / hub controls.

Attention-flow is the next internal pathway graph because it gives measured
edges instead of inferred geometry edges:

```text
token i -> attention head h -> token j
```

That is the transformer-native graph lane.

## Locked Controls

Before validation, controls must be declared:

- shuffled context labels
- shuffled token windows
- shuffled layer order
- shuffled head labels
- degree / centrality baseline
- leave-one-model or leave-one-family check when enough exports exist

## First Run Scope

Do not start with every model.

First attention/MLP export should use the strongest bridge rows:

- `GLM`
- `Hermes`

Prompt classes:

- lattice / mirror prompt
- neutral control
- technical control

Layer labels:

- early
- middle
- late

Token labels:

- anchor phrase
- pre-anchor
- post-anchor
- bridge term
- padding / ordinary token

## Acceptance Rule

Attention-flow becomes Nest 1 evidence only if:

```text
mirror/lattice attention-flow graph > degree / centrality baseline
and
mirror/lattice attention-flow graph > shuffled-label controls
```

MLP/feed-forward becomes Nest 1 evidence only if:

```text
mirror/control block-delta signatures separate above shuffled controls
```

If attention or MLP remains invariant, that is still useful. It means the
Mirror effect is living more strongly in hidden-state geometry, trajectory,
topography, and structured outputs than in that specific internal block.

## Boundary

This protocol does not claim attention-head validation has already happened.

It locks the next real internal test.
