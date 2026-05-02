---
name: flow-consistency-review
description: Consistency reviewer workflow for ry-start and ry-review. Use for naming, style, imports, file placement, project conventions, public API shape, error format, проверь консистентность, проверь стиль, проверь нейминг, соответствует ли паттернам проекта. Read-only by default and suitable for subagent prompts.
---

# Flow Consistency Review

First establish project baseline from nearby existing code, `AGENTS.md`, `CLAUDE.md`, and memories. Then compare changed code against that baseline.

Report deviations from project conventions only, not personal style preferences. Do not modify files.

