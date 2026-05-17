from __future__ import annotations

from tests.support.importing import import_script


mod = import_script("scripts/validate_skill_routing.py")


def test_frontmatter_value_strips_quotes() -> None:
    text = 'name: ry-start\ndescription: "Русский trigger and English trigger"\n'
    assert mod.frontmatter_value(text, "name") == "ry-start"
    assert mod.frontmatter_value(text, "description") == "Русский trigger and English trigger"
    assert mod.frontmatter_value(text, "missing") is None


def test_contains_any_is_case_insensitive() -> None:
    assert mod.contains_any("Проверь BROWSER визуально", ["browser"])
    assert mod.contains_any("Need DEPLOY now", ["deploy"])
    assert not mod.contains_any("plain text", ["security"])


def test_load_skills_finds_current_catalog() -> None:
    skills = mod.load_skills()
    assert "rldyour-flow:ry-start" in skills
    assert "rldyour-browser:browser-validation" in skills
    assert len(skills) == 38


def test_main_validates_current_policy() -> None:
    assert mod.main() == 0
