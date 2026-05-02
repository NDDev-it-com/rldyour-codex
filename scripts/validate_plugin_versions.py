#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require_semver(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not SEMVER_RE.match(value):
        errors.append(f"{label}: expected SemVer string, got {value!r}")


def main() -> int:
    errors: list[str] = []

    version_path = ROOT / "VERSION"
    if not version_path.is_file():
        errors.append("VERSION: missing marketplace release version")
    else:
        require_semver(version_path.read_text(encoding="utf-8").strip(), "VERSION", errors)

    for required in (
        ROOT / "CHANGELOG.md",
        ROOT / "docs/release-process.md",
        ROOT / "docs/rollback-restore.md",
        ROOT / "docs/observability.md",
        ROOT / "docs/dependency-updates.md",
    ):
        if not required.is_file():
            errors.append(f"{required.relative_to(ROOT)}: missing release/operations document")

    marketplace_path = ROOT / ".agents/plugins/marketplace.json"
    marketplace = load_json(marketplace_path)
    if not isinstance(marketplace, dict):
        errors.append(".agents/plugins/marketplace.json: expected object")
        marketplace = {}

    if marketplace.get("name") != "rldyour-codex":
        errors.append(".agents/plugins/marketplace.json: name must be rldyour-codex")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append(".agents/plugins/marketplace.json: plugins must be a non-empty list")
        plugins = []

    seen_names: set[str] = set()
    for index, entry in enumerate(plugins):
        if not isinstance(entry, dict):
            errors.append(f"marketplace.plugins[{index}]: expected object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"marketplace.plugins[{index}]: missing name")
            continue
        if name in seen_names:
            errors.append(f"marketplace.plugins[{index}]: duplicate plugin {name}")
        seen_names.add(name)

        source = entry.get("source")
        if not isinstance(source, dict):
            errors.append(f"{name}: missing source")
            continue
        rel_path = source.get("path")
        if not isinstance(rel_path, str) or not rel_path.startswith("./plugins/"):
            errors.append(f"{name}: source.path must point to ./plugins/<plugin>")
            continue
        plugin_dir = (ROOT / rel_path).resolve()
        if not plugin_dir.is_dir():
            errors.append(f"{name}: plugin directory missing: {rel_path}")
            continue
        manifest_path = plugin_dir / ".codex-plugin/plugin.json"
        if not manifest_path.is_file():
            errors.append(f"{name}: manifest missing")
            continue

        manifest = load_json(manifest_path)
        if not isinstance(manifest, dict):
            errors.append(f"{manifest_path.relative_to(ROOT)}: expected object")
            continue
        if manifest.get("name") != name:
            errors.append(f"{name}: manifest name mismatch: {manifest.get('name')!r}")
        require_semver(manifest.get("version"), f"{manifest_path.relative_to(ROOT)} version", errors)
        description = manifest.get("description")
        if not isinstance(description, str) or len(description.strip()) < 20:
            errors.append(f"{name}: manifest description must be meaningful")

    for plugin_dir in sorted((ROOT / "plugins").glob("rldyour-*")):
        if plugin_dir.name not in seen_names:
            errors.append(f"{plugin_dir.relative_to(ROOT)}: plugin directory is not listed in marketplace")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").is_file() else ""
    if "## [Unreleased]" not in changelog:
        errors.append("CHANGELOG.md: missing [Unreleased] section")
    if "Semantic Versioning" not in changelog:
        errors.append("CHANGELOG.md: must state Semantic Versioning policy")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"validated marketplace release metadata: {len(seen_names)} plugins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
