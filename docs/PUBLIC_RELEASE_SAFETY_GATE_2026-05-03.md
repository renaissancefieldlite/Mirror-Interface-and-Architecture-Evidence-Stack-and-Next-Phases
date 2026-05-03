# Public Release Safety Gate

This repository is the public-facing evidence narrative. It must not be used as
the working bench for runnable code, raw experiment outputs, generated data
dumps, model states, local machine paths, or private operational material.

## Default Rule

- Public pushes are documentation-only unless explicitly approved otherwise.
- Raw `artifacts/` stay local or private.
- Runnable `tools/` stay local or private.
- Model states and dense exports stay local or private.
- Public docs summarize the method, evidence status, controls, and findings.

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
