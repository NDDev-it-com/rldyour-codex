#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME_DIR=${CODEX_HOME:-"$HOME/.codex"}
URL_CHECK=1
URL_RETRIES=${RLDYOUR_MCP_URL_RETRIES:-3}
URL_TIMEOUT=${RLDYOUR_MCP_URL_TIMEOUT:-8}

usage() {
  cat <<'EOF'
Usage: scripts/smoke_mcp_runtime.sh [--codex-home PATH] [--skip-url-check] [--url-retries N] [--url-timeout SEC]

Verifies the installed MCP runtime beyond static JSON:
- repository .mcp.json and installed config.toml contain the same servers;
- `codex mcp get <server>` works for every server;
- local MCP command binaries exist;
- remote MCP URLs accept a Streamable HTTP initialize preflight unless --skip-url-check is used.
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
    --url-retries)
      shift
      URL_RETRIES=${1:?--url-retries requires a value}
      ;;
    --url-timeout)
      shift
      URL_TIMEOUT=${1:?--url-timeout requires a value}
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

python3 - "$ROOT" "$CODEX_HOME_DIR" "$URL_CHECK" "$URL_RETRIES" "$URL_TIMEOUT" <<'PY'
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

root = Path(sys.argv[1])
codex_home = Path(sys.argv[2])
url_check = sys.argv[3] == "1"
url_retries = int(sys.argv[4])
url_timeout = float(sys.argv[5])
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


MCP_PROTOCOL_VERSION = "2025-11-25"


def json_rpc_initialize() -> bytes:
    return json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "rldyour-mcp-runtime-smoke",
                    "version": "0.1.0",
                },
            },
        }
    ).encode("utf-8")


def configured_headers(config: dict[str, object]) -> dict[str, str]:
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    for key, value in (config.get("http_headers") or {}).items():
        headers[str(key)] = str(value)
    bearer_env_var = config.get("bearer_token_env_var")
    if bearer_env_var:
        token = os.environ.get(str(bearer_env_var))
        if token:
            headers["Authorization"] = f"Bearer {token}"
    for key, value in (config.get("env_http_headers") or {}).items():
        env_value = os.environ.get(str(value))
        if env_value:
            headers[str(key)] = env_value
    return headers


def format_initialize_result(payload: object) -> str:
    if not isinstance(payload, dict):
        raise RuntimeError("initialize response was not a JSON object")
    if payload.get("id") != 1:
        raise RuntimeError(f"initialize response id mismatch: {payload.get('id')!r}")
    if payload.get("error"):
        raise RuntimeError(f"initialize returned JSON-RPC error: {payload.get('error')!r}")
    result = payload.get("result")
    if not isinstance(result, dict):
        raise RuntimeError(f"initialize response missing result object: {payload!r}")
    protocol_version = str(result.get("protocolVersion") or "unknown")
    server_info = result.get("serverInfo") if isinstance(result.get("serverInfo"), dict) else {}
    server_name = str(server_info.get("name") or "remote")
    return f"initialize {server_name} protocol {protocol_version}"


def read_sse_initialize(response: object) -> str:
    data_lines: list[str] = []
    for _ in range(200):
        raw_line = response.readline()
        if not raw_line:
            break
        line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
        if not line:
            if not data_lines:
                continue
            data = "\n".join(data_lines)
            data_lines = []
            if not data.strip():
                continue
            return format_initialize_result(json.loads(data))
        if line.startswith(":"):
            continue
        if line.startswith("data:"):
            data_lines.append(line[5:].lstrip(" "))
    if data_lines:
        return format_initialize_result(json.loads("\n".join(data_lines)))
    raise RuntimeError("initialize SSE stream did not include a JSON-RPC response")


def probe_remote_mcp(name: str, config: dict[str, object]) -> str:
    url = str(config.get("url") or "")
    last_error = ""
    attempts = max(1, url_retries)
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(
            url,
            data=json_rpc_initialize(),
            method="POST",
            headers=configured_headers(config),
        )
        try:
            with urllib.request.urlopen(request, timeout=url_timeout) as response:
                content_type = str(response.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
                if content_type == "application/json":
                    return f"HTTP {response.status} {format_initialize_result(json.loads(response.read()))}"
                if content_type == "text/event-stream":
                    return f"HTTP {response.status} {read_sse_initialize(response)}"
                raise RuntimeError(f"unexpected initialize content type {content_type or 'unknown'}")
        except urllib.error.HTTPError as exc:
            if exc.code in {401, 403}:
                return f"HTTP {exc.code} auth required"
            last_error = f"returned HTTP {exc.code}"
        except Exception as exc:
            last_error = f"initialize failed: {exc}"
        if attempt < attempts:
            print(f"retry   url {name} attempt {attempt} failed: {last_error}", file=sys.stderr)
            time.sleep(min(attempt, 3))
    raise RuntimeError(last_error)

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
        try:
            status = probe_remote_mcp(name, config)
            print(f"ok      remote mcp {name}: {status}")
        except Exception as exc:
            errors.append(f"{name}: remote endpoint {exc}")

if errors:
    raise SystemExit("\n".join(errors))

print("MCP runtime smoke passed.")
PY
