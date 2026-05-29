<!-- Memory Metadata
Last updated: 2026-05-28
Last commit: d35c3c9
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
- date: 2026-05-28
- commit: `d7909f83ae7ec947946f374ffae99af37db5335a`
- checked by: Codex system sync after nested legacy profile cleanup

## Facts
- Hook memories record bounded, deterministic lifecycle behavior and the authoritative Stop owner.
- `scripts/smoke_codex_hook_listing.py` validates runtime `hooks/list`
  against installed rldyour plugin hooks and accepts both
  `plugins/cache/rldyour-codex/<plugin>/<version>/hooks.json` and
  `plugins/cache/rldyour-codex/<plugin>/local/hooks.json` source paths.

## Evidence
- `commit:d7909f83ae7ec947946f374ffae99af37db5335a`
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
