#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
DEFAULT_CACHE_ROOT = DEFAULT_CODEX_HOME / "plugins" / "cache" / "rldyour-codex"


@dataclass(frozen=True)
class PluginCacheEntry:
    name: str
    version: str
    source_dir: Path
    cache_dir: Path


def _load_manifest(plugin_dir: Path) -> dict[str, object]:
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{plugin_dir}: missing .codex-plugin/plugin.json") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{manifest_path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{manifest_path}: manifest must be a JSON object")
    return data


# Same gating as install_system_codex.sh and doctor_system_codex.sh: cmux is a
# macOS application, so the orchestrator plugin is never cached on other OSes.
MACOS_ONLY_PLUGINS = {"rldyour-orchestrator"}


def discover_entries(
    root: Path = ROOT,
    cache_root: Path = DEFAULT_CACHE_ROOT,
    *,
    include_local: bool = False,
) -> list[PluginCacheEntry]:
    entries: list[PluginCacheEntry] = []
    for plugin_dir in sorted((root / "plugins").glob("rldyour-*")):
        if not plugin_dir.is_dir():
            continue
        if plugin_dir.name in MACOS_ONLY_PLUGINS and sys.platform != "darwin":
            continue
        manifest = _load_manifest(plugin_dir)
        name = manifest.get("name")
        version = manifest.get("version")
        if not isinstance(name, str) or not name:
            raise ValueError(f"{plugin_dir}: manifest missing non-empty name")
        if not isinstance(version, str) or not version:
            raise ValueError(f"{plugin_dir}: manifest missing non-empty version")
        if name != plugin_dir.name:
            raise ValueError(f"{plugin_dir}: manifest name {name!r} must match directory name")
        entries.append(
            PluginCacheEntry(
                name=name,
                version=version,
                source_dir=plugin_dir,
                cache_dir=cache_root / name / version,
            )
        )
        if include_local:
            entries.append(
                PluginCacheEntry(
                    name=name,
                    version=version,
                    source_dir=plugin_dir,
                    cache_dir=cache_root / name / "local",
                )
            )
    if not entries:
        raise ValueError(f"{root / 'plugins'}: no rldyour plugins found")
    return entries


def _diff_in_sync(source_dir: Path, cache_dir: Path) -> bool:
    result = subprocess.run(
        ["diff", "-qr", "-x", "__pycache__", "-x", "*.pyc", str(source_dir), str(cache_dir)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def verify(entries: list[PluginCacheEntry]) -> int:
    failed = False
    for entry in entries:
        label = f"{entry.name}@{entry.version}"
        if entry.cache_dir.name == "local":
            label = f"{entry.name}@local ({entry.version})"
        if not entry.cache_dir.is_dir():
            print(f"missing cache directory: {entry.cache_dir}", file=sys.stderr)
            failed = True
            continue
        if not _diff_in_sync(entry.source_dir, entry.cache_dir):
            print(f"cache differs {label}: {entry.cache_dir}", file=sys.stderr)
            failed = True
            continue
        print(f"cache in sync {label}")
    return 1 if failed else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect or verify rldyour Codex plugin cache paths.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT, help="Codex marketplace cache root.")
    parser.add_argument(
        "--include-local",
        action="store_true",
        help="Also inspect/sync active local cache aliases used by local marketplaces.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="List expected plugin cache entries.")
    list_parser.add_argument("--format", choices=("tsv", "json"), default="tsv")
    subparsers.add_parser("verify", help="Verify source plugin directories match installed cache entries.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        entries = discover_entries(args.root, args.cache_root, include_local=args.include_local)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.command == "list":
        if args.format == "json":
            print(
                json.dumps(
                    [
                        {
                            "name": entry.name,
                            "version": entry.version,
                            "source_dir": str(entry.source_dir),
                            "cache_dir": str(entry.cache_dir),
                        }
                        for entry in entries
                    ],
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            for entry in entries:
                print(f"{entry.name}\t{entry.version}\t{entry.source_dir}\t{entry.cache_dir}")
        return 0

    if args.command == "verify":
        return verify(entries)

    raise AssertionError(f"unhandled command {args.command!r}")


if __name__ == "__main__":
    raise SystemExit(main())
