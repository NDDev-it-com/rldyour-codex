#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel)
GUARD="$ROOT/plugins/rldyour-flow/scripts/local_git_ai_guard.sh"
TMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-local-guard-smoke.XXXXXX")

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

fail() {
  printf 'fail    %s\n' "$1" >&2
  exit 1
}

ok() {
  printf 'ok      %s\n' "$1"
}

run_guard_expect() {
  local label=$1
  local expected_exit=$2
  local stdin_payload=$3
  local expected_text=${4:-}
  local fullrepo_branch=${5:-fullrepo}
  local output
  local status

  set +e
  output=$(cd "$TMP_ROOT/repo" && printf '%s\n' "$stdin_payload" | RLDYOUR_FULLREPO_BRANCH="$fullrepo_branch" bash "$GUARD" 2>&1)
  status=$?
  set -e

  if [ "$status" -ne "$expected_exit" ]; then
    printf '%s\n' "$output" >&2
    fail "$label exit $status, expected $expected_exit"
  fi
  if [ -n "$expected_text" ] && ! printf '%s' "$output" | grep -F "$expected_text" >/dev/null; then
    printf '%s\n' "$output" >&2
    fail "$label did not include expected text: $expected_text"
  fi
  ok "$label"
}

git init -q "$TMP_ROOT/repo"
git -C "$TMP_ROOT/repo" config user.email "local-guard-smoke@example.invalid"
git -C "$TMP_ROOT/repo" config user.name "Local Guard Smoke"

printf '# Fixture\n' > "$TMP_ROOT/repo/README.md"
git -C "$TMP_ROOT/repo" add README.md
git -C "$TMP_ROOT/repo" commit -q -m "chore: initial fixture"
base=$(git -C "$TMP_ROOT/repo" rev-parse HEAD)

printf 'Codex project instructions\n' > "$TMP_ROOT/repo/AGENTS.md"
git -C "$TMP_ROOT/repo" add AGENTS.md
git -C "$TMP_ROOT/repo" commit -q -m "docs: add agent context"
agent_commit=$(git -C "$TMP_ROOT/repo" rev-parse HEAD)

run_guard_expect \
  "product branch blocks agent-only path" \
  1 \
  "refs/heads/main ${agent_commit} refs/heads/main ${base}" \
  "blocked agent-only path"

run_guard_expect \
  "fullrepo allows agent docs with advisory marker warning" \
  0 \
  "refs/heads/fullrepo ${agent_commit} refs/heads/fullrepo ${base}" \
  "AI-context markers allowed"

mkdir -p "$TMP_ROOT/repo/.serena/memories"
printf 'Bearer token placeholder only\n' > "$TMP_ROOT/repo/.serena/memories/WORDING.md"
git -C "$TMP_ROOT/repo" add .serena/memories/WORDING.md
git -C "$TMP_ROOT/repo" commit -q -m "docs: add safe security wording"
wording_commit=$(git -C "$TMP_ROOT/repo" rev-parse HEAD)

run_guard_expect \
  "fullrepo warns on suspicious wording without blocking" \
  0 \
  "refs/heads/fullrepo ${wording_commit} refs/heads/fullrepo ${agent_commit}" \
  "warning: suspicious security wording"

printf '%s%s\n' 'Bearer ' 'abcdefghijklmnopqrstuvwxyz123456' > "$TMP_ROOT/repo/.serena/memories/SECRET.md"
git -C "$TMP_ROOT/repo" add .serena/memories/SECRET.md
git -C "$TMP_ROOT/repo" commit -q -m "docs: add unsafe token fixture"
secret_commit=$(git -C "$TMP_ROOT/repo" rev-parse HEAD)

run_guard_expect \
  "fullrepo blocks definite secret" \
  1 \
  "refs/heads/fullrepo ${secret_commit} refs/heads/fullrepo ${wording_commit}" \
  "blocked secret-looking content"

git -C "$TMP_ROOT/repo" reset -q --hard "$wording_commit"
mkdir -p "$TMP_ROOT/repo/.serena"
printf 'runtime marker\n' > "$TMP_ROOT/repo/.serena/.sync_marker"
git -C "$TMP_ROOT/repo" add -f .serena/.sync_marker
git -C "$TMP_ROOT/repo" commit -q -m "test: add runtime marker"
runtime_commit=$(git -C "$TMP_ROOT/repo" rev-parse HEAD)

run_guard_expect \
  "fullrepo blocks runtime marker" \
  1 \
  "refs/heads/fullrepo ${runtime_commit} refs/heads/fullrepo ${wording_commit}" \
  "blocked runtime/local-only path"

git -C "$TMP_ROOT/repo" reset -q --hard "$base"
printf 'Product change\n' >> "$TMP_ROOT/repo/README.md"
git -C "$TMP_ROOT/repo" add README.md
git -C "$TMP_ROOT/repo" commit -q -m "docs: update product readme"
product_commit=$(git -C "$TMP_ROOT/repo" rev-parse HEAD)

run_guard_expect \
  "mixed push checks product and fullrepo refs separately" \
  0 \
  "refs/heads/main ${product_commit} refs/heads/main ${base}
refs/heads/fullrepo ${agent_commit} refs/heads/fullrepo ${base}" \
  "AI-context markers allowed"

run_guard_expect \
  "custom fullrepo branch env is honored" \
  0 \
  "refs/heads/ai-context ${agent_commit} refs/heads/ai-context ${base}" \
  "AI-context markers allowed" \
  "ai-context"

zeros=0000000000000000000000000000000000000000

git init -q "$TMP_ROOT/install-repo"
mkdir -p "$TMP_ROOT/install-repo/.git/hooks"
cat > "$TMP_ROOT/install-repo/.git/hooks/pre-push" <<'EOF_PREVIOUS'
#!/usr/bin/env bash
set -euo pipefail
if read -r local_ref local_sha remote_ref remote_sha; then
  printf 'previous hook received %s %s %s %s\n' "$local_ref" "$local_sha" "$remote_ref" "$remote_sha" >&2
fi
EOF_PREVIOUS
chmod +x "$TMP_ROOT/install-repo/.git/hooks/pre-push"

"$ROOT/scripts/install_local_git_hooks.sh" --repo "$TMP_ROOT/install-repo" --apply >/dev/null
[ -x "$TMP_ROOT/install-repo/.git/hooks/_local_guard_ai.sh" ] || fail "installer did not write local guard wrapper"
[ -x "$TMP_ROOT/install-repo/.git/hooks/pre-push.rldyour-previous" ] || fail "installer did not preserve previous pre-push"

set +e
installer_output=$(cd "$TMP_ROOT/install-repo" && printf 'refs/heads/main %s refs/heads/main %s\n' "$zeros" "$zeros" | .git/hooks/pre-push 2>&1)
installer_status=$?
set -e
[ "$installer_status" -eq 0 ] || fail "installed pre-push exited $installer_status"
printf '%s' "$installer_output" | grep -F "previous hook received" >/dev/null || fail "installed pre-push did not replay stdin to previous hook"
ok "installer preserves and chains existing pre-push"

printf 'Local Git guard smoke passed.\n'
