# Nest 2E PFAS Pathway Validation Report

Status: `completed_real_pfas_pathway_coherence_supported`

## Inputs

- Dataset: EPA PFAS reaction library Excel (`EnvLib` + `MetaLib`)
- Valid parent/product transformation pairs: `184`
- Reaction-type classes: `13`

## Test

True EPA parent -> product pathway rows were compared against shuffled
parent/product pairings using fixed RDKit descriptor deltas.

The validation question was:

```text
are real PFAS transformation pairs more chemically coherent than random
parent/product pairings from the same library?
```

## Result

- true mean pathway coherence: `0.624682`
- shuffled mean pathway coherence: `0.291404`
- shuffled std: `0.010534`
- permutation p: `0.000200`
- permutations: `5000`

## PFAS Boundary Read

- rows with any fluorine or C-F bond reduction: `0.3370`
- rows retaining high fluorination / C-F burden: `0.8424`

The retained-fluorination read is important: a parent disappearing or
transforming is not the same as safe mineralization. The bad-descendant
penalty is the right future lane for PFAS remediation logic.

## Boundary

This validates a real PFAS pathway-coherence comparator against a public
reaction library. It does not claim PFAS destruction, remediation success,
or safe byproduct generation.
