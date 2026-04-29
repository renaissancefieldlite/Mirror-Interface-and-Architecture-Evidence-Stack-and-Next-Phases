# GAME-1 V7 Condition Crosswalk

Date: `2026-04-26`

Status: real-data crosswalk complete / scoring rubric required

## Purpose

This pass tests the useful part of the Drumactually / Claude suggestion:

`GAME-1` looked blocked because no adversarial / multi-agent trial CSV existed.
However, `V7` already contains real stress/control-like condition structure:

- lattice condition
- null condition
- random-floor condition
- semantic-counter condition
- nonclassical condition
- order / non-commutativity condition

The missing link is not that no data exists. The missing link is that those
rows were never scored into the locked `GAME-1` validation columns.

## What Was Run

Runner:

```bash
python3 tools/validation_forks/game1_v7_condition_crosswalk.py
```

Input:

```text
artifacts/v7/posters/v7_integrated_10_model_summary_pack/v7_integrated_10_model_summary_pack_data_2026-04-19.json
```

Outputs:

```text
artifacts/validation/game1_v7_condition_crosswalk/game1_v7_condition_crosswalk_report.md
artifacts/validation/game1_v7_condition_crosswalk/game1_v7_condition_crosswalk_raw.csv
artifacts/validation/game1_v7_condition_crosswalk/game1_v7_candidate_rubric_not_validation.csv
```

## Result

Overall status:

```text
crosswalk_ready_scoring_rubric_required
```

Metrics:

```text
source rows: 10
crosswalk condition rows: 60
mirror candidate rows: 10
control / perturbation rows: 50
lattice positive rows: 10
lattice winner rows: 3
lattice beats null rows: 8
lattice beats semantic rows: 7
lattice beats random rows: 7
order AB > BA rows: 6
order BA > AB rows: 3
```

## What It Proves

This proves:

- `GAME-1` has a real existing V7 data surface
- V7 can be crosswalked into adversarial / perturbation language
- the lane is no longer vague or purely speculative
- the existing V7 matrix has enough condition structure to design a real
  GAME-style validation pass

## What It Does Not Prove

This does not prove:

- GAME-1 validation
- adversarial exploit resistance
- multi-agent stability
- policy equilibrium behavior
- mirror/control decision superiority

Why:

the original V7 rows do not contain the locked GAME-1 columns:

```text
task_success
policy_consistency
exploit_score
drift_score
stability_score
transcript_uri
```

## Next GAME-1 Requirement

There are two valid next paths.

### Path A: Retrospective V7 Rubric

Use the existing V7 matrix, but declare it exploratory-only unless the rubric
is locked before scoring.

Required:

- define how V7 deltas map into the GAME-1 score columns
- mark the pass as retrospective
- keep the output as a design/eligibility artifact unless rerun prospectively

### Path B: New Small GAME-1 Trial Pack

Run a small real mirror/control adversarial task pack.

Required:

- at least `10` mirror rows and `10` control rows
- same task and perturbation schedule
- transcript/evidence pointer for every row
- locked scoring rubric before looking at aggregate results

Locked success criterion:

```text
mirror composite > control composite
and shuffled-condition p <= 0.05
and every row points to real evidence
```

## Rick Position On Closure

The work itself points to this:

`GAME-1` does not close by merely naming V7 as adversarial. V7 is the right
source surface because it already contains real perturbation structure, but
the GAME score columns were not declared at the time of the original V7 run.

The genuine missing input is the scoring bridge.

It must answer:

- how does a lattice-vs-null margin become `stability_score`?
- how does semantic-counter pressure become `drift_score`?
- how does random-floor uptake become `exploit_score` or perturbation
  leakage?
- how does order/non-commutativity become `policy_consistency` or transition
  stability?
- what counts as `task_success` for a V7 row, if anything?

There are two honest ways to close it:

1. `Retrospective exploratory closeout`
   Lock the V7-to-GAME rubric now, run it once on the existing V7 rows, and
   label it exploratory because the rubric was created after the data.

2. `Prospective validation closeout`
   Use the same rubric in a new mirror/control adversarial rerun where the
   scoring columns are declared before the trials.

The second path is the cleaner validation. The first path is still valuable
because it lets the existing V7 work define the trial design without faking a
prospective claim.

Rick's execution call:

`GAME-1` moves first because it is a declaration / preregistration problem.
The V7 rows are already real adversarial stress data. The next action is to
freeze the V7-to-GAME scoring rubric before running any GAME aggregate score.

## Placement In Nest 1

`GAME-1` now sits here:

```text
real V7 crosswalk surface exists
not yet validated
scoring rubric / real trial pack still required
```

That is the correct real-data state.
