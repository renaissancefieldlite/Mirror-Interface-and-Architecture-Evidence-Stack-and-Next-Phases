# Nest 2E PFAS Safety Logic Report

- `status`: `pfas_bad_descendant_safety_logic_supported`
- `rows`: `184`
- `permutations`: `5000`

## Result

| Metric | Value |
| --- | ---: |
| Mean coherent bad-descendant score | 0.595067 |
| Shuffled coherent bad-descendant score | 0.554863 |
| Coherent bad-descendant p-value | 0.000200 |
| Bad-descendant flag fraction | 0.733696 |
| Shuffled bad-descendant flag fraction | 0.532891 |
| Bad-descendant flag p-value | 0.000200 |
| Mean retained-burden score | 0.888164 |
| High retained-burden fraction | 0.842391 |
| Mean mineralization-quality proxy | 0.114919 |
| Low mineralization-quality fraction | 0.842391 |
| Rows with any F or C-F reduction | 0.336957 |
| Safety-candidate fraction | 0.038043 |

## Clean Read

Nest 2E safety logic is supported: true PFAS pathways are coherent and preferentially produce coherent descendants that retain fluorination / C-F burden. The lane identifies bad descendants and separates transformation from safety.

## Interpretation

This is a safety triage layer. Parent disappearance is treated as insufficient safety evidence. The scorer checks whether the product remains a coherent, highly fluorinated descendant and therefore should stay flagged for downstream remediation or degradation scoring.

## Artifacts

- row scores: `artifacts/validation/nest2e_pfas_safety_logic/nest2e_pfas_safety_logic_rows.csv`
- by reaction type: `artifacts/validation/nest2e_pfas_safety_logic/nest2e_pfas_safety_logic_by_reaction_type.csv`
- top bad descendants: `artifacts/validation/nest2e_pfas_safety_logic/nest2e_pfas_safety_logic_top_bad_descendants.csv`
- summary JSON: `artifacts/validation/nest2e_pfas_safety_logic/nest2e_pfas_safety_logic_summary.json`
