# rldyour-codex

[![validate](https://github.com/NDDev-it-com/rldyour-codex/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/NDDev-it-com/rldyour-codex/actions/workflows/validate.yml)
[![security-static](https://github.com/NDDev-it-com/rldyour-codex/actions/workflows/security-static.yml/badge.svg?branch=main)](https://github.com/NDDev-it-com/rldyour-codex/actions/workflows/security-static.yml)
[![CodeQL](https://github.com/NDDev-it-com/rldyour-codex/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/NDDev-it-com/rldyour-codex/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/NDDev-it-com/rldyour-codex/badge)](https://scorecard.dev/viewer/?uri=github.com/NDDev-it-com/rldyour-codex)
[![License: AGPL-3.0-or-later](https://img.shields.io/badge/License-AGPL--3.0--or--later-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/NDDev-it-com/rldyour-codex)](https://github.com/NDDev-it-com/rldyour-codex/releases/latest)

`rldyour-codex` is a rldyour AI CLI configuration for Codex: plugin marketplace, system install, MCP servers, hooks, managed agents, runtime validation, and Serena memory. It is maintained by Danil Silantyev (github:rldyourmnd), CEO NDDev and owns rldyour plugins, MCP server runtime definitions, skills, Codex lifecycle hooks, managed subagent role configs, execpolicy rules, validation scripts, installer/rollback tooling, CI checks, and Serena project knowledge.

It is not a generic preset, not an automatic configuration takeover, and not a bundle of unrelated third-party opinions. It is a controlled catalog where nothing is treated as enabled or correct unless explicitly decided by the maintainer.

## License

This project is licensed under the GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later). See [LICENSE](LICENSE) for the full text.

AGPL-3.0 includes a Remote Network Interaction clause (Section 13): if you run a modified version of this software and make it available to others over a network, you must offer them access to the corresponding source code under the same license. Operating the unmodified upstream release does not trigger additional obligations beyond the standard AGPL-3.0 terms.

## Control Model

- The active marketplace contains only plugins that are actually created and ready to install.
- Planned plugins stay documented here and are not added to `marketplace.json` until explicitly created.
- Each plugin has a clear responsibility boundary.
- Each tool or workflow describes its purpose, access model, risks, and usage rules.
- Repository artifacts are written in English; technical identifiers stay stable and ASCII.
- Every callable rldyour skill includes compact Russian and English trigger phrases in the `SKILL.md` frontmatter `description`; Codex uses descriptions as the primary routing surface, and details belong in the skill body or references.
- Secrets, tokens, cookies, and private keys are never stored in this repository.

## Active Catalog

The active marketplace currently contains:

- `rldyour-mcps`: the maintainer's approved MCP server set for Codex.
- `rldyour-explore`: research skills for technical MCP research and authoritative web research.
- `rldyour-serena-mcp`: Serena-first semantic code workflow, fact-only `.serena` memory sync, plans, research archive, and lifecycle hooks.
- `rldyour-security`: non-blocking OWASP-oriented secure implementation guidance and `ry-sec-review` security review skill.
- `rldyour-browser`: browser validation and debugging workflows for Playwright MCP and Chrome DevTools MCP.
- `rldyour-design`: Figma-to-code, centralized i18n, dynamic/static content classification, token-based design system, reusable UI kit, strict FSD frontend architecture, shadcn/ui, ReactBits, and browser validation gates.
- `rldyour-lsps`: language-server routing, health checks, brew-first setup profiles, and Serena LSP integration guidance.
- `rldyour-flow`: autonomous SDLC workflows for `ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-repair`, `ry-deploy`, scoped context packs, context sufficiency gates, instruction docs sync, fast offline SessionStart worktree bootstrap/context dispatcher hooks, cwd-safe PreToolUse guardrails, advisory commit hooks, reviewer tracks, and post-task synchronization.
- `rldyour-rules`: quality-first engineering rules, architecture boundaries, implementation discipline, dependency compatibility, verification gates, Codex and Claude Code project instructions, ADR policy, and `ry-rules-review`.

Resolved architecture decisions:

- No separate `rldyour-hooks` plugin. Hooks live inside the plugin that owns the lifecycle behavior.
- No separate `rldyour-memories` plugin. Project memory behavior belongs to `rldyour-serena-mcp`.
- No `rldyour-sec` alias plugin. Security behavior belongs to `rldyour-security`.

## What Codex Reads

Codex reads:

- `.agents/plugins/marketplace.json`: active installable plugin catalog;
- `plugins/<plugin>/.codex-plugin/plugin.json`: plugin manifest;
- manifest-linked files such as `skills`, `.mcp.json`, hooks, and assets.

## Local Installation

```bash
codex plugin marketplace add .
```

After changing `marketplace.json`, a plugin manifest, hooks, skills, or `.mcp.json`, apply the system install workflow and start a new Codex session so the runtime reloads the configuration:

```bash
scripts/install_system_codex.sh --dry-run
scripts/install_system_codex.sh --apply
scripts/doctor_system_codex.sh
```

The default install posture is owner-standard full-auto:
`~/.codex/config.toml` receives the active owner defaults, and
`~/.codex/rldyour-yolo.config.toml` is the explicit `--profile rldyour-yolo`
layer with `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`,
using Codex's legacy sandbox dialect. It does not write an active
`default_permissions` permission-profile field while `sandbox_mode` is present.
The optional conservative override is explicit:

```bash
scripts/install_system_codex.sh --apply --safe-mode
scripts/doctor_system_codex.sh --safe-mode
```

## System Codex Installation

This repository also stores the canonical global Codex setup for the maintainer.

Dry-run first:

```bash
scripts/install_system_codex.sh --dry-run
```

Apply to the active Codex home:

```bash
scripts/install_system_codex.sh --apply
```

Apply the owner-standard full-access profile:

```bash
scripts/install_system_codex.sh --apply
```

Verify the installed system state:

```bash
scripts/doctor_system_codex.sh
scripts/doctor_system_codex.sh --quick --strict-runtime
scripts/doctor_system_codex.sh --safe-mode
```

Run the full bootstrap smoke flow on a new or resynced machine:

```bash
scripts/bootstrap_check.sh --apply
```

The installer writes `~/.codex/AGENTS.md`, managed `~/.codex/agents/*.toml` subagent role configs, installs managed Codex execpolicy rules from `system/rules/*.rules`, registers this marketplace, enables the approved plugins, configures the approved MCP servers, enables Codex hooks and multi-agent support, writes the official Codex config schema hint, applies the owner-standard full-auto permission defaults unless `--safe-mode` is supplied, writes `~/.codex/rldyour-yolo.config.toml` and `~/.codex/rldyour-safe.config.toml` profile layers for current Codex `--profile` semantics, sets the maintainer-selected parent and subagent model defaults, writes approved MCP tool overrides, and synchronizes the versioned local plugin cache at `~/.codex/plugins/cache/rldyour-codex/<plugin>/<version>`. Existing `~/.codex/AGENTS.md`, managed subagent configs, managed rule files, `~/.codex/config.toml`, and managed profile files are backed up before write operations. Credentials and OAuth tokens are never written by this repository.

The Codex adapter contract lives in `config/rldyour-contract.json` and is documented in `docs/contract-matrix.md`. It records the intended Codex surface: 9 plugins, 39 skills, no slash commands by design, 8 managed subagents, command-only plugin hook lifecycle mappings, versioned plugin cache layout, and the owner-standard full-auto profile boundary. Validate it with `python3 scripts/validate_contract.py`.

`plugins/rldyour-mcps/.mcp.json` is the portable source of truth for MCP server definitions. The installer resolves portable commands such as `uvx`, `bunx`, and `dart` to local executable paths in `~/.codex/config.toml`; `scripts/validate_marketplace.sh` checks that the installed MCP config still matches `.mcp.json` apart from that expected command-path resolution.

Local MCP launcher packages are pinned in `.mcp.json` and mirrored in `config/mcp-runtime-versions.env`; marketplace validation fails if these sources drift. Do not use `@latest` or unpinned `uvx --from` package specs for local MCP runtime definitions; update versions intentionally and rerun capability smoke. The official GitHub MCP server binary is pinned separately as `GITHUB_MCP_SERVER_VERSION` and installed by CI from the matching upstream release artifact with checksum verification.

`dart-flutter` is intentionally declared as an external local Dart SDK runtime in `config/mcp-runtime-versions.env`; all other local package launchers remain package-pinned or binary-release-pinned. Host runtime pins for Node major, Bun, Dart SDK, and GitHub MCP also live in this file so local setup, GitHub Actions, and the devcontainer share one source of truth. GitHub Actions workflows pin external actions to full commit SHAs, with the source tag kept as an inline comment for review.

Strict runtime mode is available when the environment must be fully reproducible instead of warning-only:

```bash
scripts/install_system_codex.sh --apply --strict-runtime
scripts/install_system_codex.sh --apply --safe-mode --strict-runtime
scripts/doctor_system_codex.sh --strict-runtime
scripts/doctor_system_codex.sh --safe-mode --strict-runtime
python3 scripts/validate_runtime_prereqs.py --strict --require-codex
```

System Codex installs owner-standard full-auto defaults:
`approval_policy = "never"`, `sandbox_mode = "danger-full-access"`,
`model = "gpt-5.5"`, and `model_reasoning_effort = "xhigh"`. The same values
are also written to
`~/.codex/rldyour-yolo.config.toml` for current Codex `--profile rldyour-yolo`
startup. The optional conservative override is available through `--safe-mode`,
which writes `~/.codex/rldyour-safe.config.toml` with
`approval_policy = "on-request"` and `sandbox_mode = "workspace-write"`.
Current Codex documentation treats
`sandbox_mode` as the active older sandbox model when it is present, so this
repository does not write active `default_permissions` permission-profile fields
or migrate the owner full-auto profile to Codex permission profiles without an
explicit policy decision. Managed subagent roles in
`system/agents/*.toml` install to `~/.codex/agents/*.toml` and use
`model = "gpt-5.5"` with `model_reasoning_effort = "medium"`.

Managed subagents currently include a temporary MCP isolation policy because Codex can eagerly initialize MCP servers per spawned session/subagent. Subagents keep the lightweight core surface available through inherited runtime configuration: `sequential-thinking`, `serena`, `context7`, `grep`, `deepwiki`, `openaiDeveloperDocs`, and built-in `codex_apps`. Specialist MCP servers such as `semgrep`, `figma`, `playwright`, `chrome-devtools`, `dart-flutter`, and `shadcn` are explicitly disabled inside managed subagents and remain parent-session tools for explicit security, design, browser, Flutter, or shadcn work.

Managed execpolicy rules in `system/rules/*.rules` install to `~/.codex/rules/` and are validated with `codex execpolicy check`. They add hard rails for root deletion, direct forced Git pushes, secret-key disclosure, and release/deploy side effects without changing the maintainer-required permission defaults.

Runtime smoke checks:

```bash
scripts/validate_fast.sh
scripts/validate_runtime.sh --strict-runtime
scripts/validate_release.sh
scripts/validate_execpolicy_rules.sh
scripts/smoke_mcp_runtime.sh
scripts/smoke_mcp_capabilities.sh
scripts/smoke_hooks.sh
scripts/smoke_serena_memory_freshness.sh
scripts/smoke_serena_memory_taxonomy.sh
scripts/smoke_local_git_guard.sh
scripts/smoke_flow_branch_cleanup.sh
scripts/smoke_clean_bootstrap.sh
scripts/smoke_fullrepo_sync.sh
python3 scripts/validate_agent_tools.py
```

`scripts/smoke_mcp_runtime.sh` validates remote MCP endpoints with a Streamable HTTP `initialize` POST preflight. OAuth-gated endpoints may pass with `401`/`403`; a `405` is valid only for optional GET SSE and is not accepted as a POST initialize result.

Instruction docs checks:

```bash
plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool
python3 scripts/validate_instruction_docs.py --require-agent-docs
```

`scripts/smoke_mcp_capabilities.sh` verifies MCP protocol behavior with `initialize`, `list_tools`, and safe `call_tool` probes where a deterministic read-only tool exists. It retries each server five times by default to absorb transient remote MCP failures. Figma is skipped by default because it requires OAuth; pass `--include-auth` only after authorizing that runtime.

## Continuous Integration

GitHub Actions run automatically on this public repository:

- `validate.yml`: on every push to `main` and every pull request targeting `main`, runs fast validation on Ubuntu and macOS, runtime smoke on Ubuntu and macOS, release dry-run, MCP runtime pin freshness, and MCP safe-call smoke. `workflow_dispatch` is available for narrower scopes.
- `security-static.yml`: on push to `main`, pull requests, and weekly schedule, runs action pin validation, actionlint, repository text security scan, ShellCheck, Pyright, and Semgrep CLI without paid GitHub Code Security.
- `codeql.yml`: on push to `main`, pull requests, and weekly schedule, runs GitHub CodeQL analysis with `security-and-quality` queries for Python and GitHub Actions.
- `dependency-check.yml`: on daily schedule and on push to MCP runtime pin sources, checks pinned MCP runtime versions through `scripts/check_mcp_runtime_versions.py --fail-on-outdated`. Surfaces stale pins as a maintainer-visible signal without blocking pull requests.
- `release.yml`: on push of a SemVer tag matching `X.Y.Z[-pre]`, validates `VERSION` and `CHANGELOG.md`, builds a deterministic bundle, generates a release manifest and SPDX 2.3 SBOM, exports the GitHub dependency-graph SBOM when available, attaches artifact attestations, and publishes the GitHub Release. `workflow_dispatch` remains available as a fallback.
- `scorecard.yml`: weekly OSSF Scorecard analysis, also on push to `main` and branch protection rule changes. Uploads SARIF to the GitHub Security tab and publishes results to `scorecard.dev`.
- `dependency-review.yml`: on pull requests, blocks merges that introduce dependencies with known high-severity vulnerabilities or licenses outside the allow-list (AGPL-3.0-or-later compatible).
- `labeler.yml`: on pull requests, applies area labels (ci-cd / scripts / plugin / docs / tests / release / security) based on changed paths defined in `.github/labeler.yml`.

All external GitHub Actions are pinned by full commit SHA, with the human-readable tag kept as an inline comment. Pin enforcement is checked by `scripts/validate_action_pins.py` and gated in CI.

## Fullrepo Branch

`fullrepo` is the portable complete-state branch for agent-only files. Normal project branches keep product history clean and exclude project-root AI workflow files through `.git/info/exclude`.

In rldyour-managed projects, `AGENTS.md` is the Codex-native project instruction file and `.claude/CLAUDE.md` is the Claude Code-native project memory file. Both are agent-only context: keep them out of normal branch history and publish them through `fullrepo`.

Use:

```bash
scripts/worktree_add.sh <branch> [path]
scripts/sync_fullrepo_branch.sh --restore
scripts/sync_fullrepo_branch.sh --migrate-main
scripts/sync_fullrepo_branch.sh --publish
scripts/sync_fullrepo_branch.sh --status
```

`scripts/worktree_add.sh` creates a git worktree and runs `fullrepo_sync.py --restore` so parallel Codex sessions start with agent-only context. `--restore` initializes local agent context from `origin/fullrepo`. `--migrate-main` removes tracked agent-only files from the current branch index while keeping them locally. `--publish` builds a snapshot from current `HEAD` plus local agent-only files and pushes it to `fullrepo` with safe `--force-with-lease`.

Local product repositories can install the rldyour Git pre-push guard:

```bash
scripts/install_local_git_hooks.sh --dry-run
scripts/install_local_git_hooks.sh --apply
```

The guard is branch-aware. Product branches keep strict protection against agent-only paths and AI-marker additions. The configured fullrepo branch, `fullrepo` by default or `RLDYOUR_FULLREPO_BRANCH`, allows durable AI context while still blocking definite credentials, runtime markers, browser artifacts, and local env files.

## Release, Rollback, And Observability

Marketplace release version is stored in `VERSION`. Plugin behavior versions stay in `plugins/<plugin>/.codex-plugin/plugin.json`. Release notes live in `CHANGELOG.md`.

Operational workflows:

```bash
python3 scripts/release_manifest.py
python3 scripts/check_mcp_runtime_versions.py
scripts/rollback_system_codex.sh --list
scripts/collect_diagnostics.sh
```

Reference documents:

- [docs/release-process.md](docs/release-process.md): versioning, changelog, release evidence, and tag flow.
- [docs/rollback-restore.md](docs/rollback-restore.md): safe restore from installer backups or older Git tags.
- [docs/dependency-updates.md](docs/dependency-updates.md): pinned MCP runtime update policy.
- [docs/observability.md](docs/observability.md): diagnostics, CI artifacts, and failure triage.
- [docs/github-branch-protection.md](docs/github-branch-protection.md): desired branch protection state.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, validation, change rules, and pull request expectations. Participants are expected to follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

See [SECURITY.md](SECURITY.md) for supported surface, private disclosure procedure, and baseline controls.

## Maintainer

Danil Silantyev (github:rldyourmnd), CEO NDDev.

## Copyright

Copyright (C) 2026 Danil Silantyev (github:rldyourmnd), CEO NDDev.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
