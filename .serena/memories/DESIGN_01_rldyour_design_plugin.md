<!-- Memory Metadata
Last updated: 2026-05-02
Last commit: dbdd6ca chore(serena): record rules plugin knowledge
Scope: plugins/rldyour-design
Area: DESIGN
-->

# DESIGN_01_rldyour_design_plugin

## Purpose

`plugins/rldyour-design` is a skills-only Codex plugin that routes frontend design work into the rldyour design workflow. It does not define MCP transports directly; Figma, shadcn, Playwright, and Chrome DevTools MCP servers are provided by `plugins/rldyour-mcps`.

## Source Of Truth

- `plugins/rldyour-design/.codex-plugin/plugin.json`: plugin manifest, marketplace-facing descriptions, capabilities, keywords, and default prompts.
- `plugins/rldyour-design/skills/*/SKILL.md`: primary automatic skill trigger surface through YAML frontmatter `description`.
- `plugins/rldyour-design/skills/*/agents/openai.yaml`: UI metadata and `policy.allow_implicit_invocation: true` for every design skill.
- `plugins/rldyour-design/README.md`: trigger map and design workflow overview.

## Entry Points

- `figma-to-code`: Figma MCP source-of-truth workflow for Figma frames, files, nodes, designer layouts, visual references, and pixel-perfect frontend transfer.
- `design-system-implementation`: centralized token and UI-system workflow for CSS variables, Tailwind/shadcn theme config, component variants, typography, colors, spacing, radii, shadows, motion, Figma variables, shadcn/ui, and ReactBits.
- `fsd-frontend-architecture`: strict FSD placement workflow for frontend layers, public APIs, imports, assets, tokens, generated code, and UI architecture cleanup.
- `design-validation`: browser validation workflow for visible frontend changes, screenshots under `browser/`, responsive checks, runtime health, accessibility basics, and interaction/business behavior checks.
- `ry-design`: end-to-end command-style orchestrator for complete design/UI implementation tasks.

## Current Behavior

The plugin is optimized for automatic routing. User-facing conversation stays in Russian, while plugin documentation, code, token files, comments, and commits stay in English.

Figma MCP is treated as the source of truth when Figma context is available. Figma output must be adapted into a centralized design system, strict FSD placement, shadcn/ui primitives, optional ReactBits motion, and browser validation rather than pasted blindly.

The owner selected centralized design tokens as mandatory for meaningful design-system work. Tokens should cover colors, typography, spacing, radii, shadows, motion, and component variants when the project has or needs a design system.

Meaningful visible frontend work is not considered complete without browser evidence or an explicit validation blocker.

## Contracts And Data

Every skill must keep `policy.allow_implicit_invocation: true` in `agents/openai.yaml`.

The strongest automatic trigger fields are the YAML frontmatter `description` values in each `SKILL.md`. Marketplace and UI descriptions should mirror the same intent, but they are not the primary skill trigger contract.

Design screenshots and browser evidence belong under `browser/` and must not be committed unless explicitly requested.

## Invariants

- Keep `rldyour-design` skills-only unless the owner explicitly asks to add MCP servers or hooks.
- Do not store Figma, Context7, GitHub, or other credentials in the plugin.
- Keep design workflow docs in English and user-facing responses in Russian.
- Keep shadcn/ui as the primary UI primitive source and ReactBits as a selective motion/interactive component source.
- Preserve strict FSD layers: `app`, `pages`, `widgets`, `features`, `entities`, `shared`; no `processes`.
- Keep project-specific existing frontend architecture as the source of truth when it is coherent; use FSD as the default for new areas and refactors.

## Change Rules

- When changing automatic behavior, update the relevant `SKILL.md` frontmatter `description` first.
- Keep `README.md`, `plugin.json`, and `agents/openai.yaml` aligned with skill trigger intent.
- Validate skills with `quick_validate.py` after changing `SKILL.md`.
- Re-sync `plugins/rldyour-design/` into the active Codex plugin cache after changing plugin files used by the system Codex runtime.

## Verification

- `jq empty plugins/rldyour-design/.codex-plugin/plugin.json .agents/plugins/marketplace.json`: validates JSON metadata.
- `/opt/homebrew/bin/uv run --with pyyaml python <skill-creator>/scripts/quick_validate.py <skill-dir>`: validates a skill frontmatter file.
- `/opt/homebrew/bin/uv run --with pyyaml python -c '<parse agents/openai.yaml files>'`: validates `agents/openai.yaml` parse and `allow_implicit_invocation`.
- `diff -qr plugins/rldyour-design <codex-plugin-cache>/rldyour-design/local`: verifies system cache matches the repository plugin.
