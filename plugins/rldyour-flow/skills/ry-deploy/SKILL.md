---
name: ry-deploy
description: "Deploy with local/GitHub/server sync, checks, logs, fixes, and memory/docs/git finalization. Use for ry-deploy, deploy server, задеплой, деплой на сервер, прод."
---

# ry-deploy

## Purpose

Synchronize local repository, GitHub, and server, then deploy safely with evidence. Automation is expected, but risky operations require code/log evidence and user questions with options.

## Workflow

1. Read deploy contract from `AGENTS.md`, then `CLAUDE.md`, then `.serena/deploy/*.md`.
2. Run `plugins/rldyour-flow/scripts/deploy_readiness.sh <server>` when available.
3. Verify local git state, open PR, checks, Serena memories, docs, and GitHub sync.
4. Inspect server baseline: git status, current commit, disk, logs before restart, process manager.
5. Sync code to server.
6. Run migrations only when readiness is clear.
7. Restart/build services.
8. Verify logs, tests, health checks, and critical behavior.
9. If anything fails, perform root cause analysis using server logs, code, and internet research. Fix-forward and redeploy. Ask the user with options for risky or ambiguous decisions.
10. DB rollback only when explicit rollback command and backup/restore point are verified.
11. Finish with `flow-post-task-sync`.

## No Fake Success

If auth, missing credentials, server access, or unavailable health checks prevent validation, state the limitation and what evidence was still collected.
