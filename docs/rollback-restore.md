# Rollback And Restore

Rollback is a first-class workflow because this repository writes global Codex configuration, installed plugin cache, MCP runtime definitions, hooks, and global instructions.

## Safety Model

- Default commands are read-only.
- Restore requires an explicit backup timestamp.
- Before restore, the rollback script creates a pre-restore backup of the current `AGENTS.md`, `config.toml`, managed `agents/*.toml`, and managed `rules/*.rules`.
- The script restores only files that the installer backs up: `AGENTS.md`, `config.toml`, managed `agents/*.toml`, and managed `rules/*.rules`.
- File restore writes through a temporary file in the target directory and then renames it into place, so a copy failure should not leave a partially written target file.
- Plugin cache rollback is handled by checking out an older Git revision and rerunning the installer.
- Agent-only context rollback is handled by restoring or republishing the `fullrepo` branch after the normal branch state is selected.

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
scripts/sync_fullrepo_branch.sh --restore
```

## Failure Diagnosis Before Rollback

Before changing state, collect local evidence:

```bash
scripts/collect_diagnostics.sh --include-doctor
```

This keeps the failed state available for later analysis without storing secrets.

## Restore Fullrepo Agent Context

Use this when `AGENTS.md`, `.serena` knowledge, or other agent-only files are missing on a new or restored machine:

```bash
scripts/sync_fullrepo_branch.sh --restore
scripts/sync_fullrepo_branch.sh --status
```
