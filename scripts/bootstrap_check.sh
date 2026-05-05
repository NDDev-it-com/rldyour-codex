#!/usr/bin/env bash
set -euo pipefail

APPLY=0
CODEX_HOME_DIR=${CODEX_HOME:-"$HOME/.codex"}

usage() {
  cat <<'EOF'
Usage: scripts/bootstrap_check.sh [--dry-run] [--apply] [--codex-home PATH]

End-to-end bootstrap check for a new machine.

Default --dry-run previews installation and validates repository-local files only.
Use --apply to run the full clone -> install -> doctor -> smoke flow.
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
cd "$ROOT"

step() {
  printf '\n== %s ==\n' "$1"
}

step "Install preview"
scripts/install_system_codex.sh --dry-run --codex-home "$CODEX_HOME_DIR"

if [ "$APPLY" -ne 1 ]; then
  step "Repository-local checks"
  jq empty .agents/plugins/marketplace.json plugins/*/.codex-plugin/plugin.json plugins/rldyour-mcps/.mcp.json plugins/rldyour-serena-mcp/hooks.json plugins/rldyour-flow/hooks.json pyrightconfig.json
  shellcheck scripts/*.sh plugins/rldyour-serena-mcp/hooks/*.sh plugins/rldyour-serena-mcp/scripts/*.sh plugins/rldyour-flow/hooks/*.sh plugins/rldyour-flow/scripts/*.sh plugins/rldyour-lsps/scripts/*.sh
  scripts/smoke_fullrepo_sync.sh
  scripts/smoke_fullrepo_bootstrap_init.sh
  scripts/smoke_hooks.sh --repo-only --codex-home "$CODEX_HOME_DIR"
  printf '\nBootstrap dry-run passed. Run scripts/bootstrap_check.sh --apply to install and verify system Codex on this machine.\n'
  exit 0
fi

step "Install apply"
scripts/install_system_codex.sh --apply --codex-home "$CODEX_HOME_DIR"

step "Marketplace validation"
CODEX_HOME="$CODEX_HOME_DIR" scripts/validate_marketplace.sh

step "MCP runtime smoke"
CODEX_HOME="$CODEX_HOME_DIR" scripts/smoke_mcp_runtime.sh --codex-home "$CODEX_HOME_DIR"

step "Hook smoke"
CODEX_HOME="$CODEX_HOME_DIR" scripts/smoke_hooks.sh --codex-home "$CODEX_HOME_DIR"

step "System doctor"
scripts/doctor_system_codex.sh --codex-home "$CODEX_HOME_DIR"

step "State checks"
python3 plugins/rldyour-serena-mcp/scripts/serena_memory_state.py | python3 -m json.tool
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool
git status -sb

printf '\nBootstrap apply check passed. Restart Codex so global AGENTS.md, plugins, hooks, and MCP settings are reloaded.\n'
