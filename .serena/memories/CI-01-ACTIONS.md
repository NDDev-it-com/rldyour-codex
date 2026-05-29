<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: 39099a5e191e97f30f70512da4a6d752de9d4b5d chore(release): codex 1.1.2
Scope: GitHub Actions and local CI policy
Area: CI
-->

# CI Actions

## Scope
GitHub Actions and local CI policy

## Current source of truth
- `path:.github/workflows`
- `path:README.md`


## Source Of Truth
- `path:.github/workflows`
- `path:README.md`

## Last verified
- date: 2026-05-29
- commit: `39099a5e191e97f30f70512da4a6d752de9d4b5d`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- CI memories record which checks prove repository integrity and which checks are intentionally lightweight.
- GitHub Actions workflows pin third-party actions to full commit SHAs. Dependabot
  monitors `github-actions` monthly and groups all action version updates into a
  single PR through `.github/dependabot.yml`.

## Evidence
- `commit:39099a5e191e97f30f70512da4a6d752de9d4b5d`
- `path:.github/workflows`
- `path:.github/dependabot.yml`
- `path:README.md`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Cross-References
- `CORE-01-INDEX.md`
- `CONTEXT-01-CORE.md`
- `PATTERNS-01-CANONICAL.md`
