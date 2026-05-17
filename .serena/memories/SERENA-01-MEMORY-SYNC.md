<!-- Memory Metadata
Last updated: 2026-05-17
Last commit: 2ee72cf feat(codex): harden lifecycle and manual validation
Scope: plugins/rldyour-serena-mcp/hooks.json, plugins/rldyour-serena-mcp/hooks/*.sh, plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py, plugins/rldyour-serena-mcp/scripts/serena_memory_state.py, plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh, plugins/rldyour-serena-mcp/skills/serena-memory-sync/SKILL.md, system/agents/serena-sync.toml, scripts/smoke_serena_memory_taxonomy.sh
Area: SERENA
-->

# SERENA-01-MEMORY-SYNC

## Purpose

`rldyour-serena-mcp` owns Serena-first repository understanding and the durable project-memory sync loop. Its memory sync contract keeps `.serena/memories/` fact-only, current, and useful for future Codex, Claude Code, and other GPT-based coding sessions.

## Source Of Truth

- `plugins/rldyour-serena-mcp/skills/serena-memory-sync/SKILL.md`: memory structure, taxonomy, sync workflow, and fact-only rules.
- `system/agents/serena-sync.toml`: managed Codex memory-maintenance subagent instructions.
- `plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py`: changed-file classifier and memory-target analyzer.
- `plugins/rldyour-serena-mcp/scripts/serena_memory_state.py`: freshness state and analyzer integration.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: knowledge commit/acknowledgement helper.
- `plugins/rldyour-serena-mcp/hooks/prepare_auto_sync.sh`: records pre-commit HEAD.
- `plugins/rldyour-serena-mcp/hooks/mark_sync_required.sh`: writes machine-readable sync state after commit-like HEAD changes.
- `plugins/rldyour-serena-mcp/hooks/stop_memory_sync.sh`: Stop gate/advisory for stale memories, invoked by Flow's ordered Stop lifecycle dispatcher.
- `scripts/smoke_serena_memory_taxonomy.sh`: regression coverage for taxonomy, analyzer, hooks, and fullrepo acknowledgement.

## Entry Points

- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool`: inspect memory freshness, analyzer source, changed files, and target memories.
- `python3 plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py --from-ref <old> --to-ref <new>`: classify changed files and target memories.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: acknowledge current memories in fullrepo-managed repositories or create a knowledge-only commit where knowledge is tracked.
- `scripts/smoke_serena_memory_taxonomy.sh`: focused local smoke for the memory-brain contract.

## Current Behavior

- Memories use numbered filenames: `AREA-01-SLUG.md`. The active index is `CORE-01-INDEX.md`.
- `analyze_sync_scope.py` emits schema version `2`, taxonomy version `2`, `memory_taxonomy`, `areas`, `areas_summary`, `memory_targets`, `candidate_memory_focus`, and `risk_profile`.
- Analyzer taxonomy v2 includes the indexed areas `DESIGN`, `LSP`, and `RULES` in addition to the original CORE/CODEX/MCP/SERENA/HOOKS/FLOW/DOCS/RELEASE/TECHDEBT areas.
- The analyzer is Codex-specific: Codex agent/skill/plugin changes target `CODEX-*` memories, not Claude Code taxonomy.
- `serena_memory_state.py` recursively scans `.serena/memories/**/*.md`, parses `Last commit:` metadata, resolves commits, and reports `direct-head-reference`, `newest-synced-head`, `knowledge-only-commits-since-sync`, `stale-or-missing`, or `sync-marker-requires-refresh`.
- Serena knowledge paths are `.serena/memories/`, `.serena/plans/`, `.serena/research/`, `.serena/newproj/`, and `.serena/deploy/`. Agent instruction files are no longer treated as Serena knowledge paths for freshness; they trigger memory sync when durable behavior changed.
- `mark_sync_required.sh` writes `.serena/.serena_sync_state.json` with changed files, non-knowledge changed files, previous/current HEAD, and analyzer output when a commit-like Bash command changes HEAD.
- `stop_memory_sync.sh` exits `2` when memories are stale, includes analyzer focus and taxonomy guidance, and asks to delegate to managed Codex `serena-sync` when the active workflow allows subagents. It is not registered directly as a Stop command in `rldyour-serena-mcp/hooks.json`; `rldyour-flow/hooks/stop_lifecycle_dispatcher.sh` invokes it before Flow post-task sync to avoid concurrent cross-plugin Stop execution.
- System Codex config must include `[features].plugin_hooks = true`; otherwise the installed `rldyour-serena-mcp` hook declarations can exist in plugin cache without being loaded as bundled plugin hooks.
- Stop loop prevention uses `.serena/.sync_marker`: when the same HEAD has already requested sync in the current Stop continuation, the hook exits `0` to avoid an infinite loop.
- `commit_serena_knowledge.sh` clears runtime markers after current memories mention HEAD. In fullrepo-managed repositories it acknowledges current memories without creating a normal-branch commit.

## Contracts And Data

- Runtime files are not durable knowledge and must not be committed or published as memory content: `.serena/.sync_marker`, `.serena/.serena_sync_state.json`, `.serena/.auto_sync_head`, `.serena/.active_workflow_intent.json`, `.serena/.dirty_stop_ack`, `.serena/.flow_sync_marker`, `.serena/.flow_post_task_state.json`, `.serena/cache/`, `.serena/project.local.yml`.
- Every touched memory starts with the metadata block from the skill and includes `Last commit: <sha> <message>`.
- Analyzer memory targets for commit `2ee72cf` include `CODEX-01-PLUGIN-CANON.md`, `CORE-02-MARKETPLACE.md`, `FLOW-01-SDLC.md`, `HOOKS-01-LIFECYCLE.md`, `MCP-01-TRANSPORT.md`, `RELEASE-01-VALIDATION.md`, `SERENA-01-MEMORY-SYNC.md`, and `TECHDEBT-01-NOW.md`.
- The managed `serena-sync` subagent verifies claims from current code/config/tests at HEAD, then recent git history, then diff, then old memories.

## Invariants

- Memories are facts only: paths, entry points, behavior, contracts, invariants, change rules, verification, and known durable gaps.
- Do not store chat history, speculative plans, TODO backlogs, secrets, raw credentials, browser evidence, runtime snapshots, or transient health logs in memories.
- Memory sync runs after meaningful code, plugin, workflow, hook, config, design, security, architecture, setup, validation, or durable docs changes.
- `ry-init` remains read-only for Serena memories unless the user explicitly requested sync or a stale-memory hook requires it.

## Change Rules

- When analyzer classification changes, update `scripts/smoke_serena_memory_taxonomy.sh` with a path-level expectation.
- When adding a new durable memory area, update `MEMORY_TAXONOMY` in `analyze_sync_scope.py`, `serena-memory-sync/SKILL.md`, and `CORE-01-INDEX.md`.
- When touching Stop/mark hooks, verify hook output uses Codex `hookSpecificOutput` where machine-readable context is required and does not use Claude Code `Agent(...)` syntax.
- In fullrepo-managed repositories, update memories locally, run `commit_serena_knowledge.sh`, then publish through `fullrepo`.

## Verification

- `scripts/smoke_serena_memory_taxonomy.sh`: proves analyzer schema, taxonomy version, index-area parity, target routing, nested memory scan, Stop advisory, loop guard, and fullrepo acknowledgement/refusal.
- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool`: proves freshness against HEAD and shows analyzer payload.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: proves current fullrepo-managed memories can be acknowledged.
- `scripts/validate_marketplace.sh`: includes the taxonomy smoke and repository-wide validation.
