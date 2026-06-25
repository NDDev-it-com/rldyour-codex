from __future__ import annotations

import json
from pathlib import Path
import subprocess

from tests.support.importing import import_script


mod = import_script("plugins/rldyour-flow/scripts/project_flow_policy.py")


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def init_repo(path: Path) -> None:
    git(path, "init")
    git(path, "checkout", "-b", "main")
    git(path, "config", "user.email", "policy@example.invalid")
    git(path, "config", "user.name", "Policy Test")
    (path / "README.md").write_text("repo\n", encoding="utf-8")
    git(path, "add", "README.md")
    git(path, "commit", "-m", "init")


def write_policy(root: Path, name: str, payload: dict) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_default_policy_is_non_destructive(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    monkeypatch.chdir(tmp_path)

    payload = mod.load_policy(tmp_path)

    assert payload["source_kind"] == "default"
    assert payload["valid"] is True
    effective = payload["effective"]
    # Agent context is tracked normally on main; there is no fullrepo section.
    assert "fullrepo" not in effective
    assert effective["normal_branch_policy"]["agent_files"] == "allowed"
    assert effective["instruction_docs"]["mode"] == "tracked-main"
    assert effective["serena"]["memory_storage"] == "tracked-main"
    assert effective["execution"]["mode"] == "standard"
    assert effective["execution"]["agent_role"] == "auto"
    assert effective["execution"]["task_delegation"] == "direct"
    assert effective["cmux"]["enabled"] is False
    assert effective["cmux"]["version_policy"] == "latest-compatible"
    assert effective["orchestrator"]["concurrency"]["default_strategy"] == "single-writer"
    assert "fullrepo" not in effective["orchestrator"]["worker_permissions"]
    assert "block_on_fullrepo" not in effective["stop_hook"]
    assert effective["branch_cleanup"]["mode"] == "advisory"
    assert "dev" in effective["branch_cleanup"]["protected_branches"]
    assert "fullrepo" not in effective["branches"]["protected_branches"]


def test_tracked_local_and_env_policy_precedence(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    tracked = write_policy(
        tmp_path,
        ".rldyour/project-policy.json",
        {"schema_version": 1, "branch_cleanup": {"mode": "strict"}},
    )
    local = write_policy(
        tmp_path,
        ".rldyour/project-policy.local.json",
        {"schema_version": 1, "branch_cleanup": {"mode": "disabled"}},
    )
    env_policy = write_policy(
        tmp_path,
        "env-policy.json",
        {"schema_version": 1, "branch_cleanup": {"mode": "advisory"}},
    )
    monkeypatch.setenv("RLDYOUR_PROJECT_POLICY", str(env_policy))
    monkeypatch.chdir(tmp_path)

    payload = mod.load_policy(tmp_path)

    assert payload["sources"] == [
        {"kind": "tracked", "path": str(tracked.relative_to(tmp_path))},
        {"kind": "local", "path": str(local.relative_to(tmp_path))},
        {"kind": "env", "path": str(env_policy.relative_to(tmp_path))},
    ]
    assert payload["source_kind"] == "env"
    assert payload["effective"]["branch_cleanup"]["mode"] == "advisory"


def test_policy_unknown_fields_are_warnings_unless_strict(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    write_policy(
        tmp_path,
        ".rldyour/project-policy.json",
        {"schema_version": 1, "serena": {"mode": "enabled", "surprise": True}},
    )
    monkeypatch.chdir(tmp_path)

    loose = mod.load_policy(tmp_path)
    strict = mod.load_policy(tmp_path, strict=True)

    assert loose["valid"] is True
    assert "unknown policy field: serena.surprise" in loose["warnings"]
    assert strict["valid"] is False
    assert "unknown policy field: serena.surprise" in strict["errors"]


def test_invalid_policy_fails_closed_for_runtime_markers_and_secrets(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    write_policy(
        tmp_path,
        ".rldyour/project-policy.json",
        {
            "schema_version": 1,
            "normal_branch_policy": {"runtime_markers": "allowed", "secrets": "allowed"},
            "branch_cleanup": {"mode": "nonsense"},
        },
    )
    monkeypatch.chdir(tmp_path)

    payload = mod.load_policy(tmp_path)
    normal = payload["effective"]["normal_branch_policy"]

    assert payload["valid"] is False
    assert normal["runtime_markers"] == "forbidden"
    assert normal["secrets"] == "forbidden"
    assert "fullrepo" not in payload["effective"]
    assert payload["effective"]["branch_cleanup"]["mode"] == "advisory"


def test_execution_and_cmux_policy_are_validated(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    write_policy(
        tmp_path,
        ".rldyour/project-policy.json",
        {
            "schema_version": 1,
            "execution": {
                "mode": "orchestrator",
                "agent_role": "auto",
                "worker_agents": ["codex", "claude", "opencode"],
                "worker_count_min": 1,
                "worker_count_max": 4,
                "task_delegation": "explicit-orchestrator-only",
            },
            "cmux": {"enabled": True, "install_method": "brew-cask"},
        },
    )
    monkeypatch.chdir(tmp_path)

    payload = mod.load_policy(tmp_path)

    assert payload["valid"] is True
    assert payload["effective"]["execution"]["mode"] == "orchestrator"
    assert payload["effective"]["execution"]["worker_count_max"] == 4
    assert payload["effective"]["cmux"]["enabled"] is True
    assert payload["effective"]["cmux"]["install_method"] == "brew-cask"


def test_invalid_worker_count_fails_non_destructively(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    write_policy(
        tmp_path,
        ".rldyour/project-policy.json",
        {
            "schema_version": 1,
            "execution": {
                "mode": "orchestrator",
                "worker_count_min": 5,
                "worker_count_max": 2,
            },
        },
    )
    monkeypatch.chdir(tmp_path)

    payload = mod.load_policy(tmp_path)

    assert payload["valid"] is False
    assert "execution.worker_count_min must be <= execution.worker_count_max" in payload["errors"]
    assert payload["effective"]["execution"]["mode"] == "orchestrator"
