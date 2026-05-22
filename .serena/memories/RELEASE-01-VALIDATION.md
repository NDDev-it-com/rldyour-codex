<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 77280a6219d6de48815df6da3e33552d9c6c9283 fix: accept local hook cache paths
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
- `path:scripts/smoke_codex_hook_listing.py`


## Source Of Truth
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:.github/workflows/release.yml`
- `path:scripts/smoke_codex_hook_listing.py`

## Last verified
- date: 2026-05-22
- commit: `77280a6219d6de48815df6da3e33552d9c6c9283`
- checked by: Codex ry-start macOS system config verification

## Facts
- Release memories record numeric versioning, tags, CI gates, and clean artifact hygiene.
- Commit `77280a6219d6de48815df6da3e33552d9c6c9283` keeps product version
  `0.4.9` and updates unreleased validation behavior so
  `scripts/smoke_codex_hook_listing.py` accepts both versioned and `local`
  installed plugin cache `hooks.json` source paths.

## Evidence
- `commit:77280a6219d6de48815df6da3e33552d9c6c9283`
- `path:VERSION`
- `path:CHANGELOG.md`
- `path:config/mcp-runtime-versions.env`
- `path:.github/workflows/release.yml`
- `path:scripts/smoke_codex_hook_listing.py`

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
