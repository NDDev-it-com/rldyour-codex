#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def expected_hooks(repo_root: Path) -> dict[str, str]:
    expected: dict[str, str] = {}
    for hooks_json in sorted(repo_root.glob("plugins/rldyour-*/hooks.json")):
        plugin = hooks_json.parent.name
        data = json.loads(hooks_json.read_text(encoding="utf-8"))
        for event, groups in (data.get("hooks") or {}).items():
            if not isinstance(groups, list):
                continue
            for group_index, group in enumerate(groups):
                if not isinstance(group, dict):
                    continue
                hooks = group.get("hooks")
                if not isinstance(hooks, list):
                    continue
                for hook_index, hook in enumerate(hooks):
                    if not isinstance(hook, dict) or hook.get("type") != "command":
                        continue
                    event_key = re.sub(r"(?<!^)(?=[A-Z])", "_", event).lower()
                    key = f"hooks.json:{event_key}:{group_index}:{hook_index}"
                    expected[f"{plugin}@rldyour-codex:{key}"] = plugin
    return expected


def manifest_version(repo_root: Path, plugin: str) -> str:
    manifest_path = repo_root / "plugins" / plugin / ".codex-plugin/plugin.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = data.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{manifest_path}: missing version")
    return version


def send(stdin, payload: dict[str, Any]) -> None:
    stdin.write(json.dumps(payload) + "\n")
    stdin.flush()


def recv(stdout, stderr, target_id: int) -> dict[str, Any]:
    while True:
        line = stdout.readline()
        if not line:
            err = stderr.read() if stderr is not None else ""
            raise RuntimeError(f"codex app-server exited before response {target_id}: {err}")
        payload = json.loads(line)
        if payload.get("id") == target_id:
            return payload


def checked_response(stdout, stderr, target_id: int) -> dict[str, Any]:
    payload = recv(stdout, stderr, target_id)
    if "error" in payload:
        raise RuntimeError(json.dumps(payload["error"], ensure_ascii=False))
    return payload


def hook_listing(codex_cmd: str, codex_home: Path, repo_root: Path) -> list[dict[str, Any]]:
    proc = subprocess.Popen(
        [codex_cmd, "app-server", "--listen", "stdio://"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env={**os.environ, "CODEX_HOME": str(codex_home)},
    )
    assert proc.stdin is not None
    assert proc.stdout is not None
    assert proc.stderr is not None
    try:
        send(
            proc.stdin,
            {
                "id": 1,
                "method": "initialize",
                "params": {
                    "clientInfo": {
                        "name": "rldyour_codex_hook_listing_smoke",
                        "title": "rldyour Codex hook listing smoke",
                        "version": "0.0.0",
                    },
                    "capabilities": {"experimentalApi": True},
                },
            },
        )
        checked_response(proc.stdout, proc.stderr, 1)
        send(proc.stdin, {"id": 2, "method": "hooks/list", "params": {"cwds": [str(repo_root)]}})
        response = checked_response(proc.stdout, proc.stderr, 2)
        data = response.get("result", {}).get("data", [])
        if not isinstance(data, list) or not data:
            return []
        hooks = data[0].get("hooks", [])
        return [hook for hook in hooks if isinstance(hook, dict)]
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke Codex app-server hooks/list for installed rldyour plugin hooks.")
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--codex", default=os.environ.get("CODEX_BIN", "codex"))
    args = parser.parse_args()

    expected = expected_hooks(args.repo_root)
    hooks = hook_listing(args.codex, args.codex_home, args.repo_root)
    rldyour_hooks = [
        hook
        for hook in hooks
        if isinstance(hook.get("pluginId"), str)
        and hook["pluginId"].startswith("rldyour-")
        and hook["pluginId"].endswith("@rldyour-codex")
    ]

    errors: list[str] = []
    by_key = {str(hook.get("key")): hook for hook in rldyour_hooks}
    for expected_key, plugin in sorted(expected.items()):
        hook = by_key.get(expected_key)
        if hook is None:
            errors.append(f"missing hook in codex hooks/list: {expected_key}")
            continue
        if hook.get("trustStatus") != "trusted":
            errors.append(f"{expected_key}: trustStatus={hook.get('trustStatus')!r}")
        if hook.get("enabled") is not True:
            errors.append(f"{expected_key}: enabled={hook.get('enabled')!r}")
        if not isinstance(hook.get("currentHash"), str) or not hook.get("currentHash"):
            errors.append(f"{expected_key}: missing currentHash")
        source_path = str(hook.get("sourcePath") or "")
        version = manifest_version(args.repo_root, plugin)
        expected_source = f"/plugins/cache/rldyour-codex/{plugin}/{version}/hooks.json"
        if expected_source not in source_path:
            errors.append(f"{expected_key}: sourcePath must include {expected_source}, got {source_path!r}")

    unexpected = sorted(set(by_key) - set(expected))
    if unexpected:
        errors.append(f"unexpected rldyour hooks in codex hooks/list: {unexpected}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"validated Codex hooks/list: {len(rldyour_hooks)} trusted enabled rldyour hooks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
