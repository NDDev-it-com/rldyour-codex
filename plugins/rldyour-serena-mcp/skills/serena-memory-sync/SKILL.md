---
name: serena-memory-sync
description: Fact-only Serena project knowledge maintenance. Use after meaningful code changes, after Stop hook sync prompts, after commits, or when auditing stale .serena/memories, .serena/plans, and .serena/research files. Code, git diff, and tests are the source of truth; update only verified facts.
---

# Serena Memory Sync

## Purpose

Keep `.serena/` useful for future Codex sessions without creating hallucinated project lore. Memories must explain what the code actually does, where it lives, and which conventions are verified from the repository.

User-facing conversation stays in Russian. All stored `.serena/` knowledge files are written in English.

## Stored Locations

- `.serena/memories/`: durable project facts, conventions, architecture notes, implementation facts, and task completion requirements.
- `.serena/plans/`: non-trivial implementation plans that are worth preserving across sessions.
- `.serena/research/`: complex or long research results with source links and implementation impact.

Local/runtime files must not be committed by this plugin: `.serena/cache/`, `.serena/.gitignore`, `.serena/project.yml`, `.serena/project.local.yml`, `.serena/.sync_marker`, `.serena/.serena_sync_state.json`, `.serena/.auto_sync_head`, `.serena/.active_workflow_intent.json`, `.serena/.dirty_stop_ack`.

## Memory Structure

Name memory files as `AREA_NN_slug.md`.

Default areas: `CORE`, `BACKEND`, `FRONTEND`, `MOBILE`, `INFRA`, `API`, `AUTH`, `DATA`, `SEC`, `TEST`, `DESIGN`, `CLI`, `MCP`.

Create custom area prefixes only when the project needs a clearer domain boundary. Keep files narrow and split large memories instead of creating broad catch-all files.

Every memory starts with exactly this metadata block:

```html
<!-- Memory Metadata
Last updated: YYYY-MM-DD
Last commit: <sha> <message>
Scope: <files/dirs>
Area: <AREA>
-->
```

Do not add subjective confidence fields or unsupported metadata. If a fact is unresolved, put it in the body as an explicit unresolved gap.

## Sync Workflow

1. Inspect git state: current HEAD, recent commits, changed files, and non-memory diffs.
2. Use Serena first: `list_memories`, `read_memory` for relevant files, then `get_symbols_overview`, targeted `find_symbol`, and `find_referencing_symbols` for changed code.
3. Update or create memory files with verified facts only. Remove or correct stale statements instead of preserving outdated text.
4. Save non-trivial plans to `.serena/plans/` only when they will help future sessions continue work.
5. Save long research summaries to `.serena/research/` only when the research was complex, source-backed, and likely reusable.
6. Keep exact paths, symbol names, commands, and behavior. Avoid generic advice.
7. Run `plugins/rldyour-serena-mcp/scripts/commit_serena_knowledge.sh` when this repository contains the plugin, or the absolute script path provided by the Stop hook when the plugin is loaded from Codex cache. Use it only when `.serena/memories`, `.serena/plans`, or `.serena/research` changed and the sync should be auto-committed.

## Quality Rules

Code is the source of truth. Never write a memory fact just because an old memory, plan, comment, or README says it.

Prefer small factual paragraphs over narratives. A future Codex session should be able to quickly answer: what exists, where it is implemented, what conventions apply, what was changed, and what checks matter.

Do not store secrets, tokens, private cookies, raw credentials, or sensitive runtime data.

Do not use `.serena/memories` as a backlog. Plans and TODOs belong in `.serena/plans` only when the plan is useful and current.

## Output

Report:

- `Freshness audit`: HEAD, newest synced commit, and changed scope.
- `Updated memories`: edited files.
- `New memories`: new files, if any.
- `Plans/research archived`: files written, if any.
- `Unresolved gaps`: anything that could not be verified from code.
- `Commit`: whether the Serena knowledge-only auto-commit was created.
