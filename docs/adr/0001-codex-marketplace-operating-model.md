# ADR 0001: Codex Marketplace Operating Model

## Status

Accepted.

## Date

2026-05-17.

## Context

`rldyour-codex` is the owner-controlled Codex marketplace and system-runtime repository. It owns plugin manifests, skills, MCP transport definitions, lifecycle hooks, managed subagent role files, install/doctor/rollback scripts, validation gates, and the portable `fullrepo` agent-context branch.

The repository has several durable decisions that were previously spread across `README.md`, `AGENTS.md`, `.claude/CLAUDE.md`, Serena memories, and validation scripts. These decisions affect future safety and must be preserved as architecture decisions rather than chat history.

## Decision

- Keep one domain per plugin. `rldyour-mcps` owns only MCP transport definitions; behavior belongs to domain plugins such as `rldyour-flow`, `rldyour-serena-mcp`, `rldyour-rules`, `rldyour-browser`, `rldyour-design`, `rldyour-explore`, `rldyour-lsps`, and `rldyour-security`.
- Load bundled plugin hooks through Codex plugin runtime variables, especially `PLUGIN_ROOT`; plugin hook commands must not resolve scripts from the session repository cwd or from hardcoded cache paths.
- Serialize dependent `SessionStart` behavior inside a single bounded Flow dispatcher when ordering matters, because Codex can launch multiple matching command hooks for the same event concurrently.
- Serialize dependent Stop lifecycle behavior inside Flow's ordered dispatcher: Serena memory gating runs first, and Flow post-task synchronization runs only after Serena is current.
- Keep agent-only context out of normal branches and publish it through the `fullrepo` branch with safe `--force-with-lease`.
- Treat Serena memories as operational fact knowledge and ADRs as durable architecture-decision authority. Memories may summarize decisions but should point back to ADRs when the decision is structural.
- Use GitHub-hosted Actions with least-privilege permissions and SHA-pinned external actions. CodeQL or repository-side secret scanning can be added only when the required GitHub Code Security / Secret Protection entitlement is confirmed.
- Treat Dart/Flutter MCP as an external local Dart SDK runtime exception unless a package-level pin becomes available in the Codex MCP registry.

## Consequences

- Hook safety is validated both by `scripts/smoke_hooks.sh` and by installed hook trust checks in `scripts/doctor_system_codex.sh`.
- Cross-plugin Stop hooks must not depend on Codex hook ordering. If another plugin needs ordered Stop behavior, it should be called by the lifecycle dispatcher or proven independent.
- New plugins, skills, hooks, MCP servers, and managed agents must update validators, smoke tests, docs, and Serena memories together.
- Architecture changes that affect plugin boundaries, hook loading, fullrepo behavior, MCP runtime policy, install canon, CI security posture, or cross-agent instruction policy require a new ADR or an update to this ADR.
- External action updates require resolving the upstream tag to a full commit SHA and preserving a comment with the human-readable tag for review.

## Alternatives Considered

- Keep decisions only in Serena memories. Rejected because memories are optimized for operational recall and freshness, not tradeoff history.
- Allow separate `SessionStart` hooks to depend on array order. Rejected because current Codex hook docs say matching command hooks for the same event are launched concurrently.
- Keep GitHub Actions pinned to version tags for Dependabot convenience. Rejected because GitHub's security guidance treats full commit SHA pinning as the immutable option.

## Verification

- `scripts/smoke_hooks.sh`
- `python3 scripts/validate_action_pins.py`
- `scripts/smoke_serena_memory_taxonomy.sh`
- `scripts/smoke_fullrepo_sync.sh`
- `scripts/sync_fullrepo_branch.sh --status`
- `scripts/doctor_system_codex.sh`

## Related Code Paths

- `.agents/plugins/marketplace.json`
- `plugins/rldyour-flow/hooks.json`
- `plugins/rldyour-flow/hooks/session_start_dispatcher.sh`
- `plugins/rldyour-flow/hooks/stop_lifecycle_dispatcher.sh`
- `plugins/rldyour-flow/scripts/fullrepo_sync.py`
- `plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py`
- `plugins/rldyour-mcps/.mcp.json`
- `config/mcp-runtime-versions.env`
- `.github/workflows/validate.yml`
- `.github/workflows/dependency-check.yml`
