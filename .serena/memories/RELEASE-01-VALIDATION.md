<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: c89b5380f272ac9553b254573383c71aa1e33e33 fix: align dart mcp smoke with dart 3.12
Scope: release readiness, versioning, and artifact hygiene
Area: RELEASE
-->

# RELEASE-01-VALIDATION

## Scope
release readiness, versioning, and artifact hygiene

## Current source of truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`


## Source Of Truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`

## Last verified
- date: 2026-05-22
- commit: `c89b5380f272ac9553b254573383c71aa1e33e33`
- checked by: Codex ry-start Dart 3.12 runtime sync

## Facts
- Release memories record numeric versioning, tags, CI gates, and clean artifact hygiene.
- Commit `c89b5380f272ac9553b254573383c71aa1e33e33` updates unreleased Codex
  runtime metadata for Dart SDK `3.12.0` and keeps the product version at
  `0.4.9`.

## Evidence
- `commit:c89b5380f272ac9553b254573383c71aa1e33e33`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:config/mcp-runtime-versions.env`
- `path:.github/workflows/release.yml`

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
