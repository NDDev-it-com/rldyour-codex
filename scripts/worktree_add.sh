#!/usr/bin/env bash
# worktree_add.sh — one-step git worktree creation for the rldyour-codex
# marketplace.
#
# Wraps `git worktree add`. Agent context (AGENTS.md, .claude/CLAUDE.md,
# .serena/project.yml, .serena/memories/**) is tracked normally on the branch,
# so a fresh worktree already carries it from the checked-out tree.
#
# Usage:
#   scripts/worktree_add.sh <branch> [path]
#
# Environment:
#   RLDYOUR_WORKTREE_BASE_REF   Ref used when creating a new branch.
#                               Default: origin/main. Set to HEAD to preserve
#                               unpushed local commits.
#   RLDYOUR_DRY_RUN=1           Print actions without executing them.

set -euo pipefail
IFS=$'\n\t'
unset CDPATH

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT}"

BRANCH="${1:-}"
EXPLICIT_PATH="${2:-}"

if [[ -z "${BRANCH}" ]]; then
  cat >&2 <<'EOF'
usage: scripts/worktree_add.sh <branch> [path]

Creates a git worktree that is immediately usable for a parallel Codex session.
Agent context is tracked on the branch, so it is present in the new worktree.
EOF
  exit 2
fi

if ! [[ "${BRANCH}" =~ ^[A-Za-z0-9._/-]{1,255}$ ]]; then
  echo "FAIL invalid branch name '${BRANCH}' — must match ^[A-Za-z0-9._/-]{1,255}$" >&2
  exit 1
fi

if ! git check-ref-format --branch "${BRANCH}" >/dev/null 2>&1; then
  echo "FAIL branch name '${BRANCH}' rejected by git check-ref-format" >&2
  exit 1
fi

BASE_REF="${RLDYOUR_WORKTREE_BASE_REF:-origin/main}"
DRY_RUN="${RLDYOUR_DRY_RUN:-0}"

if [[ -n "${EXPLICIT_PATH}" ]]; then
  WT_PATH="${EXPLICIT_PATH}"
else
  REPO_NAME="$(basename "${ROOT}")"
  SAFE_BRANCH="$(printf '%s' "${BRANCH}" | tr '/' '-')"
  WT_PATH="$(cd "${ROOT}/.." && pwd)/${REPO_NAME}-${SAFE_BRANCH}"
fi

WT_PATH="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "${WT_PATH}")"

if [[ -e "${WT_PATH}" ]]; then
  echo "FAIL worktree path already exists: ${WT_PATH}" >&2
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
  BRANCH_MODE="existing-local"
  GIT_ARGS=(worktree add -- "${WT_PATH}" "${BRANCH}")
elif git show-ref --verify --quiet "refs/remotes/origin/${BRANCH}"; then
  BRANCH_MODE="existing-remote"
  GIT_ARGS=(worktree add --track -b "${BRANCH}" -- "${WT_PATH}" "origin/${BRANCH}")
else
  BRANCH_MODE="new-from-${BASE_REF}"
  GIT_ARGS=(worktree add -b "${BRANCH}" -- "${WT_PATH}" "${BASE_REF}")
fi

echo "==> rldyour-codex worktree_add"
echo "    branch     : ${BRANCH} (${BRANCH_MODE})"
echo "    path       : ${WT_PATH}"
echo "    base ref   : ${BASE_REF}"
echo "    main root  : ${ROOT}"

if [[ "${DRY_RUN}" = "1" ]]; then
  printf '    [dry-run] would run: git'
  printf ' %q' "${GIT_ARGS[@]}"
  printf '\n'
  exit 0
fi

git "${GIT_ARGS[@]}"

cat <<EOF

==> worktree ready
    cd "${WT_PATH}"
    codex

The new worktree has its own working tree and carries agent context
(AGENTS.md, .claude/CLAUDE.md, .serena/) as tracked branch files.

To remove later:
    git worktree remove "${WT_PATH}"
EOF
