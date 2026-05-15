<!-- Memory Metadata
Last updated: 2026-05-16
Last commit: 1132859 feat(serena): harden codex memory sync brain
Scope: plugins/rldyour-explore, plugins/rldyour-browser, plugins/rldyour-security, plugins/rldyour-design, plugins/rldyour-lsps, plugins/rldyour-rules, config/skill-routing-policy.json, README.md
Area: CORE
-->

# CORE-03-DOMAIN-PLUGINS

## Purpose

This memory maps the non-Flow/non-Serena domain plugins so future sessions route work to the right specialist workflow without duplicating behavior in the wrong plugin.

## Source Of Truth

- `plugins/rldyour-explore/skills/*/SKILL.md`: technical and web research workflows.
- `plugins/rldyour-browser/skills/*/SKILL.md`: browser routing, validation, and debugging workflows.
- `plugins/rldyour-security/skills/*/SKILL.md`: OWASP implementation guidance and security review workflow.
- `plugins/rldyour-design/skills/*/SKILL.md`: Figma/design-system/FSD/browser-validated UI workflows.
- `plugins/rldyour-lsps/skills/*/SKILL.md`: LSP routing, setup, health, and Serena LSP integration guidance.
- `plugins/rldyour-rules/skills/*/SKILL.md`: engineering, architecture, dependency, project-doc, verification, and review rules.
- `config/skill-routing-policy.json`: deterministic routing tests.

## Entry Points

- `$tech-research` and `$web-research`: current technical/web research.
- `$browser-tool-routing`, `$browser-validation`, `$browser-debug`: browser-visible checks and debugging.
- `$ry-sec-review` and `$owasp-top-10-implementation`: security review and implementation guidance.
- `$ry-design`, `$figma-to-code`, `$design-system-implementation`, `$fsd-frontend-architecture`, `$design-validation`: design/UI workflows.
- `$lsp-routing`, `$lsp-health-check`, `$lsp-setup`, `$serena-lsp-integration`: LSP workflows.
- `$quality-first-engineering`, `$implementation-discipline`, `$verification-quality-gates`, `$ry-rules-review`: engineering rules and verification gates.

## Current Behavior

- `rldyour-explore` uses Context7, DeepWiki, Grep, and web research when prompts ask for current docs, internet analysis, latest facts, or best practices.
- `rldyour-browser` handles browser-visible validation/debugging with Playwright MCP and Chrome DevTools MCP routing.
- `rldyour-security` is defensive and OWASP-oriented; it is used for auth/authz/API/input/file/dependency/config/secrets/payment/admin/external-integration scope or explicit security review.
- `rldyour-design` owns design implementation, Figma-to-code, centralized i18n/tokens/UI kit, strict FSD placement, shadcn/ui, ReactBits, and browser/design validation gates.
- `rldyour-lsps` owns language-server selection, setup policy, diagnostics, and Serena LSP integration.
- `rldyour-rules` owns quality, architecture boundaries, dependency compatibility, verification gates, project instruction policy, and rules review.

## Contracts And Data

- Domain plugins must not declare duplicate MCP transports; MCP registration comes from `rldyour-mcps`.
- Domain skills should keep frontmatter descriptions compact in Russian and English, with detailed behavior in skill bodies and references.
- Reviewer track skills may set `allow_implicit_invocation: false` in `agents/openai.yaml` when orchestrated by Flow.

## Invariants

- Route helper skills automatically from Russian owner prompts when the intent matches.
- Do not wait for the owner to name every helper plugin when `ry-start` or `ry-review` implies domain work.
- Keep plugin boundaries clear: research, browser, design, LSP, security, and rules behavior stay in their respective plugins.

## Change Rules

- When adding/changing a domain skill, update routing policy tests and validate with `python3 scripts/validate_skill_routing.py`.
- When changing a domain's tool dependencies, update `agents/openai.yaml` and validate with `scripts/validate_agent_tools.py`.

## Verification

- `python3 scripts/validate_skill_routing.py`: deterministic routing.
- `uv run --with pyyaml python scripts/validate_agent_tools.py`: metadata dependency validity.
- `scripts/validate_marketplace.sh`: full plugin validation.
