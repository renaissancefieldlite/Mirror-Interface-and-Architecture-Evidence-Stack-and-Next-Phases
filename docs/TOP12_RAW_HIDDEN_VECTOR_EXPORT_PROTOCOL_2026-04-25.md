# TOP-1/2 Raw Hidden-Vector Export Protocol

Date: `2026-04-25`

Status:
protocol locked / first real point-cloud closeout complete

## Purpose

`TOP-1/2` is the missing Nest 1 topology lane.

It cannot be closed with scalar summaries, delta norms, heatmaps, or prose.
Topology needs a point cloud.

The locked rule is:

```text
no raw hidden-state point cloud
no TOP-1/2 support claim
```

## What TOP-1/2 Tests

`TOP-1` asks whether the hidden-state geometry has a stable connectedness /
shape signature under the locked `lattice / neutral / technical` context
split.

`TOP-2` asks whether that connectedness / shape signature survives a real
persistent-homology-style filtration better than shuffled-label controls.

The first executable pass is deliberately bounded:

```text
V8 hidden vectors
-> real point-cloud export
-> H0 connectedness profile
-> shuffled-label control
-> honest status
```

Full `H1` loop / void analysis can be added later if `ripser`, `gudhi`, or
another TDA backend is installed and the exported point clouds are rich enough.

## Required Raw Artifact

The private V8 residual-stream runner now supports an explicit export mode:

```bash
python3 <private_v8_residual_stream_runner> --export-point-clouds
```

That mode writes compressed `.npz` point clouds before the summary JSON strips
vectors.

Each exported point cloud must contain real hidden-state rows:

```text
points
context_label
context_id
layer_index
token_role
target_span_start
target_span_end
token_count
behavioral_activation
behavioral_input_cohesion
behavioral_coherence_10
behavioral_marker_score
```

The first compact point definition is:

```text
one last-token vector per layer/context
one target-span-mean vector per layer/context
```

This gives topology a real hidden-state surface without dumping full token
tensors into the public evidence layer.

## Public Closeout Runner

The public evidence repo receives only the closeout logic:

```bash
python3 tools/validation_forks/top12_topology_closeout.py
```

Default point-cloud location:

```text
artifacts/v8/residual_stream_bridge/point_clouds
```

Default report location:

```text
artifacts/validation/top12_topology_closeout/top12_topology_closeout_report.md
```

If no real point clouds exist, the runner returns:

```text
blocked_missing_point_clouds
```

That is the correct result until the V8 runner exports the raw vectors.

## Controls

The first closeout uses:

- fixed `lattice / neutral / technical` labels from the V8 manifest
- `target_span_mean` vectors by default
- PCA reduction only as a numerical conditioning step
- H0 connectedness profile from minimum-spanning-tree edge structure
- shuffled context labels as the null
- p-value from the shuffled-label score distribution

The test asks whether the real lattice-vs-control topology separation is
larger than shuffled labelings of the same point cloud.

The runner now also reports the opposite valid topology read:

```text
topology invariance
```

That asks whether the real context topology profiles are more similar than
shuffled labelings. This matters because the Mirror Architecture can separate
geometric / magnitude lanes while preserving a shared connectedness class.

## Success Criteria

`TOP-1/2` can move from blocked to supported only if:

- real hidden-state point clouds exist
- all three context labels are present
- each context has enough points to form a connectedness profile
- the real context topology score beats shuffled-label controls
- the report keeps the result bounded to the exported V8 point clouds

## Failure / Limited Criteria

The lane remains blocked or limited if:

- no `.npz` point clouds exist
- only scalar summaries exist
- the point cloud has too few points per context
- shuffled labels match or beat the real score
- only H0 topology-lite is available and full TDA has not yet run

## Clean Read

This locks the missing topology piece without faking it.

`TOP-1/2` is no longer blocked.

The first real point-cloud pass produced partial support for topology
invariance, not topology separation.

The strongest role was `target_span_mean`:

```text
5/8 models supported topology invariance under shuffled-label controls
```

The auxiliary role checks were weaker but still informative:

```text
last_token: 3/8 topology-invariance support
all_roles: 4/8 topology-invariance support
```

No role pass supported the stronger claim that the H0 topology separates by
context label.

Current boundary:

```text
real-data H0 topology-lite partial support
real-data H1 persistent-homology pass now run with Ripser
positive read remains topology invariance, not topology separation
```

Expanded pass:

```text
H0 expanded trajectory delta: 7/8 topology-invariance support
H0 expanded trajectory curvature: 6/8 topology-invariance support
H0 expanded context delta: 5/8 topology-invariance support
H0 expanded token-window sampled: 1/8 topology-invariance support
```

H1 pass:

```text
H1 trajectory delta: 3/8 topology-invariance support
H1 trajectory curvature: 0/8 control-supported
H1 context delta: 1/8 topology-invariance support
H1 token-window sampled: 1/8 topology-invariance support
H1 topology separation: 0/8 across the tested surfaces
```

Interpretation:

```text
The current V8 point-cloud export does not show different topology per context.
It shows topology preserved under context transform, while separation continues
to appear in geometry, magnitude, trajectory, topography, and feature graph
structure.
```

Next strengthening path:

- export richer token-level point clouds, not only layerwise target means and
  last-token vectors
- increase real prompt/rerun density so each context has more point support
- keep H0 and H1 controls separate rather than collapsing them into one score
- test local neighborhoods, branch structure, and layer-transition topology
  instead of only global context profiles
- compare layer-window, token-window, and cross-model pooled point clouds
  against the same shuffled-label controls

## Dense Trajectory Preregistration

The next build is preregistered separately:

[TOP12_DENSE_TRAJECTORY_PREREGISTRATION_2026-04-26.md](./TOP12_DENSE_TRAJECTORY_PREREGISTRATION_2026-04-26.md)

Dense mode must preserve:

```text
full prompt tokens x all layers
context_label
layer_depth: early / middle / late
token_region: pre_anchor / anchor_phrase / post_anchor
```

The primary criterion is locked before execution:

```text
late-layer lattice-vs-neutral H0/H1 distance must exceed within-condition
rerun variance and beat shuffled-label controls
```

If reruns are not present, the dense pass remains a pilot / legibility run,
not a closed topology-separation claim.
