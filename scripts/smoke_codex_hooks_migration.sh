#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
TMPDIR_ROOT=$(mktemp -d)
trap 'rm -rf "$TMPDIR_ROOT"' EXIT

write_case_config() {
  local case_name=$1
  local config_path=$2

  case "$case_name" in
    no_features)
      cat >"$config_path" <<'EOF'
profile = "custom"
EOF
      ;;
    table_legacy)
      cat >"$config_path" <<'EOF'
[features]
codex_hooks = true
shell_snapshot = false
EOF
      ;;
    table_plugin_only)
      cat >"$config_path" <<'EOF'
[features]
plugin_hooks = true
shell_snapshot = false
EOF
      ;;
    table_existing_hooks)
      cat >"$config_path" <<'EOF'
[features]
hooks = false
codex_hooks = true
plugin_hooks = true
shell_snapshot = false
EOF
      ;;
    dotted_legacy)
      cat >"$config_path" <<'EOF'
features.codex_hooks = true
EOF
      ;;
    dotted_plugin_only)
      cat >"$config_path" <<'EOF'
features.plugin_hooks = true
features.shell_snapshot = false
EOF
      ;;
    dotted_existing_hooks)
      cat >"$config_path" <<'EOF'
features.hooks = false
features.plugin_hooks = true
features.shell_snapshot = false
EOF
      ;;
    quoted_legacy)
      cat >"$config_path" <<'EOF'
[features]
"codex_hooks" = true
'plugin_hooks' = true
'hooks' = false
EOF
      ;;
    quoted_dotted)
      cat >"$config_path" <<'EOF'
features."codex_hooks" = true
features."plugin_hooks" = true
features."shell_snapshot" = false
EOF
      ;;
    inline_legacy)
      cat >"$config_path" <<'EOF'
features = { codex_hooks = true, shell_snapshot = false }
EOF
      ;;
    inline_plugin_only)
      cat >"$config_path" <<'EOF'
features = { plugin_hooks = true, shell_snapshot = false }
EOF
      ;;
    inline_existing_hooks)
      cat >"$config_path" <<'EOF'
features = { hooks = false, codex_hooks = true, plugin_hooks = true, shell_snapshot = false }
EOF
      ;;
    *)
      printf 'unknown smoke case: %s\n' "$case_name" >&2
      return 2
      ;;
  esac
}

run_case() {
  local case_name=$1
  local codex_home="$TMPDIR_ROOT/$case_name"
  mkdir -p "$codex_home"
  write_case_config "$case_name" "$codex_home/config.toml"

  "$ROOT/scripts/install_system_codex.sh" --apply --codex-home "$codex_home" >/dev/null

  CASE_NAME="$case_name" CONFIG_PATH="$codex_home/config.toml" python3 <<'PY'
from __future__ import annotations

import os
import tomllib
from pathlib import Path

case_name = os.environ["CASE_NAME"]
config_path = Path(os.environ["CONFIG_PATH"])
data = tomllib.loads(config_path.read_text(encoding="utf-8"))
features = data.get("features") or {}

if features.get("hooks") is not True:
    raise SystemExit(f"{case_name}: expected [features].hooks = true, got {features!r}")
if "codex_hooks" in features:
    raise SystemExit(f"{case_name}: legacy codex_hooks key was not removed: {features!r}")
if "plugin_hooks" in features:
    raise SystemExit(f"{case_name}: legacy plugin_hooks key was not removed: {features!r}")
if case_name in {
    "table_legacy",
    "table_plugin_only",
    "table_existing_hooks",
    "dotted_plugin_only",
    "dotted_existing_hooks",
    "quoted_dotted",
    "inline_legacy",
    "inline_plugin_only",
    "inline_existing_hooks",
}:
    if features.get("shell_snapshot") is not False:
        raise SystemExit(f"{case_name}: shell_snapshot flag was not preserved: {features!r}")
PY

  printf 'ok      %s\n' "$case_name"
}

cases=(
  no_features
  table_legacy
  table_plugin_only
  table_existing_hooks
  dotted_legacy
  dotted_plugin_only
  dotted_existing_hooks
  quoted_legacy
  quoted_dotted
  inline_legacy
  inline_plugin_only
  inline_existing_hooks
)

for case_name in "${cases[@]}"; do
  run_case "$case_name"
done

if command -v codex >/dev/null 2>&1; then
  runtime_home="$TMPDIR_ROOT/codex-runtime"
  mkdir -p "$runtime_home"
  CODEX_HOME="$runtime_home" codex features enable hooks >/dev/null
  CONFIG_PATH="$runtime_home/config.toml" python3 <<'PY'
from __future__ import annotations

import os
import tomllib
from pathlib import Path

features = tomllib.loads(Path(os.environ["CONFIG_PATH"]).read_text(encoding="utf-8")).get("features") or {}
if features.get("hooks") is not True or "codex_hooks" in features:
    raise SystemExit(f"codex runtime generated unexpected hooks features: {features!r}")
if "plugin_hooks" in features:
    raise SystemExit(f"codex runtime generated unexpected plugin_hooks feature: {features!r}")
PY
  printf 'ok      codex runtime hooks flag\n'
else
  printf 'skip    codex command not found; runtime hooks flag check skipped\n'
fi

printf 'Codex hooks migration smoke passed.\n'
