---
name: flow-integration-review
description: "Оркестрирует integration review для explicit ry-start review/ry-review: contracts, schemas, configs и generated types. EN: integration review, contract sync."
---

# Flow Integration Review

Review whether all touched layers remain synchronized:

- API route, client, DTO, schema, validation, service, repository, database.
- Config, env vars, docs, deploy notes, migrations.
- Generated code and type contracts.
- Backward compatibility and integration points.

Trace references with Serena and report concrete mismatch risks. Do not modify files.
