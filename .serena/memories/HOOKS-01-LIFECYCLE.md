<!-- Memory Metadata
Last updated: 2026-05-31
Last verified: 2026-05-31
Last commit: 1252b518c85b3d3ea359109062c6d804696ef7f7 chore(release): codex 1.1.14 (other)
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
- date: 2026-05-31
- commit: `1252b518c85b3d3ea359109062c6d804696ef7f7`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Hook memories record bounded, deterministic lifecycle behavior and the authoritative Stop owner.
- The adapter contract distinguishes hook feature availability from plugin
  hook trust. Current keys are `hooks_feature_default_enabled`,
  `plugin_bundled_hooks_discoverable`, `plugin_hook_trust_required`, and
  `trusted_hook_hashes_refreshed_by_installer`; enabled plugins do not imply
  trusted hook execution until the installer refreshes trusted hook hashes.
- `scripts/smoke_codex_hook_listing.py` validates runtime `hooks/list`
  against installed rldyour plugin hooks and accepts both
  `plugins/cache/rldyour-codex/<plugin>/<version>/hooks.json` and
  `plugins/cache/rldyour-codex/<plugin>/local/hooks.json` source paths.

## Evidence
- `commit:1252b518c85b3d3ea359109062c6d804696ef7f7`
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

## Applies to
- The scope declared in this memory and the source-of-truth paths listed below.

## Invariants
- Code, configuration, tests, and git state override this memory when they disagree.

## Current State
- See `Facts` for current durable facts. Do not treat `Historical evidence` or old commit notes as current state.

## Do Not Infer
- Do not infer runtime versions, product versions, commits, permissions, release state, or tool behavior from this memory without checking the source of truth.

## Update Triggers
- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, or durable agent workflow contracts.

## Validation Commands
- `python3 scripts/validate_serena_memory_schema.py --scope all --strict-mode strict-all`
- `python3 scripts/validate_serena_memory_semantics.py --scope all --strict-current-facts`
- `python3 scripts/validate_memory_freshness.py --scope all`

## Repair Procedure
- Re-read source-of-truth files, update only verified current facts, move stale facts to historical evidence, then rerun the validation commands.
