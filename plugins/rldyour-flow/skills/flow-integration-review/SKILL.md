---
name: flow-integration-review
description: Integration synchronization reviewer workflow for ry-start and ry-review. Use for cross-module contracts, API/data/schema/config synchronization, migrations, generated types, route-client alignment, проверь синхронизацию кода, проверь интеграции, все ли связано, не сломаны ли контракты. Read-only by default and suitable for subagent prompts.
---

# Flow Integration Review

Review whether all touched layers remain synchronized:

- API route, client, DTO, schema, validation, service, repository, database.
- Config, env vars, docs, deploy notes, migrations.
- Generated code and type contracts.
- Backward compatibility and integration points.

Trace references with Serena and report concrete mismatch risks. Do not modify files.

