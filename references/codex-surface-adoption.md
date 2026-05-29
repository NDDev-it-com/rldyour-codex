# Codex Surface Adoption

Verified: 2026-05-28

Source of truth:
- Runtime baseline: `references/codex-baseline.json`
- Runtime package pin: package metadata for `@openai/codex`
- Official changelog and config docs: `https://developers.openai.com/codex/`

## Decisions

| Surface | Introduced | Decision | Implementation | Validator |
| --- | --- | --- | --- | --- |
| `--profile` as primary selector | 0.134.0 | Adopted | Owner launcher and docs use `codex --profile rldyour-yolo`; installer writes `$CODEX_HOME/rldyour-yolo.config.toml` and `$CODEX_HOME/rldyour-safe.config.toml`. | `scripts/validate_contract.py` |
| Legacy `[profiles.*]` and `profile = "..."` rejected | 0.134.0 | Adopted | Installer, doctor, contracts, and instruction docs forbid legacy profile selectors. | `scripts/validate_instruction_docs.py` |
| Permission profiles not mixed with `sandbox_mode` | 0.134.0 docs | Adopted | Owner policy remains `approval_policy = "never"` plus `sandbox_mode = "danger-full-access"`; active `default_permissions` is absent. | `scripts/validate_contract.py` |
| MCP runtime config as TOML `[mcp_servers.*]` | current docs | Adopted | `.mcp.json` remains source metadata; installer materializes native TOML runtime config. | `scripts/validate_contract.py` |
| Plugin hook feature flag removed/default-enabled | 0.134.0 | Adopted | No `[features].plugin_hooks`; trusted hook state is verified through hook listing smoke tests. | `scripts/smoke_codex_hook_listing.py` |
| Read-only MCP tool concurrency via `readOnlyHint` | 0.134.0 | Operational | No config migration required; MCP servers keep native tool metadata. | `scripts/smoke_mcp_capabilities.sh` |
| Local conversation history search | 0.134.0 | Not applicable | This is user-facing CLI behavior and does not change repository config. | n/a |

## Owner Full-Auto Policy

The owner-standard Codex mode intentionally uses `approval_policy = "never"` and
`sandbox_mode = "danger-full-access"`. Do not migrate to beta permission
profiles or add active `default_permissions` without an explicit policy
decision that updates installer, doctor, contracts, docs, and validators in one
change.

## Validation

```bash
python3 scripts/validate_contract.py
python3 scripts/validate_instruction_docs.py
python3 scripts/validate_agent_tools.py
```
