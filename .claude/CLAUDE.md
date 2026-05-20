# rldyour-codex Claude Code Memory

## Project Purpose

This repository is the maintainer's personal Codex marketplace and system setup source, published publicly under the GNU AGPL-3.0-or-later license at https://github.com/NDDev-it-com/rldyour-codex. Maintainer: Danil Silantyev (`@rldyourmnd`), CEO of NDDev. It owns rldyour plugins, skills, hooks, MCP runtime definitions, validation scripts, installer/rollback tooling, CI checks, and Serena project knowledge.

## License

- All code, configs, scripts, and tests are licensed under GNU AGPL-3.0-or-later. Canonical FSF text in `LICENSE`.
- AGPL-3.0 Section 13 (Remote Network Interaction) applies to modified versions served over a network.
- Contributions are accepted under the same license (inbound = outbound).

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
- `config/mcp-runtime-versions.env`: pinned MCP package, host runtime, and Codex CLI versions.
- `plugins/rldyour-flow/hooks.json`: Codex flow lifecycle hooks.
- `plugins/rldyour-serena-mcp/hooks.json`: Serena reminder and marker hooks; its Stop memory gate is invoked by Flow's ordered lifecycle dispatcher.
- `system/AGENTS.md`: canonical global Codex instructions installed to `~/.codex/AGENTS.md`.
- `system/agents/*.toml`: managed Codex custom subagent role configs installed to `~/.codex/agents/*.toml`, with temporary specialist-MCP isolation for spawned subagents. Disabled specialist MCP overrides must include full `command` or `url` transport metadata copied from `plugins/rldyour-mcps/.mcp.json`; built-in `codex_apps` stays inherited from Apps/connectors and must not be declared as a synthetic `[mcp_servers.codex_apps]` table.
- `system/rules/*.rules`: managed Codex execpolicy rules installed to `~/.codex/rules/*.rules`.
- `.github/workflows/*.yml`: auto-running CI/CD. `validate.yml` on push/PR/dispatch (macOS parity automatic). `security-static.yml` on push/PR/weekly schedule. `codeql.yml` on push/PR/weekly schedule with security-and-quality queries. `release.yml` on SemVer tag push and workflow_dispatch. `dependency-check.yml` on daily schedule and push to MCP pin sources. `scorecard.yml` OSSF Scorecard on push/weekly/branch-protection-rule. `dependency-review.yml` blocks PRs with high-severity deps or non-allow-list licenses. `labeler.yml` auto-labels PRs from `.github/labeler.yml`.
- `.github/branch-protection/main.json`: desired branch protection state for the public `main` branch; applied to the live repository (9 required status checks, strict, linear history, no force-push/delete).
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
- `rldyour-serena-mcp` owns Serena-first code workflow and memory sync. Its Stop script is an ordered child of the Flow lifecycle dispatcher, not a competing plugin Stop hook.
- `rldyour-flow` owns `ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-deploy`, fast offline/local-only SessionStart dispatch, cwd-safe PreToolUse guardrails, ordered local-only Stop lifecycle dispatch, instruction docs sync, post-task sync, and fullrepo sync orchestration.
- `rldyour-rules` owns quality, architecture, dependency, verification, project-instruction, agent-only file, and ADR policy.
- `rldyour-design` owns Figma-to-code, centralized i18n, dynamic/static/admin content classification, centralized tokens, UI-kit reuse, strict FSD placement, shadcn/ui, ReactBits, and browser/design validation gates.
- Other domain plugins own their workflows: explore, browser, security, and LSP.

## Validation Commands

Run the marketplace validation script before finalizing tracked source changes:

```bash
scripts/validate_marketplace.sh
scripts/validate_fast.sh
scripts/validate_runtime.sh --strict-runtime
scripts/validate_release.sh
scripts/validate_execpolicy_rules.sh
```

Targeted checks:

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
scripts/bootstrap_check.sh --apply
scripts/sync_fullrepo_branch.sh --bootstrap-init
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool
plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool
python3 scripts/validate_instruction_docs.py --require-agent-docs
python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool
python3 scripts/check_serena_memory_freshness.py
python3 scripts/validate_agent_tools.py
python3 scripts/validate_action_pins.py
python3 scripts/scan_text_security.py
uv run --with pytest --with pytest-cov --with pyyaml python -m pytest
python3 scripts/validate_plugin_versions.py
python3 scripts/validate_skill_routing.py
python3 scripts/release_sbom.py
python3 scripts/check_mcp_runtime_versions.py
python3 scripts/validate_runtime_prereqs.py --strict --require-codex
scripts/validate_execpolicy_rules.sh
scripts/doctor_system_codex.sh
scripts/doctor_system_codex.sh --quick --strict-runtime
```

## Git And Fullrepo

- Keep `main` synchronized with `origin/main` unless an explicit branch/worktree workflow is active.
- Normal branches should not track agent-only files such as `AGENTS.md`, `.claude/CLAUDE.md`, `REVIEW.md`, `.serena`, `.codex`, `.cursor/rules`, or `.agents/skills`.
- Bootstrap agent-only files at initialization with `scripts/sync_fullrepo_branch.sh --bootstrap-init`; it restores existing `fullrepo`, publishes local agent-only files when no `fullrepo` exists, installs excludes, and removes tracked agent-only files from the current branch index when migration is needed. Use `scripts/worktree_add.sh <branch> [path]` for parallel Codex worktrees that should immediately restore agent-only context from `fullrepo`.
- Publish agent-only files after normal branch sync with `scripts/sync_fullrepo_branch.sh --publish`.
- Install the local branch-aware pre-push guard in product repositories with `scripts/install_local_git_hooks.sh --repo <project> --apply`; it blocks agent-only files on product branches and permits them only on the configured fullrepo branch while keeping secret/runtime protection active.
- Treat `branch_cleanup_state` from `plugins/rldyour-flow/scripts/flow_post_task_state.py` as a finish gate: merged local/remote workflow branches and merged workflow worktrees must be cleaned or explicitly reported as blockers before final delivery.
- Treat bootstrap-only untracked `.serena` files created by tool startup, such as `.serena/project.yml` plus runtime markers, as non-work; they must not force a Stop-hook post-task sync loop.
- Standard finish order: Serena memories, `AGENTS.md` and `.claude/CLAUDE.md`, checks, atomic normal-branch commits, push, `fullrepo` publish, safe cleanup.

## System Install

- `scripts/install_system_codex.sh --dry-run` previews the system Codex install.
- `scripts/install_system_codex.sh --apply` installs global Codex instructions, managed `~/.codex/agents/*.toml`, managed `~/.codex/rules/*.rules`, config sections, the official Codex config schema hint, `[features].hooks = true`, `[features].plugin_hooks = true`, `[features].multi_agent = true`, deprecated hook alias removal, marketplace-derived rldyour plugin enablement, `.mcp.json`-derived MCP registration, YOLO/model defaults, approved MCP tool overrides, marketplace registration, versioned plugin cache under `~/.codex/plugins/cache/rldyour-codex/<plugin>/<version>`, and trusted hashes for installed rldyour plugin hooks. Add `--strict-runtime` when enabled MCP launchers must be present.
- `config/rldyour-contract.json` and `docs/contract-matrix.md` define the Codex adapter surface: 9 plugins, 38 skills, 0 slash commands by design, 8 managed subagents, command-only plugin hook lifecycle mappings, 12 MCP servers, versioned plugin cache, and owner-local-only YOLO boundaries. Validate with `python3 scripts/validate_contract.py`.
- `scripts/doctor_system_codex.sh` verifies installed state, including marketplace-derived rldyour plugin enablement, `.mcp.json`-derived MCP registration, the config schema hint, active `hooks`, `plugin_hooks`, and `multi_agent` features, managed subagent config parity, managed execpolicy rule parity, managed subagent `gpt-5.5`/`medium` settings, managed subagent temporary MCP isolation with complete disabled transport metadata, installed rldyour plugin hook trust/enabled state, and absence of deprecated hook aliases. Use `--quick --strict-runtime` for bounded strict runtime validation.
- `scripts/rollback_system_codex.sh --list` and `--restore <backup>` manage installer backups for `AGENTS.md`, `config.toml`, managed `agents/*.toml`, and managed `rules/*.rules`.
- `scripts/collect_diagnostics.sh` writes ignored diagnostics bundles for failure triage.
