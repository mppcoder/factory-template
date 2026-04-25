#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


HANDOFF_HEADING = "## Handoff в Codex"
UI_HEADING = "## Применение в Codex UI"
STRICT_HEADING = "## Строгий launch mode (опционально)"
FORBIDDEN_PATTERNS = [
    r"см\.\s*файл",
    r"смотри\s+файл",
    r"возьми\s+из\s+файла",
    r"собери\s+handoff",
    r"возьми.*codex-task-pack\.md",
    r"возьми.*codex-input\.md",
    r"возьми.*codex-context\.md",
    r"возьми.*boundary-actions\.md",
    r"собери.*codex-task-pack\.md",
    r"собери.*codex-input\.md",
    r"собери.*codex-context\.md",
    r"собери.*boundary-actions\.md",
    r"^##\s+what changed\s*$",
    r"^##\s+model-routing policy\s*$",
    r"^##\s+validation\s*$",
    r"^##\s+completion package\s*$",
    r"^##\s+known limitations?\s*$",
    r"^##\s+next steps?\s*$",
    r"known limitation:",
    r"manual steps only",
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

    ui_heading_count = len(re.findall(rf"(?m)^{re.escape(UI_HEADING)}\s*$", text))
    if ui_heading_count != 1:
        errors.append(
            f"Ожидается ровно один блок `{UI_HEADING}`, сейчас {ui_heading_count}"
        )

    strict_heading_count = len(re.findall(rf"(?m)^{re.escape(STRICT_HEADING)}\s*$", text))
    if strict_heading_count != 1:
        errors.append(
            f"Ожидается ровно один блок `{STRICT_HEADING}`, сейчас {strict_heading_count}"
        )

    any_handoff_headings = re.findall(r"(?m)^##\s+.*handoff.*$", text, flags=re.IGNORECASE)
    if len(any_handoff_headings) > 1:
        errors.append("Найдено несколько handoff-заголовков; пользователю разрешен только один цельный handoff-блок")

    ui_section = find_section(text, UI_HEADING)
    strict_section = find_section(text, STRICT_HEADING)
    section = find_section(text, HANDOFF_HEADING)
    if ui_section is None:
        errors.append(f"Не найден обязательный заголовок `{UI_HEADING}`")
        ui_text = ""
    else:
        ui_text = text[ui_section[0]:ui_section[1]]
    if strict_section is None:
        errors.append(f"Не найден обязательный заголовок `{STRICT_HEADING}`")
        strict_text = ""
    else:
        strict_text = text[strict_section[0]:strict_section[1]]
    if section is None:
        errors.append(f"Не найден обязательный заголовок `{HANDOFF_HEADING}`")
        handoff_text = ""
    else:
        handoff_text = text[section[0]:section[1]]
        if ui_section is not None and ui_section[0] > section[0]:
            errors.append("Блок `## Применение в Codex UI` должен идти раньше handoff-блока")
        if strict_section is not None and strict_section[0] > section[0]:
            errors.append("Блок `## Строгий launch mode (опционально)` должен идти раньше handoff-блока")

    lowered = text.lower()
    if ui_text:
        if "manual-ui" not in lowered:
            errors.append("UI-блок должен явно фиксировать `manual-ui` как default apply mode")
        if "picker" not in lowered:
            errors.append("UI-блок должен требовать ручной выбор model/reasoning в picker")
        if "новый чат + вставка handoff" not in lowered:
            errors.append("UI-блок должен различать новый чат + вставка handoff и executable launch path")
        if "новый task launch" not in lowered:
            errors.append("Ответ должен явно фиксировать, что надежная единица маршрутизации — новый task launch")
        if "advisory" not in lowered or "не переключает" not in lowered:
            errors.append("Ответ должен явно различать advisory layer и executable switch")
    if strict_text:
        if "```" not in strict_text:
            errors.append("Внутри strict launch-блока ожидается fenced code block с launch command")
        if "launch-codex-task.sh" not in strict_text and "codex --profile" not in strict_text:
            errors.append("Strict launch-блок не содержит явный executable launch command")

    if handoff_text:
        if "```" not in handoff_text:
            errors.append("Внутри handoff-блока ожидается fenced code block для вставки")
        if re.search(r"(?mi)^##\s+Инструкция пользователю\s*$", handoff_text):
            errors.append("`## Инструкция пользователю` не должен попадать внутрь handoff-блока")
        if re.search(r"(?mi)^##\s+", handoff_text.replace(HANDOFF_HEADING, "", 1)):
            errors.append("Внутри handoff-блока найден дополнительный `##`-заголовок; handoff должен быть цельным")

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, lowered, flags=re.IGNORECASE | re.MULTILINE):
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
