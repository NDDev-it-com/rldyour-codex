<!-- Memory Metadata
Last updated: 2026-05-28
Last commit: d7909f83ae7ec947946f374ffae99af37db5335a fix(installer): drop nested legacy profile tables
Scope: CLI runtime and package baselines
Area: RUNTIME
-->

# Runtime Baselines

## Scope
CLI runtime and package baselines

## Current source of truth
- `path:references/codex-baseline.json`


## Source Of Truth
- `path:references/codex-baseline.json`

## Last verified
- date: 2026-05-28
- commit: `d7909f83ae7ec947946f374ffae99af37db5335a`
- checked by: Codex system sync after nested legacy profile cleanup

## Facts
- Runtime memories record pinned CLI/package baselines and freshness checks.

## Evidence
- `commit:d7909f83ae7ec947946f374ffae99af37db5335a`
- `path:references/codex-baseline.json`

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
