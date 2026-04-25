# Draft Grammar-To-Real-Data Validation Ladder

Date: `2026-04-25`

Status:
local draft / not public-locked / do not publish until approved

Companion draft:
[Draft Nest 1 / Nest 2 Foundation Real Mapping Plan](./DRAFT_NEST1_NEST2_FOUNDATION_REAL_MAPPING_PLAN_2026-04-25.md)

## Purpose

This note separates the value of grammar mapping from the stronger burden of
real-data validation.

The corrected read is:

```text
grammar mapping is useful as schema discovery
real data decides whether a lane graduates
```

The grammar is not proof by itself, but it is not worthless. Its value is that
it defines what to measure, what to compare against, what should remain stable,
what drift looks like, and what would falsify a stronger claim.

## What Grammar Mapping Is Good For

Grammar mapping can legitimately do five things:

1. define the shared comparator fields:
   `state / control / transform / invariant / drift / coherence / score`
2. translate the same question across domains without pretending the domains
   are identical
3. identify what real dataset or trace each lane needs before it can be tested
4. prevent cherry-picking by declaring the score and failure mode before the
   data pass
5. turn broad intuition into falsifiable runners

That is a real methodological contribution.

It is not the same thing as empirical validation.

## What Grammar Mapping Is Not

Grammar mapping does not by itself establish:

- chemistry validation
- biology validation
- clinical effect
- environmental remediation
- physical Bell claims
- universal convergence
- that every mapped lane is equally strong

If a lane does not touch real traces, real measurements, real hardware, real
datasets, or declared benchmarks, it remains a design lane.

## Current Evidence Tiers

### Tier 1: strongest current surfaces

These already have real artifacts or hardware-facing data:

- `V7` behavioral target/control separation
- `V8` hidden-state separation
- `Phase 2` rerun stability
- `Phase 4` localization and localization reruns
- `Phase 5` context-to-readout bridge
- `Phase 6/7` PennyLane/Qiskit encoded circuit-state bridge
- `Phase 9/9B/9C/9D` IBM / PennyLane real-hardware bridge
- `Phase 10` semantic contextuality on compressed feature states

### Tier 2: real but coarse adapter

`Phase 12B HRV` belongs here.

It is real measured data and supports pattern-class separation, but it is a
coarse signal. It is currently strongest as:

- biological adapter lane
- condition-class comparator
- recovery / arousal / autonomic trend signal
- future `AI <-> user` sync/tuning side channel

It is not yet strong enough by itself to validate high-resolution biological
`SPEC-1`, `DE-1`, or `TOPOG` claims.

### Tier 3: grammar mapped, needs real data

`Nest 2` currently belongs here until the real datasets are plugged in.

The structured-matter grammar has value as a methodology map, but the next
step must use real chemistry/material data:

- `RDKit` plus `QM9`, `ZINC`, or `ChEMBL`
- PFAS / contaminant degradation-pathway data
- materials/minerals via `pymatgen`, `ASE`, and Materials Project-style data
- measured spectra or curated public spectral datasets where available

### Tier 4: scaffold only

These are useful for explanation, adapter design, or smoke tests, but not as
claim evidence:

- toy rows
- synthetic examples
- visual-only demos
- card/ontology displays
- local UI companion maps without real data behind them

## Foundation-First Next Sequence

The next work should start at the foundation, not the outer biological layer.

### Step 1: Nest 1 real-trace passes

Use actual V8/V7 artifacts already present in the repo.

Candidate runners:

- `GEO-1/2`: PCA/SVD/neighborhood separability over V8 residual and
  localization traces
- `TOP-1/2`: persistent-shape or component-stability analysis if the hidden
  traces contain enough vector detail
- `DYN-1/2`: trajectory/order-effect analysis over V7/V8 rerun and
  localization sequences
- `STAT/PROB/INFO/TENSOR`: consolidate effect sizes, rerun stability,
  information geometry, and tensor-axis separation from completed phase packs
- `NUM/GRP`: consolidate PennyLane/Qiskit/IBM numerical and symmetry behavior

This tests the formal layer against the actual AI/hardware evidence base.

### Step 2: Nest 2 real-dataset passes

Do not rely on toy chemistry rows.

Candidate runners:

- molecule property validation with `RDKit` and public molecule datasets
- molecular graph/pathway validation against known labels
- PFAS descendant-risk scoring against curated degradation-pathway data
- materials stability recovery with `pymatgen` / `ASE`
- spectral-signature comparison against public spectra where practical

This tests whether the structured-matter grammar predicts or recovers real
properties above simple baselines.

### Step 3: Return to HRV / EEG later

Park biology until the next data surface is available.

When ready:

- keep `HRV` as the autonomic / recovery / user-sync channel
- add `EEG` for alpha/theta spectra, oscillatory dynamics, and spatial
  topography
- run synchronized `EEG + HRV` instead of asking HRV alone to carry all formal
  lenses

## Decision Rule

Every lane should be labeled as one of:

```text
validated on existing data
real-data fork ready
blocked by missing data/tool/device
schema/scaffold only
```

The grammar map earns its keep by making that classification possible.

## Working Read

The grammar mapping is valuable if it becomes a disciplined routing map from
intuition into real tests.

It becomes weak if it is treated as proof before the real data pass.

The next serious build therefore starts with foundation data:

```text
Nest 1 traces -> Nest 2 real datasets -> return to HRV/EEG when ready
```
