#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

VERSION_VALUE=$(tr -d '[:space:]' < VERSION)
if ! grep -q "^## \\[$VERSION_VALUE\\]" CHANGELOG.md; then
  printf 'CHANGELOG.md has no release entry for %s\n' "$VERSION_VALUE" >&2
  exit 1
fi

mkdir -p dist/validation
python3 scripts/validate_plugin_versions.py
python3 scripts/validate_contract.py
python3 scripts/release_manifest.py > dist/validation/release-manifest.json
python3 scripts/release_sbom.py > dist/validation/sbom.spdx.json
python3 -m json.tool dist/validation/release-manifest.json >/dev/null
python3 -m json.tool dist/validation/sbom.spdx.json >/dev/null
python3 - <<'PY'
import json
from pathlib import Path

sbom = json.loads(Path("dist/validation/sbom.spdx.json").read_text(encoding="utf-8"))
if sbom.get("spdxVersion") != "SPDX-2.3":
    raise SystemExit("generated SBOM is not SPDX-2.3")
if not sbom.get("packages"):
    raise SystemExit("generated SBOM has no packages")
if not sbom.get("relationships"):
    raise SystemExit("generated SBOM has no relationships")
PY

printf 'Release validation passed for %s.\n' "$VERSION_VALUE"
