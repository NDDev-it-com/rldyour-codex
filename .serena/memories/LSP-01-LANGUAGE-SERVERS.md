<!-- Memory Metadata
Last updated: 2026-05-28
Last commit: 2a852698661384a3ba4497c4ea2c98111d941965 fix: sync plugin cache versions with adapter release
Scope: language-server setup and diagnostic proof
Area: LSP
-->

# Language Server Quality Gates

## Scope
language-server setup and diagnostic proof

## Current source of truth
- `path:plugins/rldyour-lsps`
- `path:README.md`


## Source Of Truth
- `path:plugins/rldyour-lsps`
- `path:README.md`

## Last verified
- date: 2026-05-28
- commit: `2a852698661384a3ba4497c4ea2c98111d941965`
- checked by: Codex ry-start memory-domain normalization

## Facts
- LSP memories record language-server coverage and diagnostic proof requirements.

## Evidence
- `commit:86b2555935f4c2185658417a3aff82d225d25392`
- `path:plugins/rldyour-lsps`
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
