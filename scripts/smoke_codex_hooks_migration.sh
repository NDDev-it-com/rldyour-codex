#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
TMPDIR_ROOT=$(mktemp -d)
trap 'rm -rf "$TMPDIR_ROOT"' EXIT

write_case_config() {
  local case_name=$1
  local config_path=$2

  case "$case_name" in
    suppress_warning_false)
      cat >"$config_path" <<'EOF'
suppress_unstable_features_warning = false
EOF
      ;;
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
    root_legacy_config)
      cat >"$config_path" <<'EOF'
experimental_instructions_file = "/tmp/legacy-instructions.md"
background_terminal_timeout = 120000
experimental_use_unified_exec_tool = false
EOF
      ;;
    root_canonical_config)
      cat >"$config_path" <<'EOF'
model_instructions_file = "/tmp/current-instructions.md"
experimental_instructions_file = "/tmp/legacy-instructions.md"
background_terminal_max_timeout = 90000
background_terminal_timeout = 120000
experimental_use_unified_exec_tool = false

[features]
unified_exec = true
EOF
      ;;
    features_web_search_request)
      cat >"$config_path" <<'EOF'
[features]
web_search_request = true
EOF
      ;;
    features_web_search_cached)
      cat >"$config_path" <<'EOF'
[features]
web_search_cached = true
EOF
      ;;
    features_web_search_bool_false)
      cat >"$config_path" <<'EOF'
[features]
web_search = false
EOF
      ;;
    features_web_search_canonical_wins)
      cat >"$config_path" <<'EOF'
web_search = "cached"

[features]
web_search_request = true
EOF
      ;;
    memories_legacy)
      cat >"$config_path" <<'EOF'
[memories]
no_memories_if_mcp_or_web_search = true
EOF
      ;;
    features_legacy_landlock)
      cat >"$config_path" <<'EOF'
[features]
use_legacy_landlock = true
EOF
      ;;
    profiles_nested_legacy)
      cat >"$config_path" <<'EOF'
[profiles.rldyour-yolo.features]
terminal_resize_reflow = true
memories = true

[profiles."rldyour-safe".features]
terminal_resize_reflow = false
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
text = config_path.read_text(encoding="utf-8")
schema_comment = "#:schema https://developers.openai.com/codex/config-schema.json"
if not text.startswith(f"{schema_comment}\n"):
    raise SystemExit(f"{case_name}: missing Codex config schema comment")
data = tomllib.loads(text)
features = data.get("features") or {}

if features.get("hooks") is not True:
    raise SystemExit(f"{case_name}: expected [features].hooks = true, got {features!r}")
deprecated_features = {
    "codex_hooks",
    "plugin_hooks",
    "use_legacy_landlock",
    "web_search",
    "web_search_cached",
    "web_search_request",
}
unexpected_deprecated_features = sorted(deprecated_features.intersection(features))
if unexpected_deprecated_features:
    raise SystemExit(f"{case_name}: deprecated feature keys were not removed: {unexpected_deprecated_features}: {features!r}")
for deprecated_root_key in {
    "background_terminal_timeout",
    "experimental_instructions_file",
    "experimental_use_unified_exec_tool",
}:
    if deprecated_root_key in data:
        raise SystemExit(f"{case_name}: deprecated root key was not removed: {deprecated_root_key}")
if data.get("suppress_unstable_features_warning") is not True:
    raise SystemExit(f"{case_name}: suppress_unstable_features_warning was not enabled: {data!r}")
if "profiles" in data:
    raise SystemExit(f"{case_name}: legacy profiles table was not removed: {data['profiles']!r}")

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
if case_name == "root_legacy_config":
    if data.get("model_instructions_file") != "/tmp/legacy-instructions.md":
        raise SystemExit(f"{case_name}: experimental_instructions_file was not migrated: {data!r}")
    if data.get("background_terminal_max_timeout") != 120000:
        raise SystemExit(f"{case_name}: background_terminal_timeout was not migrated: {data!r}")
    if features.get("unified_exec") is not False:
        raise SystemExit(f"{case_name}: experimental_use_unified_exec_tool was not migrated: {features!r}")
if case_name == "root_canonical_config":
    if data.get("model_instructions_file") != "/tmp/current-instructions.md":
        raise SystemExit(f"{case_name}: canonical model_instructions_file did not win: {data!r}")
    if data.get("background_terminal_max_timeout") != 90000:
        raise SystemExit(f"{case_name}: canonical background_terminal_max_timeout did not win: {data!r}")
    if features.get("unified_exec") is not True:
        raise SystemExit(f"{case_name}: canonical features.unified_exec did not win: {features!r}")
if case_name == "features_web_search_request" and data.get("web_search") != "live":
    raise SystemExit(f"{case_name}: web_search_request was not migrated to live: {data!r}")
if case_name == "features_web_search_cached" and data.get("web_search") != "cached":
    raise SystemExit(f"{case_name}: web_search_cached was not migrated to cached: {data!r}")
if case_name == "features_web_search_bool_false" and data.get("web_search") != "disabled":
    raise SystemExit(f"{case_name}: features.web_search=false was not migrated to disabled: {data!r}")
if case_name == "features_web_search_canonical_wins" and data.get("web_search") != "cached":
    raise SystemExit(f"{case_name}: canonical web_search did not win: {data!r}")
if case_name == "memories_legacy":
    memories = data.get("memories") or {}
    if memories.get("disable_on_external_context") is not True:
        raise SystemExit(f"{case_name}: memories legacy alias was not migrated: {memories!r}")
    if "no_memories_if_mcp_or_web_search" in memories:
        raise SystemExit(f"{case_name}: memories legacy alias was not removed: {memories!r}")
PY

  printf 'ok      %s\n' "$case_name"
}

cases=(
  suppress_warning_false
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
  root_legacy_config
  root_canonical_config
  features_web_search_request
  features_web_search_cached
  features_web_search_bool_false
  features_web_search_canonical_wins
  memories_legacy
  features_legacy_landlock
  profiles_nested_legacy
)

for case_name in "${cases[@]}"; do
  run_case "$case_name"
done

malformed_home="$TMPDIR_ROOT/malformed_existing_config"
mkdir -p "$malformed_home"
printf '[features\nhooks = true\n' > "$malformed_home/config.toml"
set +e
malformed_output=$("$ROOT/scripts/install_system_codex.sh" --apply --codex-home "$malformed_home" 2>&1)
malformed_status=$?
set -e
if [ "$malformed_status" -eq 0 ]; then
  printf '%s\n' "$malformed_output" >&2
  printf 'malformed_existing_config: installer unexpectedly succeeded\n' >&2
  exit 1
fi
if ! printf '%s\n' "$malformed_output" | grep -F 'Malformed existing Codex config' >/dev/null; then
  printf '%s\n' "$malformed_output" >&2
  printf 'malformed_existing_config: installer did not report parse failure\n' >&2
  exit 1
fi
printf 'ok      malformed_existing_config\n'

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
PY
  printf 'ok      codex runtime hooks flag\n'
else
  printf 'skip    codex command not found; runtime hooks flag check skipped\n'
fi

printf 'Codex hooks migration smoke passed.\n'
