---
name: cmux-orchestrator
description: "Запускает macOS cmux orchestrator workflow: один user-facing orchestrator делегирует worker terminals, собирает отчеты, валидирует и синхронизирует. EN: cmux orchestrator, multi-agent terminal workflow."
---

# cmux-orchestrator

## Purpose

Run the rldyour macOS cmux orchestrator workflow. This skill is distinct from `ry-repair-orchestrator`: it is about multi-terminal task execution, not repair-skill orchestration.

## Preconditions

- Effective project policy has `execution.mode = "orchestrator"` and `cmux.enabled = true`.
- Target OS is macOS. Linux, WSL, and Windows use `standard` mode.
- cmux config is generated through `scripts/generate_cmux_config.py` or `/ry-repair --os macos --mode orchestrator --cmux`.

## Orchestrator Duties

1. Talk to the user; workers report to the orchestrator, not directly to the user.
2. Read project policy before planning.
3. Split work into scoped tasks with exact files/directories and allowed command classes.
4. Delegate only bounded work to workers.
5. Require worker reports in JSON shape:

```json
{
  "task_id": "...",
  "status": "pass|fail|blocked|not_proven",
  "files_changed": [],
  "commands_run": [],
  "findings": [],
  "risks": [],
  "needs_orchestrator_action": []
}
```

6. Review diffs, resolve conflicts, run final validation, and own commits/push/fullrepo/Serena sync when policy allows them.

## Worker Prompt Template

```markdown
You are a rldyour worker agent running under a cmux orchestrator.

Task ID: <task_id>
Repository: <repo_path>
Branch: <branch>
Project policy source: <policy_path_or_default>
Execution mode: orchestrator
Agent role: worker
Allowed files/directories: <exact list>
Forbidden actions: push, branch deletion, fullrepo publish, system install, project-policy mutation, commits unless explicitly delegated.
Allowed commands: <exact list or class>
Validation expected: <command or NOT_PROVEN>

Return a JSON report plus concise notes. Do not perform global sync.
```

## Non-Negotiables

- Do not use cmux nightly-only `actions` for the required path; stable config uses `commands`.
- Do not let workers run final sync, branch cleanup, fullrepo publish, system installers, or policy mutations unless explicitly delegated and policy allows it.
- Do not allow parallel writes to the same file.
