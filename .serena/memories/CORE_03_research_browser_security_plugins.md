<!-- Memory Metadata
Last updated: 2026-05-03
Last commit: 614b71e chore(serena): document memory state semantics
Scope: plugins/rldyour-explore, plugins/rldyour-browser, plugins/rldyour-security
Area: CORE
-->

# CORE_03_research_browser_security_plugins

## Purpose

`rldyour-explore`, `rldyour-browser`, and `rldyour-security` are skills-only workflow plugins that provide automatic research, browser validation/debugging, and security review guidance. They depend on MCP transports from `rldyour-mcps` instead of declaring duplicate MCP servers and are designed to activate from Russian or English user requests.

## Source Of Truth

- `plugins/rldyour-explore/.codex-plugin/plugin.json`, `plugins/rldyour-explore/skills/*/SKILL.md`, `plugins/rldyour-explore/skills/*/agents/openai.yaml`, `plugins/rldyour-explore/README.md`.
- `plugins/rldyour-browser/.codex-plugin/plugin.json`, `plugins/rldyour-browser/skills/*/SKILL.md`, `plugins/rldyour-browser/skills/*/agents/openai.yaml`, `plugins/rldyour-browser/README.md`.
- `plugins/rldyour-security/.codex-plugin/plugin.json`, `plugins/rldyour-security/skills/*/SKILL.md`, `plugins/rldyour-security/skills/*/agents/openai.yaml`, `plugins/rldyour-security/README.md`.

## Entry Points

Research:

- `tech-research`: use for technical docs, APIs, frameworks, SDKs, migrations, MCP/tool sources, open-source repository architecture, production GitHub patterns, and best-practice validation before coding.
- `web-research`: use for current web information, authoritative source links, latest-state checks, non-technical research, recommendations, pricing, legal/security updates, standards, and web-only evidence.

Browser:

- `browser-tool-routing`: choose Playwright, Chrome DevTools, or both when the browser workflow is unclear.
- `browser-validation`: validate visible UI, screenshots, responsive behavior, functional flows, business logic, browser-visible data, and runtime health.
- `browser-debug`: diagnose console, network, runtime, hydration, layout, Lighthouse, performance, memory, and browser-only bugs.

Security:

- `owasp-top-10-implementation`: apply non-blocking OWASP Top 10 secure implementation comments during security-relevant coding.
- `ry-sec-review`: perform defensive security review for implementations, diffs, pull requests, or sensitive code paths.

## Current Behavior

All skills in these plugins keep `policy.allow_implicit_invocation: true`.

`tech-research` is the first choice for technical research. It uses Context7 for official documentation, DeepWiki for repository architecture, and Grep by Vercel for real GitHub usage patterns. Use `web-research` in addition when technical work needs fresh external sources beyond those MCPs or when the user explicitly asks to study the internet.

For OpenAI or Codex topics, `tech-research` uses `openaiDeveloperDocs` before Context7, DeepWiki, Grep, or general web sources. This includes OpenAI/Codex product behavior, configuration, plugins, skills, MCP, hooks, models, APIs, and migration guidance.

`web-research` first defines scope and questions, then searches in multiple passes, reads authoritative sources, rejects weak sources, compares conflicts, and answers in Russian with links. It is the correct path for current information, recommendations, standards, policies, pricing, legal/security updates, and any unstable fact.

For OpenAI or Codex current documentation, `web-research` uses `openaiDeveloperDocs` first and falls back to official OpenAI web pages before broader search.

`browser-validation` uses Playwright MCP as primary evidence for user flows, screenshots, responsive checks, accessibility snapshots, testing assertions, storage, and network checks. It adds Chrome DevTools MCP when console, network, runtime, layout, hydration, or performance diagnosis is needed.

`browser-debug` uses Chrome DevTools MCP as primary diagnosis and Playwright MCP for reproduction and re-validation.

`owasp-top-10-implementation` is advisory and non-blocking. It should surface concise security comments and apply high-confidence fixes in scope.

`ry-sec-review` is defensive-only. Findings must come first, be severity ordered, include confidence, evidence, impact, fix, and verification, and avoid weaponized exploit code or destructive instructions.

`plugins/rldyour-security/README.md` currently defines the security scope as OWASP Top 10 2025, ASVS 5.0.0, OWASP secure coding checklist principles, non-blocking implementation comments, and defensive review. The plugin has no hooks and does not block normal implementation work.

All seven skills across `rldyour-explore`, `rldyour-browser`, and `rldyour-security` keep `policy.allow_implicit_invocation: true` and are validated as callable rldyour skills by `scripts/validate_marketplace.sh`.

## Contracts And Data

Research output stays Russian for user-facing answers. Source facts and engineering conclusions must be separated; inferred conclusions should be labeled.

Browser artifacts must be written under `browser/`. Do not commit screenshots, traces, videos, PDFs, HAR-like exports, or temporary browser evidence unless the owner explicitly asks.

Security review should use Serena for semantic code mapping when available and Semgrep as optional SAST support. Scanner findings still require manual validation.

`rldyour-browser` requires screenshots and temporary browser evidence under `browser/`. Repository `.gitignore` must keep browser evidence out of commits unless the owner explicitly requests otherwise.

## Invariants

- Do not configure MCP transports inside these skills-only plugins.
- Do not expose secrets, tokens, cookies, private URLs, credentials, or closed data in research or security outputs.
- Do not let browser validation skip business logic when a UI change affects behavior.
- Do not treat security plugin comments as a blocking gate unless normal Codex safety rules apply or the owner asks for a blocking review.
- Keep user-facing responses in Russian and repository artifacts in English.

## Change Rules

- When changing auto-routing, update each affected `SKILL.md` frontmatter `description` first.
- Keep plugin README trigger maps, `plugin.json` descriptions, and `agents/openai.yaml` metadata aligned with skill descriptions.
- After changing browser artifact rules, update both `rldyour-browser` and `rldyour-design` if design validation depends on the browser rule.
- After changing security review format, update `ry-sec-review/SKILL.md` and this memory together.

## Verification

- `/opt/homebrew/bin/uv run --with pyyaml python <skill-creator>/scripts/quick_validate.py <skill-dir>`: validates each modified skill.
- `/opt/homebrew/bin/uv run --with pyyaml python -c '<parse agents/openai.yaml files>'`: validates `allow_implicit_invocation`.
- `jq empty plugins/rldyour-explore/.codex-plugin/plugin.json plugins/rldyour-browser/.codex-plugin/plugin.json plugins/rldyour-security/.codex-plugin/plugin.json`: validates manifests.
- `git diff --check`: checks whitespace before commit.
