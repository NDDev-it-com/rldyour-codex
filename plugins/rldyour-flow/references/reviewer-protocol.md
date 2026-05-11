# Reviewer Protocol

Reviewer tracks are designed to be run as parallel subagents when `ry-start` or `ry-review` explicitly invokes the review phase.

## Subagent Permission

The owner explicitly approved subagent usage for `ry-start` and `ry-review` review phases. Each spawned subagent must receive a self-contained prompt with task, scope, diff, constraints, expected output, and read-only status.

Managed rldyour reviewer roles are installed as Codex custom agents from `system/agents/*.toml` into `${CODEX_HOME:-$HOME/.codex}/agents/*.toml`. They must use `model = "gpt-5.5"` and `model_reasoning_effort = "medium"` so the parent workflow gets predictable reviewer behavior. If a parent workflow spawns an ad hoc review role that is not backed by a managed agent TOML file, set the spawn override to `model = "gpt-5.5"` and `reasoning_effort = "medium"`.

## Tracks

| Track | Skill | Focus |
| --- | --- | --- |
| Architecture | `flow-architecture-review` | boundaries, dependencies, module shape, data flow |
| Quality | `flow-quality-review` | correctness, hacks, tech debt, edge cases, error handling |
| Consistency | `flow-consistency-review` | conventions, naming, style, file placement, public API shape |
| Integration | `flow-integration-review` | cross-module synchronization, contracts, migrations, configs |
| Verification | `flow-verification-review` | tests, manual checks, browser/server evidence, quality gates |
| Security | `flow-security-review` | security-sensitive paths, OWASP, secrets, auth/authz, unsafe flows |

## Finding Format

Each finding must include:

- Severity: `critical`, `high`, `medium`, `low`.
- Confidence: `0-100`.
- Location: file and line when possible.
- Evidence: concrete code or behavior.
- Impact: what fails or becomes harder.
- Fix: actionable correction.
- Disposition: `must-fix`, `should-fix`, `defer`, or `false-positive`.

Do not report confidence below 30. Validate confidence 30-49 in the parent workflow before acting.

## Parent Integration

The parent workflow consolidates all findings, resolves contradictions with code evidence, fixes accepted findings, then reruns only the reviewer tracks that found problems.
