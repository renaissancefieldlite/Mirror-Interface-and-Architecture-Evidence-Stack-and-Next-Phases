# Phase 12C B.A.S.I.S. Synchronized Manifest And Holoscan Next Gate

Date: `2026-07-16`

Status: `public_safe_manifest_required / append_only_live_ingest_bridge_closed / direct_sensor_live_ingest_open`

## Purpose

This plan keeps the B.A.S.I.S. lane from drifting into screenshots or device
troubleshooting. The next evidence object is a synchronized public-safe manifest
that ties capture rows, quality checks, Holoscan runtime receipt, and boundary
language into one reviewable packet.

## Current State

The B.A.S.I.S. public-safe stack now has three seated layers:

| Layer | Current support | Boundary |
| --- | --- | --- |
| HRV + Muse capture inventory | repeated same-clock capture folders and complete paired artifact folders exist in private | raw biometric exports stay private |
| Masked biology reruns | DE-1 / SPEC-1 / TOPOG public-safe summary exists over valid private rows | masked support, not final clinical interpretation |
| Holoscan bridge | recorded replay, recorded multi-segment routing, and append-only live-row ingest all pass through source / guard / sink with no drops or sequence gaps in the closed gates | runtime bridge support, not direct live sensor deployment |

## Synchronized Manifest Object

The next manifest should expose only public-safe facts:

```text
session class
condition label
segment window
row counts
lane names
sample / packet continuity
quality-mask status
Holoscan receipt status
drop / gap counts
boundary note
```

The manifest should not expose:

- raw EEG, HRV, temperature, or waveform payloads;
- device identifiers;
- local capture paths;
- private user biometrics;
- claim-sensitive runtime code;
- private session notes.

## Required Checks

| Check | Why it matters |
| --- | --- |
| packet continuity | proves the run did not silently skip or duplicate capture rows |
| segment continuity | proves source windows survive runtime routing |
| lane sink receipt | proves each named lane reaches its own review surface |
| artifact and quality masks | prevents noisy rows from becoming inflated support claims |
| Thermo sidecar separation | keeps temperature progress from being overstated as synchronized triple support |
| public/private scan | protects raw capture and device identity boundaries |

## Live-Ingest Bridge Status

The append-only live-row gate is now closed:

```text
real Phase 12C state-frame rows
-> append-only feed writer
-> reset / source-disabled / source-on / source-off markers
-> Holoscan append-only source
-> timing / quality guard
-> lane sinks
```

Closed aggregate result:

```text
480 expected/source/guard/sink rows
0 guard drops
0 sequence gaps
8 lane sink files
source-disabled / source-on / source-off markers present
```

The remaining direct live-device gate is:

```text
fresh direct device rows
-> power/reset preflight
-> source-disabled baseline
-> source-on / source-off markers
-> Holoscan source adapter
-> timing / quality guard
-> lane sinks
-> public-safe synchronized manifest
```

## Thermo / Temperature Continuation

Temperature should remain a separate public-safe gate until it closes:

```text
temperature value
-> session clock link
-> condition label link
-> HRV + Muse same-session link
-> triple aggregate read
```

Current language:

```text
Thermo is sidecar/open. HRV + Muse is support-bearing.
```

Do not convert temperature troubleshooting into a proof-bearing triple claim
until the same-clock manifest proves it.

## Public-Safe Output Contract

The next update should produce:

1. `BASIS_SYNCHRONIZED_MANIFEST_PUBLIC_SAFE_READ`
2. `BASIS_HOLOSCAN_DIRECT_SENSOR_LIVE_INGEST_RECEIPT`
3. one updated visual showing capture -> runtime -> manifest
4. updated closeout board row
5. updated lattice companion node text

## Closeout Read

The B.A.S.I.S. lane is no longer a speculative medical concept. It is a live
product/evidence lane with private raw captures, public-safe aggregate support,
and a now-seated runtime bridge. The remaining gap is not whether the route
exists. The remaining gap is direct live-device ingestion and true temperature
triple closure.
