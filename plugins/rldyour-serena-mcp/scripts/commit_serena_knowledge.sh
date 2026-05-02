#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git repository" >&2
  exit 0
fi

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

KNOWLEDGE_PATTERN='^.. \.serena/(memories|plans|research)(/|$)'
RUNTIME_PATTERN='^.. \.serena/(\.sync_marker|\.serena_sync_state\.json|\.auto_sync_head|\.active_workflow_intent\.json|\.dirty_stop_ack)$'

STATUS=$(git status --porcelain 2>/dev/null | grep -vE "$RUNTIME_PATTERN" || true)
if [ -z "$STATUS" ]; then
  echo "No Serena knowledge changes to commit"
  exit 0
fi

UNEXPECTED=$(printf "%s\n" "$STATUS" | grep -vE "$KNOWLEDGE_PATTERN" || true)
if [ -n "$UNEXPECTED" ]; then
  echo "Refusing to auto-commit because non-Serena-knowledge changes exist:" >&2
  printf "%s\n" "$UNEXPECTED" >&2
  exit 1
fi

HEAD_SHORT=$(git rev-parse --short=7 HEAD 2>/dev/null || echo "unknown")

KNOWLEDGE_PATHS=()
for path in .serena/memories .serena/plans .serena/research; do
  if [ -e "$path" ]; then
    KNOWLEDGE_PATHS+=("$path")
  fi
done

if [ "${#KNOWLEDGE_PATHS[@]}" -eq 0 ]; then
  echo "No Serena knowledge directories exist"
  exit 0
fi

git add -- "${KNOWLEDGE_PATHS[@]}"
if git diff --cached --quiet -- "${KNOWLEDGE_PATHS[@]}"; then
  echo "No staged Serena knowledge changes to commit"
  exit 0
fi

git commit -m "chore(serena): sync project knowledge after ${HEAD_SHORT}"
rm -f .serena/.sync_marker .serena/.serena_sync_state.json .serena/.auto_sync_head
