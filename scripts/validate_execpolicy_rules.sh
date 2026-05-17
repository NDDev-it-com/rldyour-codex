#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

RULE_DIR=${1:-system/rules}
CODEX_CMD=${CODEX_BIN:-$(command -v codex 2>/dev/null || true)}

if [ -z "$CODEX_CMD" ]; then
  printf 'codex command not found; cannot validate execpolicy rules.\n' >&2
  exit 1
fi

if [ ! -d "$RULE_DIR" ]; then
  printf 'rules directory not found: %s\n' "$RULE_DIR" >&2
  exit 1
fi

rule_args=()
while IFS= read -r rule_file; do
  rule_args+=(--rules "$rule_file")
done < <(find "$RULE_DIR" -maxdepth 1 -type f -name '*.rules' -print | sort)

if [ "${#rule_args[@]}" -eq 0 ]; then
  printf 'no .rules files found in %s\n' "$RULE_DIR" >&2
  exit 1
fi

check_decision() {
  local expected=$1
  shift
  local output decision

  output=$("$CODEX_CMD" execpolicy check --pretty "${rule_args[@]}" -- "$@")
  decision=$(printf '%s' "$output" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("decision", "allow"))')
  if [ "$decision" != "$expected" ]; then
    printf 'execpolicy decision mismatch for:' >&2
    printf ' %q' "$@" >&2
    printf '\nexpected: %s\nactual: %s\n%s\n' "$expected" "$decision" "$output" >&2
    exit 1
  fi
  printf 'ok      execpolicy %s:' "$expected"
  printf ' %q' "$@"
  printf '\n'
}

# This validates the literal token used by Codex rules.
# shellcheck disable=SC2088
literal_ssh_rsa='~/.ssh/id_rsa'

check_decision forbidden rm -rf /
check_decision forbidden git push --force origin main
check_decision forbidden cat "$literal_ssh_rsa"
check_decision prompt git reset --hard HEAD
check_decision prompt git clean -fdx
check_decision prompt cat .env
check_decision prompt gh release create v0.3.1
check_decision prompt wrangler deploy
check_decision allow git status
check_decision allow rm -rf /tmp/rldyour-codex-smoke
check_decision allow cat .env.example

printf '\nExecpolicy rules validation passed: %s files.\n' "$((${#rule_args[@]} / 2))"
