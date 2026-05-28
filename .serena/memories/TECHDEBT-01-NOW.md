<!-- Memory Metadata
Last updated: 2026-05-28
Last commit: b92c6a3290020771e57a9e415f8b131be573a770 chore(release): harden Codex 1.0.0 runtime pins
Scope: verified current technical debt
Area: TECHDEBT
-->

# TECHDEBT-01-NOW

## Scope
verified current technical debt

## Current source of truth
- `path:README.md`
- `path:CHANGELOG.md`


## Source Of Truth
- `path:README.md`
- `path:CHANGELOG.md`

## Last verified
- date: 2026-05-28
- commit: `b92c6a3290020771e57a9e415f8b131be573a770`
- checked by: Codex ry-start release hardening

## Facts
- The audited Codex `plugin_hooks` active-doc drift is closed by the
  `.claude/CLAUDE.md` fullrepo update and by tracked active-doc forbidden-claim
  validation in `scripts/validate_instruction_docs.py`.
- The audited Chrome DevTools MCP freshness drift is closed for Codex at
  `chrome-devtools-mcp@1.1.1` and `check_mcp_runtime_versions.py` reports it
  current.
- The public-CI instruction-doc requirement mismatch is closed: `validate_fast.sh`
  now runs strict `--require-agent-docs` only when agent-only instruction docs
  are restored locally/fullrepo, while public source checkouts validate tracked
  active docs without requiring ignored files.
- The audited runtime-smoke classification debt is closed for Codex:
  `scripts/validate_runtime.sh` now exposes explicit `auto`, `static`,
  `installed`, and `live` lanes. Static mode is deterministic and verifies
  generated TOML/config invariants without a Codex binary; installed/live modes
  make binary/network requirements explicit.
- Version synchronization debt is closed for this adapter at `1.0.0`; root
  control-plane pins must reference commit
  `b92c6a3290020771e57a9e415f8b131be573a770`.
- Semgrep MCP freshness drift is closed for Codex at `semgrep==1.164.0`, and
  shadcn MCP freshness is closed at `shadcn@4.8.2`.
- CI classifier drift is closed for retried MCP TaskGroup startup noise; the
  classifier still fails on unknown non-empty lines in strict mode.
- Remaining debt should be recorded here only when current code/config evidence
  proves it is still open.

## Evidence
- `commit:b92c6a3290020771e57a9e415f8b131be573a770`
- `path:README.md`
- `path:CHANGELOG.md`
- `path:scripts/validate_instruction_docs.py`
- `path:config/mcp-runtime-versions.env`
- `path:scripts/validate_fast.sh`
- `path:scripts/validate_runtime.sh`

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
