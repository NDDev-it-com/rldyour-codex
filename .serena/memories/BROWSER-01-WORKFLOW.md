<!-- Memory Metadata
Last updated: 2026-07-10
Last verified: 2026-07-10
Last commit: 8be83a228e75b152cd3b7612bf834906310219a4 chore(release): codex adapter 1.8.5
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

## Last verified
- date: 2026-07-10
- commit: `8be83a228e75b152cd3b7612bf834906310219a4`
- checked by: Codex managed browser documentation contract refresh

## Facts
- Browser memories route UI and runtime validation through Webwright, Playwright CLI, and Chrome DevTools MCP when relevant.
- CloakBrowser is the required browser engine; `CLOAKBROWSER_VERSION=0.4.10` is the adapter policy pin, while installation remains owned by `rldyour-new-mac-or-ubuntu`.
- Chrome DevTools MCP must use `/bin/sh -c` with the exact bootstrap-managed `~/.local/bin/chrome-devtools-mcp` wrapper invocation. Stock-Chromium fallback is forbidden.
- Webwright, Playwright CLI, and Chrome DevTools MCP must use their
  bootstrap-owned wrappers under `$HOME/.local/bin`; every provider is backed
  by CloakBrowser and missing runtime health fails closed as `NOT_PROVEN`.
- Stock Chromium, the Codex in-app browser, raw browser processes, direct
  provider-package launchers, and alternate browser engines are not fallbacks.
- CloakBrowser `v0.4.10` changes wrapper behavior only (iframe humanization and JavaScript CLI entry-point fixes); the managed browser-binary pins do not change.

## Evidence
- `commit:8be83a228e75b152cd3b7612bf834906310219a4`
- `path:README.md`
- `path:plugins/rldyour-browser`
- `path:plugins/rldyour-mcps/README.md`
- `path:plugins/rldyour-mcps/.mcp.json`
- `path:config/mcp-runtime-versions.env`
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
  the exact managed transport, CloakBrowser policy pin, ownership, and
  fail-closed stock-browser rule.
- Run `bash scripts/validate_fast.sh` to exercise the browser policy in the
  repository's default CI gate.
- Run the rldyour control-plane Serena memory validators in strict mode: `validate_serena_memory_schema` (`--strict-mode strict-all`) and `validate_serena_memory_semantics` (`--strict-current-facts --strict-metadata-dates --strict-evidence-commits`).

## Repair Procedure

1. Re-read the source-of-truth files listed above.
2. Update only verified current facts; move stale facts into historical evidence.
3. Rerun the validation commands until green.
