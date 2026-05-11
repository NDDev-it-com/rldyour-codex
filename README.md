# rldyour-codex

`rldyour-codex` is a personal Codex marketplace. It is not a generic preset, not an automatic configuration takeover, and not a bundle of unrelated third-party opinions. It is a controlled catalog for the owner's own plugins, MCP servers, skills, hooks, rules, and workflows.

Main principle: nothing is treated as enabled or correct unless the owner explicitly decides it.

## Control Model

- The active marketplace contains only plugins that are actually created and ready to install.
- Planned plugins stay documented here and are not added to `marketplace.json` until explicitly created.
- Each plugin must have a clear responsibility boundary.
- Each tool or workflow must describe its purpose, access model, risks, and usage rules.
- Repository documentation is written in English.
- Technical identifiers stay stable and ASCII.
- Every callable rldyour skill must include compact Russian and English trigger phrases in the `SKILL.md` frontmatter `description`; Codex uses descriptions as the primary routing surface, and details belong in the skill body or references.
- Secrets, tokens, cookies, and private keys are never stored in this repository.

## Active Catalog

The active marketplace currently contains:

- `rldyour-mcps`: the owner's approved MCP server set for Codex.
- `rldyour-explore`: research skills for technical MCP research and authoritative web research.
- `rldyour-serena-mcp`: Serena-first semantic code workflow, fact-only `.serena` memory sync, plans, research archive, and lifecycle hooks.
- `rldyour-security`: non-blocking OWASP-oriented secure implementation guidance and `ry-sec-review` security review skill.
- `rldyour-browser`: browser validation and debugging workflows for Playwright MCP and Chrome DevTools MCP.
- `rldyour-design`: Figma-to-code, centralized token-based design system, strict FSD frontend architecture, shadcn/ui, ReactBits, and browser validation workflows.
- `rldyour-lsps`: language-server routing, health checks, brew-first setup profiles, and Serena LSP integration guidance.
- `rldyour-flow`: autonomous SDLC workflows for `ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-deploy`, scoped context packs, context sufficiency gates, instruction docs sync, advisory session/commit hooks, reviewer tracks, and post-task synchronization.
- `rldyour-rules`: quality-first engineering rules, architecture boundaries, implementation discipline, dependency compatibility, verification gates, Codex and Claude Code project instructions, ADR policy, and `ry-rules-review`.

## Planned Plugin Architecture

These plugins are plans only unless listed in the active catalog above.

- `rldyour-mcps`: created. Base MCP servers approved by the owner.
- `rldyour-serena-mcp`: created. Serena-specific workflow layer that depends on the Serena MCP server from `rldyour-mcps`.
- `rldyour-browser`: created. Browser validation, pixel-perfect checks, functional checks, business-logic verification, and runtime debugging through Playwright MCP and Chrome DevTools MCP.
- `rldyour-design`: created. Design implementation workflow through Figma MCP, centralized design tokens, strict FSD, shadcn/ui, ReactBits, and browser evidence.
- `rldyour-lsps`: created. Language-server routing, health checks, brew-first setup profiles, and Serena LSP integration guidance.
- `rldyour-flow`: created. Command-like SDLC skills, deep `ry-init` context packs, `ry-start` context sufficiency gate, reviewer workflows orchestrated by `ry-start`/`ry-review`, instruction docs sync, advisory SessionStart/PostToolUse hooks, and post-task sync hook for Serena/docs/git/GitHub cleanup.
- `rldyour-rules`: created. Hard and advisory rules for quality-first engineering, architecture, dependencies, verification, Codex/Claude project instructions, and ADRs.
- `rldyour-security`: created. Skills-only security guidance, OWASP Top 10 coverage, and defensive review workflow.
- `rldyour-explore`: created. Research workflows through Context7, DeepWiki, Grep by Vercel, and web research.

Resolved architecture decisions:

- No separate `rldyour-hooks` plugin. Hooks live inside the plugin that owns the lifecycle behavior.
- No separate `rldyour-memories` plugin. Project memory behavior belongs to `rldyour-serena-mcp`.
- No `rldyour-sec` alias plugin. Security behavior belongs to `rldyour-security`.

## MCP Skill Strategy

The original idea of one broad `rldyour-mcps-skills` plugin is replaced with a controlled per-domain approach.

Important MCPs can get dedicated plugins:

- one plugin per important MCP or workflow domain;
- separate usage rules for that MCP;
- separate skills and commands;
- separate access limits and safety checks.

This makes behavior easier to understand, disable, test, and evolve.

## What Codex Reads

Codex reads:

- `.agents/plugins/marketplace.json`: active installable plugin catalog;
- `plugins/<plugin>/.codex-plugin/plugin.json`: plugin manifest;
- manifest-linked files such as `skills`, `.mcp.json`, `.app.json`, hooks, and assets.

This README is for owner review and repository orientation. It explains the control model and plugin plan but does not enable tools by itself.

## Adding A Plugin

Before creating a new plugin, define:

- exact plugin name;
- purpose and boundary;
- files it will contain;
- whether it provides MCP servers, skills, hooks, app connectors, scripts, or documentation only;
- what Codex can do through it;
- what actions require confirmation;
- what data must never be sent outside the machine or repository.

Only then create `plugins/<name>/` and add it to `.agents/plugins/marketplace.json`.

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

## System Codex Installation

This repository also stores the canonical global Codex setup for the owner.

Dry-run first:

```bash
scripts/install_system_codex.sh --dry-run
```

Apply to the active Codex home:

```bash
scripts/install_system_codex.sh --apply
```

Verify the installed system state:

```bash
scripts/doctor_system_codex.sh
```

Run the full bootstrap smoke flow on a new or resynced machine:

```bash
scripts/bootstrap_check.sh --apply
```

The installer writes `~/.codex/AGENTS.md`, registers this marketplace, enables the approved plugins, configures the approved MCP servers, enables Codex hooks, writes the official Codex config schema hint, applies the owner-requested YOLO permission defaults, and synchronizes the local plugin cache. Existing `~/.codex/AGENTS.md` and `~/.codex/config.toml` are backed up before write operations. Secrets and OAuth tokens are never written by this repository.

`plugins/rldyour-mcps/.mcp.json` is the portable source of truth for MCP server definitions. The installer resolves portable commands such as `uvx`, `bunx`, and `dart` to local executable paths in `~/.codex/config.toml`; `scripts/validate_marketplace.sh` checks that the installed MCP config still matches `.mcp.json` apart from that expected command-path resolution.

Local MCP launcher packages are pinned in `.mcp.json` and documented in `config/mcp-runtime-versions.env`. Do not use `@latest` or unpinned `uvx --from` package specs for local MCP runtime definitions; update versions intentionally and rerun capability smoke.

System Codex is intentionally configured for unattended owner-controlled execution: `profile = "rldyour-yolo"`, `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`, and `default_permissions = ":danger-no-sandbox"`. This is an owner-required operating mode for trusted machines, not a temporary risk exception.

Runtime smoke checks:

```bash
scripts/smoke_mcp_runtime.sh
scripts/smoke_mcp_capabilities.sh
scripts/smoke_hooks.sh
scripts/smoke_local_git_guard.sh
scripts/smoke_flow_branch_cleanup.sh
scripts/smoke_clean_bootstrap.sh
scripts/smoke_fullrepo_sync.sh
```

`scripts/smoke_mcp_runtime.sh` validates remote MCP endpoints with a Streamable HTTP `initialize` POST preflight. OAuth-gated endpoints may pass with `401`/`403`; a `405` is valid only for optional GET SSE and is not accepted as a POST initialize result.

Instruction docs checks:

```bash
plugins/rldyour-flow/scripts/instruction_docs_state.py --json | python3 -m json.tool
python3 scripts/validate_instruction_docs.py --require-agent-docs
```

`scripts/smoke_mcp_capabilities.sh` verifies MCP protocol behavior with `initialize`, `list_tools`, and safe `call_tool` probes where a deterministic read-only tool exists. It retries each server five times by default to absorb transient remote MCP failures. Figma is skipped by default because it requires OAuth; pass `--include-auth` only after authorizing that runtime.

GitHub Actions runs the same marketplace/system checks on push and pull request with a temporary `CODEX_HOME`, list-only MCP capability probes, and a clean bootstrap clone.

## Fullrepo Branch

`fullrepo` is the portable complete-state branch for agent-only files. Normal project branches should keep product history clean and exclude project-root AI workflow files through `.git/info/exclude`.

In rldyour-managed projects, `AGENTS.md` is the Codex-native project instruction file and `.claude/CLAUDE.md` is the Claude Code-native project memory file. Both are agent-only context: keep them out of normal branch history and publish them through `fullrepo`.

Use:

```bash
scripts/sync_fullrepo_branch.sh --restore
scripts/sync_fullrepo_branch.sh --migrate-main
scripts/sync_fullrepo_branch.sh --publish
scripts/sync_fullrepo_branch.sh --status
```

`--restore` initializes local agent context from `origin/fullrepo`. `--migrate-main` removes tracked agent-only files from the current branch index while keeping them locally. `--publish` builds a snapshot from current `HEAD` plus local agent-only files and pushes it to `fullrepo` with safe `--force-with-lease`.

Local product repositories can install the rldyour Git pre-push guard:

```bash
scripts/install_local_git_hooks.sh --dry-run
scripts/install_local_git_hooks.sh --apply
```

The guard is branch-aware. Product branches keep strict protection against agent-only paths and AI-marker additions. The configured fullrepo branch, `fullrepo` by default or `RLDYOUR_FULLREPO_BRANCH`, allows durable AI context while still blocking definite secrets, runtime markers, browser artifacts, and local env files.

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

- `docs/release-process.md`: versioning, changelog, release evidence, and tag flow.
- `docs/rollback-restore.md`: safe restore from installer backups or older Git tags.
- `docs/dependency-updates.md`: pinned MCP runtime update policy.
- `docs/observability.md`: diagnostics, CI artifacts, and failure triage.

CI validates the repository on Ubuntu and macOS. A scheduled dependency-check workflow monitors pinned MCP runtime versions, and Dependabot tracks GitHub Actions updates.
