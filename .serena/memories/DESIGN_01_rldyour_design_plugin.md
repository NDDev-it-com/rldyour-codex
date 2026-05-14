<!-- Memory Metadata
Last updated: 2026-05-14
Last commit: f3f2385 feat(design): add Figma delivery quality gates
Scope: plugins/rldyour-design, config/skill-routing-policy.json, README.md, system/AGENTS.md, AGENTS.md, .claude/CLAUDE.md
Area: DESIGN
-->

# DESIGN_01_rldyour_design_plugin

## Purpose

Keep the operational routing contract for design work: when to use each design skill, which Figma/browser/design-system gates are mandatory, and what source-of-truth files drive behavior.

## Source Of Truth

- `plugins/rldyour-design/.codex-plugin/plugin.json`
- `plugins/rldyour-design/README.md`
- `plugins/rldyour-design/references/figma-delivery-contract.md`
- `plugins/rldyour-design/skills/*/SKILL.md`
- `plugins/rldyour-design/skills/*/agents/openai.yaml`
- `config/skill-routing-policy.json` for routing regression cases.

## Skills and Routing

- `figma-to-code`: use when Figma frames, nodes, selections, whole canvases, or design handoff are the direct source.
- `design-system-implementation`: use for centralized tokens, theme, UI kit, i18n-ready primitives, shadcn/ui, and ReactBits choices.
- `fsd-frontend-architecture`: use when UI placement, public APIs, imports, i18n, data/admin ownership, or feature boundaries need correction.
- `design-validation`: use for browser-visible proof, Figma parity, responsive states, i18n/token/static scans, runtime checks, and screenshot cleanup.
- `ry-design`: use for end-to-end design tasks that span Figma intake, content classification, design-system work, FSD placement, implementation, and final validation.

## Figma Delivery Contract

`plugins/rldyour-design/references/figma-delivery-contract.md` is the shared mandatory reference for production-quality Figma/UI work.

- Build an implementation manifest before coding: source frames/nodes, scope, Figma tools used, state matrix, content model, design-system mapping, architecture, and validation plan.
- For whole canvases or heavy frames, use metadata first to split the target into named frames/sections, then fetch exact design context and screenshots per target.
- Use Figma MCP context and screenshots as source-of-truth input; use variables/styles and Code Connect when available.
- Classify every visible block as `static-i18n`, `config-backed`, `cms-admin-backed`, `api-domain-backed`, or `user-session-backed` before implementation.
- Static content means not admin-backed; visible copy still belongs in centralized i18n/resources unless the project explicitly has no i18n system.
- Repeated records, counters, filters, forms, charts, editable marketing sections, pricing, FAQs, catalogs, account data, and role-specific UI default to dynamic until proven static.
- Map colors, typography, spacing, radius, shadow, border, layout, breakpoints, z-index, opacity, and motion through centralized tokens before page/widget code consumes them.
- Use or extend a central UI kit for reusable controls and layout primitives; do not leave generated repeated UI as page-local one-offs.
- Final delivery is blocked until browser evidence, responsive/state coverage, i18n/token/static scans, runtime checks, and screenshot cleanup pass or an explicit blocker is reported.

## Boundaries

- `rldyour-design` is skills-only and does not configure MCP servers or hooks.
- MCP tools used are supplied by `rldyour-mcps` (`figma`, `shadcn`, `playwright`, `chrome-devtools`, and docs/research tools through helper skills when needed).
- Figma is treated as source-of-truth input for design intent, assets, variables, screenshots, and Code Connect hints; output is adapted into the project's architecture.
- Centralized i18n, centralized tokens, reusable UI kit, and strict FSD layers (`app`, `pages`, `widgets`, `features`, `entities`, `shared`) are default rules unless the project already has a coherent alternative.
- Meaningful frontend output should be browser-validated and cannot be marked complete without evidence or a documented blocker.

## Invariants

- Keep `allow_implicit_invocation: true` for design skills unless governance changes.
- Keep skill descriptions compact, bilingual, and under repository routing limits.
- Do not keep generated binary artifacts in commits; keep browser artifacts under `browser/` and remove them unless the owner asks to keep evidence.
- Do not claim ReactBits, shadcn, Figma auth, browser screenshots, or Code Connect usage beyond verified project/runtime context.
- Keep comments factual and avoid speculative TODOs in memory/docs.

## Verification

- `scripts/validate_marketplace.sh`
- `python3 scripts/validate_skill_routing.py`
- `python3 scripts/validate_instruction_docs.py --require-agent-docs`
- `jq empty plugins/rldyour-design/.codex-plugin/plugin.json config/skill-routing-policy.json`
- `uv run --with pyyaml python ${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py plugins/rldyour-design/skills/<skill-dir>`
- `diff -qr plugins/rldyour-design ${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/rldyour-design/local`
- `scripts/install_system_codex.sh --apply` after design plugin behavior changes so the installed plugin cache matches source.
- `scripts/doctor_system_codex.sh` after commit/fullrepo sync to verify installed runtime and final fullrepo state.
