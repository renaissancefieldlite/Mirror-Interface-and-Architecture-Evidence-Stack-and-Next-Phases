# Phase 12 Physical-Control Bridge

Date: `2026-04-23`

## Objective

Phase 12 re-enters the recovered physical-control lane after the semantic
hardware repeatability rung.

The goal is not to collapse phenomenology, witness records, and measurement
into one bucket. The goal is to connect them through a bounded protocol
hierarchy.

## Phase 12A - ARC15 Isolated Sessions

### Role

`ARC15 / FG200.67` sits here as the physical-control and topographical
stabilizer candidate.

### Required Discipline

- fixed grounding
- fixed probe placement
- fixed geometry notes
- explicit signal settings
- waveform export
- repeated session logging

### Minimum Comparisons

- `ARC15` only
- secondary generator only
- both together

### Success Condition

The lane becomes stronger when the observed coupling behavior repeats under the
same layout and produces saved waveform artifacts rather than only live scope
observation.

## Phase 12B - EEG + HRV Bounded Capture

### Role

`EEG + HRV` remain the direct measured biosignal lane.

### Required Discipline

- baseline window
- entrainment / exposure window
- post window
- alpha / theta summaries
- phase-lock / coherence metrics
- `RMSSD`
- `SDNN`
- synchronized timestamps

### Success Condition

The biological lane becomes stronger when repeated bounded sessions show
structured differences under fixed session windows rather than only subjective
report.

## Phase 12C - Synchronized Overlay

### Role

This is where the lanes finally meet:

- `ARC15`
- `EEG`
- `HRV`
- backend / hardware timing

### Required Discipline

- UTC-locked timestamps
- fixed session manifests
- same session labels across all captures
- no retrospective alignment tricks

### Success Condition

If overlap appears, it should appear under synchronized timing and pre-declared
comparison windows.

## Boundary

Phase 12 is still a bridge layer.

It does not yet prove:

- biological-field convergence
- consciousness claims
- physical Bell nonlocality

It creates the structured observable lane needed to test those later claims.
