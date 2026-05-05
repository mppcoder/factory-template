#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_ROUTER_PHRASES = [
    "## Контракт первого ответа ChatGPT",
    "Название чата для копирования",
    "Карточка проекта",
    "Нужно выделить номер через repo chat-handoff-index / allocator.",
    "materialized repo reservation",
    "dry-run, read-only вычисление",
    "номер все равно остается занятым repo reservation",
    "render-project-lifecycle-dashboard.py --format chatgpt-card --stdout",
]
REQUIRED_DOC_PHRASES = [
    "Название чата для копирования",
    "Карточка проекта",
    "Нужно выделить номер через repo chat-handoff-index / allocator.",
    "materialized/reserved",
    "repo write не подтвержден",
    "номер остается занятым",
]
FORBIDDEN_OVERCLAIMS = [
    "автоматически переименует ChatGPT",
    "просканирует все чаты",
    "propose a stable chat title",
    "Project Instructions могут только предложить",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    errors: list[str] = []

    router = read(root / "template-repo" / "scenario-pack" / "00-master-router.md")
    for phrase in REQUIRED_ROUTER_PHRASES:
        if phrase not in router:
            errors.append(f"00-master-router.md не содержит `{phrase}`")

    handoff = read(root / "template-repo" / "scenario-pack" / "15-handoff-to-codex.md")
    for phrase in ["Название чата для копирования", "Карточка проекта"]:
        if phrase not in handoff:
            errors.append(f"15-handoff-to-codex.md не содержит `{phrase}`")

    docs = [
        root / "docs" / "operator" / "factory-template" / "01-runbook-dlya-polzovatelya-factory-template.md",
        root / "docs" / "operator" / "factory-template" / "04-chatgpt-project-sources-factory-template-20-cap.md",
        root / "docs" / "operator" / "factory-template" / "06-project-lifecycle-dashboard.md",
    ]
    for path in docs:
        text = read(path)
        for phrase in REQUIRED_DOC_PHRASES:
            if phrase not in text:
                errors.append(f"{path.relative_to(root)} не содержит `{phrase}`")
        for phrase in FORBIDDEN_OVERCLAIMS:
            if phrase in text:
                errors.append(f"{path.relative_to(root)} содержит overclaim `{phrase}`")

    card_path = root / "reports" / "project-status-card.md"
    if not card_path.exists():
        errors.append("reports/project-status-card.md отсутствует")
    else:
        card = read(card_path)
        for phrase in ["🏭", "Модули:", "В работе:"]:
            if phrase not in card:
                errors.append(f"reports/project-status-card.md не содержит `{phrase}`")
        if "\n\n" in card:
            errors.append("reports/project-status-card.md содержит лишние пустые строки")
        long_lines = [line for line in card.splitlines() if len(line) > 82]
        if long_lines:
            errors.append("reports/project-status-card.md содержит слишком длинную строку: " + long_lines[0])

    if errors:
        print("CHATGPT FIRST ANSWER CONTRACT НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CHATGPT FIRST ANSWER CONTRACT ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
