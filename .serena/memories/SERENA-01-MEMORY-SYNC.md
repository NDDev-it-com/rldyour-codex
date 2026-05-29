<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: ea419bc0900cc934ca1b9434e8ff8f4e0304328b chore(release): codex 1.1.0
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
- commit: `ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
- checked by: Codex ry-start automated release and metadata sync

## Facts
- Serena memories record memory format, evidence, freshness, fullrepo, and runtime marker policy.
- `scripts/check_serena_memory_freshness.py` compares the newest `Last commit`
  evidence in `.serena/memories/*.md` with the adapter source branch HEAD and
  fails when high-impact non-knowledge changes are not reflected.
- Root `scripts/validate_adapter_health.py` now delegates the Codex freshness
  check when adapter Serena memories are present, so root local/fullrepo health
  can catch stale adapter knowledge.
- The 2026-05-28 Codex release-hardening sync records `b92c6a3` as the current
  memory evidence head after Semgrep/shadcn MCP pin updates, product version
  `1.0.0`, and stale research-claim validation changes.
- The 2026-05-28 internal adapter release sync records `2a85269` as the current
  memory evidence head after the `1.0.2` product bump and plugin manifest
  version parity hardening.

## Evidence
- `commit:ea419bc0900cc934ca1b9434e8ff8f4e0304328b`
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
