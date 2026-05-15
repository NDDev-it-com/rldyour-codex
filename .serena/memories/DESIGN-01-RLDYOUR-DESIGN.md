<!-- Memory Metadata
Last updated: 2026-05-16
Last commit: 1132859 feat(serena): harden codex memory sync brain
Scope: plugins/rldyour-design, plugins/rldyour-browser, config/skill-routing-policy.json, README.md
Area: DESIGN
-->

# DESIGN-01-RLDYOUR-DESIGN

## Purpose

`rldyour-design` owns design and frontend UI workflows for Codex: Figma-to-code, design systems, strict FSD placement, i18n/content classification, shadcn/ui, ReactBits, and browser-validated delivery.

## Source Of Truth

- `plugins/rldyour-design/skills/ry-design/SKILL.md`: end-to-end design workflow.
- `plugins/rldyour-design/skills/figma-to-code/SKILL.md`: Figma implementation workflow.
- `plugins/rldyour-design/skills/design-system-implementation/SKILL.md`: tokens/theme/UI-kit work.
- `plugins/rldyour-design/skills/fsd-frontend-architecture/SKILL.md`: FSD placement.
- `plugins/rldyour-design/skills/design-validation/SKILL.md`: browser/static design validation.
- `plugins/rldyour-browser/skills/browser-validation/SKILL.md`: browser proof for UI changes.
- `config/skill-routing-policy.json`: routing expectations.

## Entry Points

- `$ry-design`: full design/UI workflow.
- `$figma-to-code`: implement from Figma.
- `$design-system-implementation`: centralized tokens/theme/UI kit.
- `$fsd-frontend-architecture`: FSD placement decisions.
- `$design-validation`: visual/browser/static validation.

## Current Behavior

- Figma is the source of truth for Figma-to-code tasks; implementation adapts design into project architecture, tokens, UI kit, and i18n.
- Browser-visible UI changes require browser validation when a browser can be run.
- Design workflows classify dynamic/static/admin content and avoid hardcoding project data into UI where data ownership is dynamic.
- New frontend areas default to strict FSD if the project has no stronger local architecture.

## Contracts And Data

- Use existing project components/tokens before inventing new UI primitives.
- Store screenshots and temporary browser evidence under `browser/` and do not commit them unless explicitly requested.
- Do not use visible in-app instructional text to describe app functionality unless the product itself requires it.

## Invariants

- UI text must fit its containers across mobile and desktop viewports.
- Do not build marketing landing pages when the user asked for a usable app/tool unless explicitly required.
- Use icons, tooltips, controls, and dense task-oriented layouts according to project and Codex frontend guidance.

## Change Rules

- When design workflows change, update route tests and this memory.
- When browser validation requirements change, update `rldyour-browser` skills and design validation docs together.

## Verification

- `python3 scripts/validate_skill_routing.py`: design skill routing.
- `scripts/validate_marketplace.sh`: skill metadata and routing validation.
- Browser validation through Playwright/Chrome DevTools when implementing UI.
