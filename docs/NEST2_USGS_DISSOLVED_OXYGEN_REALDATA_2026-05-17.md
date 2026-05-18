# Nest 2 / Nest 3 USGS Dissolved Oxygen Real-Data Row

Status: `public_safe_support_read / local_not_yet_pushed`

## Front-Center Read

The oxygen / redox and H2O / water branches now have a seated dissolved
oxygen real-data row.

This pass uses USGS instantaneous water-quality sensor data and tests whether
same-site same-timestamp water temperature, pH, conductance, time, and site
geometry recover dissolved oxygen state and low-oxygen class above shuffled
controls.

The row matters because it connects the earlier spectral H2O / minerals branch
to a live environmental water-quality state. Oxygen is now read as a measured
water/redox state, not only as a molecule-level redox or battery chemistry row.

## Source

- Source: USGS NWIS instantaneous values
- API: <https://waterservices.usgs.gov/nwis/iv/>
- Query: Colorado, 14-day window, parameter codes `00300`, `00010`, `00400`, `00095`
- `00300`: dissolved oxygen, water, unfiltered, mg/L
- `00010`: water temperature, deg C
- `00400`: pH
- `00095`: specific conductance

## Target QA

- time series: `493`
- raw long rows: `402,436`
- raw DO rows: `45,164`
- clean complete rows: `41,001`
- clean complete sites: `27`
- DO range: `4.000` to `13.200` mg/L
- DO mean / median: `8.424` / `8.300` mg/L
- low-oxygen threshold: `< 7.0` mg/L
- low-oxygen rows: `2,238`
- shuffled controls per read: `250`

Invalid sensor sentinels and impossible physical values are removed before
modeling.

## State Map

| Variable | Dissolved oxygen expression |
| --- | --- |
| `state` | dissolved oxygen mg/L and low-oxygen class |
| `control` | shuffled DO labels under fixed split / mode |
| `transform` | water temperature, pH, conductance, time, site geometry -> DO state |
| `drift` | diurnal timing, site context, chemistry shifts, low-oxygen movement |
| `quality` | same-site same-timestamp rows, invalid sentinel removal, physical value gates |
| `support` | site-heldout and same-site temporal recovery above shuffled controls |

## Regression Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `temp_time_site_holdout` | `9` | `28,958` | `12,043` | `0.699746` | `0.381138` | `0.696006` | `0.890767` | `0.003984` |
| `chemistry_site_holdout` | `13` | `28,959` | `12,042` | `0.841119` | `0.637957` | `0.564704` | `0.951590` | `0.003984` |
| `chemistry_temporal` | `14` | `28,688` | `12,313` | `0.943309` | `0.883940` | `0.319419` | `1.065993` | `0.003984` |

## Low-Oxygen Classification Results

| Mode | Features | Train | Test | ROC AUC | AP | Balanced Acc | Macro F1 | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `temp_time_site_holdout` | `9` | `31,906` | `9,095` | `0.888594` | `0.115491` | `0.499719` | `0.494554` | `0.003984` |
| `chemistry_site_holdout` | `13` | `26,304` | `14,697` | `0.924256` | `0.489007` | `0.500000` | `0.480065` | `0.003984` |
| `chemistry_temporal` | `14` | `28,688` | `12,313` | `0.971628` | `0.830200` | `0.855529` | `0.843680` | `0.003984` |

## Read

USGS dissolved oxygen seats a water-quality oxygen/redox state with three
useful support surfaces:

- temperature + time alone recover DO with Pearson `0.699746`
- chemistry + site-heldout mode strengthens the read to Pearson `0.841119`
  and low-oxygen ROC AUC `0.924256`
- same-site temporal chemistry mode gives the strongest state-tracking read:
  Pearson `0.943309`, R2 `0.883940`, low-oxygen ROC AUC `0.971628`, balanced
  accuracy `0.855529`

The clean public claim is that dissolved oxygen now carries a real
water/redox support surface with explicit shuffled-label controls. ROS,
ozone/peroxide, and grid-flow rows remain continuation gates for higher
reactivity and flow-system transport.

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | oxygen/redox, H2O/water, electrochemistry, and environmental-fate rows gain real water-quality DO support |
| `Nest 3` | physical sensor / water-state dynamics row gains temporal and site-heldout support |
| `Nest 4` | oxygen-state language now has a water-quality precursor before biology/metabolism rows |
| `Nest 5` | convergence matrix can route H2O, oxygen/redox, conductance, pH, and environmental state as one support family |
| `FIG.14` | external adapter lane includes water-quality sensor examples |
| `FIG.15` | support-state routing can separate site-heldout generalization, temporal tracking, and ROS/grid-flow continuation gates |

## Next Gate

```text
USGS dissolved oxygen seated
-> ROS / ozone / peroxide real-data row
-> grid-flow / water-transport real-data row
-> optional broader multi-state WQP expansion
```
