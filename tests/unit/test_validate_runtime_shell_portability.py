from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_runtime_validator_never_expands_an_empty_array_under_nounset() -> None:
    script = (ROOT / "scripts/validate_runtime.sh").read_text(encoding="utf-8")
    assert 'runtime_args=(--codex-home "$CODEX_HOME_DIR")' in script
    assert "runtime_args+=(--strict-runtime)" in script
    assert '"${runtime_args[@]}"' in script
    assert "strict_args=()" not in script
