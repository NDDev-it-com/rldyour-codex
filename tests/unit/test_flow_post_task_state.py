from __future__ import annotations

from pathlib import Path
import subprocess

from tests.support.importing import import_script


mod = import_script("plugins/rldyour-flow/scripts/flow_post_task_state.py")


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def init_repo(path: Path) -> None:
    git(path, "init")
    git(path, "checkout", "-b", "main")
    git(path, "config", "user.email", "flow-state@example.invalid")
    git(path, "config", "user.name", "Flow State")
    (path / "README.md").write_text("repo\n", encoding="utf-8")
    git(path, "add", "README.md")
    git(path, "commit", "-m", "init")


def test_installed_script_uses_codex_home(monkeypatch, tmp_path: Path) -> None:
    codex_home = tmp_path / "codex-home"
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    plugin_root = codex_home / "plugins/cache/rldyour-codex/rldyour-flow/0.3.3"
    (plugin_root / ".codex-plugin").mkdir(parents=True)
    (plugin_root / ".codex-plugin/plugin.json").write_text(
        '{"name":"rldyour-flow","version":"0.3.3"}',
        encoding="utf-8",
    )

    assert mod._installed_script("rldyour-flow", "scripts/fullrepo_sync.py") == (
        plugin_root / "scripts/fullrepo_sync.py"
    )


def test_installed_script_uses_legacy_local_when_versioned_cache_missing(monkeypatch, tmp_path: Path) -> None:
    codex_home = tmp_path / "codex-home"
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    assert mod._installed_script("rldyour-flow", "scripts/fullrepo_sync.py") == (
        codex_home / "plugins/cache/rldyour-codex/rldyour-flow/local/scripts/fullrepo_sync.py"
    )


def test_installed_script_falls_back_to_home(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("CODEX_HOME", raising=False)
    monkeypatch.setattr(mod.Path, "home", staticmethod(lambda: tmp_path))

    assert mod._codex_home() == tmp_path / ".codex"


def test_state_reports_non_git_repo(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    monkeypatch.chdir(tmp_path)

    assert mod.state() == {"is_git_repo": False, "needs_flow_sync": False, "serena_current": True}


def test_state_tracks_clean_and_dirty_git_repo(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    clean = mod.state()
    assert clean["is_git_repo"] is True
    assert clean["branch"] == "main"
    assert clean["dirty_count"] == 0
    assert clean["needs_flow_sync"] is False

    (tmp_path / "README.md").write_text("repo\nchanged\n", encoding="utf-8")
    dirty = mod.state()
    assert dirty["dirty_count"] == 1
    assert dirty["dirty_files"] == ["README.md"]
    assert dirty["needs_flow_sync"] is True


def test_state_ignores_bootstrap_only_serena_files(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    git(tmp_path, "init")
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".serena").mkdir()
    (tmp_path / ".serena/project.yml").write_text("project_name: smoke\n", encoding="utf-8")
    (tmp_path / ".serena/.gitignore").write_text("/cache\n", encoding="utf-8")
    (tmp_path / ".serena/.flow_sync_marker").write_text("marker\n", encoding="utf-8")
    (tmp_path / ".serena/.flow_post_task_state.json").write_text('{"needs_flow_sync": true}', encoding="utf-8")

    payload = mod.state()
    assert payload["is_git_repo"] is True
    assert payload["dirty_files"] == []
    assert payload["needs_flow_sync"] is False


def test_state_does_not_loop_on_local_only_fullrepo_without_remote(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(mod, "_serena_current", lambda: (True, {}))
    monkeypatch.setattr(mod, "_instruction_docs_state", lambda: {})
    monkeypatch.setattr(mod, "_branch_cleanup_state", lambda _branch: {"needs_cleanup": False})
    monkeypatch.setattr(
        mod,
        "_fullrepo_state",
        lambda: {
            "exclude_installed": True,
            "network_checked": False,
            "remote_configured": False,
            "remote_fullrepo_exists": False,
            "local_fullrepo_sha": "abc123",
            "fullrepo_matches_worktree": True,
            "local_fullrepo_matches_worktree": True,
            "tracked_agent_paths": [],
            "worktree_agent_paths": ["AGENTS.md", ".serena/memories/CORE-01-INDEX.md"],
        },
    )

    payload = mod.state()

    assert payload["fullrepo_needs_attention"] is False
    assert payload["needs_flow_sync"] is False


def test_state_requires_remote_fullrepo_when_network_remote_is_configured(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(mod, "_serena_current", lambda: (True, {}))
    monkeypatch.setattr(mod, "_instruction_docs_state", lambda: {})
    monkeypatch.setattr(mod, "_branch_cleanup_state", lambda _branch: {"needs_cleanup": False})
    monkeypatch.setattr(
        mod,
        "_fullrepo_state",
        lambda: {
            "exclude_installed": True,
            "network_checked": True,
            "remote_configured": True,
            "remote_fullrepo_exists": False,
            "local_fullrepo_sha": "abc123",
            "fullrepo_matches_worktree": True,
            "local_fullrepo_matches_worktree": True,
            "tracked_agent_paths": [],
            "worktree_agent_paths": ["AGENTS.md"],
        },
    )

    payload = mod.state()

    assert payload["fullrepo_needs_attention"] is True
    assert payload["needs_flow_sync"] is True
