<!-- Memory Metadata
Last updated: 2026-05-27
Last commit: 8b746f31da1f1435d9ca5a9de5aa65cf7ccf7fa9 fix: allow public fast validation without agent docs
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
- date: 2026-05-27
- commit: `8b746f31da1f1435d9ca5a9de5aa65cf7ccf7fa9`
- checked by: Codex ry-start current audit repair

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
- Remaining debt should be recorded here only when current code/config evidence
  proves it is still open.

## Evidence
- `commit:8b746f31da1f1435d9ca5a9de5aa65cf7ccf7fa9`
- `path:README.md`
- `path:CHANGELOG.md`
- `path:scripts/validate_instruction_docs.py`
- `path:config/mcp-runtime-versions.env`
- `path:scripts/validate_fast.sh`

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
