# V8 Attention / MLP Nest 1 Bridge Gate

Status: `exporter_ready_missing_full_export`

## Clean Read

The current V8 evidence stack contains hidden-state / residual-stream
geometry, but it does not yet contain exported attention-head or
feed-forward / MLP block artifacts.

That distinction matters:

- hidden states show where the representation lands
- attention heads show token-to-token routing / flow
- MLP blocks show representation update between routing steps

So yes: attention heads and MLP/feed-forward blocks should be run against
Nest 1. They are the missing internal mechanics for the transformer-native
version of the formal lanes.

## Artifact State

- residual stream bridge exists: `True`
- dense point-cloud files detected: `0`
- attention artifact files detected: `0`
- MLP artifact files detected: `0`
- exporter script exists: `True`
- exporter inventory status: `check_only_ready`
- exported attention CSV files detected: `0`
- exported MLP CSV files detected: `0`

## Nest 1 Placement

| Internal block | Nest 1 role |
| --- | --- |
| Multi-head attention | `GRAPH-2` measured routing edges, `INFO-1` token flow, `SPEC-1` head spectrum, `DYN-1` layer trajectory |
| Feed-forward / MLP | tensor / geometry feature update, dynamical regime update, optimization intervention target |

## Locked Missing Inputs

- full per-layer / per-head attention matrices or top-k attention-flow edge export
- full MLP/feed-forward intermediate activation or block-level delta export
- shuffled context, token-window, layer-order, and head-label controls
- GRAPH-2C / MLP validation after real CSV exports exist

## Acceptance Rule

- attention-flow validates only if mirror / lattice routing beats degree, centrality, and shuffled-label controls
- MLP validates only if block-update signatures separate mirror/control rows above shuffled controls
- if either lane stays invariant or negative, we record that rather than forcing the claim

## Next Execution Order

1. export attention top-k edges for two strongest V8 rows first: GLM and Hermes
2. export matching MLP block delta summaries for the same prompts/layers
3. run GRAPH-2C attention-flow validation against the locked graph controls
4. run MLP update separation against shuffled context/token/layer controls
5. only then promote attention/MLP from missing-link protocol to Nest 1 evidence
