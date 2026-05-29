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
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
CYRILLIC_FIRST_RE = re.compile(r"^\s*[А-Яа-яЁё]")
ASCII_ALPHA_RE = re.compile(r"[A-Za-z]")
ALLOWED_INSTALLATION = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
ALLOWED_AUTHENTICATION = {"ON_USE", "ON_INSTALL"}
EXPECTED_PLUGIN_LICENSE = "AGPL-3.0-or-later"
EXPECTED_REPOSITORY_URL = "https://github.com/NDDev-it-com/rldyour-codex"
EXPECTED_AUTHOR = "Danil Silantyev (github:rldyourmnd), CEO NDDev"
MANIFEST_PATH_FIELDS = {
    "skills": "directory",
    "mcpServers": "file",
    "hooks": "file",
    "apps": "file",
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require_semver(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not SEMVER_RE.match(value):
        errors.append(f"{label}: expected SemVer string, got {value!r}")


def require_non_empty_string(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: expected non-empty string")


def require_string_list(value: object, label: str, errors: list[str], *, min_items: int = 1) -> list[str]:
    if not isinstance(value, list) or len(value) < min_items:
        errors.append(f"{label}: expected at least {min_items} string item(s)")
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{label}[{index}]: expected non-empty string")
            continue
        result.append(item)
    return result


def require_russian_first_bilingual(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not CYRILLIC_FIRST_RE.search(value) or not ASCII_ALPHA_RE.search(value):
        errors.append(f"{label}: must be Russian-first and English-compatible")


def require_manifest_metadata(manifest: dict[str, object], plugin_name: str, manifest_path: Path, errors: list[str]) -> None:
    relative = manifest_path.relative_to(ROOT)
    author = manifest.get("author")
    if not isinstance(author, dict):
        errors.append(f"{plugin_name}: author metadata must be an object")
    else:
        require_non_empty_string(author.get("name"), f"{plugin_name}: author.name", errors)
        if author.get("name") != EXPECTED_AUTHOR:
            errors.append(f"{plugin_name}: author.name must be {EXPECTED_AUTHOR}")
    for key in ("homepage", "repository", "license"):
        require_non_empty_string(manifest.get(key), f"{plugin_name}: {key}", errors)
    if manifest.get("license") != EXPECTED_PLUGIN_LICENSE:
        errors.append(f"{plugin_name}: license must be {EXPECTED_PLUGIN_LICENSE}")
    for key in ("homepage", "repository"):
        if manifest.get(key) != EXPECTED_REPOSITORY_URL:
            errors.append(f"{plugin_name}: {key} must be {EXPECTED_REPOSITORY_URL}")
    require_string_list(manifest.get("keywords"), f"{plugin_name}: keywords", errors)

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{plugin_name}: interface metadata must be an object")
        return
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require_non_empty_string(interface.get(key), f"{plugin_name}: interface.{key}", errors)
    require_russian_first_bilingual(manifest.get("description"), f"{plugin_name}: description", errors)
    require_russian_first_bilingual(
        interface.get("shortDescription"),
        f"{plugin_name}: interface.shortDescription",
        errors,
    )
    require_russian_first_bilingual(
        interface.get("longDescription"),
        f"{plugin_name}: interface.longDescription",
        errors,
    )
    if interface.get("developerName") != EXPECTED_AUTHOR:
        errors.append(f"{plugin_name}: interface.developerName must be {EXPECTED_AUTHOR}")
    for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        value = interface.get(key)
        if value is not None and value != EXPECTED_REPOSITORY_URL:
            errors.append(f"{plugin_name}: interface.{key} must be {EXPECTED_REPOSITORY_URL}")
    require_string_list(interface.get("capabilities"), f"{plugin_name}: interface.capabilities", errors)

    default_prompt = require_string_list(
        interface.get("defaultPrompt"),
        f"{plugin_name}: interface.defaultPrompt",
        errors,
    )
    if len(default_prompt) > 3:
        errors.append(f"{plugin_name}: interface.defaultPrompt must contain at most 3 prompts")
    for index, prompt in enumerate(default_prompt):
        require_russian_first_bilingual(prompt, f"{plugin_name}: interface.defaultPrompt[{index}]", errors)
        if len(prompt) > 128:
            errors.append(f"{plugin_name}: interface.defaultPrompt[{index}] exceeds 128 characters")

    brand_color = interface.get("brandColor")
    if not isinstance(brand_color, str) or not HEX_COLOR_RE.match(brand_color):
        errors.append(f"{plugin_name}: interface.brandColor must be a #RRGGBB color")

    for field, expected_kind in MANIFEST_PATH_FIELDS.items():
        value = manifest.get(field)
        if value is None:
            continue
        if not isinstance(value, str) or not value.startswith("./"):
            errors.append(f"{relative}: {field} must be null or a plugin-relative ./ path")
            continue
        if ".." in Path(value).parts:
            errors.append(f"{relative}: {field} must not contain parent-directory segments")
            continue
        target = (manifest_path.parent.parent / value).resolve()
        try:
            target.relative_to(manifest_path.parent.parent.resolve())
        except ValueError:
            errors.append(f"{relative}: {field} must stay within the plugin directory")
            continue
        if expected_kind == "directory" and not target.is_dir():
            errors.append(f"{relative}: {field} target directory missing: {value}")
        if expected_kind == "file" and not target.is_file():
            errors.append(f"{relative}: {field} target file missing: {value}")


def main() -> int:
    errors: list[str] = []

    product_version = ""
    version_path = ROOT / "VERSION"
    if not version_path.is_file():
        errors.append("VERSION: missing marketplace release version")
    else:
        product_version = version_path.read_text(encoding="utf-8").strip()
        require_semver(product_version, "VERSION", errors)

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
    marketplace_interface = marketplace.get("interface")
    if not isinstance(marketplace_interface, dict):
        errors.append(".agents/plugins/marketplace.json: interface must be an object")
    else:
        require_non_empty_string(
            marketplace_interface.get("displayName"),
            ".agents/plugins/marketplace.json: interface.displayName",
            errors,
        )

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
        if source.get("source") != "local":
            errors.append(f"{name}: source.source must be local")
        rel_path = source.get("path")
        if not isinstance(rel_path, str) or not rel_path.startswith("./plugins/"):
            errors.append(f"{name}: source.path must point to ./plugins/<plugin>")
            continue
        if ".." in Path(rel_path).parts:
            errors.append(f"{name}: source.path must not contain parent-directory segments")
            continue
        plugin_dir = (ROOT / rel_path).resolve()
        try:
            plugin_dir.relative_to((ROOT / "plugins").resolve())
        except ValueError:
            errors.append(f"{name}: source.path must stay inside ./plugins")
            continue
        if not plugin_dir.is_dir():
            errors.append(f"{name}: plugin directory missing: {rel_path}")
            continue
        if plugin_dir.name != name:
            errors.append(f"{name}: source.path basename must match plugin name")

        policy = entry.get("policy")
        if not isinstance(policy, dict):
            errors.append(f"{name}: policy must be an object")
        else:
            if policy.get("installation") not in ALLOWED_INSTALLATION:
                errors.append(f"{name}: policy.installation must be one of {sorted(ALLOWED_INSTALLATION)}")
            if policy.get("authentication") not in ALLOWED_AUTHENTICATION:
                errors.append(f"{name}: policy.authentication must be one of {sorted(ALLOWED_AUTHENTICATION)}")
        require_non_empty_string(entry.get("category"), f"{name}: category", errors)

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
        if product_version and manifest.get("version") != product_version:
            errors.append(
                f"{manifest_path.relative_to(ROOT)} version {manifest.get('version')!r} "
                f"must match VERSION {product_version!r}"
            )
        description = manifest.get("description")
        if not isinstance(description, str) or len(description.strip()) < 20:
            errors.append(f"{name}: manifest description must be meaningful")
        declared_capabilities = {field for field in MANIFEST_PATH_FIELDS if manifest.get(field) is not None}
        if name == "rldyour-mcps":
            if manifest.get("mcpServers") is None:
                errors.append("rldyour-mcps: must declare mcpServers")
            for forbidden in ("skills", "hooks", "apps"):
                if manifest.get(forbidden) is not None:
                    errors.append(f"rldyour-mcps: must not declare {forbidden}; it is transport-only")
        elif name.startswith("rldyour-") and manifest.get("mcpServers") is not None:
            errors.append(f"{name}: only rldyour-mcps may declare mcpServers")
        if name not in {"rldyour-flow", "rldyour-serena-mcp"} and manifest.get("hooks") is not None:
            errors.append(f"{name}: only rldyour-flow and rldyour-serena-mcp may declare hooks")
        if not declared_capabilities:
            errors.append(f"{name}: manifest must declare at least one capability path")
        require_manifest_metadata(manifest, name, manifest_path, errors)

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
