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
- Secrets, tokens, cookies, and private keys are never stored in this repository.

## Active Catalog

The active marketplace currently contains:

- `rldyour-mcps`: the owner's approved MCP server set for Codex.
- `rldyour-explore`: research skills for technical MCP research and authoritative web research.
- `rldyour-serena-mcp`: Serena-first semantic code workflow, fact-only `.serena` memory sync, plans, research archive, and lifecycle hooks.

## Planned Plugin Architecture

These plugins are plans only unless listed in the active catalog above.

- `rldyour-mcps`: created. Base MCP servers approved by the owner.
- `rldyour-serena-mcp`: created. Serena-specific workflow layer that depends on the Serena MCP server from `rldyour-mcps`.
- `rldyour-lsps`: language-server configuration for navigation, diagnostics, and analysis when separate LSP setup is needed.
- `rldyour-rules`: hard rules for project work, coding standards, verification, and system `AGENTS.md`.
- `rldyour-flow`: command-like skills such as `ry-start`, `ry-init`, `ry-newp`, `ry-review`, and `ry-deploy`.
- `rldyour-memories`: future memory policies if project memory behavior grows beyond the Serena-specific plugin.
- `rldyour-hooks`: general Codex hooks and trigger policies that are not specific to Serena.
- `rldyour-sec`: security rules, secure coding, checks, and OWASP Top 10 coverage.
- `rldyour-explore`: created. Research workflows through Context7, DeepWiki, Grep by Vercel, and web research.

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

After changing `marketplace.json`, a plugin manifest, hooks, skills, or `.mcp.json`, start a new Codex session so the runtime reloads the configuration.
