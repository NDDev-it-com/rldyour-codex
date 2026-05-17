#!/usr/bin/env python3
"""Generate a lightweight SPDX 2.3 SBOM for the rldyour-codex release bundle."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import release_manifest  # noqa: E402


def spdx_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9.-]", "-", value).strip("-")
    return f"SPDXRef-{normalized or 'package'}"


def package(name: str, version: str | None = None, *, supplier: str = "Organization: rldyour") -> dict[str, object]:
    result: dict[str, object] = {
        "name": name,
        "SPDXID": spdx_id(name),
        "downloadLocation": "NOASSERTION",
        "filesAnalyzed": False,
        "licenseConcluded": "NOASSERTION",
        "licenseDeclared": "NOASSERTION",
        "copyrightText": "NOASSERTION",
        "supplier": supplier,
    }
    if version:
        result["versionInfo"] = version
    return result


def runtime_package_name(key: str) -> str:
    return key.removesuffix("_VERSION").lower().replace("_", "-")


def generate_sbom() -> dict[str, object]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    namespace = f"https://github.com/rldyour/rldyour-codex/releases/{version}/sbom-{created}"

    root_package = package("rldyour-codex", version)
    root_spdx_id = str(root_package["SPDXID"])
    packages = [root_package]
    relationships: list[dict[str, str]] = []

    for manifest in release_manifest.plugin_manifests():
        name = str(manifest["name"])
        packages.append(package(name, str(manifest.get("version") or "")))
        relationships.append(
            {
                "spdxElementId": root_spdx_id,
                "relationshipType": "CONTAINS",
                "relatedSpdxElement": spdx_id(name),
            }
        )

    for key, value in sorted(release_manifest.parse_env_file(ROOT / "config/mcp-runtime-versions.env").items()):
        name = runtime_package_name(key)
        packages.append(package(name, value, supplier="NOASSERTION"))
        relationships.append(
            {
                "spdxElementId": root_spdx_id,
                "relationshipType": "DEPENDS_ON",
                "relatedSpdxElement": spdx_id(name),
            }
        )

    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"rldyour-codex-{version}",
        "documentNamespace": namespace,
        "documentDescribes": [root_spdx_id],
        "creationInfo": {
            "created": created,
            "creators": ["Tool: scripts/release_sbom.py"],
        },
        "packages": packages,
        "relationships": relationships,
    }


def main() -> int:
    print(json.dumps(generate_sbom(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
