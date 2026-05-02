#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME_DIR=${CODEX_HOME:-"$HOME/.codex"}

usage() {
  cat <<'EOF'
Usage: scripts/doctor_system_codex.sh [--codex-home PATH]

Checks whether the current machine matches the rldyour Codex system setup.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --codex-home)
      shift
      CODEX_HOME_DIR=${1:?--codex-home requires a path}
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel 2>/dev/null); then
  :
else
  ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
fi
SYSTEM_AGENTS="$ROOT/system/AGENTS.md"
INSTALLED_AGENTS="$CODEX_HOME_DIR/AGENTS.md"
CONFIG_PATH="$CODEX_HOME_DIR/config.toml"
CACHE_ROOT="$CODEX_HOME_DIR/plugins/cache/rldyour-codex"
CODEX_CMD=${CODEX_BIN:-$(command -v codex 2>/dev/null || true)}

FAILURES=0
WARNINGS=0

pass() {
  printf 'ok      %s\n' "$1"
}

warn() {
  WARNINGS=$((WARNINGS + 1))
  printf 'warn    %s\n' "$1" >&2
}

fail() {
  FAILURES=$((FAILURES + 1))
  printf 'fail    %s\n' "$1" >&2
}

section() {
  printf '\n== %s ==\n' "$1"
}

section "Files"
if [ -f "$INSTALLED_AGENTS" ]; then
  pass "$INSTALLED_AGENTS exists"
  if cmp -s "$SYSTEM_AGENTS" "$INSTALLED_AGENTS"; then
    pass "system AGENTS matches repository template"
  else
    fail "system AGENTS differs from repository template"
  fi
else
  fail "$INSTALLED_AGENTS missing"
fi

if [ -f "$CODEX_HOME_DIR/AGENTS.override.md" ]; then
  warn "$CODEX_HOME_DIR/AGENTS.override.md exists and overrides AGENTS.md"
else
  pass "no global AGENTS.override.md"
fi

if [ -f "$CONFIG_PATH" ]; then
  pass "$CONFIG_PATH exists"
else
  fail "$CONFIG_PATH missing"
fi

section "Config"
if [ -f "$CONFIG_PATH" ]; then
  export RLDYOUR_CODEX_CONFIG="$CONFIG_PATH"
  export RLDYOUR_REPO_ROOT="$ROOT"
  python3 <<'PY' || exit_code=$?
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

path = Path(os.environ["RLDYOUR_CODEX_CONFIG"])
repo_root = os.environ["RLDYOUR_REPO_ROOT"]
text = path.read_text(encoding="utf-8")

checks = []
checks.append(("codex_hooks enabled", re.search(r"(?ms)^\[features\]\s*(?:\n(?!\[).*)*^\s*codex_hooks\s*=\s*true\s*$", text) is not None))
checks.append(("marketplace source", f'source = "{repo_root}"' in text))
checks.append(("repo trusted", f'[projects."{repo_root}"]' in text and 'trust_level = "trusted"' in text))

try:
    import tomllib
    config_data = tomllib.loads(text)
except Exception:
    config_data = {}

checks.append(("yolo profile selected", config_data.get("profile") == "rldyour-yolo"))
checks.append(("approval policy never", config_data.get("approval_policy") == "never"))
checks.append(("sandbox danger full access", config_data.get("sandbox_mode") == "danger-full-access"))
checks.append(("default permissions danger no sandbox", config_data.get("default_permissions") == ":danger-no-sandbox"))
yolo_profile = (config_data.get("profiles") or {}).get("rldyour-yolo") or {}
checks.append(("profile rldyour-yolo approval policy", yolo_profile.get("approval_policy") == "never"))
checks.append(("profile rldyour-yolo sandbox", yolo_profile.get("sandbox_mode") == "danger-full-access"))
checks.append(("profile rldyour-yolo permissions", yolo_profile.get("default_permissions") == ":danger-no-sandbox"))

plugins = [
    "gmail@openai-curated",
    "github@openai-curated",
    "rldyour-mcps@rldyour-codex",
    "rldyour-explore@rldyour-codex",
    "rldyour-serena-mcp@rldyour-codex",
    "rldyour-security@rldyour-codex",
    "rldyour-browser@rldyour-codex",
    "rldyour-design@rldyour-codex",
    "rldyour-lsps@rldyour-codex",
    "rldyour-flow@rldyour-codex",
    "rldyour-rules@rldyour-codex",
]
for plugin in plugins:
    pattern = rf'(?ms)^\[plugins\."{re.escape(plugin)}"\]\s*(?:\n(?!\[).*)*^\s*enabled\s*=\s*true\s*$'
    checks.append((f"plugin enabled {plugin}", re.search(pattern, text) is not None))

mcp_servers = [
    "serena",
    "sequential-thinking",
    "playwright",
    "chrome-devtools",
    "context7",
    "deepwiki",
    "grep",
    "semgrep",
    "shadcn",
    "dart-flutter",
    "figma",
    "openaiDeveloperDocs",
]
for server in mcp_servers:
    checks.append((f"mcp configured {server}", f"[mcp_servers.{server}]" in text))

failed = False
for label, ok in checks:
    if ok:
        print(f"ok      {label}")
    else:
        print(f"fail    {label}", file=sys.stderr)
        failed = True

raise SystemExit(1 if failed else 0)
PY
  if [ "${exit_code:-0}" -ne 0 ]; then
    FAILURES=$((FAILURES + 1))
  fi
fi

section "Repository validation"
if "$ROOT/scripts/validate_marketplace.sh"; then
  pass "repository marketplace validation"
else
  fail "repository marketplace validation"
fi

section "MCP runtime"
if [ -n "$CODEX_CMD" ]; then
  if env CODEX_HOME="$CODEX_HOME_DIR" "$CODEX_CMD" mcp list >/tmp/rldyour-codex-mcp-list.txt 2>/tmp/rldyour-codex-mcp-list.err; then
    for server in serena sequential-thinking playwright chrome-devtools context7 deepwiki grep semgrep shadcn dart-flutter figma openaiDeveloperDocs; do
      if grep -q "^${server}[[:space:]]" /tmp/rldyour-codex-mcp-list.txt; then
        pass "mcp listed $server"
      else
        fail "mcp not listed $server"
      fi
    done
    if grep -E '^context7[[:space:]].*CONTEXT7_API_KEY=\*+' /tmp/rldyour-codex-mcp-list.txt >/dev/null; then
      pass "context7 runtime environment registered"
    else
      warn "context7 runtime environment is not visible in codex mcp list output"
    fi
  else
    fail "codex mcp list failed"
    sed -n '1,40p' /tmp/rldyour-codex-mcp-list.err >&2 || true
  fi
else
  fail "codex command missing"
fi

section "Plugin cache"
for plugin_dir in "$ROOT"/plugins/rldyour-*; do
  [ -d "$plugin_dir" ] || continue
  plugin_name=$(basename "$plugin_dir")
  cache_dir="$CACHE_ROOT/$plugin_name/local"
  if [ ! -d "$cache_dir" ]; then
    fail "missing cache $cache_dir"
    continue
  fi
  if diff -qr -x __pycache__ -x '*.pyc' "$plugin_dir" "$cache_dir" >/dev/null; then
    pass "cache in sync $plugin_name"
  else
    fail "cache differs $plugin_name"
  fi
done

section "Summary"
printf 'warnings: %s\n' "$WARNINGS"
printf 'failures: %s\n' "$FAILURES"

if [ "$FAILURES" -ne 0 ]; then
  exit 1
fi

printf 'System Codex doctor passed.\n'
