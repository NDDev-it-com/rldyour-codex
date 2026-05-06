<!-- Memory Metadata
Last updated: 2026-05-06
Last commit: d675a30 fix(flow): ignore remote head in git sync audit
Scope: plugins/rldyour-explore, plugins/rldyour-browser, plugins/rldyour-security
Area: CORE
-->

# CORE_03_research_browser_security_plugins

## Purpose

Capture routing and validation facts for research, browser, and security domains, avoiding stale process assumptions and unverified behavior claims.

## Source-of-Truth

- `plugins/rldyour-explore/.codex-plugin/plugin.json`, `skills/*/SKILL.md`, `skills/*/agents/openai.yaml`
- `plugins/rldyour-browser/.codex-plugin/plugin.json`, `skills/*/SKILL.md`, `skills/*/agents/openai.yaml`
- `plugins/rldyour-security/.codex-plugin/plugin.json`, `skills/*/SKILL.md`, `skills/*/agents/openai.yaml`
- `plugins/rldyour-mcps/.mcp.json` for available MCP transports
- `scripts/validate_marketplace.sh`

## Routing Facts

Research (`rldyour-explore`):
- `tech-research`: documentation-first technical investigation (Context7, DeepWiki, Grep) and OpenAI/Codex doc work when relevant.
- `web-research`: current/unstable topics, recommendations, pricing, standards, legal/security updates, and source-backed evidence checks.

Browser (`rldyour-browser`):
- `browser-tool-routing`: select Playwright, Chrome DevTools, or both.
- `browser-validation`: UI/flow/visual proof, responsive checks, screenshots, and business-logic verification.
- `browser-debug`: console/network/runtime/layout/performance diagnosis and re-validation.

Security (`rldyour-security`):
- `owasp-top-10-implementation`: secure implementation guidance during coding.
- `ry-sec-review`: evidence-based security review with severity ordering and remediation recommendations.

## Facts and Invariants

- Active explorer/browser/security plugin count: 7 skills total.
- All skills in these three plugins currently keep `allow_implicit_invocation: true`.
- Research and review outputs remain source-backed and should separate fact from inference.
- Browser evidence belongs under `browser/`; by default it is non-committable working output.
- Security outputs must avoid exploit payloads, credentials, and destructive guidance.
- Neither plugin owns MCP transport definitions; they consume MCP from `rldyour-mcps`.

## Verification

- `python3 scripts/validate_skill_routing.py`
- `scripts/validate_marketplace.sh`
- `jq empty plugins/rldyour-explore/.codex-plugin/plugin.json plugins/rldyour-browser/.codex-plugin/plugin.json plugins/rldyour-security/.codex-plugin/plugin.json`
- `diff -qr plugins/<plugin> ${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/<plugin>/local`
