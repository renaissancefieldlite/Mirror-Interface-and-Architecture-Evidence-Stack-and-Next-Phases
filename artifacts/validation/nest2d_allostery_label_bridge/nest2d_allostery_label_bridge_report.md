# Nest 2D Allostery Label Bridge Report

Status: `allostery_label_bridge_ready_mapper_awaiting_contact_pocket_labels`

## What Ran

This pass reads the extracted AlloBench Table S3 benchmark and converts it
into a mapper-readiness bridge. The Mirror mapper scoring pass starts
once the contact / pocket / residue-label handoff is attached.

## Benchmark Surface

- real PDB benchmark rows: `100`
- allosteric-site prediction tool columns: `10`
- best mean Jaccard tool: `PASSer_Ensemble`
- best mean Jaccard: `0.19733`
- mean best-per-protein Jaccard: `0.38549`
- median best-per-protein Jaccard: `0.381`
- rows with any tool >= 0.2 Jaccard: `68`
- rows with any tool >= 0.5 Jaccard: `38`
- rows where all tools are zero / failed: `8`
- mean pairwise tool-score correlation: `0.235671399`

## Why This Matters

Allostery is the first Nest 2 lane where the mapper needs real biological
graph structure alongside molecule descriptors. The extracted table proves
we have a real benchmark family and exposes the baseline difficulty: even
the best existing table-level mean Jaccard is low, so a future path mapper
must be scored carefully against degree, centrality, and shuffled-site
controls.

## Available Now

- PDB IDs for the `100` AlloBench test proteins
- existing tool Jaccard scores against known allosteric sites
- per-row difficulty summaries and best-tool baselines
- a label manifest template for the next contact / pocket graph handoff

## Required Before Mapper Validation

- protein structure file per PDB row
- contact graph or pocket graph per PDB row
- known allosteric-site residue / pocket labels
- known active-site residue labels for communication-path direction
- Mirror mapper candidate path / pocket score on the same graph units
- controls against degree, centrality, shuffled-site labels, and random pockets

## Combined Closeout Design

The next Nest 2D mapper run uses the same `100` PDB rows and compares:

- Mirror mapper candidate path / pocket score
- existing AlloBench tools: `APOP`, `PASSer_Rank`, `PASSer_AutoML`,
  `PASSer_Ensemble`, `Ohm`, `ALLO`, `AllositePro`, `STRESS`,
  `AlloPred`, and `Allosite`
- added pocket tools where available: `fpocket`, `P2Rank`, and `PrankWeb`
- graph-naive controls: degree, centrality, shortest active-site path,
  random pocket, and shuffled allosteric labels

Closeout target:

```text
Mirror mapper > PASSer_Ensemble mean Jaccard baseline
and
Mirror mapper > graph-naive controls
and
repeat holds on a second seed / split or second allostery benchmark
```

## Clean Read

Nest 2D has a real AlloBench benchmark surface and a concrete label manifest. The current local data supports benchmark readiness and baseline characterization; Mirror mapper validation is the next pass once residue/contact/pocket labels are attached.

## Outputs

- row summary: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/nest2d_allostery_label_bridge/nest2d_allobench_proxy_row_summary.csv`
- tool summary: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/nest2d_allostery_label_bridge/nest2d_allobench_proxy_tool_summary.csv`
- label manifest template: `/Users/renaissancefieldlite1.0/Documents/Playground/Mirror-Interface-and-Architecture-Evidence-Stack-and-Next-Phases/artifacts/validation/nest2d_allostery_label_bridge/nest2d_allostery_label_manifest_template.csv`
