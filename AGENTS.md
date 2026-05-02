# rldyour-codex Agent Instructions

## Project Purpose

This repository is the owner's personal Codex marketplace. It owns rldyour plugins, skills, hooks, MCP runtime definitions, validation scripts, and Serena project knowledge for the local Codex runtime.

## Language And Documentation

- User-facing communication with the owner is Russian unless explicitly requested otherwise.
- Repository files are English: docs, plugin metadata, skills, scripts, comments, commits, Serena memories, plans, and research archives.
- Keep technical identifiers ASCII, stable, and kebab-case where applicable.

## Source Of Truth

- `.agents/plugins/marketplace.json`: active marketplace catalog.
- `plugins/<plugin>/.codex-plugin/plugin.json`: plugin manifest and linked capabilities.
- `plugins/<plugin>/skills/*/SKILL.md`: primary automatic skill routing contract.
- `plugins/<plugin>/skills/*/agents/openai.yaml`: UI metadata and implicit invocation policy.
- `plugins/rldyour-mcps/.mcp.json`: repository MCP runtime definitions.
- `/Users/rldyourmnd/.codex/config.toml`: active system Codex registration and MCP runtime config.
- `.serena/memories/*.md`: high-signal verified project knowledge.

## Plugin Boundaries

- `rldyour-mcps` owns MCP transport definitions only. It must not contain behavior policy or skills.
- `rldyour-serena-mcp` owns Serena-first code workflow, memory sync, and Serena lifecycle hooks.
- `rldyour-flow` owns SDLC commands and post-task synchronization hooks.
- `rldyour-rules` owns quality, architecture, dependency, verification, project-instruction, and ADR policy.
- `rldyour-explore`, `rldyour-browser`, `rldyour-design`, `rldyour-security`, and `rldyour-lsps` own their domain workflows and must not duplicate MCP transports.
- Curated `github@openai-curated` and `gmail@openai-curated` are intentionally enabled in system Codex.

## Development Rules

- Use `apply_patch` for manual file edits.
- Do not commit secrets, tokens, cookies, private keys, raw credentials, browser evidence, or Serena runtime markers.
- Use `plugin-creator` guidance for plugin manifests and marketplace changes.
- Use `skill-creator` guidance for skill changes.
- Use Serena-first code inspection where supported; use `rg` and direct reads for docs, JSON, shell scripts, and other text-level work.
- After meaningful changes, update `.serena/memories` with verified facts only.
- After plugin changes that affect runtime behavior, sync changed plugin directories into `/Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/<plugin>/local` and restart Codex.

## Validation

Run the marketplace validation script before finalizing repository changes:

```bash
scripts/validate_marketplace.sh
```

Additional targeted checks:

```bash
codex mcp list
python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool
plugins/rldyour-lsps/scripts/check_lsps.sh
```

For plugin cache verification:

```bash
diff -qr plugins/<plugin> /Users/rldyourmnd/.codex/plugins/cache/rldyour-codex/<plugin>/local
```

## Git And Sync

- Keep `main` synchronized with `origin/main` unless working on an explicit branch or worktree workflow.
- Prefer atomic commits with Conventional Commits.
- Use `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh` for knowledge-only Serena updates.
- Before final delivery, ensure `git status -sb` is clean and pushed when the task produced commits.

