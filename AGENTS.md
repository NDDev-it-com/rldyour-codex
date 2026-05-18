# rldyour-codex Agent Instructions

## Project Purpose

This repository is the maintainer's personal Codex marketplace, published publicly under the GNU AGPL-3.0-or-later license at https://github.com/NDDev-it-com/rldyour-codex. Maintainer: Danil Silantyev (`@rldyourmnd`), CEO of NDDev. The repository owns rldyour plugins, skills, hooks, MCP runtime definitions, validation scripts, and Serena project knowledge for the local Codex runtime.

## License

- Code, configs, scripts, and tests in this repository are licensed under GNU AGPL-3.0-or-later. The canonical FSF text lives in `LICENSE`.
- AGPL-3.0 Section 13 (Remote Network Interaction) applies to modified versions served over a network.
- Contributions are accepted under the same license (inbound = outbound).

## Language And Documentation

- User-facing communication with the owner is Russian unless explicitly requested otherwise.
- Repository files are English: docs, plugin metadata, skills, scripts, comments, commits, Serena memories, plans, and research archives.
- Keep technical identifiers ASCII, stable, and kebab-case where applicable.

## Source Of Truth

- `.agents/plugins/marketplace.json`: active marketplace catalog.
- `plugins/<plugin>/.codex-plugin/plugin.json`: plugin manifest and linked capabilities.
- `plugins/<plugin>/skills/*/SKILL.md`: primary automatic skill routing contract.
- `plugins/<plugin>/skills/*/agents/openai.yaml`: UI metadata and implicit invocation policy.
- `plugins/rldyour-mcps/.mcp.json`: repository MCP runtime definitions.
- `config/mcp-runtime-versions.env`: pinned local MCP launcher, host runtime, and Codex CLI versions used by scripts and manual CI.
- `VERSION` and `CHANGELOG.md`: marketplace release version and human-readable change history.
- `.github/workflows/validate.yml`: auto-running validation on push to main, pull requests, and workflow_dispatch. Fast and runtime jobs run on Ubuntu and macOS automatically on push/PR; release dry-run, dependency-pins, and mcp-safe-calls run on Ubuntu only.
- `.github/workflows/security-static.yml`: auto-running no-paid static security on push, pull_request, weekly schedule, and workflow_dispatch.
- `.github/workflows/codeql.yml`: auto-running GitHub CodeQL analysis on push, pull_request, weekly schedule. Matrix: Python and GitHub Actions. Pinned `github/codeql-action@458d36d7d4f47d0dd16ca424c1d3cda0060f1360 # v3`.
- `.github/workflows/release.yml`: auto-running on push of SemVer tags matching `[0-9]*.[0-9]*.[0-9]*` and prereleases `[0-9]*.[0-9]*.[0-9]*-*`, plus workflow_dispatch as a fallback.
- `.github/workflows/dependency-check.yml`: auto-running MCP runtime pin freshness on daily schedule, push to MCP pin sources, and workflow_dispatch. Job exported as `MCP runtime pin freshness (scheduled)`.
- `.github/branch-protection/main.json`: desired branch protection for the public `main` branch with required CI status checks.
- `config/skill-routing-policy.json`: deterministic prompt-to-skill routing policy tests.
- `system/agents/*.toml`: managed Codex custom subagent role configs installed to `${CODEX_HOME:-$HOME/.codex}/agents/*.toml`.
- `system/rules/*.rules`: managed Codex execpolicy rules installed to `${CODEX_HOME:-$HOME/.codex}/rules/*.rules`.
- `${CODEX_HOME:-$HOME/.codex}/config.toml`: active system Codex registration, `[features].hooks`, `[features].plugin_hooks`, `[features].multi_agent`, `[agents]` registration, YOLO permission defaults, owner-selected model defaults, approved MCP tool overrides, and MCP runtime config.
- `${CODEX_HOME:-$HOME/.codex}/agents/*.toml`: active managed subagent role configs; rldyour-managed roles use `model = "gpt-5.5"` with `model_reasoning_effort = "medium"` and temporary specialist-MCP isolation. Disabled specialist MCP overrides must include full `command` or `url` transport metadata copied from `plugins/rldyour-mcps/.mcp.json`; built-in `codex_apps` stays inherited from Apps/connectors and must not be declared as a synthetic `[mcp_servers.codex_apps]` table.
- `.claude/CLAUDE.md`: Claude Code-native project memory for this repository, published through `fullrepo`.
- `.serena/memories/*.md`: high-signal verified project knowledge.

## Plugin Boundaries

- `rldyour-mcps` owns MCP transport definitions only. It must not contain behavior policy or skills.
- `rldyour-serena-mcp` owns Serena-first code workflow, memory sync, and Serena lifecycle hook scripts. Its Stop memory gate is invoked by the ordered Flow lifecycle dispatcher, not registered as a competing plugin Stop hook.
- `rldyour-flow` owns SDLC commands, scoped context packs, context sufficiency gates, instruction docs sync, fast offline/local-only SessionStart worktree bootstrap/context dispatcher hooks, cwd-safe PreToolUse guardrails, advisory commit hooks, ordered local-only Stop lifecycle dispatch, and post-task synchronization hooks.
- `rldyour-rules` owns quality, architecture, dependency, verification, Codex/Claude project-instruction, and ADR policy.
- `rldyour-design` owns Figma-to-code, centralized i18n, dynamic/static/admin content classification, centralized tokens, UI-kit reuse, strict FSD placement, shadcn/ui, ReactBits, and browser/design validation gates.
- `rldyour-explore`, `rldyour-browser`, `rldyour-security`, and `rldyour-lsps` own their domain workflows and must not duplicate MCP transports.
- Curated `github@openai-curated` and `gmail@openai-curated` are intentionally enabled in system Codex.

## Development Rules

- Use `apply_patch` for manual file edits.
- Do not commit secrets, tokens, cookies, private keys, raw credentials, browser evidence, or Serena runtime markers.
- Use `plugin-creator` guidance for plugin manifests and marketplace changes.
- Use `skill-creator` guidance for skill changes. Every callable rldyour skill must include compact Russian and English trigger phrases in `SKILL.md` frontmatter `description`; details belong in the skill body or references. Reviewer track skills may set `allow_implicit_invocation: false` when orchestrated by `ry-start` or `ry-review`.
- Use Serena-first code inspection where supported; use `rg` and direct reads for docs, JSON, shell scripts, and other text-level work.
- After meaningful changes, update `.serena/memories` with verified facts only.
- After meaningful project behavior, workflow, setup, validation, architecture, plugin, hook, or command changes, update `AGENTS.md` for Codex and `.claude/CLAUDE.md` for Claude Code from verified code state.
- After plugin changes that affect runtime behavior, sync changed plugin directories into `${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local` and restart Codex.
- `fullrepo` is the standard branch for portable agent-only context. Normal project branches should exclude project-root `AGENTS.md`, `.claude/CLAUDE.md`, `.serena` knowledge, `.claude`, `.codex`, `.cursor/rules`, `.agents/skills`, and similar AI workflow files through `.git/info/exclude`; publish them with `scripts/sync_fullrepo_branch.sh --publish` after normal branch sync. This repository may intentionally track selected instruction templates that are product artifacts, such as `system/AGENTS.md`.

## Validation

Run the marketplace validation script before finalizing repository changes:

```bash
scripts/validate_marketplace.sh
scripts/validate_fast.sh
scripts/validate_runtime.sh --strict-runtime
scripts/validate_release.sh
scripts/validate_execpolicy_rules.sh
```

Additional targeted checks:

```bash
codex mcp list
scripts/smoke_mcp_runtime.sh
scripts/smoke_mcp_capabilities.sh
scripts/smoke_hooks.sh
scripts/smoke_codex_hooks_migration.sh
scripts/smoke_serena_memory_freshness.sh
scripts/smoke_serena_memory_taxonomy.sh
scripts/smoke_local_git_guard.sh
scripts/smoke_flow_branch_cleanup.sh
scripts/smoke_clean_bootstrap.sh
scripts/smoke_fullrepo_sync.sh
scripts/smoke_fullrepo_bootstrap_init.sh
python3 scripts/validate_agent_tools.py
python3 scripts/validate_action_pins.py
python3 scripts/scan_text_security.py
uv run --with pytest --with pytest-cov --with pyyaml python -m pytest
scripts/bootstrap_check.sh --apply
scripts/sync_fullrepo_branch.sh --status
scripts/sync_fullrepo_branch.sh --bootstrap-init
python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool
python3 scripts/check_serena_memory_freshness.py
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool
plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool
python3 scripts/validate_instruction_docs.py --require-agent-docs
plugins/rldyour-lsps/scripts/check_lsps.sh
python3 scripts/validate_plugin_versions.py
python3 scripts/validate_skill_routing.py
python3 scripts/release_manifest.py
python3 scripts/release_sbom.py
python3 scripts/check_mcp_runtime_versions.py
python3 scripts/validate_runtime_prereqs.py --strict --require-codex
scripts/doctor_system_codex.sh
scripts/doctor_system_codex.sh --quick --strict-runtime
```

For plugin cache verification:

```bash
diff -qr plugins/<plugin> "${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local"
```

## Git And Sync

- Keep `main` synchronized with `origin/main` unless working on an explicit branch or worktree workflow.
- Prefer atomic commits with Conventional Commits.
- Use `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh` for knowledge-only Serena updates.
- Use `$instruction-docs-sync` after Serena memory sync when durable project instruction facts changed.
- Use `scripts/sync_fullrepo_branch.sh --bootstrap-init` at initialization when agent-only context is expected, and `scripts/sync_fullrepo_branch.sh --publish` after normal branch push. Bootstrap restores existing `fullrepo`, publishes local agent-only files when no `fullrepo` exists, installs excludes, and removes tracked agent-only files from the current branch index when migration is needed. Use `scripts/worktree_add.sh <branch> [path]` for parallel Codex worktrees that should immediately restore agent-only context from `fullrepo`.
- Use `scripts/install_local_git_hooks.sh --repo <project> --apply` to install the branch-aware local pre-push guard in product repositories; it keeps product branches strict and allows AI context only on the configured `fullrepo` branch while still blocking secrets/runtime files.
- Treat `branch_cleanup_state` from `plugins/rldyour-flow/scripts/flow_post_task_state.py` as a finish gate: merged local/remote workflow branches and merged workflow worktrees must be cleaned or explicitly reported as blockers before final delivery.
- Treat bootstrap-only untracked `.serena` files created by tool startup, such as `.serena/project.yml` plus runtime markers, as non-work; they must not force a Stop-hook post-task sync loop.
- Standard finish order is Serena memories and durable docs from verified code, matching checks, atomic normal-branch commit and push, `fullrepo` publish from final `HEAD`, then safe cleanup of merged workflow branches and worktrees.
- Before final delivery, ensure `git status -sb` is clean and pushed when the task produced commits.

## System Install

- `system/AGENTS.md` is the canonical template for the owner's global `~/.codex/AGENTS.md`.
- `scripts/install_system_codex.sh --dry-run` shows what would be installed.
- `scripts/install_system_codex.sh --apply` writes the global AGENTS file, installs managed `agents/*.toml`, installs managed Codex execpolicy rules from `system/rules/*.rules`, patches rldyour-owned Codex config sections, writes the official Codex config schema hint, writes `[features].hooks = true`, `[features].plugin_hooks = true`, and `[features].multi_agent = true`, removes deprecated hook aliases such as `codex_hooks`, derives rldyour plugin enablement from `.agents/plugins/marketplace.json`, derives MCP server registration from `plugins/rldyour-mcps/.mcp.json`, applies owner-requested YOLO/model defaults, writes approved MCP tool overrides, registers the marketplace, syncs plugin cache, and refreshes trusted hashes for installed rldyour plugin hooks through the app-server RPC method `hooks/list` over `codex app-server --listen stdio://`. Add `--strict-runtime` when missing launchers for enabled MCP servers must fail instead of warn.
- `scripts/validate_execpolicy_rules.sh` validates managed rules with `codex execpolicy check`.
- `scripts/doctor_system_codex.sh` verifies the installed system Codex state, including marketplace-derived rldyour plugin enablement, MCP registration from `.mcp.json`, the config schema hint, active `hooks`, `plugin_hooks`, and `multi_agent` features, managed subagent config parity, managed subagent `gpt-5.5`/`medium` settings, managed subagent temporary MCP isolation with complete disabled transport metadata, installed rldyour plugin hook trust/enabled state, and absence of deprecated hook aliases. Use `--quick --strict-runtime` for a bounded strict runtime smoke and `--strict-runtime` for full strict prerequisite enforcement.
- `scripts/rollback_system_codex.sh --list` lists installer backups; `--restore <backup>` restores backed up `AGENTS.md`, `config.toml`, managed `agents/*.toml`, and managed `rules/*.rules`.
- `scripts/collect_diagnostics.sh` writes a local ignored diagnostics bundle for failure triage.
