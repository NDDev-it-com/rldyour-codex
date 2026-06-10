---
name: tech-research
description: "Технический ресёрч библиотек и кода через Context7/DeepWiki/Grep MCP. Покрывает: исследуй интернет, documentation, best practices. Используй для: изучи библиотеку, исследуй фреймворк, найди официальную доку, найди production-паттерны кода, сравни реализации, разбери архитектуру, миграция версий, что изменилось. EN triggers: library API lookup, framework research, official docs, production code patterns, compare implementations, repo architecture, migration guide, breaking changes, since version, how does X library work."
---

# Tech Research

## Purpose

Help Codex understand the technical scope before implementation: requirements, versions, APIs, architectural constraints, real usage patterns, edge cases, risks, and verification. The goal is not to collect links; the goal is to make a more accurate engineering decision and then write clean code without workarounds.

User-facing conversation stays in Russian unless requested otherwise. API names, package names, commands, and error strings stay exact.

## Auto Invocation

Use this skill without waiting for an explicit `$tech-research` call when the request is technical and asks to:

- Research, investigate, study, look up, or verify a technical topic before implementation.
- Handle Russian prompts such as `исследуй интернет`, `изучи в интернете`, `посмотри документацию`, `найди лучшие практики`, `посмотри как это сделано`, or `изучи MCP` when the subject is technical.
- Inspect official docs for a library, framework, SDK, API, migration, configuration, or runtime behavior.
- Understand an open-source repository, feature architecture, design decision, data flow, or tradeoff.
- Find production GitHub usage patterns, parameters, error handling, or edge cases.
- Validate best practices, version-specific behavior, compatibility, or migration risks.
- Research OpenAI or Codex product behavior, configuration, plugins, skills, MCP, hooks, models, APIs, or migration guidance; use `openaiDeveloperDocs` first when available.

If the owner explicitly asks to research the internet for a technical implementation, run this Triple-MCP workflow first and add `web-research` for current/latest/source-backed web evidence beyond Context7, DeepWiki, and Grep.

## When To Use

Use this skill automatically when the task is technical and the user asks to research the internet, read documentation, inspect MCP sources, find GitHub patterns, understand open-source repository architecture, handle migrations, configure SDKs/APIs, or verify best practices.

If the request is not technical, use `web-research`. If a technical request needs fresh external sources beyond Context7, DeepWiki, and Grep, supplement the MCP research with normal web search.

## Workflow

1. Define scope: what is being implemented, which stack and versions matter, which files/modules may be affected, and which unknowns block a high-quality implementation.
2. Split questions into documentation/API, comparable repository architecture, real production patterns, edge cases, security, tests, migrations, and compatibility.
3. OpenAI/Codex docs: when the subject is OpenAI, Codex, models, APIs, plugins, skills, MCP, hooks, or Codex config, use `openaiDeveloperDocs` first. Use official OpenAI web pages only as fallback.
4. Context7: use for official library, framework, SDK, API, configuration, and migration documentation. Provide an exact library ID or version when known.
5. DeepWiki: use for public open-source repositories when the task requires repository structure, feature implementation details, architectural decisions, data flow, or tradeoffs.
6. Grep by Vercel: use for real GitHub patterns: how APIs are called in production, which parameters are commonly passed, how errors are handled, and which edge cases appear.
7. Synthesize the decision: which approach is selected, which alternatives are rejected, which constraints remain, and how this affects local code.
8. If the user requested implementation, move from research to code and verification instead of stopping at theory.

## Quality Rules

Prefer primary sources: official documentation, source code, release notes, specifications, and maintained repository READMEs. Use blogs and community answers only as secondary confirmation.

Compare findings with the current project code. Do not copy GitHub patterns blindly; verify that they fit the repository architecture, versions, security model, and style.

Separate source facts from engineering conclusions. If a conclusion is an inference, label it as a decision based on the found evidence.

Do not expose secrets, tokens, cookies, private URLs, or closed data. Do not add keys or local credentials to the repository.

If the needed MCP is unavailable in the current session, state the limitation, use the best available fallback, and continue.

## Output

For a standalone research answer, respond in Russian with a short structure:

- `Questions`: what was checked.
- `Findings`: facts that affect the decision.
- `Implementation decision`: selected approach and why it fits.
- `Risks`: edge cases, compatibility, security, and open questions.
- `Verification`: tests, commands, or manual checks needed.

If you immediately implement code, keep the report short: key research conclusions, what changed, how it was verified, and remaining risks.
