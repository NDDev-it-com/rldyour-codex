#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

STRICT_RUNTIME=0
CODEX_HOME_DIR=""
MODE="auto"

usage() {
  cat <<'EOF'
Usage: scripts/validate_runtime.sh [--codex-home PATH] [--strict-runtime] [--mode auto|static|installed|live]

Modes:
  auto       Static materialization plus best-effort installed-runtime probes (default).
  static     No codex binary and no network; materialize and parse generated TOML only.
  installed  Require a local codex binary; no package-registry freshness checks.
  live       Require a local codex binary and run network-backed freshness checks.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --codex-home)
      shift
      CODEX_HOME_DIR=${1:?--codex-home requires a path}
      ;;
    --strict|--strict-runtime)
      STRICT_RUNTIME=1
      ;;
    --mode)
      shift
      MODE=${1:?--mode requires auto, static, installed, or live}
      case "$MODE" in
        auto|static|installed|live) ;;
        *)
          printf 'Invalid --mode: %s\n' "$MODE" >&2
          usage >&2
          exit 2
          ;;
      esac
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

cleanup_tmp=""
if [ -z "$CODEX_HOME_DIR" ]; then
  CODEX_HOME_DIR=$(mktemp -d "${TMPDIR:-/tmp}/rldyour-codex-runtime.XXXXXX")
  cleanup_tmp=$CODEX_HOME_DIR
fi

cleanup() {
  if [ -n "$cleanup_tmp" ]; then
    rm -rf "$cleanup_tmp"
  fi
}
trap cleanup EXIT

runtime_args=(--codex-home "$CODEX_HOME_DIR")
if [ "$STRICT_RUNTIME" -eq 1 ]; then
  runtime_args+=(--strict-runtime)
fi

scripts/install_system_codex.sh --dry-run "${runtime_args[@]}"
scripts/install_system_codex.sh --apply "${runtime_args[@]}"
python3 scripts/validate_codex_mcp_env_forwarding.py --codex-home "$CODEX_HOME_DIR"

python3 - "$CODEX_HOME_DIR" <<'PY'
from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

home = Path(sys.argv[1])
config = home / "config.toml"
yolo = home / "rldyour-yolo.config.toml"
safe = home / "rldyour-safe.config.toml"
required = [config, yolo, safe]


def fail(message: str) -> None:
    print(f"static materialization check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict:
    if not path.exists():
        fail(f"missing generated file {path}")
    text = path.read_text(encoding="utf-8")
    if "default_permissions" in text:
        fail(f"{path.name} contains active default_permissions while legacy sandbox is selected")
    if re.search(r"^\s*\[profiles\.", text, re.M):
        fail(f"{path.name} contains legacy [profiles.*] table")
    if re.search(r"^\s*profile\s*=", text, re.M):
        fail(f"{path.name} contains legacy profile selector")
    if "plugin_hooks" in text:
        fail(f"{path.name} contains removed plugin_hooks feature flag")
    with path.open("rb") as fh:
        return tomllib.load(fh)


base, yolo_cfg, safe_cfg = [load(path) for path in required]
for name, cfg in (("config.toml", base), ("rldyour-yolo.config.toml", yolo_cfg), ("rldyour-safe.config.toml", safe_cfg)):
    if cfg.get("check_for_update_on_startup") is not False:
        fail(f"{name} must disable startup update checks for the centrally managed runtime")
features = base.get("features") or {}
if features.get("hooks") is not True:
    fail("config.toml must enable features.hooks")
if features.get("multi_agent") is not True:
    fail("config.toml must enable features.multi_agent")
if "plugin_hooks" in features:
    fail("config.toml must not enable removed features.plugin_hooks")
if not base.get("mcp_servers"):
    fail("config.toml must materialize [mcp_servers.*] entries")
if yolo_cfg.get("approval_policy") != "never":
    fail("rldyour-yolo.config.toml must set approval_policy = \"never\"")
if yolo_cfg.get("sandbox_mode") != "danger-full-access":
    fail("rldyour-yolo.config.toml must set sandbox_mode = \"danger-full-access\"")
if safe_cfg.get("approval_policy") != "on-request":
    fail("rldyour-safe.config.toml must set approval_policy = \"on-request\"")
if safe_cfg.get("sandbox_mode") != "workspace-write":
    fail("rldyour-safe.config.toml must set sandbox_mode = \"workspace-write\"")
print("ok: static Codex runtime materialization")
PY

if [ "$MODE" = "static" ]; then
  printf 'Static runtime validation passed with CODEX_HOME=%s.\n' "$CODEX_HOME_DIR"
  exit 0
fi

scripts/doctor_system_codex.sh --quick "${runtime_args[@]}"
if command -v codex >/dev/null 2>&1; then
  CODEX_HOME="$CODEX_HOME_DIR" scripts/validate_execpolicy_rules.sh "$CODEX_HOME_DIR/rules"
  CODEX_HOME="$CODEX_HOME_DIR" python3 scripts/smoke_codex_hook_listing.py --codex-home "$CODEX_HOME_DIR"
elif [ "$STRICT_RUNTIME" -eq 1 ] || [ "$MODE" = "installed" ] || [ "$MODE" = "live" ]; then
  printf 'codex command not found; installed runtime validation cannot run.\n' >&2
  exit 1
else
  printf 'skip    execpolicy rules validation: codex command not found\n'
fi
scripts/smoke_hooks.sh --codex-home "$CODEX_HOME_DIR"

if [ "$MODE" = "live" ]; then
  python3 scripts/check_mcp_runtime_versions.py
fi

printf 'Runtime validation passed in %s mode with CODEX_HOME=%s.\n' "$MODE" "$CODEX_HOME_DIR"
