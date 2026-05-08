#!/usr/bin/env bash
set -euo pipefail

APPLY=0
TRUST_HOME=0
CODEX_HOME_DIR=${CODEX_HOME:-"$HOME/.codex"}

usage() {
  cat <<'EOF'
Usage: scripts/install_system_codex.sh [--dry-run] [--apply] [--codex-home PATH] [--trust-home]

Installs the current rldyour Codex system state into CODEX_HOME.

Default mode is --dry-run. Use --apply to write files.

Managed state:
- CODEX_HOME/AGENTS.md from system/AGENTS.md
- rldyour-codex marketplace registration
- enabled rldyour plugins plus curated GitHub and Gmail plugins
- hooks feature flag
- owner-requested YOLO permission defaults
- rldyour MCP server definitions
- active rldyour plugin cache copies

Secrets are not installed. Keep Context7, Figma, GitHub, Gmail, and other auth outside this repository.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      APPLY=0
      ;;
    --apply)
      APPLY=1
      ;;
    --codex-home)
      shift
      CODEX_HOME_DIR=${1:?--codex-home requires a path}
      ;;
    --trust-home)
      TRUST_HOME=1
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
CONFIG_PATH="$CODEX_HOME_DIR/config.toml"
CACHE_ROOT="$CODEX_HOME_DIR/plugins/cache/rldyour-codex"
BACKUP_ROOT="$CODEX_HOME_DIR/backups/rldyour-codex"
TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"

UVX_CMD=${UVX_BIN:-$(command -v uvx 2>/dev/null || true)}
BUNX_CMD=${BUNX_BIN:-$(command -v bunx 2>/dev/null || true)}
DART_CMD=${DART_BIN:-$(command -v dart 2>/dev/null || true)}
CODEX_CMD=${CODEX_BIN:-$(command -v codex 2>/dev/null || true)}

if [ -z "$UVX_CMD" ]; then
  UVX_CMD="uvx"
  printf 'warning: uvx not found on PATH; config will use "uvx"\n' >&2
fi
if [ -z "$BUNX_CMD" ]; then
  BUNX_CMD="bunx"
  printf 'warning: bunx not found on PATH; config will use "bunx"\n' >&2
fi
if [ -z "$DART_CMD" ]; then
  DART_CMD="dart"
  printf 'warning: dart not found on PATH; config will use "dart"\n' >&2
fi

if [ ! -f "$SYSTEM_AGENTS" ]; then
  printf 'Missing system AGENTS template: %s\n' "$SYSTEM_AGENTS" >&2
  exit 1
fi

run_or_print() {
  if [ "$APPLY" -eq 1 ]; then
    "$@"
  else
    printf 'dry-run:'
    printf ' %q' "$@"
    printf '\n'
  fi
}

backup_file() {
  local path=$1
  if [ "$APPLY" -ne 1 ] || [ ! -e "$path" ]; then
    return 0
  fi
  mkdir -p "$BACKUP_DIR"
  cp -p "$path" "$BACKUP_DIR/"
  printf 'backed up %s -> %s/\n' "$path" "$BACKUP_DIR"
}

print_plan() {
  cat <<EOF
rldyour Codex system install
mode: $([ "$APPLY" -eq 1 ] && printf 'apply' || printf 'dry-run')
repo: $ROOT
codex home: $CODEX_HOME_DIR
system AGENTS: $CODEX_HOME_DIR/AGENTS.md
config: $CONFIG_PATH
cache root: $CACHE_ROOT
uvx: $UVX_CMD
bunx: $BUNX_CMD
dart: $DART_CMD
codex: ${CODEX_CMD:-not found}
trust home: $TRUST_HOME
EOF
}

patch_config() {
  export RLDYOUR_CODEX_CONFIG="$CONFIG_PATH"
  export RLDYOUR_REPO_ROOT="$ROOT"
  export RLDYOUR_HOME="$HOME"
  export RLDYOUR_UVX_CMD="$UVX_CMD"
  export RLDYOUR_BUNX_CMD="$BUNX_CMD"
  export RLDYOUR_DART_CMD="$DART_CMD"
  export RLDYOUR_TRUST_HOME="$TRUST_HOME"
  export RLDYOUR_DRY_RUN=$((1 - APPLY))
  export RLDYOUR_MCP_CONFIG="$ROOT/plugins/rldyour-mcps/.mcp.json"

  python3 <<'PY'
from __future__ import annotations

import json
import os
import re
from pathlib import Path

config_path = Path(os.environ["RLDYOUR_CODEX_CONFIG"])
repo_root = os.environ["RLDYOUR_REPO_ROOT"]
home = os.environ["RLDYOUR_HOME"]
uvx_cmd = os.environ["RLDYOUR_UVX_CMD"]
bunx_cmd = os.environ["RLDYOUR_BUNX_CMD"]
dart_cmd = os.environ["RLDYOUR_DART_CMD"]
trust_home = os.environ.get("RLDYOUR_TRUST_HOME") == "1"
dry_run = os.environ.get("RLDYOUR_DRY_RUN") == "1"
mcp_config_path = Path(os.environ["RLDYOUR_MCP_CONFIG"])

rldyour_plugins = [
    "rldyour-mcps",
    "rldyour-explore",
    "rldyour-serena-mcp",
    "rldyour-security",
    "rldyour-browser",
    "rldyour-design",
    "rldyour-lsps",
    "rldyour-flow",
    "rldyour-rules",
]
curated_plugins = ["gmail@openai-curated", "github@openai-curated"]

mcp_source = json.loads(mcp_config_path.read_text(encoding="utf-8"))["mcpServers"]
command_overrides = {
    "uvx": uvx_cmd,
    "bunx": bunx_cmd,
    "dart": dart_cmd,
}
mcp_servers = {}
for name, raw_spec in mcp_source.items():
    spec = dict(raw_spec)
    command = spec.get("command")
    if isinstance(command, str) and command in command_overrides:
        spec["command"] = command_overrides[command]
    mcp_servers[name] = spec

managed_headers = {
    "marketplaces.rldyour-codex",
    "profiles.rldyour-yolo",
    f'projects."{repo_root}"',
}
if trust_home:
    managed_headers.add(f'projects."{home}"')
for plugin in curated_plugins:
    managed_headers.add(f'plugins."{plugin}"')
for plugin in rldyour_plugins:
    managed_headers.add(f'plugins."{plugin}@rldyour-codex"')
for server, spec in mcp_servers.items():
    managed_headers.add(f"mcp_servers.{server}")
    if "env" in spec:
        managed_headers.add(f"mcp_servers.{server}.env")

header_re = re.compile(r"^\s*\[([^\]]+)\]\s*$")
root_key_re = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*=")
existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
managed_root_keys = {"profile", "approval_policy", "sandbox_mode", "default_permissions"}
out: list[str] = [
    'profile = "rldyour-yolo"',
    'approval_policy = "never"',
    'sandbox_mode = "danger-full-access"',
    'default_permissions = ":danger-no-sandbox"',
    "",
]
skip_managed = False
in_features = False
features_seen = False
hooks_written = False
current_header: str | None = None

for raw_line in existing.splitlines():
    match = header_re.match(raw_line)
    if match:
        if in_features and not hooks_written:
            out.append("hooks = true")
            hooks_written = True
        header = match.group(1)
        if header in managed_headers:
            skip_managed = True
            in_features = False
            continue
        skip_managed = False
        in_features = header == "features"
        if in_features:
            features_seen = True
        current_header = header
        out.append(raw_line)
        continue

    if skip_managed:
        continue

    if current_header is None:
        key_match = root_key_re.match(raw_line)
        if key_match and key_match.group(1) in managed_root_keys:
            continue

    if in_features:
        key_match = root_key_re.match(raw_line)
        feature_key = key_match.group(1) if key_match else ""
        if feature_key == "codex_hooks":
            continue
        if feature_key == "hooks":
            if not hooks_written:
                out.append("hooks = true")
                hooks_written = True
            continue

    out.append(raw_line)

if in_features and not hooks_written:
    out.append("hooks = true")
    hooks_written = True

while out and out[-1] == "":
    out.pop()

def add_blank() -> None:
    if out and out[-1] != "":
        out.append("")

if not features_seen:
    add_blank()
    out.extend(["[features]", "hooks = true"])

add_blank()
out.extend([
    "[marketplaces.rldyour-codex]",
    'source_type = "local"',
    f"source = {json.dumps(repo_root)}",
])

add_blank()
out.extend([
    "[profiles.rldyour-yolo]",
    'approval_policy = "never"',
    'sandbox_mode = "danger-full-access"',
    'default_permissions = ":danger-no-sandbox"',
])

add_blank()
out.extend([f'[projects."{repo_root}"]', 'trust_level = "trusted"'])
if trust_home:
    add_blank()
    out.extend([f'[projects."{home}"]', 'trust_level = "trusted"'])

for plugin in curated_plugins:
    add_blank()
    out.extend([f'[plugins."{plugin}"]', "enabled = true"])

for plugin in rldyour_plugins:
    add_blank()
    out.extend([f'[plugins."{plugin}@rldyour-codex"]', "enabled = true"])

def toml_value(value: object) -> str:
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return json.dumps(value)
    raise TypeError(f"Unsupported TOML value: {value!r}")

for server, spec in mcp_servers.items():
    add_blank()
    out.append(f"[mcp_servers.{server}]")
    for key in ("command", "url", "args", "env_vars", "startup_timeout_sec", "tool_timeout_sec"):
        if key in spec:
            out.append(f"{key} = {toml_value(spec[key])}")
    env = spec.get("env")
    if isinstance(env, dict):
        add_blank()
        out.append(f"[mcp_servers.{server}.env]")
        for key, value in env.items():
            out.append(f"{key} = {toml_value(value)}")

new_text = "\n".join(out).rstrip() + "\n"

if dry_run:
    print(f"dry-run: would patch {config_path}")
    print(f"dry-run: managed plugins: {len(rldyour_plugins) + len(curated_plugins)}")
    print(f"dry-run: managed MCP servers: {len(mcp_servers)}")
else:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(new_text, encoding="utf-8")
    print(f"patched {config_path}")
PY
}

sync_plugin_cache() {
  local plugin_dir plugin_name cache_dir
  for plugin_dir in "$ROOT"/plugins/rldyour-*; do
    [ -d "$plugin_dir" ] || continue
    plugin_name=$(basename "$plugin_dir")
    cache_dir="$CACHE_ROOT/$plugin_name/local"
    if [ "$APPLY" -eq 1 ]; then
      mkdir -p "$cache_dir"
      rsync -a --delete "$plugin_dir/" "$cache_dir/"
      printf 'synced plugin cache %s\n' "$plugin_name"
    else
      printf 'dry-run: sync %s -> %s\n' "$plugin_dir/" "$cache_dir/"
    fi
  done
}

print_plan

if [ "$APPLY" -eq 1 ]; then
  mkdir -p "$CODEX_HOME_DIR"
fi

backup_file "$CODEX_HOME_DIR/AGENTS.md"
backup_file "$CONFIG_PATH"

if [ "$APPLY" -eq 1 ]; then
  install -m 0644 "$SYSTEM_AGENTS" "$CODEX_HOME_DIR/AGENTS.md"
  printf 'installed %s\n' "$CODEX_HOME_DIR/AGENTS.md"
else
  printf 'dry-run: install %s -> %s\n' "$SYSTEM_AGENTS" "$CODEX_HOME_DIR/AGENTS.md"
fi

if [ -n "$CODEX_CMD" ]; then
  run_or_print env CODEX_HOME="$CODEX_HOME_DIR" "$CODEX_CMD" plugin marketplace add "$ROOT"
else
  printf 'warning: codex command not found; marketplace add skipped\n' >&2
fi

patch_config
sync_plugin_cache

cat <<EOF

Next checks:
  scripts/doctor_system_codex.sh --codex-home "$CODEX_HOME_DIR"

Restart Codex after install so global AGENTS.md, plugins, hooks, and MCP settings are reloaded.
EOF
