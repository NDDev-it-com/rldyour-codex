#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
unset CDPATH

CODEX_HOME_DIR=${CODEX_HOME:-"$HOME/.codex"}
BACKUP_ROOT=""
RESTORE=""
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  scripts/rollback_system_codex.sh [--codex-home DIR] --list
  scripts/rollback_system_codex.sh [--codex-home DIR] --restore BACKUP_NAME [--dry-run]

Restore AGENTS.md, config.toml, managed agents/*.toml, and managed rules/*.rules from installer-created rldyour-codex backups.
EOF
}

LIST=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --codex-home)
      CODEX_HOME_DIR=${2:-}
      if [ -z "$CODEX_HOME_DIR" ]; then
        printf 'missing value for --codex-home\n' >&2
        exit 1
      fi
      shift 2
      ;;
    --list)
      LIST=1
      shift
      ;;
    --restore)
      RESTORE=${2:-}
      if [ -z "$RESTORE" ]; then
        printf 'missing value for --restore\n' >&2
        exit 1
      fi
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

BACKUP_ROOT="$CODEX_HOME_DIR/backups/rldyour-codex"

if [ "$LIST" = "1" ]; then
  if [ ! -d "$BACKUP_ROOT" ]; then
    printf 'No backup root found: %s\n' "$BACKUP_ROOT"
    exit 0
  fi
  find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d -print | sort | while IFS= read -r dir; do
    printf '%s\n' "$(basename "$dir")"
  done
  exit 0
fi

if [ -z "$RESTORE" ]; then
  usage >&2
  exit 1
fi

SOURCE_DIR="$BACKUP_ROOT/$RESTORE"
if [ ! -d "$SOURCE_DIR" ]; then
  printf 'Backup not found: %s\n' "$SOURCE_DIR" >&2
  exit 1
fi

restore_file() {
  local file=$1
  local source="$SOURCE_DIR/$file"
  local target="$CODEX_HOME_DIR/$file"
  local target_dir
  local tmp_target
  if [ ! -f "$source" ]; then
    printf 'skip missing backup file: %s\n' "$source"
    return 0
  fi
  if [ "$DRY_RUN" = "1" ]; then
    printf 'would restore %s -> %s\n' "$source" "$target"
  else
    target_dir=$(dirname "$target")
    mkdir -p "$target_dir"
    tmp_target=$(mktemp "$target_dir/.restore.$(basename "$target").XXXXXX")
    install -m 0644 "$source" "$tmp_target"
    mv -f "$tmp_target" "$target"
    printf 'restored %s\n' "$target"
  fi
}

if [ "$DRY_RUN" = "1" ]; then
  printf 'Dry-run restore from %s into %s\n' "$SOURCE_DIR" "$CODEX_HOME_DIR"
else
  PRE_RESTORE_DIR="$BACKUP_ROOT/pre-restore-$(date -u '+%Y%m%dT%H%M%SZ')"
  mkdir -p "$PRE_RESTORE_DIR"
  for file in AGENTS.md config.toml; do
    if [ -f "$CODEX_HOME_DIR/$file" ]; then
      cp "$CODEX_HOME_DIR/$file" "$PRE_RESTORE_DIR/$file"
    fi
  done
  if [ -d "$CODEX_HOME_DIR/agents" ]; then
    mkdir -p "$PRE_RESTORE_DIR/agents"
    find "$CODEX_HOME_DIR/agents" -maxdepth 1 -type f -name '*.toml' -print | sort | while IFS= read -r agent_file; do
      cp "$agent_file" "$PRE_RESTORE_DIR/agents/"
    done
  fi
  if [ -d "$CODEX_HOME_DIR/rules" ]; then
    mkdir -p "$PRE_RESTORE_DIR/rules"
    find "$CODEX_HOME_DIR/rules" -maxdepth 1 -type f -name '*.rules' -print | sort | while IFS= read -r rule_file; do
      cp "$rule_file" "$PRE_RESTORE_DIR/rules/"
    done
  fi
  printf 'current state backed up to %s\n' "$PRE_RESTORE_DIR"
fi

restore_file AGENTS.md
restore_file config.toml
if [ -d "$SOURCE_DIR/agents" ]; then
  find "$SOURCE_DIR/agents" -maxdepth 1 -type f -name '*.toml' -print | sort | while IFS= read -r source; do
    target="$CODEX_HOME_DIR/agents/$(basename "$source")"
    if [ "$DRY_RUN" = "1" ]; then
      printf 'would restore %s -> %s\n' "$source" "$target"
    else
      target_dir=$(dirname "$target")
      mkdir -p "$target_dir"
      tmp_target=$(mktemp "$target_dir/.restore.$(basename "$target").XXXXXX")
      install -m 0644 "$source" "$tmp_target"
      mv -f "$tmp_target" "$target"
      printf 'restored %s\n' "$target"
    fi
  done
fi
if [ -d "$SOURCE_DIR/rules" ]; then
  find "$SOURCE_DIR/rules" -maxdepth 1 -type f -name '*.rules' -print | sort | while IFS= read -r source; do
    target="$CODEX_HOME_DIR/rules/$(basename "$source")"
    if [ "$DRY_RUN" = "1" ]; then
      printf 'would restore %s -> %s\n' "$source" "$target"
    else
      target_dir=$(dirname "$target")
      mkdir -p "$target_dir"
      tmp_target=$(mktemp "$target_dir/.restore.$(basename "$target").XXXXXX")
      install -m 0644 "$source" "$tmp_target"
      mv -f "$tmp_target" "$target"
      printf 'restored %s\n' "$target"
    fi
  done
fi

if [ "$DRY_RUN" = "0" ]; then
  printf 'Restore complete. Restart Codex and run scripts/doctor_system_codex.sh.\n'
fi
