# TOP-1/2 Dense Trajectory Preregistration

Date: `2026-04-26`

Status:
protocol locked before dense run

## Purpose

The first `TOP-1/2` point-cloud passes found topology preservation /
invariance, not context-topology separation.

That result is useful, but the current point clouds are still compressed:
target-span means, last-token vectors, target-window tokens, target-mean
layer deltas, curvature, and context deltas.

The dense trajectory pass tests the missing link:

```text
Does context-specific topology appear when the point cloud preserves
per-token, per-layer hidden-state trajectories instead of compressed
context summaries?
```

## Locked Scope

Start small:

```text
models: GLM and Hermes
contexts: lattice, neutral, technical
export: full prompt tokens x all layers
mode: dense_trajectory
```

Reason:

`GLM` and `Hermes` are strong discriminator rows from the existing bridge
work. Two models are enough to test whether dense topology has a signal before
spending compute on the full model matrix.

## Required Labels

Every point must carry:

```text
context_label: lattice / neutral / technical
layer_index: exact layer number
layer_depth: early / middle / late
token_index: exact prompt-token position
token_region: pre_anchor / anchor_phrase / post_anchor / no_anchor / padding
token_role: dense_prompt_token
feature_family: dense_trajectory
```

The run is not interpretable without these labels.

## Preregistered Read

Primary topology-separation claim:

```text
Late-layer lattice-vs-neutral persistence diagrams differ more than the
within-condition rerun variance, under shuffled-label controls.
```

Operational criterion:

```text
between_condition_distance(lattice, neutral, late, anchor_or_near_anchor)
>
within_condition_rerun_distance(lattice, late, anchor_or_near_anchor)
and
>
within_condition_rerun_distance(neutral, late, anchor_or_near_anchor)
```

The result must also beat the shuffled-label null:

```text
separation_p_value <= 0.05
```

If reruns are not present, the dense pass is a pilot / legibility run only.
It cannot close the topology-separation claim.

## Secondary Reads

Secondary but predeclared:

- `late` layer depth is expected to be stronger than `early`
- `anchor_phrase` and near-anchor tokens are expected to be stronger than
  far `pre_anchor` / far `post_anchor`
- `lattice` vs `neutral` is the primary contrast
- `lattice` vs `technical` and `technical` vs `neutral` are secondary
  contrasts
- H0 connectedness and H1 persistence must be reported separately

## Controls

Required controls:

- shuffled context labels
- layer-order shuffle
- token-window shuffle
- leave-one-rerun-out where reruns exist
- leave-one-model-out only after more than two models are added

## Boundary

A dense pilot can show whether the topology surface becomes richer.

It does not prove context-topology separation unless the preregistered
between-condition-vs-within-rerun criterion is satisfied.

If H0/H1 still show invariance, the clean read remains:

```text
Mirror context transform preserves topology while moving geometry,
magnitude, trajectory, topography, and graph structure.
```

