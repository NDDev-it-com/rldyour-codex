<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: 4bd04d1837100ecc64530665cdd0fd8c3118697b feat(browser): enforce managed CloakBrowser skill boundary
Scope: browser-visible validation and debugging workflows
Area: BROWSER
-->

# Browser Workflow

## Scope
browser-visible validation and debugging workflows

## Current source of truth
- `path:README.md`
- `path:plugins/rldyour-browser`
- `path:plugins/rldyour-mcps/README.md`
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:config/mcp-runtime-versions.env`
- `path:config/rldyour-contract.json`
- `path:scripts/validate_browser_provider_policy.py`
- `path:scripts/install_system_codex.sh`
- `path:scripts/doctor_system_codex.sh`
- `path:tests/fixtures/codex_app_managed_browser_config.toml`

## Last verified
- date: 2026-07-10
- commit: `4bd04d1837100ecc64530665cdd0fd8c3118697b`
- checked by: Codex 1.8.8 browser skill-boundary implementation

## Facts
- Every browser-capable `rldyour-browser` skill runs exact
  `$HOME/.local/bin/cloakbrowser-cdp-health` before every browser action and
  stops as `NOT_PROVEN` when the preflight is missing or nonzero.
- CloakBrowser is the required browser engine; `CLOAKBROWSER_VERSION=0.4.10` is the adapter policy pin, while installation remains owned by `rldyour-new-mac-or-ubuntu`.
- Chrome DevTools MCP must use `/bin/sh -c` with the exact bootstrap-managed `~/.local/bin/chrome-devtools-mcp` wrapper invocation. Stock-Chromium fallback is forbidden.
- Browser actions may use only exact `$HOME/.local/bin/playwright-cli` without
  `run-code`/`--filename`, or Chrome DevTools MCP through its exact managed
  wrapper transport. The `webwright-task` name is compatibility-only and never
  starts a Webwright or Python runtime.
- Webwright runtime, stock/raw/in-app Browser, browser/computer-use helpers,
  Playwright MCP/raw Playwright, direct packages, alternate CDP/config or
  executable paths, and all fallbacks are forbidden.
- System install explicitly disables `browser@openai-bundled`; app-managed
  `node_repl` and `computer-use` MCP metadata is preserved only with
  `enabled = false`. Doctor rejects an active or reinjected surface and directs
  the operator to rerun the installer and restart Codex.
- CloakBrowser `v0.4.10` changes wrapper behavior only (iframe humanization and JavaScript CLI entry-point fixes); the managed browser-binary pins do not change.

## Evidence
- `commit:4bd04d1837100ecc64530665cdd0fd8c3118697b`
- `path:README.md`
- `path:plugins/rldyour-browser`
- `path:plugins/rldyour-mcps/README.md`
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:config/mcp-runtime-versions.env`
- `path:scripts/install_system_codex.sh`
- `path:scripts/doctor_system_codex.sh`
- `path:tests/fixtures/codex_app_managed_browser_config.toml`
- `https://github.com/CloakHQ/CloakBrowser/tree/v0.4.10`
- `https://pypi.org/project/cloakbrowser/0.4.10/`

## Known pitfalls
- Treat this memory as derived context. Current code, configuration, runtime output, and GitHub state override stale memory text.

## Update policy
Update after verified changes to the referenced source-of-truth files.

## Delete / merge policy
- Delete or merge only when the referenced source-of-truth files no longer support this memory and the replacement memory preserves the durable facts.

## Applies to

- The scope and source-of-truth paths declared in this memory.

## Source of truth

- The `Current source of truth` entries above, plus current code, configuration, tests, git state, and live GitHub state where this memory references live release or repository surfaces.

## Invariants

- Current code, configuration, tests, validators, git state, and live GitHub state override this memory whenever they disagree.

## Current State

- Treat the `Facts` section as the current durable state. Do not treat historical evidence, superseded notes, or previous release entries as current.

## Do Not Infer

- Do not infer runtime versions, product versions, commits, permissions, release state, security posture, or tool behavior from this memory without checking the source of truth.

## Update Triggers

- Update after verified changes to the source-of-truth files, runtime baselines, release tuple, validation gates, live release state, or durable agent-workflow contracts.

## Validation Commands

- Run `python3 scripts/validate_browser_provider_policy.py --strict` to verify
  every browser skill's preflight, exact provider transports, forbidden
  surfaces, CloakBrowser policy pin, and fail-closed behavior.
- Run `bash scripts/validate_fast.sh` to exercise the browser policy in the
  repository's default CI gate.
- Run the rldyour control-plane Serena memory validators in strict mode: `validate_serena_memory_schema` (`--strict-mode strict-all`) and `validate_serena_memory_semantics` (`--strict-current-facts --strict-metadata-dates --strict-evidence-commits`).

## Repair Procedure

1. Re-read the source-of-truth files listed above.
2. Update only verified current facts; move stale facts into historical evidence.
3. Rerun the validation commands until green.
