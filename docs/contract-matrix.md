# rldyour Codex Contract Matrix

This repository is the Codex adapter for the rldyour automation system. The
machine-readable contract is `config/rldyour-contract.json`; this document is
the human-readable matrix for the same facts.

## Adapter Surface

| Area | Codex contract |
| --- | --- |
| Public repository | `https://github.com/NDDev-it-com/rldyour-codex` |
| License | `AGPL-3.0-or-later` |
| Marketplace plugins | 9 local `rldyour-*` plugins |
| Skills | 38 `SKILL.md` files |
| Slash commands | 0 by design; Codex uses skills and managed subagents |
| Managed subagents | 8 TOML roles under `system/agents/` |
| Hook manifests | `rldyour-flow` and `rldyour-serena-mcp` |
| MCP profile | 12 servers from `plugins/rldyour-mcps/.mcp.json` |
| Plugin cache layout | `${CODEX_HOME}/plugins/cache/rldyour-codex/<plugin>/<version>` |

## Canonical Agent Roles

| Canonical role ID | Codex role |
| --- | --- |
| `agent.explore.research` | `research-explorer` |
| `agent.review.architecture` | `architecture-reviewer` |
| `agent.review.browser` | `browser-tester` |
| `agent.review.consistency` | `consistency-reviewer` |
| `agent.review.quality` | `quality-reviewer` |
| `agent.review.security` | `security-audit` |
| `agent.review.verification` | `test-reviewer` |
| `agent.sync.serena-memory` | `serena-sync` |

## Hook Lifecycle Mapping

Codex bundled plugin hooks require `[features].plugin_hooks = true`. Hook
handlers are command handlers and resolve plugin-owned scripts through
`PLUGIN_ROOT`.

| Lifecycle contract | Plugin | Codex event | Script |
| --- | --- | --- | --- |
| `prompt.submit.sync-required` | `rldyour-serena-mcp` | `UserPromptSubmit` | `hooks/user_prompt_submit.sh` |
| `session.start.context` | `rldyour-flow` | `SessionStart` | `hooks/session_start_dispatcher.sh` |
| `tool.pre.git-policy` | `rldyour-serena-mcp` | `PreToolUse` | `hooks/prepare_auto_sync.sh` |
| `tool.pre.env-protection` | `rldyour-flow` | `PreToolUse` | `hooks/pre_tool_use_cwd_guard.sh` |
| `tool.post.sync-marker` | `rldyour-serena-mcp` | `PostToolUse` | `hooks/mark_sync_required.sh` |
| `tool.post.commit-advice` | `rldyour-flow` | `PostToolUse` | `hooks/post_tool_use_commit_advice.sh` |
| `task.stop.sync` | `rldyour-flow` | `Stop` | `hooks/stop_lifecycle_dispatcher.sh` |
| `task.stop.memory-sync` | `rldyour-serena-mcp` | dispatched by `task.stop.sync` | `hooks/stop_memory_sync.sh` |

## Security Contract

The maintainer standard profile is full-auto / YOLO:
`profile = "rldyour-yolo"`, `approval_policy = "never"`,
`sandbox_mode = "danger-full-access"`, and
`default_permissions = ":danger-no-sandbox"`. This is the default installer and
doctor contract. `--safe-mode` remains available only as an explicit
conservative override.

## Validation

Run:

```bash
python3 scripts/validate_contract.py
```

The validator compares this adapter contract against the real marketplace,
plugin manifests, skills, managed agents, hooks, MCP server profile, slash
command absence, and owner-standard full-auto policy.
