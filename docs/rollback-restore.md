# Rollback And Restore

Rollback is a first-class workflow because this repository writes global Codex configuration, installed plugin cache, MCP runtime definitions, hooks, and global instructions.

## Safety Model

- Default commands are read-only.
- Restore requires an explicit backup timestamp.
- Before restore, the rollback script creates a pre-restore backup of the current `AGENTS.md`, `config.toml`, managed `agents/*.toml`, and managed `rules/*.rules`.
- The script restores only files that the installer backs up: `AGENTS.md`, `config.toml`, managed `agents/*.toml`, and managed `rules/*.rules`.
- File restore writes through a temporary file in the target directory and then renames it into place, so a copy failure should not leave a partially written target file.
- Plugin cache rollback is handled by checking out an older Git revision and rerunning the installer.
- Agent context (`.serena/`, `AGENTS.md`, `.claude/`) is tracked normally on `main`, so it rolls back with the rest of the tree via a normal `git checkout`/`git restore`.

## List Backups

```bash
scripts/rollback_system_codex.sh --list
```

With a custom Codex home:

```bash
scripts/rollback_system_codex.sh --codex-home /path/to/codex-home --list
```

## Dry-Run Restore

```bash
scripts/rollback_system_codex.sh --restore <backup-timestamp> --dry-run
```

## Apply Restore

```bash
scripts/rollback_system_codex.sh --restore <backup-timestamp>
scripts/doctor_system_codex.sh
```

Restart Codex after restoring global configuration.

## Restore A Released Marketplace State

Use this when plugin cache, hooks, or MCP definitions need to move back to a released repository state:

```bash
git fetch --tags origin
git checkout v<version>
scripts/install_system_codex.sh --dry-run
scripts/install_system_codex.sh --apply
scripts/doctor_system_codex.sh
```

Return to active development after validation:

```bash
git checkout main
```

Agent context is tracked on `main`, so checking out `main` restores it with the rest of the tree.

## Failure Diagnosis Before Rollback

Before changing state, collect local evidence:

```bash
scripts/collect_diagnostics.sh --include-doctor
```

This keeps the failed state available for later analysis without storing secrets.

## Restore Agent Context

Agent context (`AGENTS.md`, `.serena/` knowledge, `.claude/`) is tracked normally on `main` as ordinary source. On a new or restored machine it arrives with the clone, and a missing or modified file is recovered with a normal Git restore:

```bash
git restore --source=main -- AGENTS.md .claude .serena
git status -sb
```
