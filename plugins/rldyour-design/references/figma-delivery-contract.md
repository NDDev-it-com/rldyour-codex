# Figma Delivery Contract

Use this reference for every Figma-driven or high-fidelity UI implementation before coding and again before final delivery.

## Implementation Manifest

Create a short manifest before editing code. Keep it in the working notes or final report; do not commit it unless the project already has a durable design spec location.

Required fields:

- `source`: Figma URL or selected node, file key, node IDs, frame names, and whether the input is a whole canvas, page frame, component, or selection.
- `scope`: target route/page/widget/component, in-scope frames, out-of-scope frames, and requested responsive sizes.
- `figma context`: tools called and outputs used: `get_metadata` for whole canvases or heavy frames, `get_design_context`, `get_screenshot`, `get_variable_defs`, and Code Connect or design-system lookup when available.
- `state matrix`: default, hover, focus, active, disabled, selected, loading, empty, error, long localized text, authenticated/unauthenticated, and any designer-specified variants.
- `content model`: classification table from the section below.
- `design system`: token mappings, UI-kit components, shadcn/registry items, assets, and unresolved token gaps.
- `architecture`: FSD layer/slice/segment placement, public APIs, data-fetching ownership, admin/CMS ownership, and i18n namespace/key placement.
- `validation`: browser viewports, screenshots, visual comparison method, static scans, functional flows, and blockers.

For a whole Figma canvas or large page, do not run one broad implementation pass. First use metadata to split the work into named frames and logical sections, then fetch exact context and screenshots per target frame or section.

## Content And Data Classification

Classify every visible block before implementation:

| Class | Use When | Implementation |
| --- | --- | --- |
| `static-i18n` | The content is intentionally fixed and not expected to change without a deploy. | Store user-visible text in i18n resources or an existing localized content file. Do not inline JSX/template literals. |
| `config-backed` | Content is fixed for now but product owners may tune it without touching UI code. | Store in a typed config/content module plus i18n keys. |
| `cms-admin-backed` | Marketing sections, pricing, FAQs, testimonials, team, catalog, articles, hero copy, banners, or any content the owner/admin should edit. | Reuse or design admin/CMS schema, API contract, loading/empty/error states, and preview/fallback behavior. |
| `api-domain-backed` | Tables, lists, cards, dashboards, charts, counters, forms, filters, search, entity details, or domain-specific data. | Use existing entity/feature API/model patterns; mock only external services in tests. |
| `user-session-backed` | Auth, permissions, profile data, personalization, role-specific UI, or account state. | Follow existing auth/session boundaries and test allowed/empty/denied states. |

Decision rules:

- If the block contains repeated records, counts, filters, charts, forms, edit controls, or domain nouns, assume dynamic until proven static.
- If the owner says the content is "static", treat that as "not admin-backed"; user-visible text still belongs in i18n unless the project explicitly has no i18n system yet.
- If no i18n system exists, create or extend the smallest project-consistent centralized i18n structure before adding new visible text.
- Hardcoded visible strings are allowed only for technical constants, test fixtures, ARIA-hidden decorative text, or an explicit owner exception recorded in the final residual gaps.

## Design System And UI Kit

Map Figma variables/styles to project tokens before writing page/widget code:

- Colors, typography, spacing, radius, shadow, border, layout, breakpoints, z-index, opacity, and motion must have centralized token ownership.
- Raw hex/RGB/HSL/OKLCH values belong only in token source files or generated design-token artifacts.
- Feature/page/widget code should consume semantic tokens, variant props, or shared UI primitives, not raw design values.
- When Code Connect maps a Figma component to a code component, prefer that code component and extend it if needed.
- Use shadcn/ui or project registry items to seed primitives, then adapt them into the project's `shared/ui` or existing UI-kit location.
- Keep business logic out of `shared/ui`; put domain behavior in `features`, `entities`, `widgets`, or `pages`.
- New reusable primitives need public exports and predictable props; do not keep demo-only variants or placeholder data.

## Validation Gate

A design implementation is not complete until the matching evidence exists or the blocker is explicit:

- Figma reference screenshot exists for each implemented target frame or section.
- Browser screenshots exist for desktop and mobile, plus every provided Figma frame size when possible.
- The rendered UI is compared against Figma for layout, spacing, typography, color, radius, shadows, assets, and state variants.
- Interactions, navigation, forms, dialogs, menus, and business rules touched by the UI are exercised.
- Loading, empty, error, permission-denied, and long localized text states are tested for dynamic blocks.
- Console errors, failed network requests, hydration/runtime issues, text overflow, and incoherent overlaps are absent.
- Keyboard reachability, labels, focus visibility, and reduced-motion behavior are checked when relevant.
- Static scans cover user-visible string literals, raw colors/design values outside token files, placeholder assets/copy, duplicated one-off components, and unused generated code.
- Browser artifacts are stored under `browser/` during validation and removed before commit unless the owner explicitly asks to keep them.

If any required gate cannot run, say why, keep the task open if the blocker can be fixed locally, or report the exact residual risk if it depends on unavailable Figma access, credentials, external services, or missing product decisions.

## Final Report Contract

Final design delivery must include:

- `Figma`: frames/nodes inspected and tools used.
- `Content model`: dynamic/static/admin/i18n decisions.
- `Design system`: tokens, UI-kit components, assets, and Code Connect usage.
- `Architecture`: FSD placement and public APIs.
- `Validation`: browser/static commands or MCP evidence, screenshots cleanup, and failures fixed.
- `Residual gaps`: only real blockers; do not hide unvalidated states.
