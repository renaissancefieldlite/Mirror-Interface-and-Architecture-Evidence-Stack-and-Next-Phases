# Phase 12C B.A.S.I.S. Capture Hub Visual Map

Date: `2026-05-09`

Status: `public evidence visual map / docs-first release / patent-gated code release`

## Capture-To-Readout Map

```mermaid
flowchart LR
    A["Muse S Athena"] --> B["Native capture adapter"]
    B --> C["Stream-ready gate"]
    C --> D["Raw local packet archive"]
    D --> E["Athena decoder"]
    E --> F["Normalized engineering lanes"]
    F --> G["Phase 12C window table"]
    G --> H["B.A.S.I.S. state-vector layer"]
    H --> I["Mirror Architecture readout"]
    H --> J["Golden Mirror live tuning adapter"]
```

## What The Adapter Separates

```mermaid
flowchart TB
    A["Captured device stream"] --> B["Preserve raw evidence locally"]
    A --> C["Decode public evidence lane summaries"]
    C --> D["EEG engineering lane"]
    C --> E["Optical / PPG / fNIRS-candidate lane"]
    C --> F["Motion artifact lane"]
    C --> G["Contact / reference quality lane"]
    C --> H["Device-status audit lane"]
    D --> I["Windowed feature table"]
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J["Controls and recurrence"]
    J --> K["Public evidence finding"]
```

## Phase 12C Window Discipline

```mermaid
gantt
    title Phase 12C Window Timing
    dateFormat  X
    axisFormat %s
    section Session
    Baseline :0, 60
    Condition :60, 120
    Post :180, 60
```

Every sample is interpreted through this window map:

```text
sample timestamp
-> session manifest
-> baseline / condition / post label
-> condition class
-> lane-specific feature table
-> control-aware readout
```

## Five-Run Capture Pack

```mermaid
flowchart LR
    A["Five full Phase 12C captures"] --> B["3 mirror_coherence runs"]
    A --> C["1 seated_calm control"]
    A --> D["1 drift_control"]
    B --> E["Preliminary mirror average"]
    C --> F["Control average"]
    D --> F
    E --> G["Mirror minus control deltas"]
    F --> G
    G --> H["Motion/contact filtering next"]
```

## What We Found

The five-run pack shows:

- stable capture density across all runs,
- decoded engineering lanes across every baseline / condition / post session,
- preliminary mirror-vs-control differences in optical, quality, and selected
  EEG channels,
- motion/contact lanes available for filtering and replication.

The public evidence interpretation is:

```text
Phase 12C has moved from protocol design into real windowed Muse S Athena
capture. The B.A.S.I.S. Capture Hub pathway works as an adapter pattern, and
the first five-run pack provides preliminary signal structure for controlled
follow-up.
```

## Capture Hub Pattern

```mermaid
flowchart TB
    A["Device-specific adapter"] --> B["Raw packet/event preservation"]
    B --> C["Decoder / normalizer"]
    C --> D["Lane table"]
    D --> E["Shared session manifest"]
    E --> F["Windowed experiment record"]
    F --> G["B.A.S.I.S. state-vector bus"]
    G --> H["Mirror Architecture / AI interface"]

    I["HRV"] --> A
    J["EEG / optical"] --> A
    K["ECG"] --> A
    L["PPG / SpO2"] --> A
    M["GSR / EDA"] --> A
    N["CSV / API / OSC / LSL"] --> A
```

The release discipline:

`evidence and public logging first, raw code and raw biosignal data private
through patent completion, selected public code later after review.`
