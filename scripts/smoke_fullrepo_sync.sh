#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel 2>/dev/null); then
  :
else
  ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
fi

FULLREPO_SCRIPT="$ROOT/plugins/rldyour-flow/scripts/fullrepo_sync.py"
TMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-fullrepo-smoke.XXXXXX")

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
  mkdir -p .serena/memories src
  printf 'product\n' > src/app.txt
  printf '# Project Agent Instructions\n' > AGENTS.md
  printf '# Claude Compatibility\n' > CLAUDE.md
  printf '# Memory\n' > .serena/memories/CORE_01_project.md
  git add .
  git commit --quiet -m "chore: seed project"
  git push --quiet -u origin main

  python3 "$FULLREPO_SCRIPT" --install-exclude
  python3 "$FULLREPO_SCRIPT" --publish
  git ls-remote --exit-code --heads origin fullrepo >/dev/null

  python3 "$FULLREPO_SCRIPT" --migrate-main
  git commit --quiet -m "chore: keep agent files in fullrepo"
  git push --quiet origin main

  git ls-files | grep -q '^src/app.txt$'
  if git ls-files | grep -qE '^(AGENTS.md|CLAUDE.md|\.serena/)'; then
    echo "agent-only files remained tracked in main" >&2
    exit 1
  fi
  test -f AGENTS.md
  test -f .serena/memories/CORE_01_project.md
  git check-ignore -q AGENTS.md
  git check-ignore -q .serena/memories/CORE_01_project.md
)

git clone --quiet --branch main "$REMOTE" "$CLONE"
(
  cd "$CLONE"
  test ! -e AGENTS.md
  test ! -e .serena/memories/CORE_01_project.md
  python3 "$FULLREPO_SCRIPT" --restore
  test -f AGENTS.md
  test -f CLAUDE.md
  test -f .serena/memories/CORE_01_project.md
  git check-ignore -q AGENTS.md
  git check-ignore -q .serena/memories/CORE_01_project.md
  python3 "$FULLREPO_SCRIPT" --status-json | python3 -m json.tool >/dev/null
)

printf 'Fullrepo sync smoke passed.\n'
