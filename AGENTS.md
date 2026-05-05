# rldyour-codex Agent Instructions

## Project Purpose

This repository is the owner's personal Codex marketplace. It owns rldyour plugins, skills, hooks, MCP runtime definitions, validation scripts, and Serena project knowledge for the local Codex runtime.

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
- `config/mcp-runtime-versions.env`: pinned local MCP launcher and Codex CLI versions used by scripts and CI.
- `VERSION` and `CHANGELOG.md`: marketplace release version and human-readable change history.
- `.github/workflows/validate.yml`: Ubuntu/macOS push/pull-request validation for marketplace, temporary system install, MCP capability smoke, hook lifecycle smoke, and clean bootstrap.
- `.github/workflows/dependency-check.yml`: scheduled MCP runtime pin freshness check.
- `config/skill-routing-policy.json`: deterministic prompt-to-skill routing policy tests.
- `${CODEX_HOME:-$HOME/.codex}/config.toml`: active system Codex registration, YOLO permission defaults, and MCP runtime config.
- `.claude/CLAUDE.md`: Claude Code-native project memory for this repository, published through `fullrepo`.
- `.serena/memories/*.md`: high-signal verified project knowledge.

## Plugin Boundaries

- `rldyour-mcps` owns MCP transport definitions only. It must not contain behavior policy or skills.
- `rldyour-serena-mcp` owns Serena-first code workflow, memory sync, and Serena lifecycle hooks.
- `rldyour-flow` owns SDLC commands, scoped context packs, context sufficiency gates, instruction docs sync, advisory session/commit hooks, and post-task synchronization hooks.
- `rldyour-rules` owns quality, architecture, dependency, verification, Codex/Claude project-instruction, and ADR policy.
- `rldyour-explore`, `rldyour-browser`, `rldyour-design`, `rldyour-security`, and `rldyour-lsps` own their domain workflows and must not duplicate MCP transports.
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
```

Additional targeted checks:

```bash
codex mcp list
scripts/smoke_mcp_runtime.sh
scripts/smoke_mcp_capabilities.sh
scripts/smoke_hooks.sh
scripts/smoke_local_git_guard.sh
scripts/smoke_clean_bootstrap.sh
scripts/smoke_fullrepo_sync.sh
scripts/bootstrap_check.sh --apply
scripts/sync_fullrepo_branch.sh --status
python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool
plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool
python3 scripts/validate_instruction_docs.py --require-agent-docs
plugins/rldyour-lsps/scripts/check_lsps.sh
python3 scripts/validate_plugin_versions.py
python3 scripts/validate_skill_routing.py
python3 scripts/release_manifest.py
python3 scripts/check_mcp_runtime_versions.py
scripts/doctor_system_codex.sh
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
- Use `scripts/sync_fullrepo_branch.sh --restore` at initialization when agent-only context is expected, and `scripts/sync_fullrepo_branch.sh --publish` after normal branch push.
- Use `scripts/install_local_git_hooks.sh --repo <project> --apply` to install the branch-aware local pre-push guard in product repositories; it keeps product branches strict and allows AI context only on the configured `fullrepo` branch while still blocking secrets/runtime files.
- Standard finish order is Serena memories and durable docs from verified code, matching checks, atomic normal-branch commit and push, `fullrepo` publish from final `HEAD`, then safe cleanup of merged workflow branches and worktrees.
- Before final delivery, ensure `git status -sb` is clean and pushed when the task produced commits.

## System Install

- `system/AGENTS.md` is the canonical template for the owner's global `~/.codex/AGENTS.md`.
- `scripts/install_system_codex.sh --dry-run` shows what would be installed.
- `scripts/install_system_codex.sh --apply` writes the global AGENTS file, patches rldyour-owned Codex config sections, applies owner-requested YOLO defaults, registers the marketplace, and syncs plugin cache.
- `scripts/doctor_system_codex.sh` verifies the installed system Codex state.
- `scripts/rollback_system_codex.sh --list` lists installer backups; `--restore <backup>` restores backed up `AGENTS.md` and `config.toml`.
- `scripts/collect_diagnostics.sh` writes a local ignored diagnostics bundle for failure triage.
