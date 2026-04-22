#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
python3 - <<'PY'
from tools.factory_template_phase_detection import detect_phase, load_policy

policy = load_policy()

def assert_phase(name: str, expected: str, changed_paths: list[str], overrides: dict[str, str] | None = None) -> None:
    result = detect_phase(policy, changed_paths, overrides)
    actual = result.get("phase")
    if actual != expected:
        raise SystemExit(
            f"{name}: expected phase {expected}, got {actual}. Result: {result}"
        )
    print(f"{name}: OK -> {actual}")

release_checklist = """# Release Checklist

## Intent Signals

- [x] release pass started
- [x] release note drafted
- [x] go/no-go review in progress

## Before Release Decision

- [x] Проверить `CHANGELOG.md`

## Required Commands

- [x] `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- [x] `bash PRE_RELEASE_AUDIT.sh`

## Go / No-Go

- [x] release bundle можно собирать
"""

bug_report = """# Отчет о дефекте

## Нужен ли feedback в фабрику
Да, потому что дефект reusable.

## Временный обход
- временно запускать validator вручную

## Граница ответственности
shared-unknown

## Статус
зафиксировано, workaround есть
"""

assert_phase(
    "default-controlled-fixes",
    "controlled-fixes",
    [
        "README.md",
        "factory-template-ops-policy.yaml",
    ],
)

assert_phase(
    "release-intent",
    "release",
    [
        "RELEASE_CHECKLIST.md",
        "VERIFY_SUMMARY.md",
        "meta-template-project/RELEASE_NOTES.md",
    ],
    {
        "RELEASE_CHECKLIST.md": release_checklist,
    },
)

assert_phase(
    "bugfix-intent",
    "bugfix-drift",
    [
        "reports/bugs/bug-002-sample.md",
        "template-repo/scripts/validate-quality.py",
    ],
    {
        "reports/bugs/bug-002-sample.md": bug_report,
    },
)

print("PHASE DETECTION TEST ПРОЙДЕН")
PY
