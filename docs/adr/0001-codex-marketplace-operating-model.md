# ADR 0001: Codex Marketplace Operating Model

## Status

Accepted.

Superseded in part (1.7.0): the `fullrepo` agent-context branch is retired. Agent context (`.serena/`, `AGENTS.md`, `.claude/`) is now tracked normally on `main` as ordinary source; there is no agent-only overlay, restore, or publish step.

## Date

2026-05-17.

## Context

`rldyour-codex` is the owner-controlled Codex marketplace and system-runtime repository. It owns plugin manifests, skills, MCP transport definitions, lifecycle hooks, managed subagent role files, install/doctor/rollback scripts, and validation gates. Agent context is tracked normally on `main` (see the 1.7.0 supersession note above; earlier revisions used a portable `fullrepo` agent-context branch).

The repository has several durable decisions that were previously spread across `README.md`, `AGENTS.md`, `.claude/CLAUDE.md`, Serena memories, and validation scripts. These decisions affect future safety and must be preserved as architecture decisions rather than chat history.

## Decision

- Keep one domain per plugin. `rldyour-mcps` owns only MCP transport definitions; behavior belongs to domain plugins such as `rldyour-flow`, `rldyour-serena-mcp`, `rldyour-rules`, `rldyour-browser`, `rldyour-design`, `rldyour-explore`, `rldyour-lsps`, and `rldyour-security`.
- Load bundled plugin hooks through Codex plugin runtime variables, especially `PLUGIN_ROOT`; plugin hook commands must not resolve scripts from the session repository cwd or from hardcoded cache paths.
- Serialize dependent `SessionStart` behavior inside a single bounded Flow dispatcher when ordering matters, because Codex can launch multiple matching command hooks for the same event concurrently.
- Serialize dependent Stop lifecycle behavior inside Flow's ordered dispatcher: Serena memory gating runs first, and Flow post-task synchronization runs only after Serena is current.
- Track agent context (`.serena/`, `AGENTS.md`, `.claude/`) normally on `main` as ordinary source; keep only runtime-local cache/state/markers gitignored. (Superseded the earlier rule that kept agent-only context out of normal branches and published it through a `fullrepo` branch.)
- Treat Serena memories as operational fact knowledge and ADRs as durable architecture-decision authority. Memories may summarize decisions but should point back to ADRs when the decision is structural.
- Use public GitHub-hosted Actions with least-privilege permissions and
  SHA-pinned external actions. CodeQL, dependency review, Gitleaks, and
  GitHub-native public repository secret scanning are part of the public adapter
  security baseline; live GitHub settings are validated from the private root
  control plane when an owner token is available.
- Treat Dart/Flutter MCP as an external local Dart SDK runtime exception unless a package-level pin becomes available in the Codex MCP registry.

## Consequences

- Hook safety is validated both by `scripts/smoke_hooks.sh` and by installed hook trust checks in `scripts/doctor_system_codex.sh`.
- Cross-plugin Stop hooks must not depend on Codex hook ordering. If another plugin needs ordered Stop behavior, it should be called by the lifecycle dispatcher or proven independent.
- New plugins, skills, hooks, MCP servers, and managed agents must update validators, smoke tests, docs, and Serena memories together.
- Architecture changes that affect plugin boundaries, hook loading, agent-context tracking, MCP runtime policy, install canon, CI security posture, or cross-agent instruction policy require a new ADR or an update to this ADR.
- External action updates require resolving the upstream tag to a full commit SHA and preserving a comment with the human-readable tag for review.

## Alternatives Considered

- Keep decisions only in Serena memories. Rejected because memories are optimized for operational recall and freshness, not tradeoff history.
- Allow separate `SessionStart` hooks to depend on array order. Rejected because current Codex hook docs say matching command hooks for the same event are launched concurrently.
- Keep GitHub Actions pinned to version tags for Dependabot convenience. Rejected because GitHub's security guidance treats full commit SHA pinning as the immutable option.

## Verification

- `scripts/smoke_hooks.sh`
- `python3 scripts/validate_action_pins.py`
- `scripts/smoke_serena_memory_taxonomy.sh`
- `scripts/doctor_system_codex.sh`

## Related Code Paths

- `.agents/plugins/marketplace.json`
- `plugins/rldyour-flow/hooks.json`
- `plugins/rldyour-flow/hooks/session_start_dispatcher.sh`
- `plugins/rldyour-flow/hooks/stop_lifecycle_dispatcher.sh`
- `plugins/rldyour-flow/scripts/flow_post_task_state.py`
- `plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py`
- `plugins/rldyour-mcps/.mcp.json`
- `config/mcp-runtime-versions.env`
- `.github/workflows/validate.yml`
- `.github/workflows/dependency-check.yml`
