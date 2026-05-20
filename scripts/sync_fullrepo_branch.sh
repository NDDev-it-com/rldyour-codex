#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if ROOT=$(git -C "$SCRIPT_DIR/.." rev-parse --show-toplevel 2>/dev/null); then
  :
else
  ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
fi

PLUGIN_SCRIPT="$ROOT/plugins/rldyour-flow/scripts/fullrepo_sync.py"
CACHE_PLUGIN_BASE="${CODEX_HOME:-$HOME/.codex}/plugins/cache/rldyour-codex/rldyour-flow"

if [ -f "$PLUGIN_SCRIPT" ]; then
  exec python3 "$PLUGIN_SCRIPT" "$@"
fi

for cache_script in "$CACHE_PLUGIN_BASE"/*/scripts/fullrepo_sync.py "$CACHE_PLUGIN_BASE"/local/scripts/fullrepo_sync.py; do
  if [ -f "$cache_script" ]; then
    exec python3 "$cache_script" "$@"
  fi
done

printf 'fullrepo sync script not found in repository or Codex plugin cache\n' >&2
exit 1
