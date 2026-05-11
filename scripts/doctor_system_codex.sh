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
SYSTEM_AGENT_DIR="$ROOT/system/agents"
INSTALLED_AGENTS="$CODEX_HOME_DIR/AGENTS.md"
INSTALLED_AGENT_DIR="$CODEX_HOME_DIR/agents"
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
  export RLDYOUR_SYSTEM_AGENT_DIR="$SYSTEM_AGENT_DIR"
  python3 <<'PY' || exit_code=$?
from __future__ import annotations

import os
import sys
import tomllib
from pathlib import Path

path = Path(os.environ["RLDYOUR_CODEX_CONFIG"])
repo_root = os.environ["RLDYOUR_REPO_ROOT"]
codex_home = path.parent
system_agent_dir = Path(os.environ["RLDYOUR_SYSTEM_AGENT_DIR"])
text = path.read_text(encoding="utf-8")
config_data = tomllib.loads(text)
schema_comment = "#:schema https://developers.openai.com/codex/config-schema.json"

checks = []
checks.append(("config schema comment", text.startswith(f"{schema_comment}\n")))
marketplace = (config_data.get("marketplaces") or {}).get("rldyour-codex") or {}
checks.append(("marketplace source", marketplace.get("source") == repo_root and marketplace.get("source_type") == "local"))
project = (config_data.get("projects") or {}).get(repo_root) or {}
checks.append(("repo trusted", project.get("trust_level") == "trusted"))

features = config_data.get("features") or {}
checks.append(("hooks feature enabled", features.get("hooks") is True))
checks.append(("multi-agent feature enabled", features.get("multi_agent") is True))
checks.append(("legacy codex_hooks absent", "codex_hooks" not in features))
checks.append(("legacy plugin_hooks absent", "plugin_hooks" not in features))

checks.append(("yolo profile selected", config_data.get("profile") == "rldyour-yolo"))
checks.append(("approval policy never", config_data.get("approval_policy") == "never"))
checks.append(("sandbox danger full access", config_data.get("sandbox_mode") == "danger-full-access"))
checks.append(("default permissions danger no sandbox", config_data.get("default_permissions") == ":danger-no-sandbox"))
checks.append(("default model gpt-5.5", config_data.get("model") == "gpt-5.5"))
checks.append(("default reasoning effort xhigh", config_data.get("model_reasoning_effort") == "xhigh"))
yolo_profile = (config_data.get("profiles") or {}).get("rldyour-yolo") or {}
checks.append(("profile rldyour-yolo approval policy", yolo_profile.get("approval_policy") == "never"))
checks.append(("profile rldyour-yolo sandbox", yolo_profile.get("sandbox_mode") == "danger-full-access"))
checks.append(("profile rldyour-yolo permissions", yolo_profile.get("default_permissions") == ":danger-no-sandbox"))

agents_config = config_data.get("agents") or {}
checks.append(("agents max_threads", agents_config.get("max_threads") == 6))
checks.append(("agents max_depth", agents_config.get("max_depth") == 1))
configured_agents = agents_config
for agent_path in sorted(system_agent_dir.glob("*.toml")):
    agent_data = tomllib.loads(agent_path.read_text(encoding="utf-8"))
    name = agent_data.get("name")
    if not isinstance(name, str):
        checks.append((f"agent {agent_path.name} name", False))
        continue
    agent_config = configured_agents.get(name) or {}
    expected_path = str(codex_home / "agents" / agent_path.name)
    checks.append((f"agent configured {name}", agent_config.get("config_file") == expected_path))
    checks.append((f"agent description {name}", agent_config.get("description") == agent_data.get("description")))

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
configured_plugins = config_data.get("plugins") or {}
for plugin in plugins:
    plugin_config = configured_plugins.get(plugin) or {}
    checks.append((f"plugin enabled {plugin}", plugin_config.get("enabled") is True))

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
configured_mcp_servers = config_data.get("mcp_servers") or {}
for server in mcp_servers:
    checks.append((f"mcp configured {server}", server in configured_mcp_servers))

tool_approvals = {
    "sequential-thinking": {"sequentialthinking": "approve"},
    "deepwiki": {
        "ask_question": "approve",
        "read_wiki_structure": "approve",
    },
    "grep": {"searchGitHub": "approve"},
}
for server, tools in tool_approvals.items():
    server_config = configured_mcp_servers.get(server) or {}
    configured_tools = server_config.get("tools") or {}
    for tool, expected_mode in tools.items():
        tool_config = configured_tools.get(tool) or {}
        checks.append((f"mcp tool approval {server}.{tool}", tool_config.get("approval_mode") == expected_mode))

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

section "Subagents"
export RLDYOUR_SYSTEM_AGENT_DIR="$SYSTEM_AGENT_DIR"
export RLDYOUR_INSTALLED_AGENT_DIR="$INSTALLED_AGENT_DIR"
python3 <<'PY' || FAILURES=$((FAILURES + 1))
from __future__ import annotations

import os
import sys
import tomllib
from pathlib import Path

system_dir = Path(os.environ["RLDYOUR_SYSTEM_AGENT_DIR"])
installed_dir = Path(os.environ["RLDYOUR_INSTALLED_AGENT_DIR"])
errors = False

for source in sorted(system_dir.glob("*.toml")):
    target = installed_dir / source.name
    label = source.stem
    if not target.is_file():
        print(f"fail    subagent installed {label}", file=sys.stderr)
        errors = True
        continue
    source_text = source.read_text(encoding="utf-8")
    target_text = target.read_text(encoding="utf-8")
    if source_text == target_text:
        print(f"ok      subagent file in sync {label}")
    else:
        print(f"fail    subagent file differs {label}", file=sys.stderr)
        errors = True
    try:
        data = tomllib.loads(source_text)
    except Exception as exc:
        print(f"fail    subagent TOML parses {label}: {exc}", file=sys.stderr)
        errors = True
        continue
    checks = {
        "name": data.get("name") == label,
        "model gpt-5.5": data.get("model") == "gpt-5.5",
        "reasoning medium": data.get("model_reasoning_effort") == "medium",
        "description": isinstance(data.get("description"), str) and bool(data.get("description", "").strip()),
        "developer instructions": isinstance(data.get("developer_instructions"), str) and bool(data.get("developer_instructions", "").strip()),
    }
    for check, ok in checks.items():
        if ok:
            print(f"ok      subagent {label} {check}")
        else:
            print(f"fail    subagent {label} {check}", file=sys.stderr)
            errors = True

raise SystemExit(1 if errors else 0)
PY

section "Repository validation"
if "$ROOT/scripts/validate_marketplace.sh"; then
  pass "repository marketplace validation"
else
  fail "repository marketplace validation"
fi

section "Fullrepo"
if python3 "$ROOT/plugins/rldyour-flow/scripts/fullrepo_sync.py" --status-json >/tmp/rldyour-codex-fullrepo-state.json 2>/tmp/rldyour-codex-fullrepo-state.err; then
  pass "fullrepo state script"
  if python3 -m json.tool /tmp/rldyour-codex-fullrepo-state.json >/dev/null 2>&1; then
    pass "fullrepo state JSON"
    if python3 - /tmp/rldyour-codex-fullrepo-state.json <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
dirty = payload.get("dirty_non_agent_paths") or []
if dirty:
    raise SystemExit(f"non-agent files are dirty: {dirty}")
if payload.get("branch") == "main" and payload.get("worktree_agent_paths") and payload.get("fullrepo_matches_worktree") is not True:
    raise SystemExit("fullrepo does not match current HEAD plus agent-only files")
PY
    then
      pass "fullrepo current-state gate"
    else
      fail "fullrepo current-state gate"
    fi
  else
    fail "fullrepo state JSON invalid"
  fi
else
  fail "fullrepo state script failed"
  sed -n '1,40p' /tmp/rldyour-codex-fullrepo-state.err >&2 || true
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
