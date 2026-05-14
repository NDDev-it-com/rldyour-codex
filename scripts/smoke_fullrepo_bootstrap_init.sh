#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel 2>/dev/null); then
  :
else
  ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
fi

FULLREPO_SCRIPT="$ROOT/plugins/rldyour-flow/scripts/fullrepo_sync.py"
TMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-fullrepo-bootstrap.XXXXXX")

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

REMOTE="$TMP_ROOT/origin.git"
WORK="$TMP_ROOT/work"
CLONE="$TMP_ROOT/clone"

git init --bare --quiet "$REMOTE"
git clone --quiet "$REMOTE" "$WORK"

(
  cd "$WORK"
  git config user.email "rldyour-codex@example.invalid"
  git config user.name "rldyour Codex Smoke"
  git checkout -b main >/dev/null 2>&1
  mkdir -p .claude .serena/memories src
  printf 'product\n' > src/app.txt
  git add src/app.txt
  git commit --quiet -m "chore: seed product"
  git push --quiet -u origin main

  printf '# Project Agent Instructions\n\nCodex Validation Git\n' > AGENTS.md
  printf '# Claude Code Project Memory\n\nClaude Code Validation Git\n' > .claude/CLAUDE.md
  printf '# Memory\n' > .serena/memories/CORE_01_project.md
  python3 "$FULLREPO_SCRIPT" --bootstrap-init

  git ls-remote --exit-code --heads origin fullrepo >/dev/null
  git check-ignore -q AGENTS.md
  git check-ignore -q .claude/CLAUDE.md
  git check-ignore -q .serena/memories/CORE_01_project.md
  test -z "$(git status --porcelain --untracked-files=all -- src/app.txt)"
)

git clone --quiet --branch main "$REMOTE" "$CLONE"
(
  cd "$CLONE"
  test ! -e AGENTS.md
  test ! -e .claude/CLAUDE.md
  test ! -e .serena/memories/CORE_01_project.md
  python3 "$FULLREPO_SCRIPT" --bootstrap-init
  test -f AGENTS.md
  test -f .claude/CLAUDE.md
  test -f .serena/memories/CORE_01_project.md
  git check-ignore -q AGENTS.md
  git check-ignore -q .claude/CLAUDE.md
  git check-ignore -q .serena/memories/CORE_01_project.md
)

TRACKED="$TMP_ROOT/tracked"
git clone --quiet "$REMOTE" "$TRACKED"
(
  cd "$TRACKED"
  git checkout --quiet main
  git config user.email "rldyour-codex@example.invalid"
  git config user.name "rldyour Codex Smoke"
  mkdir -p .claude
  printf '# Tracked Agent Instructions\n' > AGENTS.md
  printf '# Tracked Claude Instructions\n' > .claude/CLAUDE.md
  git add -f AGENTS.md .claude/CLAUDE.md
  git commit --quiet -m "chore: accidentally track agent docs"

  python3 "$FULLREPO_SCRIPT" --bootstrap-init
  if git ls-files | grep -qE '^(AGENTS.md|\.claude/CLAUDE.md)$'; then
    echo "tracked agent-only file remained in current branch index" >&2
    exit 1
  fi
  test -f AGENTS.md
  test -f .claude/CLAUDE.md
  git check-ignore -q AGENTS.md
  git check-ignore -q .claude/CLAUDE.md
  git diff --cached --name-status | grep -q '^D[[:space:]]\+AGENTS.md$'
  git diff --cached --name-status | grep -q '^D[[:space:]]\+\.claude/CLAUDE.md$'
)

printf 'Fullrepo bootstrap init smoke passed.\n'
