#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git_output(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def plugin_manifests() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for path in sorted((ROOT / "plugins").glob("rldyour-*/.codex-plugin/plugin.json")):
        data = load_json(path)
        assert isinstance(data, dict)
        result.append(
            {
                "name": data.get("name"),
                "version": data.get("version"),
                "path": str(path.parent.parent.relative_to(ROOT)),
                "description": data.get("description"),
            }
        )
    return result


def mcp_servers() -> dict[str, object]:
    data = load_json(ROOT / "plugins/rldyour-mcps/.mcp.json")
    assert isinstance(data, dict)
    return data.get("mcpServers", {})


def main() -> int:
    marketplace = load_json(ROOT / ".agents/plugins/marketplace.json")
    assert isinstance(marketplace, dict)

    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repository": {
            "name": "rldyour-codex",
            "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            "head_sha": git_output("rev-parse", "HEAD"),
            "branch": git_output("branch", "--show-current"),
            "remote": git_output("config", "--get", "remote.origin.url"),
            "dirty": bool(git_output("status", "--porcelain")),
        },
        "environment": {
            "codex_home": os.environ.get("CODEX_HOME", str(Path.home() / ".codex")),
        },
        "marketplace": {
            "name": marketplace.get("name"),
            "display_name": (marketplace.get("interface") or {}).get("displayName"),
            "plugins": [
                {
                    "name": entry.get("name"),
                    "source": entry.get("source"),
                    "category": entry.get("category"),
                    "policy": entry.get("policy"),
                }
                for entry in marketplace.get("plugins", [])
                if isinstance(entry, dict)
            ],
        },
        "plugin_manifests": plugin_manifests(),
        "mcp_runtime_versions": parse_env_file(ROOT / "config/mcp-runtime-versions.env"),
        "mcp_servers": mcp_servers(),
    }
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
