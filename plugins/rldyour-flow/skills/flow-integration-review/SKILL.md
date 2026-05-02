---
name: flow-integration-review
description: "Orchestrated integration review for ry-start/ry-review. Use explicitly for contracts, schemas, configs, generated types; триггеры: интеграции, синхронизация кода."
---

# Flow Integration Review

Review whether all touched layers remain synchronized:

- API route, client, DTO, schema, validation, service, repository, database.
- Config, env vars, docs, deploy notes, migrations.
- Generated code and type contracts.
- Backward compatibility and integration points.

Trace references with Serena and report concrete mismatch risks. Do not modify files.
