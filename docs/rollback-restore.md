# Rollback And Restore

Rollback is a first-class workflow because this repository writes global Codex configuration, installed plugin cache, MCP runtime definitions, hooks, and global instructions.

## Safety Model

- Default commands are read-only.
- Restore requires an explicit backup timestamp.
- Before restore, the rollback script creates a pre-restore backup of the current `AGENTS.md` and `config.toml`.
- The script restores only files that the installer backs up: `AGENTS.md` and `config.toml`.
- Plugin cache rollback is handled by checking out an older Git revision and rerunning the installer.

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

## Failure Diagnosis Before Rollback

Before changing state, collect local evidence:

```bash
scripts/collect_diagnostics.sh --include-doctor
```

This keeps the failed state available for later analysis without storing secrets.
