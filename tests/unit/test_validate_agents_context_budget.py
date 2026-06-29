from __future__ import annotations

from pathlib import Path

from tests.support.importing import import_script

mod = import_script("scripts/validate_agents_context_budget.py")


SYSTEM_TEXT = """# System

rldyour-flow
rldyour-serena-mcp
sandbox_mode
default_permissions
"""

PROJECT_TEXT = """# Project

scripts/validate_marketplace.sh
scripts/codex_openai_metadata_policy.py
plugins/rldyour-mcps/.mcp.json
AGPL-3.0-or-later
"""


def write_docs(root: Path, *, system_text: str = SYSTEM_TEXT, project_text: str = PROJECT_TEXT) -> None:
    (root / "system").mkdir()
    (root / "system" / "AGENTS.md").write_text(system_text, encoding="utf-8")
    (root / "AGENTS.md").write_text(project_text, encoding="utf-8")


def test_budget_accepts_compact_instruction_pair(tmp_path: Path) -> None:
    write_docs(tmp_path)

    errors, warnings = mod.validate_budget(tmp_path, require_project_agents=True)

    assert errors == []
    assert warnings == []


def test_budget_rejects_combined_context_bloat(tmp_path: Path) -> None:
    write_docs(tmp_path, project_text=PROJECT_TEXT + ("x" * 100))

    errors, _ = mod.validate_budget(
        tmp_path,
        max_single_bytes=10_000,
        max_combined_bytes=len(SYSTEM_TEXT) + len(PROJECT_TEXT) + 50,
        require_project_agents=True,
    )

    assert any("combined AGENTS context" in error for error in errors)


def test_budget_rejects_missing_required_terms(tmp_path: Path) -> None:
    write_docs(tmp_path, system_text="# System\nplaceholder\n", project_text=PROJECT_TEXT)

    errors, _ = mod.validate_budget(tmp_path, require_project_agents=True)

    assert any("rldyour-flow" in error for error in errors)
    assert any("sandbox_mode" in error for error in errors)
