---
name: cmux-worker
description: "Описывает worker role внутри macOS cmux orchestrator: scoped work, JSON report, без push/fullrepo/system install/project policy mutation. EN: cmux worker role."
---

# cmux-worker

## Purpose

Run a bounded worker task delegated by the cmux orchestrator.

## Worker Rules

- Work only inside explicitly assigned file/directory scope.
- Do not talk to the user as the primary respondent.
- Do not push, force-push, delete branches, publish fullrepo, install system configs, mutate project policy, or run final flow sync.
- Do not commit unless the orchestrator explicitly delegates commit permission for the task ID.
- If assigned scope is unclear or dirty files are outside scope, stop and report.

## Completion Signal

The orchestrator exports `RLDYOUR_TASK_ID` and `RLDYOUR_WORKER_ALLOWED_PATHS` at
delegation time; an empty `RLDYOUR_WORKER_ALLOWED_PATHS` means no delegated
write scope. Finish every task with both signals:

1. The JSON report (file path below when requested; create the directory on demand).
2. `cmux notify --title "worker ${RLDYOUR_WORKER_ID}" --body "task ${RLDYOUR_TASK_ID} exit <code>"`
   with the real exit code, because cmux emits no per-command exit-code event.

## Report

Return this JSON plus concise notes:

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

Runtime report files, when requested, go under `.serena/cache/cmux-orchestrator/<workspace-id>/<task-id>.json` and must not be committed.
