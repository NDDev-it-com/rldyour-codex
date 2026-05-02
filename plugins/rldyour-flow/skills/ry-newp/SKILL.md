---
name: ry-newp
description: "Plan a new project with skeptical questions, research, architecture docs, and optional scaffold after approval. Use for ry-newp, new project, новый проект, ТЗ, проект с нуля."
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

## Output

Produce English project documents and Russian user-facing summaries.

Default docs: HLO, requirements, architecture, ADRs, tech stack, API, data, infra, security, testing, structure, conventions, delivery plan.
