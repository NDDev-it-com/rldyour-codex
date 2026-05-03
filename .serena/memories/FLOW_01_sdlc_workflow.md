<!-- Memory Metadata
Last updated: 2026-05-03
Last commit: 614b71e chore(serena): document memory state semantics
Scope: plugins/rldyour-flow, AGENTS.md, system/AGENTS.md, scripts/smoke_hooks.sh, scripts/validate_marketplace.sh, scripts/doctor_system_codex.sh
Area: FLOW
-->

# FLOW_01_sdlc_workflow

## Purpose

`plugins/rldyour-flow` defines the rldyour SDLC orchestration layer for Codex. It turns owner commands such as `ry-init`, `ry-start`, `ry-newp`, `ry-review`, and `ry-deploy` into reusable workflows and adds advisory SessionStart/PostToolUse hooks plus a Stop hook that finishes task state after Serena memories are current.

## Source Of Truth

- `plugins/rldyour-flow/.codex-plugin/plugin.json`: plugin manifest, capability list, automatic workflow description, and linked skills/hooks.
- `plugins/rldyour-flow/skills/*/SKILL.md`: command and reviewer workflow trigger descriptions plus execution rules.
- `plugins/rldyour-flow/skills/*/agents/openai.yaml`: UI metadata and invocation policy for command, post-task, and reviewer skills.
- `plugins/rldyour-flow/hooks.json`: SessionStart, PostToolUse, and Stop hook registration.
- `plugins/rldyour-flow/hooks/session_start_context.sh`: read-only SessionStart hook that emits compact repository context through `hookSpecificOutput.additionalContext`.
- `plugins/rldyour-flow/hooks/post_tool_use_commit_advice.sh`: read-only PostToolUse hook that emits non-blocking commit quality advice through `systemMessage` after Bash `git commit`.
- `plugins/rldyour-flow/hooks/stop_post_task_sync.sh`: post-task Stop hook implementation and loop guard.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py`: deterministic state payload for dirty files, branch, upstream, worktrees, Serena freshness, and fingerprint.
- `plugins/rldyour-flow/references/*.md`: detailed lifecycle, post-task sync, reviewer, deploy, and source-backed design contracts.
- `plugins/rldyour-flow/references/init-context-pack.md`: `ry-init` context-pack contract for scope, architecture, symbols, data, contracts, integration paths, checks, risks, and ready-for tasks.
- `plugins/rldyour-flow/references/context-sufficiency-gate.md`: `ry-start` gate that requires evidence for code, data, patterns, research, quality, and risks before edits.
- `scripts/smoke_hooks.sh`: validates Flow hook behavior from repository sources and installed plugin cache, including temporary git lifecycle checks.

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

`plugins/rldyour-flow/.codex-plugin/plugin.json` version is `0.1.2`. The manifest describes deep `ry-init` context packs, `ry-start` context sufficiency, reviewer skills, deployment, and non-blocking sync hooks.

`plugins/rldyour-flow/skills/ry-init/SKILL.md` now requires reading `references/init-context-pack.md` and building a scoped context pack. It must map modules, layers, symbols, DB fields, schemas, APIs, generated artifacts, configs, tests, integration paths, risks, gaps, and what Codex can safely change.

`plugins/rldyour-flow/skills/ry-start/SKILL.md` now requires reading `references/context-sufficiency-gate.md` and passing the gate before edits. The gate is self-correcting, not a hard blocker: if evidence is missing, Codex must gather more code/research/browser/security/design evidence or ask the owner with options.

`plugins/rldyour-flow/skills/ry-start/SKILL.md` has an `Automatic Helper Routing` section. The owner normally invokes only `rldyour-flow` commands and writes Russian prompts, so `ry-start` must automatically route helper skills instead of waiting for explicit helper skill names.

Current `ry-start` helper routing:

- Repository/code prompts route to `serena-code-workflow`, `lsp-routing`, `quality-first-engineering`, and `implementation-discipline`.
- Technical internet research prompts such as `исследуй интернет`, `изучи в интернете`, and `посмотри документацию` route to `tech-research` first with Context7, DeepWiki, and Grep by Vercel. `web-research` is added for current/latest/source-backed evidence beyond the three MCPs.
- Browser-visible prompts route to `browser-tool-routing`, `browser-validation`, and `browser-debug` when debugging evidence is needed.
- Design/UI/Figma prompts route to `ry-design`, `figma-to-code`, `design-system-implementation`, `fsd-frontend-architecture`, and `design-validation`.
- Security-sensitive prompts route to `owasp-top-10-implementation` during implementation, `ry-sec-review` for explicit security-review requests, and `flow-security-review` in the orchestrated review phase when the touched scope is sensitive.
- Verification and finish route to `verification-quality-gates`, `flow-verification-review`, `serena-memory-sync`, and `flow-post-task-sync`.

`flow-post-task-sync` runs after Serena memory freshness, not before it. The flow Stop hook exits without blocking when Serena state is stale, allowing the Serena Stop hook to request memory sync first. After Serena is current, the flow hook requests docs/git/GitHub cleanup.

The flow SessionStart hook is advisory and read-only. It emits branch, HEAD, upstream, ahead/behind, dirty files, worktree count, project instruction docs, Serena freshness, and flow sync state. It explicitly tells Codex to trigger scoped `ry-init` when context is insufficient and to use the context sufficiency gate before edits.

The flow PostToolUse hook is advisory and read-only. It watches Bash `git commit` commands and emits warnings for non-Conventional Commit subjects, first lines longer than 72 characters, commits touching more than 20 files, sensitive-looking file paths, Serena runtime markers, and committed browser image evidence. It never rejects the command.

`scripts/smoke_hooks.sh` validates Flow hooks in two modes for both repository sources and installed plugin cache:

- Synthetic payload smoke checks Flow `SessionStart`, Flow `PostToolUse`, and Flow Stop skip gate without mutating the current repository.
- Temporary git lifecycle smoke creates a disposable repository, runs Flow `SessionStart`, verifies Flow Stop sync prompt after Serena knowledge is made current, verifies Flow Stop loop guard, creates a non-conventional commit, and verifies Flow commit-advice output.

`scripts/validate_marketplace.sh` and `scripts/doctor_system_codex.sh` run this hook smoke, so Flow hook regressions fail normal validation.

`flow_post_task_state.py` reads raw `git status --porcelain` output with `rstrip("\n")` and then uses `line[3:]` for paths. This preserves porcelain leading status columns and prevents paths such as `.agents/...` from losing the leading dot.

Repository dirtiness is not stored as a durable memory fact. Use `plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool` for current branch, upstream, worktree, dirty-file, ahead/behind, and Serena freshness state.

After commit `614b71e`, `plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool` reported `branch: main`, `upstream: origin/main`, `ahead: 0`, `behind: 0`, `worktree_count: 1`, `needs_flow_sync: false`, and `serena_current: true` before this memory-sync edit. Treat those values as point-in-time verification, not as durable branch state.

## Contracts And Data

The Stop hook ignores `.serena/.flow_sync_marker` and `.serena/.flow_post_task_state.json` through `.gitignore`. These files are runtime loop guards and must not be committed.

`flow_post_task_state.py` filters known Serena runtime files from dirty status and computes a fingerprint from HEAD, branch, dirty files, ahead/behind status, and Serena freshness.

`flow-post-task-sync` may update `AGENTS.md` when durable Codex project instructions changed. It updates `CLAUDE.md` only when that file exists or the project explicitly uses Claude Code compatibility. Both files must contain verified project facts, not conversation history or speculative plans.

Reviewer tracks are `flow-architecture-review`, `flow-quality-review`, `flow-consistency-review`, `flow-integration-review`, `flow-verification-review`, and `flow-security-review`. These six skills set `policy.allow_implicit_invocation: false`; `ry-start` and `ry-review` are the approved flow contexts for parallel reviewer subagents, and each reviewer prompt must be self-contained and read-only.

Flow runtime markers are `.serena/.flow_sync_marker` and `.serena/.flow_post_task_state.json`. They are ignored runtime loop guards, not knowledge files.

SessionStart hook output uses:

- `hookSpecificOutput.hookEventName`: `SessionStart`.
- `hookSpecificOutput.additionalContext`: compact repository context and advisory next actions.

PostToolUse commit advice output uses:

- `systemMessage`: non-blocking commit review text when a warning exists.

## Invariants

- Do not duplicate MCP transport definitions in `rldyour-flow`.
- Do not commit flow runtime markers, browser artifacts, secrets, tokens, cookies, private keys, or local env files.
- Do not let the flow Stop hook update Serena memories directly; Serena remains the memory source of truth.
- Do not let advisory SessionStart or PostToolUse hooks mutate files, commit, push, or block execution.
- Do not create infinite Stop-hook loops. Repeated prompts for the same fingerprint must allow stop and report the blocker.
- Do not silently delete branches or worktrees unless they are verified merged into `main` and safe to remove.
- Do not claim deployment success without server logs, health checks, or an explicit validation blocker.

## Change Rules

- Update `references/flow-lifecycle.md` when changing command-level lifecycle behavior.
- Update `references/init-context-pack.md` when changing `ry-init` required context-pack sections or evidence.
- Update `references/context-sufficiency-gate.md` when changing `ry-start` pre-edit evidence requirements.
- Update `hooks/session_start_context.sh` and `hooks.json` together when changing SessionStart context behavior.
- Update `hooks/post_tool_use_commit_advice.sh` and `hooks.json` together when changing commit advice behavior.
- Update `references/post-task-sync.md`, `hooks/stop_post_task_sync.sh`, and `scripts/flow_post_task_state.py` together when changing Stop-hook sync semantics.
- Update `references/reviewer-protocol.md` when adding, removing, or changing reviewer tracks.
- Update `references/deploy-contract.md` when changing deploy contract fields or safety policy.
- Keep `README.md`, `plugin.json`, `SKILL.md` descriptions, and `agents/openai.yaml` aligned with automatic routing intent.
- Keep compact Russian and English trigger phrases in all flow and helper skill descriptions used by `ry-start`.
- Re-sync `plugins/rldyour-flow/` into the active Codex plugin cache after changes.
- After changing Flow hooks, run `scripts/smoke_hooks.sh --repo-only`, `scripts/install_system_codex.sh --apply`, `scripts/smoke_hooks.sh --installed-only`, and `scripts/doctor_system_codex.sh`.

## Verification

- `jq empty plugins/rldyour-flow/.codex-plugin/plugin.json plugins/rldyour-flow/hooks.json .agents/plugins/marketplace.json`: validates plugin and marketplace JSON.
- `uv run --with pyyaml python /Users/rldyourmnd/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/rldyour-flow/skills/<skill>`: validates each flow skill.
- `scripts/validate_marketplace.sh`: validates `agents/openai.yaml` parse, default prompt length, `$skill-name` prompt reference, short description length, MCP dependencies, and reviewer implicit-invocation exceptions.
- `python3 -m py_compile plugins/rldyour-flow/scripts/flow_post_task_state.py`: validates the Python state script.
- `shellcheck plugins/rldyour-flow/hooks/*.sh plugins/rldyour-flow/scripts/*.sh`: validates flow shell hooks and scripts.
- `printf '{"source":"startup"}' | plugins/rldyour-flow/hooks/session_start_context.sh`: verifies SessionStart JSON output.
- `printf '{"tool_name":"Bash","tool_input":{"command":"git commit -m test"}}' | plugins/rldyour-flow/hooks/post_tool_use_commit_advice.sh`: verifies commit-advice hook exits cleanly against the current HEAD.
- `plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool`: verifies state payload and dirty-path handling.
- `scripts/smoke_hooks.sh`: verifies Flow and Serena hook behavior, including temporary git lifecycle transitions.
- `diff -qr plugins/rldyour-flow /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/rldyour-flow/local`: verifies system cache matches the repository plugin.
