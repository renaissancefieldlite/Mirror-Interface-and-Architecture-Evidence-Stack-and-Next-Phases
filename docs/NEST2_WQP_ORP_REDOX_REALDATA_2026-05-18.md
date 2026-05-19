# Nest 2 / Nest 3 WQP ORP Redox-Potential Real-Data Row

Status: `public_safe_support_read / local_ready_unpushed`

## Front-Center Read

The dissolved oxidant chemistry gate is now seated through real Water Quality
Portal / NWIS oxidation-reduction potential records.

The clean dissolved-oxidant move is ORP: raw or unspecified field redox
potential readings recover SHE-referenced ORP state under site holdout and
shuffled-target controls. Species-level peroxide / dissolved oxidant rows stay
queued for the next source-rich chemistry pass.

Current support level: measured redox-potential transform support. This row
strengthens oxygen / redox, electrochemistry, water-quality chemistry,
environmental fate, and Nest 3 physical measurement dynamics. Peroxide
concentration, dissolved oxidant species, and richer co-measured chemistry
remain continuation gates.

## Sources

- Water Quality Portal result service: <https://www.waterqualitydata.us/data/Result/search>
- Water Quality Portal SRS parameter list: <https://www.waterqualitydata.us/Codes/public_srsnames/?mimeType=csv>
- ORP parameter codes:
  - `00090`: oxidation reduction potential, reference electrode not specified
  - `63001`: oxidation reduction potential, raw EMF
  - `63002`: oxidation reduction potential, relative to the standard hydrogen electrode (SHE)

## Target QA

- source rows: `4,916`
- source activities: `4,102`
- source sites: `877`
- support rows with SHE target and raw/unspecified ORP source: `814`
- support sites: `328`
- date range: `2015-01-21` to `2024-02-27`
- high SHE ORP threshold: `>= 300 mV`
- high SHE ORP rows: `420`
- shuffled controls per read: `250`

## Source Code Counts

| Parameter | Meaning | Rows |
| --- | --- | ---: |
| `00090` | ORP, reference electrode not specified | `2,657` |
| `63001` | ORP, raw EMF | `494` |
| `63002` | ORP relative to SHE | `1,765` |

## Support Media

| Medium | Support rows |
| --- | ---: |
| Groundwater | `774` |
| Surface Water | `28` |
| Effluent | `12` |

## State Map

| Variable | ORP / dissolved oxidant expression |
| --- | --- |
| `state` | SHE-referenced ORP in mV and high-SHE ORP class |
| `control` | shuffled SHE ORP targets and shuffled high-ORP labels under fixed site holdout |
| `transform` | raw / unspecified ORP field readings -> SHE-referenced redox state |
| `drift` | site, medium, sampling date, depth, hydrologic event, and reference-electrode movement |
| `quality` | official WQP / NWIS rows, mV unit gate, physical ORP sanity gate, site-heldout split |
| `support` | redox-transform recovery above metadata-only and shuffled-target controls |

## Regression Results

| Mode | Features | Train | Test | Pearson | R2 | RMSE | Baseline RMSE | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `metadata_site_holdout` | `8` | `625` | `189` | `0.510220` | `0.234411` | `168.439399` | `196.138671` | `0.007968` |
| `redox_transform_site_holdout` | `16` | `625` | `189` | `0.995849` | `0.991323` | `17.931916` | `196.138671` | `0.003984` |

## High SHE ORP Classification Results

| Mode | Features | Train | Test | ROC AUC | AP | Balanced Acc | Macro F1 | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `metadata_site_holdout` | `8` | `625` | `189` | `0.610341` | `0.766394` | `0.607344` | `0.564663` | `0.139442` |
| `redox_transform_site_holdout` | `16` | `625` | `189` | `0.998237` | `0.998920` | `0.980200` | `0.977895` | `0.003984` |

## Read

The clean read is that real ORP measurement context recovers SHE-referenced
redox state very strongly under site holdout:

```text
metadata-only site-heldout:
  SHE ORP Pearson       0.510220
  high-SHE ORP AUC      0.610341

raw/unspecified ORP transform:
  SHE ORP Pearson       0.995849
  high-SHE ORP AUC      0.998237
  p                     0.003984
```

This seats a dissolved oxidant chemistry row as a real measurement-transform
surface. It is a different support surface than dissolved oxygen concentration:
dissolved oxygen seats oxygen-state water quality, while ORP seats redox
potential and reference-standard transform behavior.

## Cross-Nest Seating

| Nest / figure | Support role |
| --- | --- |
| `Nest 2` | oxygen/redox and electrochemistry gain real ORP / redox-potential measurement-transform support |
| `Nest 3` | physical measurement dynamics gain raw/reference-standard redox-potential transform support |
| `Nest 4` | biology-facing oxygen/redox interpretation gains a cleaner water-chemistry precursor before physiology rows |
| `Nest 5` | convergence routing can separate dissolved oxygen, ORP/redox potential, grid-flow, ozone, and precursor / meteorology rows |
| `FIG.14` | external adapter lane gains WQP/NWIS water-quality result-service examples |
| `FIG.15` | support-state routing can separate oxygen concentration, redox potential, atmospheric oxidants, and peroxide continuation gates |

## Next Gate

```text
WQP ORP / redox-potential seated
-> richer co-measured water chemistry join
-> peroxide / dissolved oxidant species if a stronger public source appears
-> smoke / PM2.5 / wildfire proxy if we stay atmospheric
```
