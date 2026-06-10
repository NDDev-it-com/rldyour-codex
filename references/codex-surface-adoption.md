# Codex Surface Adoption

Verified: 2026-06-10

Source of truth:
- Runtime baseline: `references/codex-baseline.json`
- Runtime package pin: package metadata for `@openai/codex`
- Official changelog and config docs: `https://github.com/openai/codex/releases/tag/rust-v0.139.0` and `https://developers.openai.com/codex/changelog`

## Decisions

| Surface | Introduced | Decision | Implementation | Validator |
| --- | --- | --- | --- | --- |
| Codex CLI runtime baseline | 0.139.0 | Adopted | Root contract and adapter runtime pins require `@openai/codex` / `codex-cli` `0.139.0`; local installed runtime must report `codex-cli 0.139.0`. | `python3 scripts/check_mcp_runtime_versions.py --fail-on-outdated` |
| `[tui].status_line` owner status line | 0.119.0 | Adopted | `scripts/install_system_codex.sh` manages `status_line = ["model-with-reasoning", "context-remaining", "five-hour-limit", "weekly-limit", "git-branch", "current-dir"]` and `status_line_use_colors = true` in `config.toml` and both `rldyour-yolo`/`rldyour-safe` profile configs so every session footer shows model, context remainder, and five-hour/weekly rate-limit remainder. Only these two keys are managed; other user `[tui]` keys are preserved. | `tests/unit/test_install_system_codex_tui_status_line.py` |
| `/app` desktop handoff and Windows workspace launch | 0.138.0 | Operational | Treat as runtime capability. Repository config does not hard-code Desktop handoff state, but installed-runtime smoke may rely on the `codex` binary being at the 0.138.0 baseline before diagnosing app/server integration behavior. | `scripts/doctor_system_codex.sh --quick --strict-runtime` |
| Local image file paths exposed to the model | 0.138.0 | Capability-dependent | Local image attachment and generated-image path exposure is runtime behavior. Do not add repository claims about availability unless installed-runtime checks prove the active account/session supports the capability. | n/a |
| Plugin command JSON and richer plugin metadata | 0.138.0 | Operational | 0.138.0 documents richer plugin JSON surfaces. The adapter already treats JSON plugin inventory as installed-runtime evidence and keeps static validators from inventing runtime plugin state. | root `scripts/ry_repair_sync.py --plan --apply-system --json` |
| App-server token-usage and v2 personal access token support | 0.138.0 | Capability-dependent | Authentication tokens and account usage data remain external runtime state. Do not store PATs, OAuth tokens, or account usage in repository config, logs, memories, or fixtures. | `scripts/validate_instruction_docs.py` |
| Model-defined reasoning effort ordering | 0.138.0 | Operational | Keep managed subagent TOML defaults static unless the owner changes model policy. Runtime-provided effort ordering is accepted as CLI behavior, not a repository schema migration. | `scripts/validate_agent_tools.py` |
| Stable release boundary vs. prereleases | 0.139.0 | Adopted | Stable `0.139.0` is the release-grade baseline. `0.140.0-alpha.*` and later alpha tags remain excluded unless the owner explicitly enables prerelease runtime policy. | `scripts/check_mcp_runtime_versions.py --fail-on-outdated` |
| Code-mode standalone web search and richer MCP schemas | 0.139.0 | Operational | 0.139.0 lets code mode call standalone web search (including nested JS tool calls) and preserves `oneOf`/`allOf` plus more shallow structure in compacted tool schemas. Runtime behavior only: keep MCP definitions in `.mcp.json` unchanged and treat improved schema fidelity as compatibility, not a config migration. | `scripts/smoke_mcp_capabilities.py` |
| `codex doctor` editor/pager environment details | 0.139.0 | Operational | `codex doctor` now reports editor and pager environment details locally while redacting raw values in JSON output; keep using the doctor in installed-runtime diagnostics without storing raw environment values. | `scripts/doctor_system_codex.sh --quick` |
| Marketplace `list --json` source field and cached catalog responses | 0.139.0 | Operational | `codex plugin marketplace list --json` now includes each marketplace source and plugin lists may return from the cached remote catalog before background refresh; installed-runtime checks must treat cached-vs-fresh catalog responses as equivalent evidence. | root `scripts/ry_repair_sync.py --plan --json` |
| `codex doctor` diagnostics | 0.135.0 | Operational | Owner doctor flow remains `scripts/doctor_system_codex.sh`; `/ry-repair --apply-system` also plans direct `codex doctor` when installed runtime is available. | `scripts/doctor_system_codex.sh --quick --strict-runtime`; root `scripts/ry_repair_sync.py --plan --apply-system --json` |
| Remote `/status` server-version details | 0.135.0 | Not applicable | Remote TUI status output is user-facing runtime behavior and does not change repository config. | n/a |
| `/permissions` named/custom profile display | 0.135.0 | Operational | Use `/permissions` and `codex doctor` to inspect resolved permission profiles. Do not migrate the owner profile from the legacy `sandbox_mode` dialect without an explicit policy change. | `scripts/validate_instruction_docs.py` |
| Packaged patched zsh helper discovery | 0.135.0 | Operational | Treat as installed-runtime diagnostic behavior only; no config migration is required. | `scripts/doctor_system_codex.sh --quick --strict-runtime` |
| Vim mode text-object and binding refinements | 0.135.0 | Not applicable | User-facing editor behavior; no config, plugin, hook, or MCP migration is required. | n/a |
| `--profile` as primary selector | 0.134.0 | Adopted | Owner launcher and docs use `codex --profile rldyour-yolo`; installer writes `$CODEX_HOME/rldyour-yolo.config.toml` and `$CODEX_HOME/rldyour-safe.config.toml`. | `scripts/validate_contract.py` |
| Legacy `[profiles.*]` and `profile = "..."` rejected | 0.134.0 | Adopted | Installer, doctor, contracts, and instruction docs forbid legacy profile selectors. | `scripts/validate_instruction_docs.py` |
| Permission profiles not mixed with `sandbox_mode` | 0.134.0 docs | Adopted | Owner policy remains `approval_policy = "never"` plus `sandbox_mode = "danger-full-access"`; active `default_permissions` is absent. | `scripts/validate_contract.py` |
| MCP runtime config as TOML `[mcp_servers.*]` | current docs | Adopted | `.mcp.json` remains source metadata; installer materializes native TOML runtime config. | `scripts/validate_contract.py` |
| Plugin hook feature flag removed/default-enabled | 0.134.0 | Adopted | No `[features].plugin_hooks`; trusted hook state is verified through hook listing smoke tests. | `scripts/smoke_codex_hook_listing.py` |
| Read-only MCP tool concurrency via `readOnlyHint` | 0.134.0 | Operational | No config migration required; MCP servers keep native tool metadata. | `scripts/smoke_mcp_capabilities.sh` |
| Local conversation history search | 0.134.0 | Not applicable | This is user-facing CLI behavior and does not change repository config. | n/a |

## Owner Full-Auto Policy

The owner-standard Codex mode intentionally uses `approval_policy = "never"` and
`sandbox_mode = "danger-full-access"`. Do not migrate to Codex permission
profiles or add active `default_permissions` without an explicit policy
decision that updates installer, doctor, contracts, docs, and validators in one
change.

## Validation

```bash
python3 scripts/validate_contract.py
python3 scripts/validate_instruction_docs.py
python3 scripts/validate_agent_tools.py
```
