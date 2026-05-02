#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

UV_BIN=${UV_BIN:-/opt/homebrew/bin/uv}
QUICK_VALIDATE=${QUICK_VALIDATE:-/Users/rldyourmnd/.codex/skills/.system/skill-creator/scripts/quick_validate.py}
CODEX_HOME_DIR=${CODEX_HOME:-/Users/rldyourmnd/.codex}
CACHE_ROOT=${CACHE_ROOT:-"$CODEX_HOME_DIR/plugins/cache/rldyour-codex"}

step() {
  printf '\n== %s ==\n' "$1"
}

step "JSON metadata"
jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json plugins/rldyour-mcps/.mcp.json plugins/rldyour-serena-mcp/hooks.json plugins/rldyour-flow/hooks.json

step "Skill frontmatter"
skill_count=0
while IFS= read -r skill_md; do
  skill_dir=$(dirname "$skill_md")
  "$UV_BIN" run --with pyyaml python "$QUICK_VALIDATE" "$skill_dir" >/dev/null
  printf 'valid %s\n' "$skill_dir"
  skill_count=$((skill_count + 1))
done < <(find plugins -path '*/skills/*/SKILL.md' -print | sort)
printf 'validated skills: %s\n' "$skill_count"

step "OpenAI skill metadata"
"$UV_BIN" run --with pyyaml python - <<'PY'
from pathlib import Path
import sys
import yaml

errors = []
count = 0
for path in sorted(Path("plugins").glob("rldyour-*/skills/*/agents/openai.yaml")):
    count += 1
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        errors.append(f"{path}: parse failed: {exc}")
        continue
    policy = data.get("policy") if isinstance(data, dict) else None
    if not isinstance(policy, dict):
        errors.append(f"{path}: missing policy object")
        continue
    if policy.get("allow_implicit_invocation") is not True:
        errors.append(f"{path}: policy.allow_implicit_invocation must be true")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print(f"validated OpenAI metadata files: {count}")
PY

step "Shell scripts"
shellcheck plugins/rldyour-serena-mcp/hooks/*.sh plugins/rldyour-serena-mcp/scripts/*.sh plugins/rldyour-flow/hooks/*.sh plugins/rldyour-flow/scripts/*.sh plugins/rldyour-lsps/scripts/*.sh scripts/*.sh

step "Python scripts"
python3 - <<'PY'
from pathlib import Path
import ast

paths = [
    Path("plugins/rldyour-serena-mcp/scripts/serena_memory_state.py"),
    Path("plugins/rldyour-flow/scripts/flow_post_task_state.py"),
]

for path in paths:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(f"syntax ok {path}")
PY

step "LSP health"
plugins/rldyour-lsps/scripts/check_lsps.sh

step "Serena memory state"
python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool >/dev/null

step "Flow post-task state"
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool >/dev/null

step "MCP registration"
codex mcp list >/dev/null

step "Plugin cache sync"
if [ -d "$CACHE_ROOT" ]; then
  for plugin_dir in plugins/rldyour-*; do
    plugin_name=$(basename "$plugin_dir")
    cache_dir="$CACHE_ROOT/$plugin_name/local"
    if [ ! -d "$cache_dir" ]; then
      printf 'missing cache directory: %s\n' "$cache_dir" >&2
      exit 1
    fi
    diff -qr "$plugin_dir" "$cache_dir" >/dev/null
    printf 'cache in sync %s\n' "$plugin_name"
  done
else
  printf 'cache root missing: %s\n' "$CACHE_ROOT" >&2
  exit 1
fi

step "Secret pattern scan"
if rg -n 'ctx7sk-[A-Za-z0-9-]+|ghp_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]{16,}|xox[baprs]-[A-Za-z0-9-]+|BEGIN (RSA|OPENSSH|PRIVATE) KEY|Bearer [A-Za-z0-9._-]+' .serena/memories plugins .agents AGENTS.md README.md scripts system; then
  printf 'Potential secret pattern detected\n' >&2
  exit 1
fi

step "Whitespace"
git diff --check

printf '\nMarketplace validation passed.\n'
