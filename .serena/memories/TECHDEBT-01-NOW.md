<!-- Memory Metadata
Last updated: 2026-05-29
Last commit: 818d3c1
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
- date: 2026-05-29
- commit: `818d3c19388978564b29724488678cd803b99867`
- checked by: Codex system sync after nested legacy profile cleanup

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
- Version synchronization debt is now closed for this adapter at `1.0.3`; root
  control-plane pins must reference commit
  `818d3c19388978564b29724488678cd803b99867`.
- CodeQL action freshness debt is closed for Codex at `github/codeql-action`
  `v4.36.0`; Dependabot GitHub Actions version updates are grouped into one
  reviewable PR.
- Dependabot cadence noise is closed for Codex: GitHub Actions updates are
  checked monthly and grouped under the `github-actions` group.
- Semgrep MCP freshness drift is closed for Codex at `semgrep==1.164.0`, and
  shadcn MCP freshness is closed at `shadcn@4.8.2`.
- CI classifier drift is closed for retried MCP TaskGroup startup noise and for
  warnings emitted by explicitly superseded Serena research claims; the
  classifier still fails on unknown non-empty lines in strict mode.
- Remaining debt should be recorded here only when current code/config evidence
  proves it is still open.

## Evidence
- `commit:d7909f83ae7ec947946f374ffae99af37db5335a`
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
