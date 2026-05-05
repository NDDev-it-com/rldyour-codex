<!-- Memory Metadata
Last updated: 2026-05-05
Last commit: 14f70e0 fix(flow): make local git guard fullrepo-aware
Scope: plugins/rldyour-serena-mcp, plugins/rldyour-serena-mcp/scripts/serena_memory_state.py, plugins/rldyour-flow/scripts/fullrepo_sync.py, plugins/rldyour-flow/hooks, scripts/smoke_hooks.sh, scripts/smoke_fullrepo_sync.sh, scripts/validate_marketplace.sh, scripts/doctor_system_codex.sh
Area: MCP
-->

# MCP_02_serena_workflow_hooks

## Purpose

`plugins/rldyour-serena-mcp` owns the Serena lifecycle hooks and memory freshness contract used by flow stop logic and task completion.

## Source Of Truth

- `plugins/rldyour-serena-mcp/hooks.json`
- `plugins/rldyour-serena-mcp/hooks/user_prompt_submit.sh`
- `plugins/rldyour-serena-mcp/hooks/prepare_auto_sync.sh`
- `plugins/rldyour-serena-mcp/hooks/mark_sync_required.sh`
- `plugins/rldyour-serena-mcp/hooks/stop_memory_sync.sh`
- `plugins/rldyour-serena-mcp/scripts/serena_memory_state.py`
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`
- `scripts/smoke_hooks.sh`

## Hook Contracts

`hooks.json` resolves local plugin script first, then installed cache path:

- `UserPromptSubmit` -> `user_prompt_submit.sh`
- `PreToolUse` -> `prepare_auto_sync.sh`
- `PostToolUse` -> `mark_sync_required.sh`
- `Stop` -> `stop_memory_sync.sh`

All hooks are lightweight and shell-based.

### UserPromptSubmit

- Input: prompt from hook payload.
- Activates Serena context when prompt contains project/code/symbol/refactor/implementation keywords in Russian or English.
- Adds `hookSpecificOutput.additionalContext` with ordered tool suggestions:
  `check_onboarding_performed` → `list_memories` → `read_memory` → `get_symbols_overview` → `find_symbol` → `find_referencing_symbols` → `search_for_pattern`.
- No side effects, advisory only.

### PreToolUse

- Watches Bash commands containing:
  `git commit|merge|cherry-pick|rebase|am`.
- Writes `.serena/.auto_sync_head` with pre-command HEAD only.
- No exit blocking.

### PostToolUse

- Handles only Bash commands in the same commit-like command set.
- If a real HEAD change occurred and commit touched non-serena knowledge paths, writes `.serena/.serena_sync_state.json` with changed files.
- Emits a single advisory `systemMessage` requiring Serena knowledge sync before task stop.
- Uses `.serena/.serena_sync_state.json` as a machine-readable marker.

### Stop

- If Serena is current, runtime markers are removed and hook exits.
- If stale, writes `stop` marker and exits code `2` with required sync reason and changed file list.
- If already requested for same HEAD (`.serena/.sync_marker` present), exits code `0` with a loop-block message to avoid repeated Stop prompts.
- No direct commit or install actions.

## Memory Freshness

`serena_memory_state.py` is the state source for stop/post-tool logic:

- scans memory count from `.serena/memories/*.md`
- parses `Last commit:` metadata (`7..40` hex chars)
- detects newest synced commit among memory metadata
- compares changed files since newest synced commit
- returns:
  - `is_current`
  - `memory_matches_head`
  - `memory_directly_mentions_head`
  - `memory_match_reason` (`direct-head-reference`, `newest-synced-head`, `knowledge-only-commits-since-sync`, `stale-or-missing`, `sync-marker-requires-refresh`)
- carries `sync_state` for forced sync markers.

`commit_serena_knowledge.sh` behavior:

- no-op when no in-repo changes
- refuses non-knowledge changes
- commits only `.serena/memories`, `.serena/plans`, `.serena/research` when tracked and changed
- commit message format: `chore(serena): sync project knowledge after <head>`
- in fullrepo-managed mode (knowledge in worktree but untracked/ignored in current index), acknowledges current memory state and clears markers without committing AI files to current branch.

## Knowledge Path and Runtime Path Rules

- Knowledge directories:
  - `.serena/memories/`
  - `.serena/plans/`
  - `.serena/research/`
- Runtime-only ignores:
  - `.serena/.sync_marker`
  - `.serena/.serena_sync_state.json`
  - `.serena/.auto_sync_head`
  - `.serena/.active_workflow_intent.json`
  - `.serena/.dirty_stop_ack`

Flow stop sync requires Serena freshness first; flow stop exits without forcing sync if Serena sync is still required.

## Verification

- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool`
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`
- `scripts/smoke_hooks.sh`
- `scripts/validate_marketplace.sh`
- `python3 plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool`

## Invariants

- Do not block execution in advisory Serena hooks.
- Do not commit runtime marker files or runtime secrets.
- No fullrepo-managed knowledge mutation in current normal branch index.
- Stop-hook loop prevention must stay in place.
