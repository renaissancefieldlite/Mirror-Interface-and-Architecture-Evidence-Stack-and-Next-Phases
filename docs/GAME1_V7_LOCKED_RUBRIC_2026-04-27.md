# GAME-1 V7 Locked Rubric

Date: 2026-04-27

## Purpose

`GAME-1` tests whether the Mirror / lattice condition behaves like a more
stable decision policy under control and perturbation pressure.

The existing `V7` rows are not a new adversarial or multi-agent trial pack, but
they are real stress/control data: each model has measured `lattice`, `null`,
`nonclassical`, `random_floor`, `semantic_counter`, and order-pressure fields.

This rubric locks a retrospective V7 scoring pass. It is allowed to support
`GAME-1` as an existing-data lane, but it does not replace a future prospective
adversarial / multi-agent trial.

## Source

`artifacts/v7/posters/v7_integrated_10_model_summary_pack/v7_integrated_10_model_summary_pack_data_2026-04-19.json`

## Candidate Conditions

- `lattice`
- `null`
- `nonclassical`
- `random_floor`
- `semantic_counter`

The declared Mirror condition is `lattice`.

## Locked Score Columns

For each model and candidate condition:

- `task_success`: `1` if the candidate condition has positive activation delta,
  otherwise `0`.
- `policy_consistency`: fraction of the other four candidate conditions that the
  candidate condition beats.
- `exploit_score`: fraction of the other four candidate conditions that beat the
  candidate condition.
- `drift_score`: fraction of semantic / random / nonclassical drift controls
  that beat the candidate condition, excluding the candidate itself if needed.
- `stability_score`: `1 - normalized_abs_order_pressure`, where order pressure
  is `abs(order_ab_minus_ba)` normalized by the maximum absolute order pressure
  in the V7 matrix.

Composite:

`task_success + policy_consistency + stability_score - exploit_score - drift_score`

## Control

The control is a shuffled-condition null:

- keep the real model rows and real condition deltas
- randomly assign one of the five candidate conditions as the candidate policy
  for each model
- recompute the same locked composite
- compare the declared `lattice` composite against the shuffled null

## Closure Rule

`GAME-1 / V7 rubric support` requires:

- declared `lattice` mean composite above shuffled-label mean
- shuffled-label p-value `<= 0.05`

If this does not hold, `GAME-1` remains open and must move to prospective real
adversarial / multi-agent trials.

## Boundary

This is a retrospective V7 validation fork. It can show that existing V7
stress/control rows support the `GAME-1` decision-stability score schema, but it is
not a prospective adversarial benchmark and does not validate biology,
chemistry, physical systems, or multi-agent deployment behavior.
