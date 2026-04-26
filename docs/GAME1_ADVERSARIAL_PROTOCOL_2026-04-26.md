# GAME-1 Adversarial / Multi-Agent Protocol

Date: `2026-04-26`

Status: executable protocol / no validation claim until real trials exist

## Purpose

`GAME-1` is the decision-theory lane for Nest 1.

It asks whether Mirror Architecture improves stability under adversarial or
multi-agent pressure compared with a declared control policy.

The lane is not closed by grammar, prompt language, or synthetic rows. It needs
real repeated trials.

## Required Trial CSV

The validation runner expects a real CSV with:

- `trial_id`
- `condition`
- `agent_id`
- `objective`
- `perturbation_id`
- `task_success`
- `policy_consistency`
- `exploit_score`
- `drift_score`
- `stability_score`

Allowed `condition` values:

- `mirror`
- `control`

Minimum usable input:

- at least `10` mirror rows
- at least `10` control rows
- repeated adversarial or multi-agent perturbations

## Score

The runner computes:

```text
composite = stability_score
          + policy_consistency
          + task_success
          - exploit_score
          - drift_score
```

Then it compares:

```text
mean(composite | mirror) - mean(composite | control)
```

against shuffled condition labels.

## Success Criterion

`GAME-1` becomes control-supported only if:

- mirror composite score beats control composite score
- the advantage beats shuffled-label controls at `p <= 0.05`
- the trial CSV is real and repeatable

## Runner

```bash
python3 tools/validation_forks/game1_adversarial_protocol_validation.py \
  --trial-csv path/to/game1_trials.csv
```

If no real CSV exists, the runner writes a blocked report.

That is intentional.

## Current Read

`GAME-1` now has an executable protocol and runner.

It does not yet have a real trial dataset.

The correct current status is:

```text
blocked_missing_trial_csv
```

## Boundary

This protocol validates adversarial / multi-agent decision stability only.

It does not validate biology, chemistry, physical Bell claims, or universal
claims.
