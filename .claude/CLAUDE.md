# rldyour-codex Claude Code Project Memory

## Purpose

This file is the Claude Code-native project memory for the `rldyour-codex`
adapter. The product runtime remains Codex-native; Claude Code uses this file
only to understand repository boundaries, validation gates, and Git workflow.

## Source Of Truth

- `AGENTS.md`: primary Codex-native project instructions.
- `config/rldyour-contract.json`: adapter contract, runtime baseline, native
  surfaces, MCP mapping, hooks, and managed-agent policy.
- `.agents/plugins/marketplace.json`: Codex plugin marketplace.
- `plugins/*/.codex-plugin/plugin.json`: plugin manifests and versions.
- `plugins/*/skills/*/SKILL.md`: skill instructions and Russian-first routing
  descriptions.
- `plugins/*/skills/*/agents/openai.yaml`: OpenAI skill metadata.
- `plugins/rldyour-mcps/.mcp.json`: source MCP definitions.
- `VERSION` and `CHANGELOG.md`: public adapter release version and history.
- `.github/workflows/*.yml`: public/free GitHub Actions release and validation
  workflows.
- `.serena/memories/*.md`: fullrepo-only durable memory, subordinate to code.

## Native Boundaries

- Do not convert Codex plugins, skills, hooks, managed agents, or MCP runtime
  definitions into Claude slash-command formats.
- Codex flows are plugin skills; `.codex-plugin/plugin.json` and
  `.agents/plugins/marketplace.json` are the release surfaces.
- Codex MCP runtime materialization is TOML `[mcp_servers.*]`; source MCP
  policy lives in `plugins/rldyour-mcps/.mcp.json`.
- Flow owns Stop lifecycle ordering. Serena sync runs through Flow, not as a
  competing Stop hook.

## Validation

Run adapter-local gates after Codex adapter changes:

```bash
scripts/validate_marketplace.sh
scripts/validate_fast.sh
scripts/validate_runtime.sh --strict-runtime
scripts/validate_release.sh
scripts/validate_execpolicy_rules.sh
python3 scripts/codex_openai_metadata_policy.py --repo-root .
python3 scripts/validate_agent_tools.py
python3 scripts/validate_plugin_versions.py
python3 scripts/validate_contract.py
python3 scripts/validate_skill_routing.py
python3 scripts/validate_instruction_docs.py --require-agent-docs
python3 scripts/check_serena_memory_freshness.py
uv run --with pytest --with pytest-cov --with pyyaml python -m pytest
```

Runtime-only gates may require installed `codex`, `shellcheck`, `bunx`, `dart`,
and `github-mcp-server`.

## Git And Fullrepo

- Use atomic Conventional Commits for normal source changes.
- Do not force-push `main`.
- Keep agent-only context, including this file and `.serena/`, on `fullrepo`.
- Publish agent-only updates with `scripts/sync_fullrepo_branch.sh --publish`.
- Public adapter CI must use standard Ubuntu GitHub-hosted runners only unless
  the owner explicitly approves a future paid-risk policy exception.
