#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", frontmatter, re.M)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def load_skills() -> dict[str, dict[str, str]]:
    skills: dict[str, dict[str, str]] = {}
    for path in sorted((ROOT / "plugins").glob("rldyour-*/skills/*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            continue
        name = frontmatter_value(match.group(1), "name")
        description = frontmatter_value(match.group(1), "description")
        if not name or not description:
            continue
        plugin = path.parts[path.parts.index("plugins") + 1]
        skills[f"{plugin}:{name}"] = {
            "description": description,
            "path": str(path.relative_to(ROOT)),
        }
    return skills


def contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.casefold()
    return any(term.casefold() in lowered for term in terms)


def main() -> int:
    policy_path = ROOT / "config/skill-routing-policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    cases = policy.get("cases", [])
    if not isinstance(cases, list) or not cases:
        print("config/skill-routing-policy.json: cases must be a non-empty list", file=sys.stderr)
        return 1

    skills = load_skills()
    errors: list[str] = []

    for case in cases:
        case_id = str(case.get("id") or "<missing-id>")
        prompt = str(case.get("prompt") or "")
        prompt_terms = case.get("prompt_terms", [])
        if not prompt:
            errors.append(f"{case_id}: prompt is empty")
        if not isinstance(prompt_terms, list) or not prompt_terms:
            errors.append(f"{case_id}: prompt_terms must be a non-empty list")
        elif not contains_any(prompt, [str(term) for term in prompt_terms]):
            errors.append(f"{case_id}: prompt does not contain any configured prompt_terms")

        expected = case.get("expected", [])
        if not isinstance(expected, list) or not expected:
            errors.append(f"{case_id}: expected must be a non-empty list")
            continue

        for expected_entry in expected:
            if not isinstance(expected_entry, dict):
                errors.append(f"{case_id}: expected entries must be objects")
                continue
            skill_name = str(expected_entry.get("skill") or "")
            if skill_name not in skills:
                errors.append(f"{case_id}: expected skill not found: {skill_name}")
                continue
            terms = expected_entry.get("description_terms", [])
            if not isinstance(terms, list) or not terms:
                errors.append(f"{case_id}: {skill_name} must define description_terms")
                continue
            description = skills[skill_name]["description"]
            if not contains_any(description, [str(term) for term in terms]):
                errors.append(
                    f"{case_id}: {skill_name} description does not contain any expected routing term; "
                    f"path={skills[skill_name]['path']}"
                )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"validated skill routing policy cases: {len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
