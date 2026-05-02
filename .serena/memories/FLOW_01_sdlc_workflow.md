<!-- Memory Metadata
Last updated: 2026-05-02
Last commit: 5006272 feat(codex): add lsp and flow workflow plugins
Scope: plugins/rldyour-flow, .agents/plugins/marketplace.json, README.md, .gitignore
Area: FLOW
-->

# FLOW_01_sdlc_workflow

## Purpose

`plugins/rldyour-flow` defines the rldyour SDLC orchestration layer for Codex. It turns owner commands such as `ry-init`, `ry-start`, `ry-newp`, `ry-review`, and `ry-deploy` into reusable workflows and adds a Stop hook that finishes task state after Serena memories are current.

## Source Of Truth

- `plugins/rldyour-flow/.codex-plugin/plugin.json`: plugin manifest, capability list, automatic workflow description, and linked skills/hooks.
- `plugins/rldyour-flow/skills/*/SKILL.md`: command and reviewer workflow trigger descriptions plus execution rules.
- `plugins/rldyour-flow/skills/*/agents/openai.yaml`: UI metadata and `policy.allow_implicit_invocation: true` for every flow skill.
- `plugins/rldyour-flow/hooks.json`: Stop hook registration.
- `plugins/rldyour-flow/hooks/stop_post_task_sync.sh`: post-task Stop hook implementation and loop guard.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py`: deterministic state payload for dirty files, branch, upstream, worktrees, Serena freshness, and fingerprint.
- `plugins/rldyour-flow/references/*.md`: detailed lifecycle, post-task sync, reviewer, deploy, and source-backed design contracts.

## Entry Points

- `ry-init`: initializes a project, sphere, module, or feature scope with a git/worktree audit and Serena-first semantic discovery.
- `ry-start`: full feature/task lifecycle with scoped init, research, plan verification, implementation, atomic commits, quality gates, reviewer tracks, and post-task sync.
- `ry-newp`: new-project discovery, skeptical questions, source-backed technology selection, `.serena/newproj/<project>/` documents, and optional approved scaffold.
- `ry-review`: report-only review of a diff, PR, branch, file scope, or prompt scope plus affected integration graph.
- `ry-deploy`: local-GitHub-server deployment workflow with server baseline logs, checks, deploy, logs/health verification, and fix-forward failure handling.
- `flow-post-task-sync`: finalizes Serena/doc/git/GitHub state after meaningful work or Stop hook prompt.

## Current Behavior

The plugin is skills-and-hooks only. It does not define MCP servers or app connectors; it coordinates existing capabilities from `rldyour-serena-mcp`, `rldyour-explore`, `rldyour-lsps`, `rldyour-browser`, `rldyour-security`, GitHub tooling, and normal Codex tools.

User-facing workflow output stays Russian. Repository docs, plugin docs, memories, plans, research archives, code comments, and commits stay English.

`flow-post-task-sync` runs after Serena memory freshness, not before it. The flow Stop hook exits without blocking when Serena state is stale, allowing the Serena Stop hook to request memory sync first. After Serena is current, the flow hook requests docs/git/GitHub cleanup.

## Contracts And Data

The Stop hook ignores `.serena/.flow_sync_marker` and `.serena/.flow_post_task_state.json` through `.gitignore`. These files are runtime loop guards and must not be committed.

`flow_post_task_state.py` filters known Serena runtime files from dirty status and computes a fingerprint from HEAD, branch, dirty files, ahead/behind status, and Serena freshness.

`flow-post-task-sync` may update `AGENTS.md` when durable Codex project instructions changed. It updates `CLAUDE.md` only when that file exists or the project explicitly uses Claude Code compatibility. Both files must contain verified project facts, not conversation history or speculative plans.

Reviewer tracks are `flow-architecture-review`, `flow-quality-review`, `flow-consistency-review`, `flow-integration-review`, `flow-verification-review`, and `flow-security-review`. `ry-start` and `ry-review` are the approved flow contexts for parallel reviewer subagents, and each reviewer prompt must be self-contained and read-only.

## Invariants

- Do not duplicate MCP transport definitions in `rldyour-flow`.
- Do not commit flow runtime markers, browser artifacts, secrets, tokens, cookies, private keys, or local env files.
- Do not let the flow Stop hook update Serena memories directly; Serena remains the memory source of truth.
- Do not create infinite Stop-hook loops. Repeated prompts for the same fingerprint must allow stop and report the blocker.
- Do not silently delete branches or worktrees unless they are verified merged into `main` and safe to remove.
- Do not claim deployment success without server logs, health checks, or an explicit validation blocker.

## Change Rules

- Update `references/flow-lifecycle.md` when changing command-level lifecycle behavior.
- Update `references/post-task-sync.md`, `hooks/stop_post_task_sync.sh`, and `scripts/flow_post_task_state.py` together when changing Stop-hook sync semantics.
- Update `references/reviewer-protocol.md` when adding, removing, or changing reviewer tracks.
- Update `references/deploy-contract.md` when changing deploy contract fields or safety policy.
- Keep `README.md`, `plugin.json`, `SKILL.md` descriptions, and `agents/openai.yaml` aligned with automatic routing intent.
- Re-sync `plugins/rldyour-flow/` into the active Codex plugin cache after changes.

## Verification

- `jq empty plugins/rldyour-flow/.codex-plugin/plugin.json plugins/rldyour-flow/hooks.json .agents/plugins/marketplace.json`: validates plugin and marketplace JSON.
- `uv run --with pyyaml python /Users/rldyourmnd/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/rldyour-flow/skills/<skill>`: validates each flow skill.
- `uv run --with pyyaml python -c '<parse agents/openai.yaml files>'`: validates `agents/openai.yaml` parse and implicit invocation.
- `python3 -m py_compile plugins/rldyour-flow/scripts/flow_post_task_state.py`: validates the Python state script.
- `shellcheck plugins/rldyour-flow/hooks/stop_post_task_sync.sh plugins/rldyour-flow/scripts/*.sh`: validates shell scripts.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool`: verifies state payload and dirty-path handling.
- `diff -qr plugins/rldyour-flow /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/rldyour-flow/local`: verifies system cache matches the repository plugin.
