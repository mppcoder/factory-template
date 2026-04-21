#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


HANDOFF_HEADING = "## Handoff в Codex"
FORBIDDEN_PATTERNS = [
    r"см\.\s*файл",
    r"смотри\s+файл",
    r"возьми\s+из\s+файла",
    r"собери\s+handoff",
    r"codex-task-pack\.md",
    r"codex-input\.md",
    r"codex-context\.md",
    r"boundary-actions\.md",
]


def read_input(argv: list[str]) -> tuple[str, str]:
    if len(argv) > 1 and argv[1] != "-":
        path = Path(argv[1])
        return path.read_text(encoding="utf-8"), str(path)
    return sys.stdin.read(), "<stdin>"


def find_section(text: str, heading: str) -> tuple[int, int] | None:
    pattern = re.compile(rf"(?m)^{re.escape(heading)}\s*$")
    match = pattern.search(text)
    if not match:
        return None
    start = match.start()
    next_heading = re.search(r"(?m)^##\s+", text[match.end():])
    if next_heading:
        end = match.end() + next_heading.start()
    else:
        end = len(text)
    return start, end


def main() -> int:
    text, source = read_input(sys.argv)
    errors: list[str] = []

    handoff_heading_count = len(re.findall(rf"(?m)^{re.escape(HANDOFF_HEADING)}\s*$", text))
    if handoff_heading_count != 1:
        errors.append(
            f"Ожидается ровно один блок `{HANDOFF_HEADING}`, сейчас {handoff_heading_count}"
        )

    any_handoff_headings = re.findall(r"(?m)^##\s+.*handoff.*$", text, flags=re.IGNORECASE)
    if len(any_handoff_headings) > 1:
        errors.append("Найдено несколько handoff-заголовков; пользователю разрешен только один цельный handoff-блок")

    section = find_section(text, HANDOFF_HEADING)
    if section is None:
        errors.append(f"Не найден обязательный заголовок `{HANDOFF_HEADING}`")
        handoff_text = ""
    else:
        handoff_text = text[section[0]:section[1]]

    if handoff_text:
        if "```" not in handoff_text:
            errors.append("Внутри handoff-блока ожидается fenced code block для copy-paste")
        if re.search(r"(?mi)^##\s+Инструкция пользователю\s*$", handoff_text):
            errors.append("`## Инструкция пользователю` не должен попадать внутрь handoff-блока")
        if re.search(r"(?mi)^##\s+", handoff_text.replace(HANDOFF_HEADING, "", 1)):
            errors.append("Внутри handoff-блока найден дополнительный `##`-заголовок; handoff должен быть цельным")

    lowered = text.lower()
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            errors.append(f"Найден запрещенный file-based handoff pattern: `{pattern}`")

    if errors:
        print("HANDOFF RESPONSE FORMAT НЕВАЛИДЕН")
        print(f"Источник: {source}")
        for err in errors:
            print("-", err)
        return 1

    print("HANDOFF RESPONSE FORMAT ВАЛИДЕН")
    print(f"Источник: {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
