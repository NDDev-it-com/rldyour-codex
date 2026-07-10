<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: 7f39e8f3704126d9808604168a5c9061da228684 chore(release): codex adapter 1.8.4
Scope: MCP runtime transport and pin policy
Area: MCP
-->

# MCP Transport

## Scope
MCP runtime transport and pin policy

## Current source of truth
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:config/mcp-runtime-versions.env`
- `path:README.md`
- `https://registry.npmjs.org/@modelcontextprotocol/server-sequential-thinking/2026.7.4`
- `https://registry.npmjs.org/@upstash/context7-mcp/3.2.3`

## Last verified
- date: 2026-07-10
- commit: `7f39e8f3704126d9808604168a5c9061da228684`
- checked by: Codex MCP runtime pin refresh

## Facts
- MCP memories record server ownership, transports, versions, and toolset constraints.
- Sequential Thinking MCP is pinned to `2026.7.4` and Context7 MCP is pinned to
  `3.2.3` identically in `config/mcp-runtime-versions.env` and
  `plugins/rldyour-mcps/.mcp.json`.
- Chrome DevTools MCP remains on the exact bootstrap-managed CloakBrowser
  transport; this dependency refresh does not change browser routing.

## Evidence
- `commit:7f39e8f3704126d9808604168a5c9061da228684`
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:config/mcp-runtime-versions.env`
- `path:README.md`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Applies to

- The scope and source-of-truth paths declared in this memory.

## Source of truth

- The `Current source of truth` entries above, plus current code, configuration, tests, git state, and live GitHub state where this memory references live release or repository surfaces.

## Invariants

- Current code, configuration, tests, validators, git state, and live GitHub state override this memory whenever they disagree.

## Current State

- Treat the `Facts` section as the current durable state. Do not treat historical evidence, superseded notes, or previous release entries as current.

## Do Not Infer

- Do not infer runtime versions, product versions, commits, permissions, release state, security posture, or tool behavior from this memory without checking the source of truth.

## Update Triggers

- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, live release state, or durable agent-workflow contracts.

## Validation Commands

- Run the rldyour control-plane Serena memory validators in strict mode: `validate_serena_memory_schema` (`--strict-mode strict-all`) and `validate_serena_memory_semantics` (`--strict-current-facts --strict-metadata-dates --strict-evidence-commits`).

## Repair Procedure

1. Re-read the source-of-truth files listed above.
2. Update only verified current facts; move stale facts into historical evidence.
3. Rerun the validation commands until green.
