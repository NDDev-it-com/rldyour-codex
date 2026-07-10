# rldyour-design

`rldyour-design` is a skills-only design implementation plugin for Codex.

It does not configure MCP servers directly. Figma and shadcn MCP plus Chrome
DevTools MCP are provided by `rldyour-mcps`; browser work delegates to
`rldyour-browser`, which permits only managed Playwright CLI and the approved
Chrome DevTools MCP wrapper after the mandatory CloakBrowser health preflight.

User-facing conversation stays in Russian unless the owner asks otherwise. Repository documentation is written in English.

## Auto Invocation

The plugin is optimized for automatic skill selection. Codex should route design work to these skills when a task mentions Figma, designer layouts, pixel-perfect frontend implementation, UI creation or restyling, centralized design tokens, centralized i18n, dynamic/static content decisions, admin/CMS-backed blocks, shadcn/ui, ReactBits, strict FSD placement, responsive visual changes, or browser-based design validation.

`policy.allow_implicit_invocation` is enabled for every skill. The primary trigger surface is each `SKILL.md` frontmatter `description`; plugin manifest descriptions and `agents/openai.yaml` metadata mirror the same intent for marketplace and UI discovery.

## Scope

- Use Figma MCP as the source of truth for designer-provided layouts, variables, components, layout data, assets, screenshots, and Code Connect hints when available.
- For whole canvases or heavy page frames, use metadata first, split work into exact frames/sections, then fetch design context and screenshots per target.
- Classify every visible block as static localized content, config-backed, admin/CMS-backed, API/domain-backed, or user/session-backed before implementing it.
- Keep user-visible text in centralized i18n/resources; static content means not admin-backed, not inline literals in components.
- Build a centralized design system with explicit tokens for color, typography, spacing, radius, shadow, border, layout, breakpoints, z-index, motion, opacity, and component states.
- Build or extend a centralized UI kit for reusable primitives and components; do not leave repeated generated UI as page-local one-offs.
- Use strict Feature-Sliced Design by default: `app`, `pages`, `widgets`, `features`, `entities`, `shared`; no `processes`.
- Use shadcn/ui MCP as the primary UI primitive and registry workflow.
- Use ReactBits.dev only for purposeful animated or interactive React components, preferably through shadcn-compatible install URLs when available.
- Validate design implementation in the browser with `rldyour-browser`; screenshots and browser evidence belong under `browser/` and final delivery is blocked until visual, functional, i18n, token, dynamic-state, and runtime gates pass or the blocker is explicit.

## Skills

- `figma-to-code`: pixel-perfect transfer from Figma to code.
- `design-system-implementation`: centralized token-based design system with shadcn/ui and ReactBits rules.
- `fsd-frontend-architecture`: strict FSD placement for frontend design implementation.
- `design-validation`: browser proof for design implementation quality.
- `ry-design`: command-like end-to-end design workflow.

## References

- `references/figma-delivery-contract.md`: required manifest, content classification, i18n/token/UI-kit rules, and final validation gate for production-quality Figma/UI work.

## Trigger Map

- Figma file, frame, node, selection, design handoff, designer layout, or pixel-perfect transfer: use `figma-to-code`.
- Tokens, CSS variables, Tailwind/shadcn theme, UI kit, component variants, or visual consistency: use `design-system-implementation`.
- FSD placement, public APIs, imports, frontend layers, generated code adaptation, or architecture cleanup: use `fsd-frontend-architecture`.
- Browser proof, screenshots, visual regression, responsive checks, runtime checks, or final frontend validation: use `design-validation`.
- Complete design/page/component implementation that requires multiple design steps: use `ry-design`.

## Design Standard

Do not paste generated Figma code blindly. Use Figma context as structured source material, then adapt it into the project's architecture, design system, i18n resources, UI kit, data/admin contracts, tokens, components, and browser-validated behavior.

Pixel-perfect means matching layout, spacing, typography, colors, assets, state variants, responsive frames, and interaction behavior as closely as possible through iterative browser screenshots and fixes.

## Sources

- Figma MCP server: https://developers.figma.com/docs/figma-mcp-server
- Figma Implement Design skill: https://developers.figma.com/docs/figma-mcp-server/skill-figma-implement-design/
- Figma Codex setup: https://help.figma.com/hc/en-us/articles/39888629089175-Codex-and-Figma-Set-up-the-MCP-server
- Figma Code Connect: https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect
- W3C Design Tokens Format Module: https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/
- Playwright visual comparisons: https://playwright.dev/docs/test-snapshots
- i18next best practices: https://www.i18next.com/principles/best-practices
- shadcn/ui MCP: https://ui.shadcn.com/docs/mcp
- shadcn registry MCP: https://ui.shadcn.com/docs/registry/mcp
- Feature-Sliced Design overview: https://fsd.how/docs/get-started/overview
- Feature-Sliced Design layers: https://fsd.how/docs/reference/layers
- Feature-Sliced Design slices and segments: https://fsd.how/docs/reference/slices-segments
