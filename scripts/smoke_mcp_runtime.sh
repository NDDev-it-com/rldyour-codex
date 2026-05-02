#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME_DIR=${CODEX_HOME:-"$HOME/.codex"}
URL_CHECK=1

usage() {
  cat <<'EOF'
Usage: scripts/smoke_mcp_runtime.sh [--codex-home PATH] [--skip-url-check]

Verifies the installed MCP runtime beyond static JSON:
- repository .mcp.json and installed config.toml contain the same servers;
- `codex mcp get <server>` works for every server;
- local MCP command binaries exist;
- remote MCP URLs are reachable unless --skip-url-check is used.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --codex-home)
      shift
      CODEX_HOME_DIR=${1:?--codex-home requires a path}
      ;;
    --skip-url-check)
      URL_CHECK=0
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

python3 - "$ROOT" "$CODEX_HOME_DIR" "$URL_CHECK" <<'PY'
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

root = Path(sys.argv[1])
codex_home = Path(sys.argv[2])
url_check = sys.argv[3] == "1"
repo_mcp = root / "plugins/rldyour-mcps/.mcp.json"
config_path = codex_home / "config.toml"
codex = shutil.which(os.environ.get("CODEX_BIN", "codex"))

if codex is None:
    raise SystemExit("codex command not found")
if not repo_mcp.is_file():
    raise SystemExit(f"missing {repo_mcp}")
if not config_path.is_file():
    raise SystemExit(f"missing {config_path}")

repo_servers = json.loads(repo_mcp.read_text(encoding="utf-8"))["mcpServers"]
config_servers = tomllib.loads(config_path.read_text(encoding="utf-8")).get("mcp_servers", {})
repo_names = set(repo_servers)
config_names = set(config_servers)
errors: list[str] = []

if repo_names != config_names:
    errors.append(
        "MCP server name mismatch: "
        f"missing={sorted(repo_names - config_names)} extra={sorted(config_names - repo_names)}"
    )

env = dict(os.environ)
env["CODEX_HOME"] = str(codex_home)

print("rldyour MCP runtime smoke")
print(f"codex_home: {codex_home}")
print(f"servers: {len(repo_servers)}")

for name in sorted(repo_servers):
    config = config_servers.get(name, {})

    get_proc = subprocess.run(
        [codex, "mcp", "get", name],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=root,
    )
    if get_proc.returncode == 0:
        print(f"ok      codex mcp get {name}")
    else:
        errors.append(f"codex mcp get {name} failed: {get_proc.stderr.strip() or get_proc.stdout.strip()}")

    command = config.get("command")
    if command:
        command_text = str(command)
        if Path(command_text).is_absolute():
            ok = os.access(command_text, os.X_OK)
            resolved = command_text
        else:
            resolved = shutil.which(command_text) or ""
            ok = bool(resolved)
        if ok:
            print(f"ok      command {name}: {resolved}")
        else:
            errors.append(f"{name}: command not executable or not found: {command_text}")

    url = config.get("url")
    if url and url_check:
        request = urllib.request.Request(
            str(url),
            method="GET",
            headers={"Accept": "application/json, text/event-stream, */*"},
        )
        try:
            with urllib.request.urlopen(request, timeout=8) as response:
                print(f"ok      url {name}: HTTP {response.status}")
        except urllib.error.HTTPError as exc:
            if exc.code < 500:
                print(f"ok      url {name}: HTTP {exc.code}")
            else:
                errors.append(f"{name}: remote endpoint returned HTTP {exc.code}")
        except Exception as exc:
            errors.append(f"{name}: remote endpoint unreachable: {exc}")

if errors:
    raise SystemExit("\n".join(errors))

print("MCP runtime smoke passed.")
PY
