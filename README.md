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
- `rldyour-flow`: autonomous SDLC workflows for `ry-init`, `ry-start`, `ry-newp`, `ry-review`, `ry-deploy`, scoped context packs, context sufficiency gates, advisory session/commit hooks, reviewer tracks, and post-task synchronization.
- `rldyour-rules`: quality-first engineering rules, architecture boundaries, implementation discipline, dependency compatibility, verification gates, project instructions, ADR policy, and `ry-rules-review`.

## Planned Plugin Architecture

These plugins are plans only unless listed in the active catalog above.

- `rldyour-mcps`: created. Base MCP servers approved by the owner.
- `rldyour-serena-mcp`: created. Serena-specific workflow layer that depends on the Serena MCP server from `rldyour-mcps`.
- `rldyour-browser`: created. Browser validation, pixel-perfect checks, functional checks, business-logic verification, and runtime debugging through Playwright MCP and Chrome DevTools MCP.
- `rldyour-design`: created. Design implementation workflow through Figma MCP, centralized design tokens, strict FSD, shadcn/ui, ReactBits, and browser evidence.
- `rldyour-lsps`: created. Language-server routing, health checks, brew-first setup profiles, and Serena LSP integration guidance.
- `rldyour-flow`: created. Command-like SDLC skills, deep `ry-init` context packs, `ry-start` context sufficiency gate, reviewer workflows orchestrated by `ry-start`/`ry-review`, advisory SessionStart/PostToolUse hooks, and post-task sync hook for Serena/docs/git/GitHub cleanup.
- `rldyour-rules`: created. Hard and advisory rules for quality-first engineering, architecture, dependencies, verification, project instructions, and ADRs.
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

The installer writes `~/.codex/AGENTS.md`, registers this marketplace, enables the approved plugins, configures the approved MCP servers, enables Codex hooks, applies the owner-requested YOLO permission defaults, and synchronizes the local plugin cache. Existing `~/.codex/AGENTS.md` and `~/.codex/config.toml` are backed up before write operations. Secrets and OAuth tokens are never written by this repository.

`plugins/rldyour-mcps/.mcp.json` is the portable source of truth for MCP server definitions. The installer resolves portable commands such as `uvx`, `bunx`, and `dart` to local executable paths in `~/.codex/config.toml`; `scripts/validate_marketplace.sh` checks that the installed MCP config still matches `.mcp.json` apart from that expected command-path resolution.

System Codex is intentionally configured for unattended owner-controlled execution: `profile = "rldyour-yolo"`, `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`, and `default_permissions = ":danger-no-sandbox"`. This mirrors the current Codex full-access behavior and should be used only on the owner's trusted machines.
