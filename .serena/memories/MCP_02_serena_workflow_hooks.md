<!-- Memory Metadata
Last updated: 2026-05-04
Last commit: 018cc6e feat(flow): add fullrepo agent context sync
Scope: plugins/rldyour-serena-mcp, plugins/rldyour-flow/scripts/fullrepo_sync.py, plugins/rldyour-flow/hooks, scripts/smoke_hooks.sh, scripts/smoke_fullrepo_sync.sh, scripts/validate_marketplace.sh, scripts/doctor_system_codex.sh
Area: MCP
-->

# MCP_02_serena_workflow_hooks

## Purpose

`plugins/rldyour-serena-mcp` defines the Serena-specific workflow layer for Codex. It depends on the `serena` MCP server from `rldyour-mcps` and adds skills plus lifecycle hooks for semantic code work and fact-only project knowledge synchronization.

## Source Of Truth

- `plugins/rldyour-serena-mcp/.codex-plugin/plugin.json`: manifest with `skills: "./skills/"` and `hooks: "./hooks.json"`.
- `plugins/rldyour-serena-mcp/README.md`: plugin scope, automatic invocation, trigger map, hook summary, and memory quality target.
- `plugins/rldyour-serena-mcp/skills/serena-code-workflow/SKILL.md`: Serena-first semantic code workflow.
- `plugins/rldyour-serena-mcp/skills/serena-memory-sync/SKILL.md`: fact-only `.serena` knowledge maintenance rules.
- `plugins/rldyour-serena-mcp/hooks.json`: Codex hook registrations.
- `plugins/rldyour-serena-mcp/hooks/*.sh`: UserPromptSubmit, PreToolUse, PostToolUse, and Stop hook behavior.
- `plugins/rldyour-serena-mcp/scripts/serena_memory_state.py`: computes whether Serena knowledge is current.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: commits tracked knowledge-only `.serena` updates or acknowledges fullrepo-managed knowledge without committing AI files to the current branch.
- `scripts/smoke_hooks.sh`: validates repository and installed Serena/Flow hooks with synthetic payloads and a real temporary git lifecycle.

## Entry Points

- `serena-code-workflow`: auto-routes repository inspection, indexing, symbol-aware exploration, reference tracing, refactors, implementation planning, and non-trivial edits.
- `serena-memory-sync`: auto-routes project memory maintenance after meaningful changes, commits, Stop hook prompts, durable plans, and reusable research.
- `UserPromptSubmit` hook: injects a Serena-first reminder for code/repository prompts.
- `PreToolUse` hook: records `.serena/.auto_sync_head` before git commit-like Bash commands.
- `PostToolUse` hook: writes `.serena/.serena_sync_state.json` after git commit-like changes touch non-Serena-knowledge files.
- `Stop` hook: blocks final stop with a sync prompt when project knowledge is stale.
- `scripts/smoke_hooks.sh`: validates Serena hook behavior in both repository source layout and installed plugin-cache layout.

## Current Behavior

Hook commands in `hooks.json` first try the repository-local hook path, then the active Codex plugin cache path. This lets hooks work both inside this repository and after plugin installation.

`user_prompt_submit.sh` parses hook JSON, extracts `prompt`, and only emits Serena context for prompts matching code/project/file/repo/refactor/bug/architecture/implementation/index keywords in English or Russian.

`prepare_auto_sync.sh` only reacts to Bash commands that include git commit-like operations: `commit`, `merge`, `cherry-pick`, `rebase`, or `am`.

`mark_sync_required.sh` compares the pre-commit and post-commit HEAD. If the new commit changed non-Serena-knowledge files, it writes `.serena/.serena_sync_state.json` with the changed file list and emits a system message that Stop will require `serena-memory-sync`.

`stop_memory_sync.sh` exits when `RLDYOUR_SKIP_STOP_GATES=1` or `RLDYOUR_SKIP_SERENA_SYNC=1`. Otherwise it runs `serena_memory_state.py`, removes stale sync markers when knowledge is current, and exits with code `2` plus a sync prompt when knowledge is stale.

`stop_memory_sync.sh` uses `.serena/.sync_marker` to avoid a Stop-hook loop for the same HEAD during a continuation.

The current repository has twelve durable memory files in `.serena/memories`. There are no tracked `.serena/plans` or `.serena/research` files at this point. Normal product repositories should keep `.serena` knowledge out of normal branches and publish it through `fullrepo`; this repository still tracks selected memories because the Codex setup repository uses them as project source-of-truth knowledge.

`plugins/rldyour-serena-mcp/.codex-plugin/plugin.json` version is `0.2.0`. The manifest now describes fullrepo-aware project memory sync.

`scripts/smoke_hooks.sh` now has two layers for both repository and installed plugin cache paths:

- Synthetic non-mutating payload checks for Serena `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, Stop skip gate, Flow `SessionStart`, Flow `PostToolUse`, and Flow Stop skip gate.
- Temporary git lifecycle checks that create a disposable repository, run Flow `SessionStart`, Serena `UserPromptSubmit`, Serena `PreToolUse` before a real git commit, Serena `PostToolUse` after the commit, Serena Stop sync prompt, Flow Stop sync prompt, Flow Stop loop guard, and Flow commit advice for a non-conventional commit.

`scripts/validate_marketplace.sh` and `scripts/doctor_system_codex.sh` run `scripts/smoke_hooks.sh`, so hook lifecycle regressions fail local validation and system doctor.

`commit_serena_knowledge.sh` now has two paths:

- If `.serena/memories`, `.serena/plans`, or `.serena/research` are tracked in the current branch, it preserves the previous knowledge-only commit behavior and removes Serena runtime sync markers after the commit.
- If those knowledge paths are untracked/ignored in a fullrepo-managed project, it requires `serena_memory_state.py` to report `memory_matches_head: true`, then removes runtime sync markers without committing AI files to the current branch. `rldyour-flow` is responsible for publishing the final `fullrepo` snapshot.

Current verified memory-state behavior reports `memory_count: 12` for this repository and uses semantic current-state matching so a knowledge-only memory commit after the newest synced source commit remains current instead of appearing stale.

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

After commit `d12a51f`, `serena_memory_state.py` separates literal and semantic memory matching:

- `memory_directly_mentions_head`: true only when a memory metadata `Last commit:` directly references current `HEAD`.
- `memory_matches_head`: semantic current-state match used by hooks and Flow; this is true for direct matches, newest-synced-is-head, or knowledge-only commits since the newest synced code commit.
- `memory_match_reason`: explains why the state is current or stale. Current values include `direct-head-reference`, `newest-synced-head`, `knowledge-only-commits-since-sync`, `stale-or-missing`, and `sync-marker-requires-refresh`.

This avoids reporting a false mismatch after knowledge-only commits while still exposing whether the current `HEAD` is directly referenced by memory metadata.

`commit_serena_knowledge.sh` refuses to auto-commit if non-Serena-knowledge changes are present. It commits only existing tracked Serena knowledge directories from `.serena/memories`, `.serena/plans`, and `.serena/research` with message `chore(serena): sync project knowledge after <head>`. Missing optional knowledge directories do not prevent staging existing memory changes. In fullrepo-managed repositories, the script acknowledges current memory sync instead of committing.

`serena_memory_state.py` parses `Last commit:` metadata using a 7-to-40 hex character commit SHA. Missing or unresolvable metadata is ignored rather than treated as authoritative.

## Invariants

- Memory files are fact-only English implementation maps, not chat logs or speculative plans.
- Code, git diff, and tests are the source of truth for memory content.
- Do not store secrets, credentials, private cookies, raw tokens, local-only sensitive paths, or generic advice in memories.
- Do not spawn a separate memory-sync agent; the Stop hook asks the current Codex session to sync.
- Do not commit ignored Serena runtime files.
- Do not commit `.serena` knowledge to normal branches in fullrepo-managed product repositories.

## Change Rules

- When changing hook behavior, update `hooks.json`, relevant hook scripts, and this memory.
- When changing memory format or sync semantics, update `serena-memory-sync/SKILL.md`, `serena_memory_state.py`, `commit_serena_knowledge.sh`, hook prompts, and this memory together.
- Use Serena tools first for code inspection when supported; use raw `rg` and file reads as fallback for unsupported file types such as JSON and Markdown.
- After changing this plugin, re-sync `plugins/rldyour-serena-mcp/` into the active Codex plugin cache.
- After changing Serena or Flow hooks, run `scripts/smoke_hooks.sh --repo-only`, `scripts/install_system_codex.sh --apply`, `scripts/smoke_hooks.sh --installed-only`, and `scripts/doctor_system_codex.sh`.

## Verification

- `jq empty plugins/rldyour-serena-mcp/.codex-plugin/plugin.json plugins/rldyour-serena-mcp/hooks.json`: validates manifest and hooks.
- `python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool`: shows current memory freshness status.
- `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh`: commits tracked knowledge-only `.serena` changes, acknowledges fullrepo-managed current knowledge, and refuses mixed changes.
- `scripts/smoke_hooks.sh`: verifies repository and installed hook behavior, including temporary git lifecycle transitions.
- `scripts/smoke_fullrepo_sync.sh`: verifies the fullrepo path used for agent-only Serena knowledge in normal repositories.
- `git status -sb --ignored`: confirms only expected ignored Serena runtime files remain ignored/untracked.
