#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


FORBIDDEN_ENGLISH_HEADINGS = [
    "goal",
    "hard constraints",
    "required implementation",
    "expected artifacts",
    "verification commands",
    "completion requirements",
    "required artifacts",
    "implementation plan",
    "acceptance criteria",
    "known limitations",
    "next steps",
]

FORBIDDEN_ENGLISH_PHRASES = [
    "do not hardcode",
    "required implementation",
    "expected artifacts to update",
    "verification commands",
    "completion requirements",
    "manual steps only",
    "known limitations",
]


def read_input(argv: list[str]) -> tuple[str, str]:
    if len(argv) > 1 and argv[1] != "-":
        path = Path(argv[1])
        return path.read_text(encoding="utf-8", errors="ignore"), str(path)
    return sys.stdin.read(), "<stdin>"


def main() -> int:
    text, source = read_input(sys.argv)
    lowered = text.lower()
    errors: list[str] = []

    for heading in FORBIDDEN_ENGLISH_HEADINGS:
        pattern = rf"(?m)^\s*(?:#+\s*)?{re.escape(heading)}\s*:?\s*$"
        if re.search(pattern, lowered):
            errors.append(f"англоязычный handoff heading `{heading}`")

    for phrase in FORBIDDEN_ENGLISH_PHRASES:
        if phrase in lowered:
            errors.append(f"англоязычная handoff phrase `{phrase}`")

    for label in ("repo", "goal", "entry point", "scope"):
        if re.search(rf"(?mi)^{re.escape(label)}\s*:", text):
            errors.append(f"англоязычный handoff label `{label}:`")

    if "## handoff в codex" in lowered:
        if "язык ответа codex: русский" not in lowered:
            errors.append("handoff не фиксирует обязательный русский язык ответа Codex")
        if "отвечай пользователю по-русски" not in lowered:
            errors.append("handoff не содержит прямую инструкцию Codex отвечать пользователю по-русски")

    if errors:
        print("ЯЗЫК HANDOFF НЕВАЛИДЕН")
        print(f"Источник: {source}")
        print("- Человекочитаемый handoff для factory-template должен быть на русском языке.")
        print("- Английский допустим только для technical literal values: команды, файлы, YAML keys, model IDs, route fields.")
        for error in errors:
            print("-", error)
        return 1

    print("ЯЗЫК HANDOFF ВАЛИДЕН")
    print(f"Источник: {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
