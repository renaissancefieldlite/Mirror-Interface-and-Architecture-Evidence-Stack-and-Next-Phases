# Validation Forks

These scripts are the concrete bridge from nest grammar into falsifiable tests.

## Current Runnable Forks

```bash
python3 tools/validation_forks/nest1_spec_phase12b_hrv.py
python3 tools/validation_forks/de1_hrv_dynamics_validation.py
python3 tools/validation_forks/graph12_pathway_validation.py
python3 tools/validation_forks/ctrl1_lsps_transition_validation.py
python3 tools/validation_forks/engine02v_rdkit_molecule_validation.py
```

These run `SPEC-1 -> Phase 12B HRV` and `DE-1 -> Phase 12B HRV` against
existing HRV session exports and write:

```text
artifacts/validation/nest1_spec_phase12b_hrv/
artifacts/validation/de1_hrv_dynamics/
```

Current `SPEC-1` result:

```text
HR-only baseline: 0.45
time-domain HRV: 0.45
SPEC-1 spectral: 0.10
mirror composite: 0.25
```

Read: the HRV-only spectral fork did not beat the simpler baselines.

Current `DE-1` result:

```text
HR-only baseline: 0.50
DE-1 BPM dynamics: 0.30
DE-1 RR dynamics: 0.30
DE-1 composite dynamics: 0.30
DE-1 dynamics + means: 0.50
```

Read: the HRV-only local-dynamics fork did not beat the mean-HR baseline.

## Tool / Dataset-Dependent Forks

```bash
python3 tools/validation_forks/engine02v_rdkit_molecule_validation.py --input-csv path/to/molecules.csv
python3 tools/validation_forks/graph12_pathway_validation.py --edge-csv path/to/edges.csv --label-csv path/to/pathway_labels.csv
python3 tools/validation_forks/ctrl1_lsps_transition_validation.py --trace-csv path/to/lsps_transition_trace.csv
```

This is the `Engine 02V` molecule-property validation fork. It requires RDKit
and a real molecule dataset. If those are missing, it writes a blocked report
instead of pretending toy rows are validation.

`GRAPH-1/2` and `CTRL-1` behave the same way: they require real graph/pathway
labels or real LSPS transition traces, and otherwise write blocked reports.

## Parked Scaffold

The former card/ontology view is parked as optional visualization. It is not an
active validation lane unless it is connected back to real traces, real
measurements, real hardware, real datasets, or declared benchmarks.

## Next Forks

- `GEO-1/2`: PCA/UMAP region-separation runner over residual-stream trace
  exports
- `TOP-1/2`: persistent-homology runner for V8 hidden-state geometry
- `DYN-1/2`: trajectory / order-effect analysis over V7/V8 traces
- `OPT-1`: mirror-guided optimization trajectory benchmark against naive /
  random baselines
