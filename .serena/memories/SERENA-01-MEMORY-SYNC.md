<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: 818d3c1
Scope: Serena memory, fullrepo, and knowledge sync policy
Area: SERENA
-->

# SERENA-01-MEMORY-SYNC

## Scope
Serena memory, fullrepo, and knowledge sync policy

## Current source of truth
- `path:plugins/rldyour-serena-mcp`
- `path:.serena/project.yml`
- `path:README.md`


## Source Of Truth
- `path:plugins/rldyour-serena-mcp`
- `path:.serena/project.yml`
- `path:README.md`

## Last verified
- date: 2026-05-29
- commit: `818d3c19388978564b29724488678cd803b99867`
- checked by: Codex system sync after nested legacy profile cleanup

## Facts
- Serena memories record memory format, evidence, freshness, fullrepo, and runtime marker policy.
- `scripts/check_serena_memory_freshness.py` compares the newest `Last commit`
  evidence in `.serena/memories/*.md` with the adapter source branch HEAD and
  fails when high-impact non-knowledge changes are not reflected.
- Root `scripts/validate_adapter_health.py` now delegates the Codex freshness
  check when adapter Serena memories are present, so root local/fullrepo health
  can catch stale adapter knowledge.
- The 2026-05-29 Codex release sync records `818d3c1` as the current memory
  evidence head after refreshing plugin package manifests, `VERSION`, and
  release metadata to `1.0.3`.

## Evidence
- `commit:d7909f83ae7ec947946f374ffae99af37db5335a`
- `path:plugins/rldyour-serena-mcp`
- `path:.serena/project.yml`
- `path:README.md`
- `path:scripts/check_serena_memory_freshness.py`

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
