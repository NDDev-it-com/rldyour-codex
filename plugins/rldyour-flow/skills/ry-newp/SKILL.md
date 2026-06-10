---
name: ry-newp
description: "Дизайн нового проекта: скептические вопросы, research, архитектура docs, опциональный scaffold после approval. Используй для: /rldyour-flow:ry-newp, новый проект, новый стартап, ТЗ, проект с нуля, спроектируй сервис. EN triggers: new project, design new project, brief intake, scaffold project, greenfield project, MVP design, architecture docs, project from scratch."
---

# ry-newp

## Purpose

Design a new project with enough rigor that implementation can start with clear architecture, technology choices, business logic, quality gates, and delivery plan.

## Workflow

1. Gather all provided context: prompt, docs, chats, requirements, screenshots, business constraints.
2. Ask skeptical Russian questions with options. Cover product scope, users, business logic, data, integrations, security, deployment, observability, tests, and constraints.
3. Research current best technologies and architecture patterns with `rldyour-explore`.
4. Write planning docs under `.serena/newproj/<project>/` using `references/flow-lifecycle.md`.
5. Ask for approval before creating any scaffold code.
6. If scaffold is approved, create the minimal useful project structure, commit atomically, and initialize Serena memories.

## Serena Memory Seeds

After scaffold approval and the first real commit, initialize Serena memories
from verified project facts only. At minimum seed `CONTEXT-01-CORE.md` for
current source-of-truth facts and `FUTURE-01-VISION.md` for future-shape
constraints. Propose ADR memories for non-obvious decisions, but do not write
ADR meaning without explicit owner approval.

## Output

Produce English project documents and Russian user-facing summaries.

Default docs: HLO, requirements, architecture, ADRs, tech stack, API, data, infra, security, testing, structure, conventions, delivery plan.
