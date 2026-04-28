# CAT-1 Composition / Transfer Benchmark

Date: 2026-04-27

## Purpose

`CAT-1` asks whether the same relation structure survives when moved through a
composition chain.

For the current stack, the cleanest real chain is:

`Phase 6 PennyLane encoded state relation -> Phase 7 Qiskit statevector mirror -> Phase 9D hardware subset`

## Benchmark A: PennyLane -> Qiskit

Inputs:

- `artifacts/v8/phase6_pennylane_encoding/v8_phase6_pennylane_encoding_data_2026-04-22.json`
- `artifacts/v8/phase7_qiskit_mirror/v8_phase7_qiskit_mirror_data_2026-04-22.json`

Metrics:

- matrix max absolute delta
- matrix mean absolute delta
- top-pair preservation
- top-3 pair preservation

Closure:

supported if both angle and amplitude relation matrices preserve to numerical
precision and preserve top-pair structure.

## Benchmark B: Qiskit / Encoding -> Hardware Subset

Input:

`artifacts/validation/opt1_perspective_nest_benchmark/opt1_perspective_nest_benchmark_report.json`

Metric:

whether the best Phase 6 feature pair agrees with the best Phase 9D hardware
parity-similarity pair over the executed feature-circuit subset.

Boundary:

only three hardware feature circuits exist in this subset, so this is hardware
partial, not a full composition closeout across all model pairs.

## Status Rule

If PennyLane -> Qiskit is numerically preserved and the hardware subset agrees
only at small-N, `CAT-1` is marked:

`completed_implementation_composition_supported_hardware_partial`

That means composition is real and measured at the implementation layer, while
the hardware-subset transfer still needs a larger executed sample.
