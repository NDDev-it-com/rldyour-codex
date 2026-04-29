<!-- Memory Metadata
Last updated: 2026-04-29
Last commit: b1bf776 docs(serena): record plugin auto routing
Scope: plugins/rldyour-serena-mcp
Area: MCP
-->

# MCP_02_serena_workflow_hooks

## Purpose

`plugins/rldyour-serena-mcp` defines the Serena-specific workflow layer for Codex. It depends on the `serena` MCP server from `rldyour-mcps` and adds skills plus lifecycle hooks for semantic code work and fact-only project knowledge synchronization.

## Source Of Truth

- `plugins/rldyour-serena-mcp/.codex-plugin/plugin.json`: manifest with `skills: "./skills/"` and `hooks: "./hooks.json"`.
- `plugins/rldyour-serena-mcp/skills/serena-code-workflow/SKILL.md`: Serena-first semantic code workflow.
- `plugins/rldyour-serena-mcp/skills/serena-memory-sync/SKILL.md`: fact-only `.serena` knowledge maintenance rules.
- `plugins/rldyour-serena-mcp/hooks.json`: Codex hook registrations.
- `plugins/rldyour-serena-mcp/hooks/*.sh`: UserPromptSubmit, PreToolUse, PostToolUse, and Stop hook behavior.
- `plugins/rldyour-serena-mcp/scripts/serena_memory_state.py`: computes whether Serena knowledge is current.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: commits knowledge-only `.serena` updates.

## Entry Points

- `serena-code-workflow`: auto-routes repository inspection, indexing, symbol-aware exploration, reference tracing, refactors, implementation planning, and non-trivial edits.
- `serena-memory-sync`: auto-routes project memory maintenance after meaningful changes, commits, Stop hook prompts, durable plans, and reusable research.
- `UserPromptSubmit` hook: injects a Serena-first reminder for code/repository prompts.
- `PreToolUse` hook: records `.serena/.auto_sync_head` before git commit-like Bash commands.
- `PostToolUse` hook: writes `.serena/.serena_sync_state.json` after git commit-like changes touch non-Serena-knowledge files.
- `Stop` hook: blocks final stop with a sync prompt when project knowledge is stale.

## Current Behavior

Hook commands in `hooks.json` first try the repository-local hook path, then the active Codex plugin cache path. This lets hooks work both inside this repository and after plugin installation.

`user_prompt_submit.sh` parses hook JSON, extracts `prompt`, and only emits Serena context for prompts matching code/project/file/repo/refactor/bug/architecture/implementation/index keywords in English or Russian.

`prepare_auto_sync.sh` only reacts to Bash commands that include git commit-like operations: `commit`, `merge`, `cherry-pick`, `rebase`, or `am`.

`mark_sync_required.sh` compares the pre-commit and post-commit HEAD. If the new commit changed non-Serena-knowledge files, it writes `.serena/.serena_sync_state.json` with the changed file list and emits a system message that Stop will require `serena-memory-sync`.

`stop_memory_sync.sh` exits when `RLDYOUR_SKIP_STOP_GATES=1` or `RLDYOUR_SKIP_SERENA_SYNC=1`. Otherwise it runs `serena_memory_state.py`, removes stale sync markers when knowledge is current, and exits with code `2` plus a sync prompt when knowledge is stale.

`stop_memory_sync.sh` uses `.serena/.sync_marker` to avoid a Stop-hook loop for the same HEAD during a continuation.

## Contracts And Data

Trackable knowledge locations:

- `.serena/memories/`: durable project facts.
- `.serena/plans/`: non-trivial implementation plans worth preserving.
- `.serena/research/`: complex or long source-backed research summaries.

Ignored runtime state:

- `.serena/cache/`
- `.serena/.gitignore`
- `.serena/project.yml`
- `.serena/project.local.yml`
- `.serena/.sync_marker`
- `.serena/.serena_sync_state.json`
- `.serena/.auto_sync_head`
- `.serena/.active_workflow_intent.json`
- `.serena/.dirty_stop_ack`

`serena_memory_state.py` treats knowledge as current when a memory references the current HEAD, when newest synced metadata equals current HEAD, or when changes since the newest synced metadata are knowledge-only.

`commit_serena_knowledge.sh` refuses to auto-commit if non-Serena-knowledge changes are present. It commits only `.serena/memories`, `.serena/plans`, and `.serena/research` with message `chore(serena): sync project knowledge after <head>`.

## Invariants

- Memory files are fact-only English implementation maps, not chat logs or speculative plans.
- Code, git diff, and tests are the source of truth for memory content.
- Do not store secrets, credentials, private cookies, raw tokens, local-only sensitive paths, or generic advice in memories.
- Do not spawn a separate memory-sync agent; the Stop hook asks the current Codex session to sync.
- Do not commit ignored Serena runtime files.

## Change Rules

- When changing hook behavior, update `hooks.json`, relevant hook scripts, and this memory.
- When changing memory format or sync semantics, update `serena-memory-sync/SKILL.md`, `serena_memory_state.py`, hook prompts, and this memory together.
- Use Serena tools first for code inspection when supported; use raw `rg` and file reads as fallback for unsupported file types such as JSON and Markdown.
- After changing this plugin, re-sync `plugins/rldyour-serena-mcp/` into the active Codex plugin cache.

## Verification

- `jq empty plugins/rldyour-serena-mcp/.codex-plugin/plugin.json plugins/rldyour-serena-mcp/hooks.json`: validates manifest and hooks.
- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool`: shows current memory freshness status.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: commits knowledge-only `.serena` changes and refuses mixed changes.
- `git status -sb --ignored`: confirms only expected ignored Serena runtime files remain ignored/untracked.
