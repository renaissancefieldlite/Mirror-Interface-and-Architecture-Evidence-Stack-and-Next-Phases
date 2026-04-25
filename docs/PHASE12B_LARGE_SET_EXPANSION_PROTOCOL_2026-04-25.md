# Phase 12B Large-Set Expansion Protocol

Date: `2026-04-25`

Status:
local protocol / next biological data expansion plan

## Purpose

The completed `Phase 12B` `5 x 4` HRV matrix is now control-supported as a
coarse biological adapter lane.

The current control-closeout found:

- `mirror_coherence` had the strongest average `HR` downshift
- the `dancing_activation - mirror_coherence` `Delta HR` gap beat shuffled
  labels
- `HR-only` leave-one-run-out classification beat shuffled labels
- multi-feature `HRV` classification was supportive but softer, especially
  under within-run block shuffle

That means the next biological upgrade is not to add claims. It is to expand
the data surface.

## Why Multi-Feature Was Softer

The current matrix has:

```text
5 runs x 4 conditions = 20 sessions
```

That is enough for the cleanest low-dimensional signal:

```text
Delta HR
```

It is not enough to fully stabilize a richer feature set:

```text
Delta HR
Delta RMSSD
Delta SDNN
post-condition recovery features
```

The multi-feature read is softer because:

- `RMSSD` and `SDNN` are naturally noisier over short windows
- `6` features over only `20` sessions creates a high feature-to-sample ratio
- within-run block shuffle is stricter because it controls order / day /
  fatigue / sequence effects
- the current fixed four-condition layout is good for discipline, but larger
  data should rotate order so condition identity does not collapse into
  sequence position

## Large-Set Target

Minimum upgrade:

```text
20 blocks x 4 conditions = 80 sessions
20 sessions per condition
```

Preferred upgrade:

```text
30 blocks x 4 conditions = 120 sessions
30 sessions per condition
```

High-confidence expansion:

```text
50 blocks x 4 conditions = 200 sessions
50 sessions per condition
```

## Condition Set

Keep the same four canonical conditions:

```text
seated_calm
drift_control
mirror_coherence
dancing_activation
```

Do not add more conditions until the `20 x 4` expansion is complete.

## Timing Options

Fast-continuity option:

```text
60s baseline / 120s condition / 60s post
```

This preserves direct comparability to the existing `5 x 4` matrix.

Stronger HRV option:

```text
180s baseline / 300s condition / 180s post
```

This gives `RMSSD`, `SDNN`, and spectral / nonlinear features more room to
stabilize, but it takes much longer.

Recommended path:

```text
finish 20 x 4 using the existing timing first
then run a smaller long-window confirmation set
```

## Order Control

The original run order was useful for execution:

```text
seated_calm -> drift_control -> mirror_coherence -> dancing_activation
```

For the large set, rotate order with a four-condition Latin-square pattern:

```text
block 01: seated_calm -> drift_control -> mirror_coherence -> dancing_activation
block 02: drift_control -> mirror_coherence -> dancing_activation -> seated_calm
block 03: mirror_coherence -> dancing_activation -> seated_calm -> drift_control
block 04: dancing_activation -> seated_calm -> drift_control -> mirror_coherence
```

Then repeat that `4`-block cycle.

This preserves the same condition vocabulary while preventing condition from
being identical to sequence position.

## Additional Fields To Capture

Keep the existing fields:

- `mean HR`
- `RMSSD`
- `SDNN`
- `condition - baseline`
- `post - condition`

Add if available from the strap/session export:

- raw `RR` intervals
- median `RR`
- `pNN50`
- Poincare `SD1 / SD2`
- sample entropy or approximate entropy
- artifact / drop count
- movement flag
- strap-quality flag
- subjective effort `0-10`
- music / no-music flag
- caffeine / food / sleep notes when relevant

The most important upgrade is raw `RR` intervals. Raw `RR` allows richer
features later without rerunning the session.

## Scoring Upgrade

The next control-closeout should score:

1. `Delta HR` only
2. time-domain HRV features
3. recovery features
4. raw-RR derived features
5. combined feature set with feature-selection locked before scoring

Controls:

- balanced label shuffle
- within-run block shuffle
- leave-one-block-out validation
- leave-one-day-out validation if the sessions span multiple days
- condition-order control using the Latin-square sequence

Success criteria:

```text
multi-feature accuracy beats HR-only or adds stable class separation
under within-run and leave-block controls
```

If multi-feature does not beat `HR-only`, the honest read remains:

```text
HRV is a useful coarse adapter, and Delta HR is the dominant signal.
```

That is still a valid result.

## Clean Next Step

Run:

```text
Phase 12B-L20
20 blocks x 4 conditions
80 total sessions
same condition set
Latin-square order
same timing as original matrix
raw RR export whenever available
```

Then rerun:

```text
tools/validation_forks/phase12b_biological_control_closeout.py
```

against the expanded data pack.

## Boundary

This protocol strengthens the biological adapter lane.

It does not turn `HRV` into `EEG`, clinical biology, or high-resolution
spectral / spatial physiology.

The later biological upgrade is still:

```text
simultaneous EEG + HRV
```

The large HRV set makes the existing adapter stronger before that hardware
layer is added.
