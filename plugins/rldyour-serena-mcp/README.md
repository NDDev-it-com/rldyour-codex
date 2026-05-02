# rldyour-serena-mcp

`rldyour-serena-mcp` defines the Serena-specific workflow layer for Codex.

It does not start or configure the Serena MCP server directly. The MCP transport belongs to `rldyour-mcps`; this plugin defines how Codex should use Serena once the server is available.

## Auto Invocation

The plugin is optimized for automatic Serena skill selection. Codex should route code work to these skills when a task asks to inspect, index, explore, understand, map, edit, refactor, review, or trace repository code, directories, files, symbols, call sites, dependencies, architecture, or implementation scope. Codex should route knowledge maintenance to `serena-memory-sync` after meaningful changes, commits, Stop hook prompts, or durable decisions that future sessions need.

`policy.allow_implicit_invocation` is enabled for every skill. The primary trigger surface is each `SKILL.md` frontmatter `description`; plugin manifest descriptions and `agents/openai.yaml` metadata mirror the same intent for marketplace and UI discovery.

## Scope

- Prefer Serena MCP for semantic code inspection, repository exploration, symbol search, reference tracing, and structured edits.
- Keep `.serena/memories` fact-only, high-signal, and synchronized with verified code state.
- Store durable non-trivial plans in `.serena/plans`.
- Store long source-backed research summaries in `.serena/research`.
- Keep generated local Serena project files, runtime markers, and cache files out of commits. `rldyour-flow` owns scoped project initialization; promote Serena project config to portable repository state only when the owner explicitly wants that behavior.

## Skills

- `serena-code-workflow`: Serena-first code reading and editing workflow.
- `serena-memory-sync`: fact-only `.serena` knowledge synchronization.

## Trigger Map

- Code inspection, indexing, exploration, symbol search, reference tracing, refactors, implementation planning, or non-trivial code edits: use `serena-code-workflow`.
- Meaningful verified changes, plugin workflow changes, commit-like changes, Stop hook sync prompts, stale memories, durable plans, or reusable research archives: use `serena-memory-sync`.

## Hooks

The plugin includes lifecycle hooks for:

- `UserPromptSubmit`: add a concise Serena-first reminder for code tasks.
- `PreToolUse` / `PostToolUse`: mark project knowledge as stale after git commit-like changes.
- `Stop`: continue the current turn with a Serena memory sync prompt when project knowledge is stale.

The Stop hook does not spawn a separate sync agent. It asks the current Codex session to run `serena-memory-sync`, then optionally auto-commit knowledge-only changes through `scripts/commit_serena_knowledge.sh`.

## Memory Quality Target

Memory files are not chat logs or summaries of intent. They are compact implementation maps for future Codex sessions. A good memory tells the model what exists, where the source of truth is, how the area behaves, which invariants must not break, how to change it safely, and how to verify the result.
