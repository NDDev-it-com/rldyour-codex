from __future__ import annotations

from pathlib import Path
import subprocess

from tests.support.importing import import_script


mod = import_script("plugins/rldyour-flow/scripts/fullrepo_sync.py")


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def configure_git_identity(cwd: Path) -> None:
    git(cwd, "config", "user.email", "test@example.test")
    git(cwd, "config", "user.name", "Test User")


def init_repo(tmp_path: Path) -> tuple[Path, Path]:
    remote = tmp_path / "remote.git"
    work = tmp_path / "work"
    git(tmp_path, "init", "--bare", str(remote))
    git(tmp_path, "init", str(work))
    git(work, "checkout", "-b", "main")
    configure_git_identity(work)
    git(work, "remote", "add", "origin", str(remote))
    (work / "README.md").write_text("repo\n", encoding="utf-8")
    git(work, "add", "README.md")
    git(work, "commit", "-m", "init")
    git(work, "push", "-u", "origin", "main")
    return remote, work


def test_agent_only_and_runtime_paths() -> None:
    assert mod.is_agent_path("AGENTS.md") is True
    assert mod.is_agent_path(".claude/CLAUDE.md") is True
    assert mod.is_agent_path(".serena/memories/CORE-01-INDEX.md") is True
    assert mod.is_agent_path(".serena/research/CODEX-2026-05-15-OFFICIAL-CAPABILITIES.md") is True

    assert mod.is_agent_path(".serena/.sync_marker") is False
    assert mod.is_agent_path(".serena/cache/symbols.pkl") is False
    assert mod.is_agent_path("plugins/rldyour-flow/hooks.json") is False


def test_exclude_block_contains_runtime_negations() -> None:
    block = mod.exclude_block()
    assert block.startswith(mod.EXCLUDE_BEGIN)
    assert "/AGENTS.md" in block
    assert "/.serena/memories/**" in block
    assert "!/.serena/.sync_marker" in block
    assert block.endswith(mod.EXCLUDE_END + "\n")


def test_split_porcelain_path_handles_renames() -> None:
    assert mod.split_porcelain_path(" M AGENTS.md") == "AGENTS.md"
    assert mod.split_porcelain_path("R  old.md -> .claude/CLAUDE.md") == ".claude/CLAUDE.md"


def test_iter_worktree_agent_files_and_secret_scan(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text("safe", encoding="utf-8")
    (tmp_path / ".serena/memories").mkdir(parents=True)
    (tmp_path / ".serena/memories/CORE-01-INDEX.md").write_text("safe", encoding="utf-8")
    (tmp_path / ".serena/.sync_marker").write_text("runtime", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src/app.py").write_text("print('not agent')", encoding="utf-8")

    assert mod.iter_worktree_agent_files(tmp_path) == [
        ".serena/memories/CORE-01-INDEX.md",
        "AGENTS.md",
    ]

    assert mod.scan_for_secrets(tmp_path, ["AGENTS.md"]) == []
    (tmp_path / "AGENTS.md").write_text("Bearer " + "abcdefghijklmnopqrstuvwxyz", encoding="utf-8")
    assert mod.scan_for_secrets(tmp_path, ["AGENTS.md"]) == ["AGENTS.md"]


def test_publish_status_restore_and_migrate_main(tmp_path: Path, monkeypatch) -> None:
    remote, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")
    (work / ".serena/memories").mkdir(parents=True)
    (work / ".serena/memories/CORE-01-INDEX.md").write_text("memory\n", encoding="utf-8")

    assert mod.dirty_non_agent_paths() == []
    mod.publish("origin", "fullrepo")
    payload = mod.status("origin", "fullrepo")
    assert payload["fullrepo_matches_worktree"] is True
    assert "AGENTS.md" in payload["worktree_agent_paths"]

    clone = tmp_path / "clone"
    git(tmp_path, "clone", str(remote), str(clone))
    configure_git_identity(clone)
    monkeypatch.chdir(clone)
    git(clone, "checkout", "main")
    mod.restore("origin", "fullrepo")
    assert (clone / "AGENTS.md").read_text(encoding="utf-8") == "agent docs\n"

    git(clone, "add", "-f", "AGENTS.md")
    git(clone, "commit", "-m", "track agent doc")
    assert "AGENTS.md" in mod.tracked_agent_paths_in_index()
    mod.migrate_main()
    assert "AGENTS.md" not in mod.tracked_agent_paths_in_index()


def test_publish_uses_identity_env_fallback(tmp_path: Path, monkeypatch) -> None:
    _, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    for key in (
        "GIT_AUTHOR_NAME",
        "GIT_AUTHOR_EMAIL",
        "GIT_COMMITTER_NAME",
        "GIT_COMMITTER_EMAIL",
    ):
        monkeypatch.delenv(key, raising=False)
    git(work, "config", "--unset", "user.name")
    git(work, "config", "--unset", "user.email")
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")

    mod.publish("origin", "fullrepo")

    commit = git(work, "rev-parse", "refs/heads/fullrepo")
    identity = git(work, "show", "-s", "--format=%an <%ae>|%cn <%ce>", commit)
    assert identity == (
        "rldyour-codex <rldyour-codex@example.invalid>|"
        "rldyour-codex <rldyour-codex@example.invalid>"
    )


def test_publish_refuses_non_agent_dirty(tmp_path: Path, monkeypatch) -> None:
    _, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / "src.py").write_text("dirty\n", encoding="utf-8")
    try:
        mod.publish("origin", "fullrepo")
    except mod.FullrepoError as exc:
        assert "non-agent files are dirty" in str(exc)
    else:
        raise AssertionError("publish should refuse non-agent dirty files")
