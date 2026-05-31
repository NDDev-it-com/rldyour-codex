#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel 2>/dev/null); then
  :
else
  ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
fi

VERSIONS_FILE="$ROOT/config/mcp-runtime-versions.env"
if [ -f "$VERSIONS_FILE" ]; then
  # shellcheck disable=SC1090,SC1091
  . "$VERSIONS_FILE"
fi

UV_BIN=${UV_BIN:-$(command -v uv 2>/dev/null || true)}
if [ -z "$UV_BIN" ]; then
  printf 'uv command not found\n' >&2
  exit 1
fi

MCP_PYTHON_SDK_VERSION=${MCP_PYTHON_SDK_VERSION:-1.27.2}

exec "$UV_BIN" run --with "mcp==${MCP_PYTHON_SDK_VERSION}" python "$ROOT/scripts/smoke_mcp_capabilities.py" --root "$ROOT" "$@"
