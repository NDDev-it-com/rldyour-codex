# rldyour-serena-mcp

`rldyour-serena-mcp` defines the Serena-specific workflow layer for Codex.

It does not start or configure the Serena MCP server directly. The MCP transport belongs to `rldyour-mcps`; this plugin defines how Codex should use Serena once the server is available.

## Auto Invocation

The plugin is optimized for automatic Serena skill selection. Codex should route code work to these skills when a task asks to inspect, index, explore, understand, map, edit, refactor, review, or trace repository code, directories, files, symbols, call sites, dependencies, architecture, or implementation scope. Codex should route knowledge maintenance to `serena-memory-sync` after meaningful changes, commits, Stop hook prompts, stale-memory markers, or explicit memory-sync requests.

Read-only init, context discovery, report-only review, exploratory debugging, log audit, and current-status snapshot workflows must not write Serena memories by default. They may report memory candidates and wait for explicit permission.

`policy.allow_implicit_invocation` is enabled for every skill. The primary trigger surface is each `SKILL.md` frontmatter `description`; plugin manifest descriptions and `agents/openai.yaml` metadata mirror the same intent for marketplace and UI discovery.

## Scope

- Prefer Serena MCP for semantic code inspection, repository exploration, symbol search, reference tracing, and structured edits.
- Keep `.serena/memories` fact-only, high-signal, and synchronized with verified code state.
- Store durable non-trivial plans in `.serena/plans`.
- Store long source-backed research summaries in `.serena/research`.
- Track Serena knowledge normally on `main` as ordinary source; `rldyour-flow` owns scoped project initialization.
- Keep generated local Serena runtime markers and cache files out of commits; they stay gitignored.
- Treat agent instruction and workflow files as project knowledge for freshness checks, so `AGENTS.md`, `.serena/*`, `.claude/*`, `.codex/*`, `.cursor/rules/*`, or `.agents/*` are read directly from the tracked `main` tree.

## Skills

- `serena-code-workflow`: Serena-first code reading and editing workflow.
- `serena-memory-sync`: fact-only `.serena` knowledge synchronization.

## Trigger Map

- Code inspection, indexing, exploration, symbol search, reference tracing, refactors, implementation planning, or non-trivial code edits: use `serena-code-workflow`.
- Meaningful verified changes, plugin workflow changes, commit-like changes, Stop hook sync prompts, stale memories, explicit memory-sync requests, durable plans, or reusable research archives: use `serena-memory-sync`.

## Hooks

The plugin includes lifecycle hooks for:

- `UserPromptSubmit`: add a concise Serena-first reminder for code tasks.
- `PreToolUse` / `PostToolUse`: mark project knowledge as stale after git commit-like changes.
- `Stop`: continue the current turn with a Serena memory sync prompt when project knowledge is stale.

The Stop hook routes memory refresh work to the managed Codex `serena-sync` subagent when delegation is allowed, or to the main `serena-memory-sync` workflow as a fallback. The sync keeps `.serena/memories/*.md` in the numbered taxonomy and enforces source-of-truth-only updates.

The Stop hook requires a fresh `serena_memory_state.py` state check and uses a loop guard so it does not re-prompt for the same stale HEAD.

Use `serena-memory-sync` for durable `.serena/` updates in the current task and, for large updates, delegate the audit/update pass to the managed Codex `serena-sync` subagent.

## Memory Quality Target

Memory files are not chat logs or summaries of intent. They are compact implementation maps for future Codex sessions. A good memory tells the model what exists, where the source of truth is, how the area behaves, which invariants must not break, how to change it safely, and how to verify the result. Use `AREA-01-SLUG.md` naming with `CORE-01-INDEX.md` as the map.
