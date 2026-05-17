#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

UV_BIN=${UV_BIN:-$(command -v uv 2>/dev/null || true)}
if [ -z "$UV_BIN" ]; then
  printf 'uv command not found\n' >&2
  exit 1
fi
QUICK_VALIDATE=${QUICK_VALIDATE:-"$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py"}
CODEX_HOME_DIR=${CODEX_HOME:-"$HOME/.codex"}
CACHE_ROOT=${CACHE_ROOT:-"$CODEX_HOME_DIR/plugins/cache/rldyour-codex"}

step() {
  printf '\n== %s ==\n' "$1"
}

step "JSON metadata"
jq empty .agents/plugins/marketplace.json config/skill-routing-policy.json plugins/*/.codex-plugin/plugin.json plugins/rldyour-mcps/.mcp.json plugins/rldyour-serena-mcp/hooks.json plugins/rldyour-flow/hooks.json pyrightconfig.json

step "Release metadata"
python3 scripts/validate_plugin_versions.py
python3 scripts/release_manifest.py >/dev/null

step "GitHub Actions pinning"
python3 scripts/validate_action_pins.py

step "Skill frontmatter"
skill_count=0
while IFS= read -r skill_md; do
  skill_dir=$(dirname "$skill_md")
  if [ -f "$QUICK_VALIDATE" ]; then
    "$UV_BIN" run --with pyyaml python "$QUICK_VALIDATE" "$skill_dir" >/dev/null
  else
    python3 - "$skill_md" <<'PY' >/dev/null
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
if not match:
    raise SystemExit(f"{path}: missing YAML frontmatter")
frontmatter = match.group(1)
for field in ("name", "description"):
    if not re.search(rf"^{field}:\s*.+$", frontmatter, re.M):
        raise SystemExit(f"{path}: missing {field}")
if not re.search(r"^#\s+", text, re.M):
    raise SystemExit(f"{path}: missing markdown title")
PY
  fi
  printf 'valid %s\n' "$skill_dir"
  skill_count=$((skill_count + 1))
done < <(find plugins -path '*/skills/*/SKILL.md' -print | sort)
printf 'validated skills: %s\n' "$skill_count"

step "Skill routing descriptions"
python3 - <<'PY'
from pathlib import Path
import re
import sys

MAX_DESCRIPTION_CHARS = 240
errors = []
count = 0
seen_names = {}
seen_descriptions = {}
for path in sorted(Path("plugins").glob("rldyour-*/skills/*/SKILL.md")):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        continue
    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.M)
    desc = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    if not name_match:
        errors.append(f"{path}: missing name")
        continue
    if not desc:
        errors.append(f"{path}: missing description")
        continue
    name = name_match.group(1).strip().strip("\"'")
    description = desc.group(1).strip().strip("\"'")
    count += 1
    if name in seen_names:
        errors.append(f"{path}: duplicate skill name {name} also used by {seen_names[name]}")
    seen_names[name] = path
    if description in seen_descriptions:
        errors.append(f"{path}: duplicate skill description also used by {seen_descriptions[description]}")
    seen_descriptions[description] = path
    if len(description) > MAX_DESCRIPTION_CHARS:
        errors.append(f"{path}: description length {len(description)} exceeds {MAX_DESCRIPTION_CHARS}")
    if not re.search(r"[А-Яа-яЁё]", description):
        errors.append(f"{path}: description must include Russian trigger phrases")
    if not re.search(r"[A-Za-z]", description):
        errors.append(f"{path}: description must include English trigger phrases")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print(f"validated compact bilingual routing descriptions: {count}")
PY

step "Skill routing policy"
python3 scripts/validate_skill_routing.py

step "Instruction docs policy"
python3 scripts/validate_instruction_docs.py

step "OpenAI skill metadata"
"$UV_BIN" run --with pyyaml python - <<'PY'
import json
from pathlib import Path
import re
import sys
import yaml

MAX_DEFAULT_PROMPT_CHARS = 128
MIN_SHORT_DESCRIPTION_CHARS = 25
MAX_SHORT_DESCRIPTION_CHARS = 64
ORCHESTRATED_ONLY = {
    "flow-architecture-review",
    "flow-consistency-review",
    "flow-integration-review",
    "flow-quality-review",
    "flow-security-review",
    "flow-verification-review",
}
KNOWN_MCP_SERVERS = set(
    json.loads(Path("plugins/rldyour-mcps/.mcp.json").read_text(encoding="utf-8"))["mcpServers"]
)


def skill_name_for(path: Path) -> str | None:
    skill_md = path.parent.parent / "SKILL.md"
    if not skill_md.is_file():
        return None
    match = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(encoding="utf-8"), re.S)
    if not match:
        return None
    name = re.search(r"^name:\s*(.+)$", match.group(1), re.M)
    if not name:
        return None
    return name.group(1).strip().strip("\"'")


errors = []
count = 0
for path in sorted(Path("plugins").glob("rldyour-*/skills/*/agents/openai.yaml")):
    count += 1
    skill_name = skill_name_for(path)
    if not skill_name:
        errors.append(f"{path}: cannot resolve sibling SKILL.md name")
        continue
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        errors.append(f"{path}: parse failed: {exc}")
        continue
    interface = data.get("interface") if isinstance(data, dict) else None
    if not isinstance(interface, dict):
        errors.append(f"{path}: missing interface object")
        continue
    short_description = str(interface.get("short_description") or "")
    default_prompt = str(interface.get("default_prompt") or "")
    if not (MIN_SHORT_DESCRIPTION_CHARS <= len(short_description) <= MAX_SHORT_DESCRIPTION_CHARS):
        errors.append(
            f"{path}: interface.short_description length {len(short_description)} must be "
            f"{MIN_SHORT_DESCRIPTION_CHARS}-{MAX_SHORT_DESCRIPTION_CHARS}"
        )
    if len(default_prompt) > MAX_DEFAULT_PROMPT_CHARS:
        errors.append(f"{path}: interface.default_prompt length {len(default_prompt)} exceeds {MAX_DEFAULT_PROMPT_CHARS}")
    if f"${skill_name}" not in default_prompt:
        errors.append(f"{path}: interface.default_prompt must mention ${skill_name}")
    policy = data.get("policy") if isinstance(data, dict) else None
    if not isinstance(policy, dict):
        errors.append(f"{path}: missing policy object")
        continue
    allow_implicit = policy.get("allow_implicit_invocation")
    if skill_name in ORCHESTRATED_ONLY:
        if allow_implicit is not False:
            errors.append(f"{path}: orchestrated reviewer skill must set policy.allow_implicit_invocation=false")
    elif allow_implicit is not True:
        errors.append(f"{path}: policy.allow_implicit_invocation must be true")

    dependencies = data.get("dependencies") if isinstance(data, dict) else None
    tools = dependencies.get("tools", []) if isinstance(dependencies, dict) else []
    if tools is None:
        tools = []
    if not isinstance(tools, list):
        errors.append(f"{path}: dependencies.tools must be a list")
        continue
    for tool in tools:
        if not isinstance(tool, dict):
            errors.append(f"{path}: dependency tool entries must be objects")
            continue
        if tool.get("type") != "mcp":
            errors.append(f"{path}: dependencies.tools only supports type=mcp")
            continue
        value = str(tool.get("value") or "")
        if value not in KNOWN_MCP_SERVERS:
            errors.append(f"{path}: unknown MCP dependency {value!r}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print(f"validated OpenAI metadata files: {count}")
PY

step "System subagent configs"
python3 - "$CODEX_HOME_DIR" <<'PY'
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

CODEX_HOME = Path(sys.argv[1])
SYSTEM_AGENT_DIR = Path("system/agents")
INSTALLED_AGENT_DIR = CODEX_HOME / "agents"
EXPECTED_MODEL = "gpt-5.5"
EXPECTED_REASONING = "medium"
REQUIRED_FIELDS = ("name", "description", "developer_instructions")

errors: list[str] = []
source_files = sorted(SYSTEM_AGENT_DIR.glob("*.toml"))
if not source_files:
    errors.append("system/agents: expected managed subagent TOML files")

for path in source_files:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: TOML parse failed: {exc}")
        continue

    name = data.get("name")
    if name != path.stem:
        errors.append(f"{path}: name must match filename stem")
    for field in REQUIRED_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}: missing non-empty {field}")
    if data.get("model") != EXPECTED_MODEL:
        errors.append(f"{path}: model must be {EXPECTED_MODEL}")
    if data.get("model_reasoning_effort") != EXPECTED_REASONING:
        errors.append(f"{path}: model_reasoning_effort must be {EXPECTED_REASONING}")
    nicknames = data.get("nickname_candidates")
    if nicknames is not None:
        if not isinstance(nicknames, list) or not all(isinstance(item, str) and item for item in nicknames):
            errors.append(f"{path}: nickname_candidates must be a non-empty string list when present")
        elif len(set(nicknames)) != len(nicknames):
            errors.append(f"{path}: nickname_candidates must be unique")

    installed = INSTALLED_AGENT_DIR / path.name
    if INSTALLED_AGENT_DIR.exists():
        if not installed.is_file():
            errors.append(f"{installed}: missing installed managed subagent config")
        elif installed.read_text(encoding="utf-8") != path.read_text(encoding="utf-8"):
            errors.append(f"{installed}: differs from {path}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print(f"validated managed subagent configs: {len(source_files)}")
PY

step "Codex agent tool surfaces"
"$UV_BIN" run --with pyyaml python scripts/validate_agent_tools.py

step "Shell scripts"
shellcheck plugins/rldyour-serena-mcp/hooks/*.sh plugins/rldyour-serena-mcp/scripts/*.sh plugins/rldyour-flow/hooks/*.sh plugins/rldyour-flow/scripts/*.sh plugins/rldyour-lsps/scripts/*.sh scripts/*.sh

step "Python scripts"
python3 - <<'PY'
from pathlib import Path
import ast

paths = [
    Path("plugins/rldyour-serena-mcp/scripts/analyze_sync_scope.py"),
    Path("plugins/rldyour-serena-mcp/scripts/serena_memory_state.py"),
    Path("plugins/rldyour-flow/scripts/flow_post_task_state.py"),
    Path("plugins/rldyour-flow/scripts/instruction_docs_state.py"),
    Path("plugins/rldyour-flow/scripts/fullrepo_sync.py"),
    Path("scripts/smoke_mcp_capabilities.py"),
    Path("scripts/validate_instruction_docs.py"),
    Path("scripts/validate_plugin_versions.py"),
    Path("scripts/validate_skill_routing.py"),
    Path("scripts/release_manifest.py"),
    Path("scripts/release_sbom.py"),
    Path("scripts/check_mcp_runtime_versions.py"),
    Path("scripts/check_serena_memory_freshness.py"),
    Path("scripts/validate_agent_tools.py"),
    Path("scripts/validate_action_pins.py"),
    Path("scripts/scan_text_security.py"),
    Path("scripts/classify_ci_noise.py"),
]

for path in paths:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(f"syntax ok {path}")
PY

step "GitHub Action SHA pins"
python3 scripts/validate_action_pins.py

step "Python unit tests"
"$UV_BIN" run --with pytest --with pytest-cov --with pyyaml python -m pytest

step "Codex hooks migration"
scripts/smoke_codex_hooks_migration.sh

step "LSP health"
if [ "${RLDYOUR_SKIP_LSP_HEALTH:-0}" = "1" ]; then
  printf 'skip    LSP health disabled by RLDYOUR_SKIP_LSP_HEALTH\n'
else
  plugins/rldyour-lsps/scripts/check_lsps.sh
fi

step "Serena memory freshness smoke"
scripts/smoke_serena_memory_freshness.sh

step "Serena memory taxonomy smoke"
scripts/smoke_serena_memory_taxonomy.sh

step "Serena memory state"
if [ "${GITHUB_ACTIONS:-}" = "true" ] \
  && ! git ls-files --error-unmatch ".serena/memories/CORE-01-INDEX.md" >/dev/null 2>&1; then
  printf 'skip    fullrepo-managed Serena memories are not tracked in this GitHub normal-branch checkout\n'
elif [ -f ".serena/memories/CORE-01-INDEX.md" ]; then
  python3 scripts/check_serena_memory_freshness.py
else
  printf 'skip    fullrepo-managed Serena memories absent from this normal-branch checkout\n'
fi

step "Flow post-task state"
plugins/rldyour-flow/scripts/flow_post_task_state.py | python3 -m json.tool >/dev/null

step "MCP registration"
codex mcp list >/dev/null

step "MCP config sync"
python3 - "$CODEX_HOME_DIR" <<'PY'
from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

repo_path = Path("plugins/rldyour-mcps/.mcp.json")
config_path = Path(sys.argv[1]) / "config.toml"

repo_servers = json.loads(repo_path.read_text(encoding="utf-8"))["mcpServers"]
config_servers = tomllib.loads(config_path.read_text(encoding="utf-8")).get("mcp_servers", {})

errors: list[str] = []
repo_names = set(repo_servers)
config_names = set(config_servers)

for name in sorted(repo_names - config_names):
    errors.append(f"missing installed MCP server {name!r}")
for name in sorted(config_names - repo_names):
    errors.append(f"extra installed MCP server {name!r}")


def normalized_command(value: object) -> str | None:
    if value is None:
        return None
    return Path(str(value)).name


for name in sorted(repo_names & config_names):
    repo = repo_servers[name]
    config = config_servers[name]

    repo_command = normalized_command(repo.get("command"))
    config_command = normalized_command(config.get("command"))
    if repo_command != config_command:
        errors.append(
            f"{name}: command mismatch, repo {repo.get('command')!r}, installed {config.get('command')!r}"
        )

    for key in ("url", "args", "env_vars", "startup_timeout_sec", "tool_timeout_sec"):
        if repo.get(key) != config.get(key):
            errors.append(f"{name}: {key} mismatch, repo {repo.get(key)!r}, installed {config.get(key)!r}")

    if (repo.get("env") or {}) != (config.get("env") or {}):
        errors.append(f"{name}: env mismatch")

if errors:
    raise SystemExit("\n".join(errors))

print(f"MCP config in sync: {len(repo_servers)} servers")
PY

step "MCP pinning policy"
python3 - <<'PY'
from __future__ import annotations

import json
import re
from pathlib import Path

servers = json.loads(Path("plugins/rldyour-mcps/.mcp.json").read_text(encoding="utf-8"))["mcpServers"]
errors: list[str] = []


def bun_package_is_pinned(package: str) -> bool:
    if package.endswith("@latest"):
        return False
    if package.startswith("@"):
        _, _, version = package.rpartition("@")
        return bool(re.match(r"^\d", version))
    _, sep, version = package.partition("@")
    return bool(sep and re.match(r"^\d", version))


for name, spec in sorted(servers.items()):
    command = spec.get("command")
    args = [str(arg) for arg in spec.get("args") or []]
    if any("@latest" in arg for arg in args):
        errors.append(f"{name}: @latest is not allowed in MCP runtime args")
    if command == "bunx":
        if not args:
            errors.append(f"{name}: bunx MCP server must declare a package argument")
        elif not bun_package_is_pinned(args[0]):
            errors.append(f"{name}: bunx package is not pinned: {args[0]}")
    if command == "uvx":
        for index, arg in enumerate(args):
            if arg == "--from":
                if index + 1 >= len(args):
                    errors.append(f"{name}: uvx --from missing package spec")
                    continue
                package = args[index + 1]
                if "==" not in package:
                    errors.append(f"{name}: uvx --from package must use an exact version: {package}")

if errors:
    raise SystemExit("\n".join(errors))

print("MCP local runtime package specs are pinned")
PY

step "MCP runtime pin parity"
python3 - <<'PY'
from __future__ import annotations

import json
from pathlib import Path


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def runtime_package_spec(server_name: str) -> str:
    spec = servers.get(server_name)
    if not isinstance(spec, dict):
        return ""
    command = spec.get("command")
    args = [str(arg) for arg in spec.get("args") or []]
    if command == "bunx":
        return args[0] if args else ""
    if command == "uvx":
        for index, arg in enumerate(args):
            if arg == "--from" and index + 1 < len(args):
                return args[index + 1]
    return ""


pins = parse_env(Path("config/mcp-runtime-versions.env"))
servers = json.loads(Path("plugins/rldyour-mcps/.mcp.json").read_text(encoding="utf-8"))["mcpServers"]
checks = (
    ("SERENA_AGENT_VERSION", "serena", "serena-agent", "=="),
    ("SEMGREP_VERSION", "semgrep", "semgrep", "=="),
    ("SEQUENTIAL_THINKING_MCP_VERSION", "sequential-thinking", "@modelcontextprotocol/server-sequential-thinking", "@"),
    ("PLAYWRIGHT_MCP_VERSION", "playwright", "@playwright/mcp", "@"),
    ("CHROME_DEVTOOLS_MCP_VERSION", "chrome-devtools", "chrome-devtools-mcp", "@"),
    ("CONTEXT7_MCP_VERSION", "context7", "@upstash/context7-mcp", "@"),
    ("SHADCN_VERSION", "shadcn", "shadcn", "@"),
)
errors: list[str] = []

if servers.get("dart-flutter", {}).get("command") == "dart":
    if pins.get("DART_FLUTTER_MCP_RUNTIME") != "external-local-dart-sdk":
        errors.append("dart-flutter: local Dart SDK runtime exception must be declared in DART_FLUTTER_MCP_RUNTIME")

for key, server_name, package, separator in checks:
    version = pins.get(key)
    if not version:
        errors.append(f"{key}: missing pin")
        continue
    expected = f"{package}{separator}{version}"
    actual = runtime_package_spec(server_name)
    if actual != expected:
        errors.append(f"{server_name}: expected {expected!r} from {key}, found {actual!r}")

if errors:
    raise SystemExit("\n".join(errors))

print(f"MCP runtime pins match .mcp.json specs: {len(checks)} packages")
PY

step "MCP runtime smoke"
scripts/smoke_mcp_runtime.sh --codex-home "$CODEX_HOME_DIR"

step "MCP capability smoke"
capability_args=(--codex-home "$CODEX_HOME_DIR")
if [ "${RLDYOUR_MCP_CAPABILITY_LIST_ONLY:-0}" = "1" ]; then
  capability_args+=(--list-only)
fi
if [ "${RLDYOUR_MCP_CAPABILITY_ALLOW_MISSING_ENV:-0}" = "1" ]; then
  capability_args+=(--allow-missing-env)
fi
if [ "${RLDYOUR_MCP_CAPABILITY_INCLUDE_AUTH:-0}" = "1" ]; then
  capability_args+=(--include-auth)
fi
if [ -n "${RLDYOUR_MCP_CAPABILITY_SKIP_SERVERS:-}" ]; then
  IFS=',' read -r -a skip_servers <<< "$RLDYOUR_MCP_CAPABILITY_SKIP_SERVERS"
  for server in "${skip_servers[@]}"; do
    [ -n "$server" ] && capability_args+=(--skip-server "$server")
  done
fi
scripts/smoke_mcp_capabilities.sh "${capability_args[@]}"

step "Plugin cache sync"
if [ -d "$CACHE_ROOT" ]; then
  for plugin_dir in plugins/rldyour-*; do
    plugin_name=$(basename "$plugin_dir")
    cache_dir="$CACHE_ROOT/$plugin_name/local"
    if [ ! -d "$cache_dir" ]; then
      printf 'missing cache directory: %s\n' "$cache_dir" >&2
      exit 1
    fi
    diff -qr -x __pycache__ -x '*.pyc' "$plugin_dir" "$cache_dir" >/dev/null
    printf 'cache in sync %s\n' "$plugin_name"
  done
else
  printf 'cache root missing: %s\n' "$CACHE_ROOT" >&2
  exit 1
fi

step "Hook smoke"
scripts/smoke_hooks.sh --codex-home "$CODEX_HOME_DIR"

step "Fullrepo sync smoke"
scripts/smoke_fullrepo_sync.sh

step "Fullrepo bootstrap init smoke"
scripts/smoke_fullrepo_bootstrap_init.sh

step "Local Git guard smoke"
scripts/smoke_local_git_guard.sh

step "Flow branch cleanup smoke"
scripts/smoke_flow_branch_cleanup.sh

step "Text security scan"
python3 scripts/scan_text_security.py

step "Whitespace"
git diff --check

printf '\nMarketplace validation passed.\n'
