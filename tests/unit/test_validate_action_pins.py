from __future__ import annotations

from pathlib import Path

from tests.support.importing import import_script

mod = import_script("scripts/validate_action_pins.py")


def test_is_external_action() -> None:
    assert mod.is_external_action("actions/checkout@0123456789012345678901234567890123456789")
    assert not mod.is_external_action("./.github/actions/setup")
    assert not mod.is_external_action("docker://alpine:3.20")


def test_validate_file_rejects_tag_pin(tmp_path: Path) -> None:
    workflow = tmp_path / "workflow.yml"
    workflow.write_text(
        "steps:\n  - uses: actions/checkout@v4\n  - uses: ./.github/actions/setup\n",
        encoding="utf-8",
    )
    errors = mod.validate_file(workflow)
    assert len(errors) == 1
    assert "must be pinned to a 40-char commit SHA" in errors[0]


def test_validate_file_accepts_sha_pin(tmp_path: Path) -> None:
    workflow = tmp_path / "workflow.yml"
    workflow.write_text(
        "steps:\n  - uses: actions/checkout@0123456789012345678901234567890123456789\n",
        encoding="utf-8",
    )
    assert mod.validate_file(workflow) == []


def test_main_reports_errors(monkeypatch, tmp_path: Path, capsys) -> None:
    workflow = tmp_path / "workflow.yml"
    workflow.write_text("steps:\n  - uses: actions/checkout@v4\n", encoding="utf-8")
    monkeypatch.setattr(mod, "workflow_files", lambda: [workflow])
    assert mod.main() == 1
    assert "actions/checkout@v4" in capsys.readouterr().err
