<!-- Memory Metadata
Last updated: 2026-05-22
Last commit: 8e503c6c3674e9628e0ce4d537871e2d68a533b0 chore(mcp): bump GitHub MCP server pin to 1.5.0
Scope: verified current technical debt
Area: TECHDEBT
-->

# Current Technical Debt

## Scope
verified current technical debt

## Current source of truth
- `path:README.md`
- `path:CHANGELOG.md`

## Last verified
- date: 2026-05-22
- commit: `8e503c6c3674e9628e0ce4d537871e2d68a533b0`
- checked by: Codex ry-start memory taxonomy sync

## Facts
- Technical debt memories record verified open debt only when it has code/config evidence.
- The previously stale GitHub MCP server runtime pin is closed: `config/mcp-runtime-versions.env` now records `GITHUB_MCP_SERVER_VERSION=1.5.0`, and the root release sync prepares Codex `1.7.13` so the fix is covered by a new GitHub Release instead of retagging `1.7.12`.
- `scripts/smoke_mcp_capabilities.py` documents a two-layer external-MCP smoke resilience (per-server handler graceful skip + `--skip-server` CI policy) so unreachable hosted/localhost MCPs are skipped in CI by policy while staying statically validated. Last documented in commit `5c7b9e2c72b9e163b1398f316402faebbd1e08de` (`fix(flow): start fullrepo tree from empty tree, not HEAD`); no behavior change for the smoke script itself, only the surrounding fullrepo_tree contract.

## Evidence
- `commit:8e503c6c3674e9628e0ce4d537871e2d68a533b0`
- `path:README.md`
- `path:CHANGELOG.md`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.
