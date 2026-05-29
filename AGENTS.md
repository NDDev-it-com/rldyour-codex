# rldyour-codex Agent Instructions

## Purpose

This repository is the Codex-native adapter for `rldyour-ai-cli-tools`: local plugin marketplace, plugin manifests, skills, OpenAI metadata, hooks, managed subagents, MCP source definitions, system installer, runtime doctors, validation gates, and Serena project knowledge.

GitHub: `https://github.com/NDDev-it-com/rldyour-codex`.
License: `AGPL-3.0-or-later`.
Maintainer: Danil Silantyev (`@rldyourmnd`), CEO NDDev.

## Language

- User-facing conversation with the owner is Russian unless explicitly requested otherwise.
- Repository artifacts are English.
- Stable identifiers stay ASCII and kebab-case where applicable.

## Source Of Truth

- `.agents/plugins/marketplace.json`: repo-scoped Codex plugin marketplace.
- `plugins/<plugin>/.codex-plugin/plugin.json`: plugin manifest, version, user-facing marketplace metadata, linked skills/hooks/MCP/apps.
- `plugins/<plugin>/skills/*/SKILL.md`: primary skill routing metadata and workflow body.
- `plugins/<plugin>/skills/*/agents/openai.yaml`: compact OpenAI skill UI/dependency metadata and implicit invocation policy.
- `plugins/rldyour-mcps/.mcp.json`: source MCP runtime definitions; Codex runtime materialization is TOML `[mcp_servers.*]`.
- `config/rldyour-contract.json`: Codex adapter contract, native surfaces, model/runtime policy, hook semantics, and MCP mapping.
- `config/skill-routing-policy.json`: deterministic prompt-to-skill routing fixtures.
- `config/mcp-runtime-versions.env`: pinned local MCP launcher, host runtime, and Codex CLI versions used by scripts.
- `system/AGENTS.md`: compact global Codex instruction template installed to `~/.codex/AGENTS.md`.
- `system/agents/*.toml`: managed Codex subagent roles.
- `system/rules/*.rules`: managed Codex execpolicy rules.
- `VERSION` and `CHANGELOG.md`: marketplace product version and release history.
- `.github/workflows/*.yml`: public adapter CI and release workflows.
- `.serena/memories/*.md`: fullrepo-only durable project knowledge.

## Native Boundaries

- Codex flows are skills/plugins, not custom slash-command files copied from Claude or OpenCode.
- `rldyour-mcps` owns transport definitions only and must not contain skills or behavior policy.
- `rldyour-flow` owns SDLC skills, SessionStart/PreToolUse/Stop lifecycle scripts, instruction docs sync, fullrepo sync, and post-task sync.
- `rldyour-serena-mcp` owns Serena-first code workflow, memory sync, plans/research guidance, and helper scripts. Its Stop work is invoked by Flow, not registered as an independent competing Stop hook.
- `rldyour-rules`, `rldyour-explore`, `rldyour-browser`, `rldyour-design`, `rldyour-lsps`, and `rldyour-security` own their domain workflows and must not duplicate MCP transports.
- Plugin-bundled hooks are discoverable from manifests, but trusted hook hashes must be refreshed by installer/doctor through Codex `hooks/list` before they run.

## Metadata Policy

- First-party `SKILL.md` descriptions are Russian-first with an English suffix.
- `agents/openai.yaml` must use the shared policy in `scripts/codex_openai_metadata_policy.py`:
  - `interface.short_description`: 25-64 chars, Russian-first, English-compatible.
  - `interface.default_prompt`: <=128 chars, Russian-first, English-compatible, and mentions the exact `$<skill-name>`.
  - `dependencies.tools[*].description`: Russian-first, English-compatible, compact.
  - reviewer track skills are orchestrated-only and set `allow_implicit_invocation: false`.
- Plugin manifest user-facing fields are Russian-first with English compatibility: `description`, `interface.shortDescription`, `interface.longDescription`, and `interface.defaultPrompt`.
- Keep metadata compact. Put detailed instructions in skill bodies, references, docs, or Serena memories.

## Permission And Runtime Policy

- Owner-standard mode is full-auto/YOLO: `approval_policy = "never"` plus `sandbox_mode = "danger-full-access"`.
- Safe mode is explicit only through `scripts/install_system_codex.sh --apply --safe-mode`.
- Do not mix beta permission profiles (`default_permissions` or `[permissions]`) with legacy `sandbox_mode` in the same active config layer.
- Required Codex features are `hooks = true` and `multi_agent = true`.
- Parent owner profile uses `gpt-5.5` with `model_reasoning_effort = "xhigh"`.
- Managed subagents use `gpt-5.5` with `model_reasoning_effort = "medium"` unless the owner explicitly changes policy.
- Removed/deprecated config aliases such as `plugin_hooks`, `codex_hooks`, legacy profile selectors, legacy web-search flags, and active `default_permissions` with `sandbox_mode` must not appear.

## Development Rules

- Use `apply_patch` for manual edits.
- Do not commit secrets, tokens, cookies, private keys, raw credentials, browser evidence, caches, or Serena runtime markers.
- Use repo-local patterns and validators; avoid parallel hardcoded plugin/MCP lists.
- Use Serena-first inspection where supported; use `rg` and direct reads for docs, JSON, shell, TOML, YAML, and generated metadata.
- After meaningful behavior/config/workflow/release changes, sync `.serena/memories` with verified facts only.
- Keep `system/AGENTS.md` and this `AGENTS.md` compact. The combined standard Codex instruction pair must stay comfortably below the default project-doc cap.

## Validation

Run the marketplace gate before finalizing adapter changes:

```bash
scripts/validate_marketplace.sh
```

Targeted checks:

```bash
python3 scripts/codex_openai_metadata_policy.py --repo-root .
python3 scripts/validate_agent_tools.py
python3 scripts/validate_plugin_versions.py
python3 scripts/validate_contract.py
python3 scripts/validate_skill_routing.py
python3 scripts/validate_instruction_docs.py --require-agent-docs
python3 scripts/check_serena_memory_freshness.py
scripts/validate_fast.sh
scripts/validate_runtime.sh --strict-runtime
scripts/validate_release.sh
scripts/validate_execpolicy_rules.sh
uv run --with pytest --with pytest-cov --with pyyaml python -m pytest
```

Runtime/doctor checks when the installed Codex environment is in scope:

```bash
scripts/install_system_codex.sh --dry-run
scripts/install_system_codex.sh --apply
scripts/doctor_system_codex.sh --quick --strict-runtime
scripts/smoke_mcp_runtime.sh
scripts/smoke_mcp_capabilities.sh
python3 scripts/smoke_codex_hook_listing.py
scripts/smoke_hooks.sh
scripts/smoke_codex_hooks_migration.sh
scripts/smoke_serena_memory_freshness.sh
scripts/smoke_serena_memory_taxonomy.sh
scripts/smoke_fullrepo_sync.sh
scripts/smoke_fullrepo_bootstrap_init.sh
```

## Git And Fullrepo

- Prefer atomic Conventional Commits.
- Split unrelated implementation, validators/tests, docs/instructions, release metadata, generated artifacts, and Serena/fullrepo sync when independently reviewable.
- Keep `main` focused on product source. This repository intentionally tracks `system/AGENTS.md` as a product template; project-root `AGENTS.md`, `.claude/CLAUDE.md`, `.serena`, `.codex`, `.cursor/rules`, and similar agent-only context live on `fullrepo`.
- Use `scripts/sync_fullrepo_branch.sh --bootstrap-init` when restoring agent-only context and `scripts/sync_fullrepo_branch.sh --publish` after normal branch sync.
- Do not force-push `main`. Do not rewrite already-pushed history without explicit owner approval.
- Before final delivery, ensure normal branch status is clean, pushed if required, and `fullrepo` is published when agent-only context changed.

## Release

- Default version movement is patch. Minor/major releases require explicit owner direction.
- Plugin manifest versions must match `VERSION`.
- Release evidence lives in `VERSION`, `CHANGELOG.md`, `docs/release-process.md`, `docs/rollback-restore.md`, `docs/dependency-updates.md`, `docs/observability.md`, release workflow outputs, and generated release manifests/SBOM.
- Do not call a release production-ready while `scripts/validate_marketplace.sh` or the root control-plane release gate fails.
