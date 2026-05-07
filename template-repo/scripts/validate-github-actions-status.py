#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")
REQUIRED_PHRASES = [
    "# Статус GitHub Actions",
    "Repository:",
    "Access path:",
    "Workflow:",
    "Self-reference boundary:",
    "## Последний workflow run",
    "status/conclusion:",
    "## Задачи workflow",
    "## Текущий вывод",
    "latest_actions_result:",
]


def validate(text: str) -> list[str]:
    errors: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            errors.append(f"report не содержит `{phrase}`")
    if SECRET_RE.search(text) or "-----BEGIN" in text:
        errors.append("report содержит secret-like content")
    if "Access path: `public" in text:
        errors.append("report не должен использовать public URL fallback как default access path")
    if "status/conclusion: `unknown` / `unknown`" in text and "Blocker:" not in text:
        errors.append("unknown Actions status требует named blocker")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repo-local GitHub Actions latest status report.")
    parser.add_argument("path", nargs="?", default="reports/ci/latest-actions-status.md")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print("GITHUB ACTIONS STATUS REPORT НЕВАЛИДЕН")
        print(f"- report отсутствует: {path}")
        return 1
    errors = validate(path.read_text(encoding="utf-8"))
    if errors:
        print("GITHUB ACTIONS STATUS REPORT НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("GITHUB ACTIONS STATUS REPORT ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
