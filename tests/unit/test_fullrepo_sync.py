from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

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


def clone_repo(remote: Path, clone: Path) -> Path:
    git(clone.parent, "clone", str(remote), str(clone))
    configure_git_identity(clone)
    git(clone, "checkout", "main")
    return clone


def test_agent_only_and_runtime_paths() -> None:
    assert mod.is_agent_path("AGENTS.md") is True
    assert mod.is_agent_path(".claude/CLAUDE.md") is True
    assert mod.is_agent_path(".serena/memories/CORE-01-INDEX.md") is True
    assert mod.is_agent_path(".serena/research/CODEX-2026-05-15-OFFICIAL-CAPABILITIES.md") is True

    assert mod.is_agent_path(".serena/.sync_marker") is False
    assert mod.is_agent_path(".serena/cache/symbols.pkl") is False
    assert mod.is_agent_path("plugins/rldyour-flow/hooks.json") is False


def test_cli_delegates_to_repo_local_fullrepo_wrapper(tmp_path: Path) -> None:
    git(tmp_path, "init")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/fullrepo_sync.py").write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json",
                "import os",
                "import sys",
                "print(json.dumps({",
                "    'argv': sys.argv[1:],",
                f"    'guard': os.environ.get({mod.DELEGATION_GUARD_ENV!r}),",
                "}, sort_keys=True))",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    proc = subprocess.run(
        [sys.executable, str(Path(mod.__file__)), "--status-json"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout) == {
        "argv": ["--status-json"],
        "guard": "1",
    }


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


def test_restore_local_uses_existing_tracking_ref_without_fetch(tmp_path: Path, monkeypatch) -> None:
    remote, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")
    mod.publish("origin", "fullrepo")

    clone = tmp_path / "clone-local"
    git(tmp_path, "clone", str(remote), str(clone))
    configure_git_identity(clone)
    monkeypatch.chdir(clone)
    git(clone, "checkout", "main")
    assert not (clone / "AGENTS.md").exists()

    def fail_fetch(*_args, **_kwargs):
        raise AssertionError("restore_local must not fetch or inspect the network")

    monkeypatch.setattr(mod, "fetch_fullrepo", fail_fetch)
    mod.restore_local("origin", "fullrepo")

    assert (clone / "AGENTS.md").read_text(encoding="utf-8") == "agent docs\n"


def test_status_local_only_uses_existing_tracking_ref_without_network(tmp_path: Path, monkeypatch) -> None:
    remote, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")
    mod.publish("origin", "fullrepo")

    clone = tmp_path / "clone-status-local"
    git(tmp_path, "clone", str(remote), str(clone))
    configure_git_identity(clone)
    monkeypatch.chdir(clone)
    git(clone, "checkout", "main")
    (clone / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")

    def fail_network(*_args, **_kwargs):
        raise AssertionError("local-only status must not fetch or query the network")

    monkeypatch.setattr(mod, "fetch_fullrepo", fail_network)
    monkeypatch.setattr(mod, "remote_branch_sha", fail_network)

    payload = mod.status("origin", "fullrepo", local_only=True)

    assert payload["network_checked"] is False
    assert payload["remote_configured"] is True
    assert payload["remote_fullrepo_exists"] is True
    assert payload["fullrepo_matches_worktree"] is True


def test_status_reports_missing_remote_without_treating_local_ref_as_network(tmp_path: Path, monkeypatch) -> None:
    git(tmp_path, "init")
    git(tmp_path, "checkout", "-b", "main")
    configure_git_identity(tmp_path)
    (tmp_path / "README.md").write_text("repo\n", encoding="utf-8")
    git(tmp_path, "add", "README.md")
    git(tmp_path, "commit", "-m", "init")
    monkeypatch.chdir(tmp_path)

    payload = mod.status("origin", "fullrepo", local_only=True)

    assert payload["network_checked"] is False
    assert payload["remote_configured"] is False
    assert payload["remote_fullrepo_exists"] is False


def test_bootstrap_init_skips_missing_compatible_overlay(monkeypatch) -> None:
    printed: list[dict[str, object]] = []

    monkeypatch.setattr(
        mod,
        "_project_policy",
        lambda: {"effective": {"fullrepo": {"mode": "auto", "install_exclude": False}}},
    )
    monkeypatch.setattr(mod, "enforce_fullrepo_policy", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(mod, "repo_root", lambda: Path("/repo"))
    monkeypatch.setattr(mod, "iter_worktree_agent_files", lambda _root: [])
    monkeypatch.setattr(mod, "fetch_fullrepo", lambda _remote, _branch: True)
    monkeypatch.setattr(mod, "tracked_agent_paths_in_index", lambda: [])
    monkeypatch.setattr(mod, "status", lambda _remote, _branch: {"ok": True})
    monkeypatch.setattr(mod, "print_status", lambda payload, as_json=False: printed.append(payload))

    def fail_restore(*_args, **_kwargs):
        raise mod.FullrepoError(
            "no compatible fullrepo overlay found in refs/remotes/origin/fullrepo "
            "for source abc (tree def)"
        )

    monkeypatch.setattr(mod, "restore", fail_restore)

    mod.bootstrap_init("origin", "fullrepo")

    assert printed == [
        {
            "ok": True,
            "bootstrap_actions": ["restore-skipped-no-compatible-overlay"],
        }
    ]


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
        "Danil Silantyev <rldyourmnd@users.noreply.github.com>|"
        "Danil Silantyev <rldyourmnd@users.noreply.github.com>"
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


def test_fullrepo_disabled_policy_refuses_publish_and_returns_stub_status(tmp_path: Path, monkeypatch) -> None:
    _, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / ".rldyour").mkdir()
    (work / ".rldyour/project-policy.json").write_text(
        '{"schema_version":1,"fullrepo":{"mode":"disabled"}}',
        encoding="utf-8",
    )
    git(work, "add", ".rldyour/project-policy.json")
    git(work, "commit", "-m", "policy")
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")

    payload = mod.status("origin", "fullrepo")

    assert payload["mode"] == "disabled"
    assert payload["fullrepo_needs_attention"] is False
    assert payload["worktree_agent_paths"] == []
    try:
        mod.publish("origin", "fullrepo")
    except mod.FullrepoError as exc:
        assert "fullrepo disabled by project policy" in str(exc)
    else:
        raise AssertionError("publish should be refused when fullrepo is disabled")


def test_bootstrap_init_does_not_create_missing_fullrepo_without_explicit_policy(tmp_path: Path, monkeypatch) -> None:
    remote, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")

    mod.bootstrap_init("origin", "fullrepo")

    assert mod.remote_branch_sha("origin", "fullrepo") == ""
    assert mod.local_ref_sha("refs/heads/fullrepo") == ""
    assert remote.is_dir()


def test_bootstrap_ci_restores_exact_head_overlay_without_publish(tmp_path: Path, monkeypatch) -> None:
    remote, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")
    (work / ".serena/memories").mkdir(parents=True)
    (work / ".serena/memories/CORE-01-INDEX.md").write_text("memory\n", encoding="utf-8")
    mod.publish("origin", "fullrepo")

    clone = clone_repo(remote, tmp_path / "clone-bootstrap-ci")
    monkeypatch.chdir(clone)
    receipt = clone / "receipt.json"

    mod.bootstrap_ci("origin", "fullrepo", attempts=1, sleep_seconds=0, receipt_path=receipt)

    assert (clone / "AGENTS.md").read_text(encoding="utf-8") == "agent docs\n"
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert payload["state"] == "PASS"
    assert payload["mode"] == "bootstrap-ci"
    assert payload["resolution_mode"] == "exact-head"
    assert payload["restore_count"] == 2
    assert mod.local_ref_sha("refs/heads/fullrepo") == ""


def test_bootstrap_ci_works_from_detached_head(tmp_path: Path, monkeypatch) -> None:
    remote, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")
    mod.publish("origin", "fullrepo")

    clone = clone_repo(remote, tmp_path / "clone-bootstrap-ci-detached")
    commit = git(clone, "rev-parse", "HEAD")
    git(clone, "checkout", "--detach", commit)
    monkeypatch.chdir(clone)

    mod.bootstrap_ci(
        "origin",
        "fullrepo",
        attempts=1,
        sleep_seconds=0,
        receipt_path=clone / "receipt.json",
    )

    assert (clone / "AGENTS.md").read_text(encoding="utf-8") == "agent docs\n"


def test_bootstrap_ci_retries_until_overlay_resolves(tmp_path: Path, monkeypatch) -> None:
    remote, work = init_repo(tmp_path)
    monkeypatch.chdir(work)
    (work / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")
    mod.publish("origin", "fullrepo")

    clone = clone_repo(remote, tmp_path / "clone-bootstrap-ci-retry")
    monkeypatch.chdir(clone)
    original_resolve = mod.resolve_fullrepo_ref
    calls = {"count": 0}

    def flaky_resolve(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] == 1:
            raise mod.FullrepoError("overlay not ready yet")
        return original_resolve(*args, **kwargs)

    monkeypatch.setattr(mod, "resolve_fullrepo_ref", flaky_resolve)

    mod.bootstrap_ci(
        "origin",
        "fullrepo",
        attempts=2,
        sleep_seconds=0,
        receipt_path=clone / "receipt.json",
    )

    payload = json.loads((clone / "receipt.json").read_text(encoding="utf-8"))
    assert calls["count"] == 2
    assert payload["state"] == "PASS"
    assert payload["attempt"] == 2
    assert payload["errors"] == ["attempt 1: overlay not ready yet"]


def test_bootstrap_ci_fails_missing_overlay_without_publish(tmp_path: Path, monkeypatch) -> None:
    remote, work = init_repo(tmp_path)
    clone = clone_repo(remote, tmp_path / "clone-bootstrap-ci-missing")
    monkeypatch.chdir(clone)
    receipt = clone / "receipt.json"

    try:
        mod.bootstrap_ci("origin", "fullrepo", attempts=1, sleep_seconds=0, receipt_path=receipt)
    except mod.FullrepoError as exc:
        assert "fullrepo branch origin/fullrepo does not exist or could not be fetched" in str(exc)
    else:
        raise AssertionError("bootstrap_ci should fail without a compatible fullrepo overlay")

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert payload["state"] == "FAIL"
    assert mod.remote_branch_sha("origin", "fullrepo") == ""
    assert mod.local_ref_sha("refs/heads/fullrepo") == ""
