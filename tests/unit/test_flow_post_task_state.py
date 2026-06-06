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
    (tmp_path / ".serena/.flow_blocker_ack.json").write_text('{"fingerprint": "same"}', encoding="utf-8")

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
    monkeypatch.setattr(mod, "_branch_cleanup_state", lambda _branch, _policy: {"needs_cleanup": False})
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


def test_state_requires_remote_fullrepo_only_when_policy_requires_it(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(mod, "_serena_current", lambda: (True, {}))
    monkeypatch.setattr(mod, "_instruction_docs_state", lambda: {})
    (tmp_path / ".rldyour").mkdir()
    (tmp_path / ".rldyour/project-policy.json").write_text(
        '{"schema_version":1,"fullrepo":{"mode":"required"}}',
        encoding="utf-8",
    )
    git(tmp_path, "add", ".rldyour/project-policy.json")
    git(tmp_path, "commit", "-m", "policy")

    monkeypatch.setattr(mod, "_branch_cleanup_state", lambda _branch, _policy: {"needs_cleanup": False})
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


def test_foreign_policy_allows_tracked_ai_docs_without_fullrepo_loop(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".rldyour").mkdir()
    (tmp_path / ".rldyour/project-policy.json").write_text(
        json_policy(
            fullrepo={"mode": "disabled"},
            normal_branch_policy={
                "agent_files": "allowed",
                "ai_marker_additions": "allowed",
                "instruction_docs": "tracked-normal-branch",
            },
            instruction_docs={"mode": "tracked-normal-branch"},
            branch_cleanup={"mode": "advisory", "protected_branches": ["main", "dev"]},
            stop_hook={"block_on_fullrepo": False, "block_on_branch_cleanup": False},
        ),
        encoding="utf-8",
    )
    (tmp_path / "AGENTS.md").write_text("agent docs\n", encoding="utf-8")
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude/CLAUDE.md").write_text("claude docs\n", encoding="utf-8")
    (tmp_path / ".serena/memories").mkdir(parents=True)
    (tmp_path / ".serena/memories/CORE-01-INDEX.md").write_text("memory\n", encoding="utf-8")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "track project ai docs")

    monkeypatch.setattr(mod, "_serena_current", lambda: (True, {}))
    monkeypatch.setattr(mod, "_instruction_docs_state", lambda: {"needs_instruction_docs_review": False})

    payload = mod.state()

    assert payload["project_policy"]["source"] == ".rldyour/project-policy.json"
    assert payload["fullrepo_needs_attention"] is False
    assert payload["branch_cleanup_state"]["protected_branches"].count("dev") == 1
    assert payload["blocking_reasons"] == []
    assert payload["needs_flow_sync"] is False


def test_branch_cleanup_dev_is_protected_and_nonworkflow_is_advisory(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    git(tmp_path, "checkout", "-b", "dev")
    git(tmp_path, "checkout", "main")
    git(tmp_path, "checkout", "-b", "feature/merged")
    (tmp_path / "feature.txt").write_text("feature\n", encoding="utf-8")
    git(tmp_path, "add", "feature.txt")
    git(tmp_path, "commit", "-m", "feature")
    git(tmp_path, "checkout", "main")
    git(tmp_path, "merge", "--no-ff", "feature/merged", "-m", "merge feature")

    state = mod._branch_cleanup_state("main", mod.load_policy(tmp_path))

    assert "dev" not in state["local_merged_branches"]
    assert "feature/merged" in state["advisory_local_branches"]
    assert state["blocking_candidates"] == []
    assert state["needs_cleanup"] is False


def test_strict_branch_cleanup_blocks_workflow_branches(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".rldyour").mkdir()
    (tmp_path / ".rldyour/project-policy.json").write_text(
        json_policy(branch_cleanup={"mode": "strict", "block_stop": True}),
        encoding="utf-8",
    )
    git(tmp_path, "checkout", "-b", "codex/merged")
    (tmp_path / "workflow.txt").write_text("workflow\n", encoding="utf-8")
    git(tmp_path, "add", "workflow.txt")
    git(tmp_path, "commit", "-m", "workflow")
    git(tmp_path, "checkout", "main")
    git(tmp_path, "merge", "--no-ff", "codex/merged", "-m", "merge workflow")

    state = mod._branch_cleanup_state("main", mod.load_policy(tmp_path))

    assert "codex/merged" in state["blocking_local_branches"]
    assert state["needs_cleanup"] is True


def test_orchestrator_worker_reports_dirty_without_global_fullrepo_block(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    monkeypatch.setenv("RLDYOUR_EXECUTION_MODE", "orchestrator")
    monkeypatch.setenv("RLDYOUR_AGENT_ROLE", "worker")
    monkeypatch.setenv("RLDYOUR_WORKER_ID", "worker-codex-test")
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("repo\nworker change\n", encoding="utf-8")

    monkeypatch.setattr(mod, "_serena_current", lambda: (False, {"reason": "stale"}))
    monkeypatch.setattr(mod, "_instruction_docs_state", lambda: {"needs_instruction_docs_review": True})
    monkeypatch.setattr(
        mod,
        "_branch_cleanup_state",
        lambda _branch, _policy: {
            "needs_cleanup": True,
            "blocking_candidates": ["codex/merged"],
            "advisory_candidates": [],
        },
    )
    monkeypatch.setattr(
        mod,
        "_fullrepo_state",
        lambda: {
            "exclude_installed": False,
            "network_checked": False,
            "remote_configured": False,
            "remote_fullrepo_exists": False,
            "local_fullrepo_sha": None,
            "fullrepo_matches_worktree": False,
            "local_fullrepo_matches_worktree": False,
            "tracked_agent_paths": [],
            "worktree_agent_paths": ["AGENTS.md"],
        },
    )

    payload = mod.state()

    assert payload["execution"]["agent_role"] == "worker"
    assert payload["execution"]["worker_id"] == "worker-codex-test"
    assert "worker-report-required" in payload["blocking_reasons"]
    assert "fullrepo-required" not in payload["blocking_reasons"]
    assert "branch-cleanup-required" not in payload["blocking_reasons"]
    assert "serena-stale" not in payload["blocking_reasons"]
    assert "worker-fullrepo-report" in payload["advisory_reasons"]
    assert "worker-branch-cleanup-report" in payload["advisory_reasons"]
    assert "worker-serena-stale-report" in payload["advisory_reasons"]
    assert payload["needs_flow_sync"] is True


def test_orchestrator_worker_dirty_outside_assigned_scope_blocks_report(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    monkeypatch.setenv("RLDYOUR_EXECUTION_MODE", "orchestrator")
    monkeypatch.setenv("RLDYOUR_AGENT_ROLE", "worker")
    monkeypatch.setenv("RLDYOUR_WORKER_ALLOWED_PATHS", "docs/")
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("repo\nout of scope\n", encoding="utf-8")

    monkeypatch.setattr(mod, "_serena_current", lambda: (True, {}))
    monkeypatch.setattr(mod, "_instruction_docs_state", lambda: {})
    monkeypatch.setattr(mod, "_branch_cleanup_state", lambda _branch, _policy: {"needs_cleanup": False})
    monkeypatch.setattr(
        mod,
        "_fullrepo_state",
        lambda: {
            "exclude_installed": True,
            "network_checked": False,
            "remote_configured": False,
            "remote_fullrepo_exists": False,
            "local_fullrepo_sha": None,
            "fullrepo_matches_worktree": True,
            "local_fullrepo_matches_worktree": True,
            "tracked_agent_paths": [],
            "worktree_agent_paths": [],
        },
    )

    payload = mod.state()

    assert payload["execution"]["worker_allowed_paths"] == ["docs"]
    assert "worker-dirty-out-of-scope" in payload["blocking_reasons"]
    assert "worker-report-required" in payload["blocking_reasons"]


def json_policy(**sections: object) -> str:
    import json

    payload = {"schema_version": 1}
    payload.update(sections)
    return json.dumps(payload)
