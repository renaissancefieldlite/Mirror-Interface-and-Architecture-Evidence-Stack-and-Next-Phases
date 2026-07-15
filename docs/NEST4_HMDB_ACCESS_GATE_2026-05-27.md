# HMDB Access Gate

Date: `2026-05-27`

Status: `access_gate / official_downloads_page_verified / no_bulk_download_run`

## Source

Official page:

```text
https://www.hmdb.ca/downloads
```

The HMDB downloads page lists HMDB as a public resource and states that use and
redistribution for commercial purposes requires explicit permission of the
authors and source acknowledgment.

The current page exposes HMDB Version `5.0` download rows including:

- metabolite structures in SDF format;
- all metabolites in XML format;
- tissue/fluid subsets including urine, serum, CSF, saliva, feces, and sweat;
- spectra packets, including raw peaklists and XML spectra.

The page also exposes a download information form requesting:

```text
Email / Affiliation / Organization / Industry-Commercial-Academic-Other
```

## Local Probe

A local `curl` probe to the downloads page returned a Cloudflare challenge HTML
instead of the rendered downloads table:

```text
private-local probe artifact: experiments/nest4_glytoucan_glycan_confirmation/data/raw/hmdb_downloads_page_probe.html
```

Browser verification was used for the page read. No HMDB bulk file was
downloaded and no HMDB-derived support run was executed.

## Gate Read

HMDB remains an access/permission gate, not a failed experiment.

Current state:

```text
official source available -> commercial/industry permission language present -> form path required -> no local bulk download -> no HMDB support score
```

Public-safe wording:

```text
HMDB was verified as the next metabolomics source gate, but the current
official page requires explicit commercial/industry permission handling before a
bulk HMDB-derived run is treated as cleared. The Nest 4 HMDB lane remains open.
```

## Boundary

This document does not claim HMDB support, metabolomics closeout, tissue-fluid
validation, or clinical metabolism support.

## Next Gate

Proceed with:

```text
HRV + Muse + Thermo paired physiology manifest
```

HMDB can be resumed after the permission/download path is cleared.
