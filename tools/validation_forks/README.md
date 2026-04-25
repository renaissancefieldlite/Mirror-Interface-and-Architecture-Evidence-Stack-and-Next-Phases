# Validation Forks

These scripts are the concrete bridge from nest grammar into falsifiable tests.

## Current Runnable Forks

```bash
python3 tools/validation_forks/nest1_spec_phase12b_hrv.py
python3 tools/validation_forks/graph12_pathway_validation.py
python3 tools/validation_forks/ctrl1_lsps_transition_validation.py
python3 tools/validation_forks/engine02v_rdkit_molecule_validation.py
python3 tools/validation_forks/nest1_fortress_card_registry.py
```

This runs `SPEC-1 -> Phase 12B HRV` against existing HRV session exports and
writes:

```text
artifacts/validation/nest1_spec_phase12b_hrv/
```

Current result:

```text
HR-only baseline: 0.45
time-domain HRV: 0.45
SPEC-1 spectral: 0.10
mirror composite: 0.25
```

Read: the HRV-only spectral fork did not beat the simpler baselines.

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

## Fortress Cards

```bash
python3 tools/validation_forks/nest1_fortress_card_registry.py
```

This writes:

```text
artifacts/validation/nest1_fortress_cards/
```

The card registry separates evidence-connected lanes from partial, blocked,
seed, and grammar-only lanes.

## Next Forks

- `TOP-1/2`: persistent-homology runner for V8 hidden-state geometry
- `GEO-1/2`: PCA/UMAP region-separation runner over residual-stream trace
  exports
- `OPT-1`: mirror-guided optimization trajectory benchmark against naive /
  random baselines
