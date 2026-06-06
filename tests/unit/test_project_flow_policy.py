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
    assert effective["fullrepo"]["mode"] == "auto"
    assert effective["fullrepo"]["create_if_missing"] is False
    assert effective["branch_cleanup"]["mode"] == "advisory"
    assert "dev" in effective["branch_cleanup"]["protected_branches"]


def test_tracked_local_and_env_policy_precedence(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    tracked = write_policy(
        tmp_path,
        ".rldyour/project-policy.json",
        {"schema_version": 1, "fullrepo": {"mode": "required"}},
    )
    local = write_policy(
        tmp_path,
        ".rldyour/project-policy.local.json",
        {"schema_version": 1, "fullrepo": {"mode": "disabled"}},
    )
    env_policy = write_policy(
        tmp_path,
        "env-policy.json",
        {"schema_version": 1, "fullrepo": {"mode": "advisory"}},
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
    assert payload["effective"]["fullrepo"]["mode"] == "advisory"


def test_policy_unknown_fields_are_warnings_unless_strict(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    write_policy(
        tmp_path,
        ".rldyour/project-policy.json",
        {"schema_version": 1, "fullrepo": {"mode": "disabled", "surprise": True}},
    )
    monkeypatch.chdir(tmp_path)

    loose = mod.load_policy(tmp_path)
    strict = mod.load_policy(tmp_path, strict=True)

    assert loose["valid"] is True
    assert "unknown policy field: fullrepo.surprise" in loose["warnings"]
    assert strict["valid"] is False
    assert "unknown policy field: fullrepo.surprise" in strict["errors"]


def test_invalid_policy_fails_closed_for_runtime_markers_and_secrets(tmp_path: Path, monkeypatch) -> None:
    init_repo(tmp_path)
    write_policy(
        tmp_path,
        ".rldyour/project-policy.json",
        {
            "schema_version": 1,
            "normal_branch_policy": {"runtime_markers": "allowed", "secrets": "allowed"},
            "fullrepo": {"mode": "nonsense"},
            "branch_cleanup": {"mode": "nonsense"},
        },
    )
    monkeypatch.chdir(tmp_path)

    payload = mod.load_policy(tmp_path)
    normal = payload["effective"]["normal_branch_policy"]

    assert payload["valid"] is False
    assert normal["runtime_markers"] == "forbidden"
    assert normal["secrets"] == "forbidden"
    assert payload["effective"]["fullrepo"]["mode"] == "auto"
    assert payload["effective"]["branch_cleanup"]["mode"] == "advisory"
