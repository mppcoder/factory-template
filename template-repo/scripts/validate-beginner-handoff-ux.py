#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_FRAGMENTS = [
    "один цельный",
    "Язык ответа Codex: русский",
    "manual-ui",
    "уже открытая live session не является надежным",
    "defer-to-final-closeout",
    "deferred_user_actions",
    "placeholder_replacements",
    "owner_boundary",
    "continuation outcome",
]
FORBIDDEN_PATTERNS = [
    re.compile(r"(?i)read .*codex-input\.md.*instead"),
    re.compile(r"(?i)file-based handoff"),
    re.compile(r"(?i)run this shell command first.*then paste"),
    re.compile(r"(?i)already-open .*auto-switch"),
    re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+"),
]


def validate_text(text: str) -> list[str]:
    errors: list[str] = []
    for fragment in REQUIRED_FRAGMENTS:
        if fragment not in text:
            errors.append(f"missing `{fragment}`")
    code_blocks = re.findall(r"```", text)
    if len(code_blocks) > 2:
        errors.append("expected one copy-paste block, found multiple fenced blocks")
    for pattern in FORBIDDEN_PATTERNS:
        match = pattern.search(text)
        if match:
            context = text[max(0, match.start() - 80): match.end() + 80].lower()
            if "не является" in context or "запрещ" in context or "not default" in context:
                continue
            errors.append(f"forbidden pattern `{match.group(0)}`")
    if "следующий пользовательский шаг отсутствует" not in text and "## Инструкция пользователю" not in text:
        errors.append("missing final continuation outcome or user instruction block")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет beginner full handoff UX scorecard.")
    parser.add_argument("path", nargs="?", default="tests/beginner-handoff-ux/positive/handoff.md")
    args = parser.parse_args()
    path = Path(args.path)
    errors = validate_text(path.read_text(encoding="utf-8"))
    if errors:
        print("BEGINNER HANDOFF UX НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("BEGINNER HANDOFF UX ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
