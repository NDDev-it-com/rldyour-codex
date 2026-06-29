from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TIMEOUT = 60

MANAGED_STATUS_LINE = [
    "model-with-reasoning",
    "context-remaining",
    "five-hour-limit",
    "weekly-limit",
    "git-branch",
    "current-dir",
]


def run_installer(codex_home: Path) -> None:
    subprocess.run(
        ["bash", "scripts/install_system_codex.sh", "--apply", "--codex-home", str(codex_home)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=DEFAULT_TIMEOUT,
    )


def load_toml(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def assert_managed_tui(data: dict) -> None:
    tui = data.get("tui")
    assert isinstance(tui, dict), data
    assert tui.get("status_line") == MANAGED_STATUS_LINE, tui
    assert tui.get("status_line_use_colors") is True, tui


def test_fresh_install_writes_managed_tui_status_line(tmp_path: Path) -> None:
    codex_home = tmp_path / "fresh"
    codex_home.mkdir()

    run_installer(codex_home)

    assert_managed_tui(load_toml(codex_home / "config.toml"))
    assert_managed_tui(load_toml(codex_home / "rldyour-yolo.config.toml"))
    assert_managed_tui(load_toml(codex_home / "rldyour-safe.config.toml"))


def test_existing_tui_keys_preserved_and_status_line_managed(tmp_path: Path) -> None:
    codex_home = tmp_path / "keep"
    codex_home.mkdir()
    (codex_home / "config.toml").write_text(
        "\n".join(
            [
                "[tui]",
                "notifications = true",
                'status_line = ["model"]',
                "animations = false",
                "",
                "[tui.extra]",
                "custom = 1",
                "",
            ]
        ),
        encoding="utf-8",
    )

    run_installer(codex_home)

    data = load_toml(codex_home / "config.toml")
    assert_managed_tui(data)
    assert data["tui"]["notifications"] is True
    assert data["tui"]["animations"] is False
    assert data["tui"]["extra"] == {"custom": 1}


def test_root_dotted_tui_keys_migrate_into_managed_table(tmp_path: Path) -> None:
    codex_home = tmp_path / "dotted"
    codex_home.mkdir()
    (codex_home / "config.toml").write_text(
        'tui.notifications = true\ntui.status_line = ["model"]\n',
        encoding="utf-8",
    )

    run_installer(codex_home)

    data = load_toml(codex_home / "config.toml")
    assert_managed_tui(data)
    assert data["tui"]["notifications"] is True


def test_reinstall_is_idempotent_for_tui(tmp_path: Path) -> None:
    # Full-file equality is not asserted because the post-install hook trust
    # refresh may append [hooks.state] through a live codex app-server.
    codex_home = tmp_path / "idem"
    codex_home.mkdir()

    run_installer(codex_home)
    first = load_toml(codex_home / "config.toml")
    run_installer(codex_home)
    second_text = (codex_home / "config.toml").read_text(encoding="utf-8")
    second = tomllib.loads(second_text)

    assert first["tui"] == second["tui"]
    assert_managed_tui(second)
    assert second_text.count("status_line =") == 1
