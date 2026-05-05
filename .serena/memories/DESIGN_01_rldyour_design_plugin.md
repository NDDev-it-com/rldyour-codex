<!-- Memory Metadata
Last updated: 2026-05-05
Last commit: 14f70e0 fix(flow): make local git guard fullrepo-aware
Scope: plugins/rldyour-design
Area: DESIGN
-->

# DESIGN_01_rldyour_design_plugin

## Purpose

Keep the operational routing contract for design work: when to use each design skill, what tools are in scope, and what source-of-truth files drive behavior.

## Source-of-Truth

- `plugins/rldyour-design/.codex-plugin/plugin.json`
- `plugins/rldyour-design/README.md`
- `plugins/rldyour-design/skills/*/SKILL.md`
- `plugins/rldyour-design/skills/*/agents/openai.yaml`

## Skills and Routing

- `figma-to-code`: use when Figma frames, nodes, or design handoff is the direct source.
- `design-system-implementation`: use for centralized tokens/theme/systematic variants and shadcn/ui/ReactBits choices.
- `fsd-frontend-architecture`: use when placement, public APIs, imports, or feature boundaries need correction.
- `design-validation`: use for browser-visible proof after implementation.
- `ry-design`: use for end-to-end design tasks that span these steps.

## Boundaries

- `rldyour-design` is skills-only and does not configure MCP servers or hooks.
- MCP tools used are supplied by `rldyour-mcps` (`figma`, `shadcn`, `playwright`, `chrome-devtools`).
- Figma is treated as source-of-truth input for design intent and assets; output is adapted into the project's architecture.
- Centralized tokens and strict FSD layers (`app`, `pages`, `widgets`, `features`, `entities`, `shared`) are default rules unless the project already has a coherent alternative.
- Meaningful frontend output should be browser-validated.

## Invariants

- Keep `allow_implicit_invocation: true` for design skills unless governance changes.
- Do not keep generated binary artifacts in commits; keep browser artifacts under `browser/`.
- Do not claim ReactBits or shadcn usage beyond current project constraints.
- Keep comments factual and avoid speculative TODOs in memory/docs.

## Verification

- `scripts/validate_marketplace.sh`
- `jq empty plugins/rldyour-design/.codex-plugin/plugin.json`
- `uv run --with pyyaml python ${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py plugins/rldyour-design/skills/<skill-dir>` (when available)
- `diff -qr plugins/rldyour-design ${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/rldyour-design/local`
