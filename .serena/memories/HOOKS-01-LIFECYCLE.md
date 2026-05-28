<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: 818d3c19388978564b29724488678cd803b99867 chore(release): codex 1.0.3
Scope: deterministic hook lifecycle behavior
Area: HOOKS
-->

# HOOKS-01-LIFECYCLE

## Scope
deterministic hook lifecycle behavior

## Current source of truth
- `path:plugins/rldyour-flow/hooks`
- `path:scripts/smoke_hooks.sh`
- `path:scripts/smoke_codex_hook_listing.py`


## Source Of Truth
- `path:plugins/rldyour-flow/hooks`
- `path:scripts/smoke_hooks.sh`
- `path:scripts/smoke_codex_hook_listing.py`

## Last verified
- date: 2026-05-29
- commit: `818d3c19388978564b29724488678cd803b99867`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Hook memories record bounded, deterministic lifecycle behavior and the authoritative Stop owner.
- `scripts/smoke_codex_hook_listing.py` validates runtime `hooks/list`
  against installed rldyour plugin hooks and accepts both
  `plugins/cache/rldyour-codex/<plugin>/<version>/hooks.json` and
  `plugins/cache/rldyour-codex/<plugin>/local/hooks.json` source paths.

## Evidence
- `commit:77280a6219d6de48815df6da3e33552d9c6c9283`
- `path:plugins/rldyour-flow/hooks`
- `path:scripts/smoke_hooks.sh`
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
