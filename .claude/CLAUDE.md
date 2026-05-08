# rldyour-codex Claude Code Memory

## Project Purpose

This repository is the owner's personal Codex marketplace and system setup source. It owns rldyour plugins, skills, hooks, MCP runtime definitions, validation scripts, installer/rollback tooling, CI checks, and Serena project knowledge.

## Language

- User-facing conversation with the owner is Russian unless explicitly requested otherwise.
- Repository artifacts are English: code, comments, commits, docs, plugin metadata, skills, scripts, Serena memories, plans, and research archives.
- Keep identifiers ASCII and stable.

## Source Of Truth

- `.agents/plugins/marketplace.json`: marketplace catalog.
- `plugins/<plugin>/.codex-plugin/plugin.json`: plugin manifests.
- `plugins/<plugin>/skills/*/SKILL.md`: Codex skill routing and workflow contracts.
- `plugins/<plugin>/skills/*/agents/openai.yaml`: skill UI metadata and implicit invocation policy.
- `plugins/rldyour-mcps/.mcp.json`: MCP runtime definitions.
- `plugins/rldyour-flow/hooks.json`: Codex flow lifecycle hooks.
- `plugins/rldyour-serena-mcp/hooks.json`: Serena lifecycle hooks.
- `system/AGENTS.md`: canonical global Codex instructions installed to `~/.codex/AGENTS.md`.
- `AGENTS.md`: Codex-native project instructions, restored from and published to `fullrepo`.
- `.claude/CLAUDE.md`: Claude Code-native project memory, restored from and published to `fullrepo`.
- `.serena/memories/*.md`: verified project facts.

## Claude Code Workflow

- Explore first, then plan, then edit. Prefer exact code/config facts over assumptions.
- Use `/context` to inspect loaded memory and context pressure when behavior seems inconsistent.
- Use `/memory` to confirm this `.claude/CLAUDE.md` and any project memory are loaded.
- Use `/hooks`, `/mcp`, `/permissions`, `/doctor`, and `/status` to debug Claude Code configuration when tools or rules do not behave as expected.
- Keep this file concise and Claude Code-specific. Do not replace it with only an `@AGENTS.md` import.
- Do not create `.claude/rules/` for this repository unless the project grows path-specific Claude Code rules.

## Engineering Rules

- Quality and correctness are higher priority than speed.
- Do not use hacks, temporary workarounds, fake implementations, swallowed errors, or hidden technical debt.
- Do not commit secrets, tokens, cookies, private keys, browser evidence, Serena runtime markers, or local credentials.
- Use `apply_patch` for manual file edits.
- Use `rg` for text search and `rg --files` for file discovery.
- Use Serena-first code inspection where supported; use direct reads for docs, JSON, shell scripts, and other text-level files.
- After meaningful changes, update Serena memories with verified facts only.

## Plugin Boundaries

- `rldyour-mcps` owns MCP transport definitions only.
- `rldyour-serena-mcp` owns Serena-first code workflow and memory sync.
- `rldyour-flow` owns `ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-deploy`, instruction docs sync, post-task sync, and fullrepo sync orchestration.
- `rldyour-rules` owns quality, architecture, dependency, verification, project-instruction, agent-only file, and ADR policy.
- Domain plugins own their workflows: explore, browser, design, security, and LSP.

## Validation Commands

Run the marketplace validation script before finalizing tracked source changes:

```bash
scripts/validate_marketplace.sh
```

Targeted checks:

```bash
codex mcp list
scripts/smoke_mcp_runtime.sh
scripts/smoke_mcp_capabilities.sh
scripts/smoke_hooks.sh
scripts/smoke_codex_hooks_migration.sh
scripts/smoke_local_git_guard.sh
scripts/smoke_flow_branch_cleanup.sh
scripts/smoke_clean_bootstrap.sh
scripts/smoke_fullrepo_sync.sh
scripts/smoke_fullrepo_bootstrap_init.sh
scripts/bootstrap_check.sh --apply
scripts/sync_fullrepo_branch.sh --bootstrap-init
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool
plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool
python3 scripts/validate_instruction_docs.py --require-agent-docs
python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool
python3 scripts/validate_plugin_versions.py
python3 scripts/validate_skill_routing.py
python3 scripts/check_mcp_runtime_versions.py
scripts/doctor_system_codex.sh
```

## Git And Fullrepo

- Keep `main` synchronized with `origin/main` unless an explicit branch/worktree workflow is active.
- Normal branches should not track agent-only files such as `AGENTS.md`, `.claude/CLAUDE.md`, `REVIEW.md`, `.serena`, `.codex`, `.cursor/rules`, or `.agents/skills`.
- Bootstrap agent-only files at initialization with `scripts/sync_fullrepo_branch.sh --bootstrap-init`; it restores existing `fullrepo`, publishes local agent-only files when no `fullrepo` exists, installs excludes, and removes tracked agent-only files from the current branch index when migration is needed.
- Publish agent-only files after normal branch sync with `scripts/sync_fullrepo_branch.sh --publish`.
- Install the local branch-aware pre-push guard in product repositories with `scripts/install_local_git_hooks.sh --repo <project> --apply`; it blocks agent-only files on product branches and permits them only on the configured fullrepo branch while keeping secret/runtime protection active.
- Treat `branch_cleanup_state` from `plugins/rldyour-flow/scripts/flow_post_task_state.py` as a finish gate: merged local/remote workflow branches and merged workflow worktrees must be cleaned or explicitly reported as blockers before final delivery.
- Standard finish order: Serena memories, `AGENTS.md` and `.claude/CLAUDE.md`, checks, atomic normal-branch commits, push, `fullrepo` publish, safe cleanup.

## System Install

- `scripts/install_system_codex.sh --dry-run` previews the system Codex install.
- `scripts/install_system_codex.sh --apply` installs global Codex instructions, config sections, `[features].hooks = true`, deprecated or unstable hook feature key removal, YOLO defaults, marketplace registration, and plugin cache.
- `scripts/doctor_system_codex.sh` verifies installed state, including the active `hooks` feature and absence of deprecated or unstable hook feature keys.
- `scripts/rollback_system_codex.sh --list` and `--restore <backup>` manage installer backups.
- `scripts/collect_diagnostics.sh` writes ignored diagnostics bundles for failure triage.
