# Public Release Safety Gate

This repository is the public-facing evidence narrative. It must not be used as
the working bench for runnable code, raw experiment outputs, generated data
dumps, model states, local machine paths, or private operational material.

## Default Rule

- Public pushes are documentation-only unless explicitly approved otherwise.
- Patent-hold rule: until the patent / IP package is submitted and public-code
  clearance is given, this repo stays docs-only by default.
- Raw `artifacts/` stay local or private.
- Runnable `tools/` stay local or private.
- Model states and dense exports stay local or private.
- Public docs summarize the method, evidence status, controls, and findings.

## Private Parking Rule

The private workbench is preserved locally for later patent-cleared release.
Removing code and artifacts from the public Git index must not delete the local
research bench. Parked material can remain in ignored folders such as
`artifacts/` and `tools/`, or in a private archive / private repo, until it is
explicitly cleared.

## Required Check Before Push

Before any public push, verify the pending diff and run the private release
scanner:

```bash
git diff --name-status origin/main..HEAD
git diff --cached --name-status
```

The push is blocked if any public diff contains code, raw artifacts, generated
outputs, local absolute paths, model states, or credential-looking strings.

## Clean Public Shape

The public repo should contain:

- `README.md`
- public-safe `docs/`
- approved public visuals / PDFs only when explicitly cleared
- no runnable experiment code
- no raw output folders
- no model checkpoint or SAE state files
- no local absolute file paths
