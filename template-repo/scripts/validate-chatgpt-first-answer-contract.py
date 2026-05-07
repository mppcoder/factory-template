#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_ROUTER_PHRASES = [
    "## Контракт первого ответа ChatGPT",
    "Название чата для копирования",
    "Карточка проекта",
    "Нужно выделить номер через repo chat-handoff-index / allocator.",
    "materialized repo reservation",
    "allocation-not-attempted",
    "first substantive answer",
    "materialized allocation or allocator blocker",
    "Третье состояние запрещено",
    "dry-run, read-only вычисление",
    "номер все равно остается занятым repo reservation",
    "render-project-lifecycle-dashboard.py --format chatgpt-card --stdout",
    "однострочный fenced `text` code block",
    "copy button",
    "repo-local allocator",
    "GitHub connector write path",
    "confirm fetch",
    "blocker нельзя выводить",
    "connector-safe reservation patch",
    "append one item and bump `next_chat_number`",
]
REQUIRED_HANDOFF_PHRASES = [
    "Название чата для копирования",
    "Карточка проекта",
    "materialized allocation or allocator blocker",
    "третье состояние запрещено",
    "allocation attempt/blocker",
    "chatgpt-first-answer-allocation-not-attempted",
    "однострочный fenced `text` code block",
    "copy button",
    "repo-local allocator",
    "GitHub connector write path",
    "confirm fetch",
    "blocker нельзя выводить",
    "connector-safe reservation patch",
    "append one item and bump `next_chat_number`",
]
REQUIRED_DOC_PHRASES = [
    "Название чата для копирования",
    "Карточка проекта",
    "Нужно выделить номер через repo chat-handoff-index / allocator.",
    "materialized/reserved",
    "allocation-not-attempted",
    "first substantive answer",
    "materialized allocation or allocator blocker",
    "третье состояние запрещено",
    "ошибка первого ответа",
    "repo write не подтвержден",
    "номер остается занятым",
    "однострочный fenced `text` code block",
    "copy button",
    "repo-local allocator",
    "GitHub connector write path",
    "confirm fetch",
    "blocker нельзя выводить",
    "connector-safe reservation patch",
    "append one item and bump `next_chat_number`",
]
FORBIDDEN_OVERCLAIMS = [
    "автоматически переименует ChatGPT",
    "просканирует все чаты",
    "propose a stable chat title",
    "Project Instructions могут только предложить",
]
TITLE_HEADER = "## Название чата для копирования"
CARD_HEADER = "## Карточка проекта"
ALLOCATOR_BLOCKER = "Нужно выделить номер через repo chat-handoff-index / allocator."
CHAT_TITLE_RE = re.compile(r"\b[A-Z][A-Z0-9]*-CH-\d{4} [a-z0-9][a-z0-9-]*\b")
TITLE_COPY_BLOCK_RE = re.compile(r"\A\s*```text\n([^\n]+)\n```\s*", re.MULTILINE)
ROUTE_MARKER_RE = re.compile(r"(?im)^\s*(?:#+\s*)?(route receipt|handoff|анализ|начинаю анализ)\b")
CONNECTOR_WRITE_AVAILABLE_MARKERS = [
    "repo_write_path: github_connector_available",
    "GitHub connector write path available",
]
REPO_LOCAL_ALLOCATOR_UNAVAILABLE_MARKERS = [
    "repo_local_allocator: unavailable_in_chatgpt_connector_context",
    "repo-local allocator unavailable in ChatGPT connector context",
]
CONFIRMED_WRITE_BLOCKER_MARKERS = [
    "confirmed_write_blocker:",
    "allocator_blocker_reason:",
    "confirm fetch failed",
    "GitHub connector write rejected",
    "GitHub connector write unavailable",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_visible_first_answer_outcome(text: str) -> list[str]:
    errors: list[str] = []
    title_pos = text.find(TITLE_HEADER)
    card_pos = text.find(CARD_HEADER)

    if title_pos < 0:
        errors.append("нет блока `Название чата для копирования`")
    if card_pos < 0:
        errors.append("нет блока `Карточка проекта`")
    if title_pos >= 0 and card_pos >= 0 and title_pos > card_pos:
        errors.append("блок title расположен после card")

    marker_positions = [match.start() for match in ROUTE_MARKER_RE.finditer(text)]
    first_route_pos = min(marker_positions) if marker_positions else -1
    if first_route_pos >= 0:
        if title_pos < 0 or title_pos > first_route_pos:
            errors.append("route/analysis/handoff начался до title allocation outcome")
        if card_pos < 0 or card_pos > first_route_pos:
            errors.append("route/analysis/handoff начался до project card")

    if title_pos >= 0:
        title_end = card_pos if card_pos > title_pos else len(text)
        title_block = text[title_pos:title_end]
        has_materialized_title = bool(CHAT_TITLE_RE.search(title_block))
        has_allocator_blocker = ALLOCATOR_BLOCKER in title_block
        connector_write_available = any(marker in text for marker in CONNECTOR_WRITE_AVAILABLE_MARKERS)
        repo_local_allocator_unavailable = any(marker in text for marker in REPO_LOCAL_ALLOCATOR_UNAVAILABLE_MARKERS)
        has_confirmed_write_blocker = any(marker in text for marker in CONFIRMED_WRITE_BLOCKER_MARKERS)
        if not has_materialized_title and not has_allocator_blocker:
            errors.append("title block не содержит materialized allocation or allocator blocker")
        if (
            connector_write_available
            and repo_local_allocator_unavailable
            and has_allocator_blocker
            and not has_materialized_title
            and not has_confirmed_write_blocker
        ):
            errors.append(
                "allocator blocker нельзя выводить, когда GitHub connector write path доступен; "
                "нужен materialized FT-CH item или explicit confirmed write blocker reason"
            )
        title_body = title_block[len(TITLE_HEADER) :]
        copy_match = TITLE_COPY_BLOCK_RE.match(title_body)
        if not copy_match:
            errors.append("title block должен начинаться с однострочного fenced `text` code block для one-click copy")
        else:
            copy_value = copy_match.group(1).strip()
            if copy_value != ALLOCATOR_BLOCKER and not CHAT_TITLE_RE.fullmatch(copy_value):
                errors.append("copyable title line должен быть stable title или exact allocator blocker")

    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    errors: list[str] = []

    router = read(root / "template-repo" / "scenario-pack" / "00-master-router.md")
    for phrase in REQUIRED_ROUTER_PHRASES:
        if phrase not in router:
            errors.append(f"00-master-router.md не содержит `{phrase}`")

    handoff = read(root / "template-repo" / "scenario-pack" / "15-handoff-to-codex.md")
    for phrase in REQUIRED_HANDOFF_PHRASES:
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

    negative_fixture = root / "tests" / "chatgpt-first-answer-contract" / "negative" / "allocation-not-attempted.md"
    if not negative_fixture.exists():
        errors.append(f"{negative_fixture.relative_to(root)} отсутствует")
    else:
        fixture_errors = validate_visible_first_answer_outcome(read(negative_fixture))
        if not fixture_errors:
            errors.append(
                f"{negative_fixture.relative_to(root)} должен быть negative fixture для allocation-not-attempted, но прошел проверку"
            )

    not_copyable_fixture = root / "tests" / "chatgpt-first-answer-contract" / "negative" / "title-not-one-click-copyable.md"
    if not not_copyable_fixture.exists():
        errors.append(f"{not_copyable_fixture.relative_to(root)} отсутствует")
    else:
        fixture_errors = validate_visible_first_answer_outcome(read(not_copyable_fixture))
        if not fixture_errors:
            errors.append(
                f"{not_copyable_fixture.relative_to(root)} должен быть negative fixture для title-not-one-click-copyable, но прошел проверку"
            )

    positive_fixtures = [
        root / "tests" / "chatgpt-first-answer-contract" / "positive" / "materialized-title-copyable.md",
        root / "tests" / "chatgpt-first-answer-contract" / "positive" / "allocator-blocker-copyable.md",
        root / "tests" / "chatgpt-first-answer-contract" / "positive" / "connector-write-fallback-materialized.md",
        root / "tests" / "chatgpt-first-answer-contract" / "positive" / "connector-safe-reservation-patch.md",
    ]
    for path in positive_fixtures:
        if not path.exists():
            errors.append(f"{path.relative_to(root)} отсутствует")
            continue
        fixture_errors = validate_visible_first_answer_outcome(read(path))
        if fixture_errors:
            errors.append(f"{path.relative_to(root)} не прошел positive fixture: {'; '.join(fixture_errors)}")

    connector_false_blocker_fixture = (
        root / "tests" / "chatgpt-first-answer-contract" / "negative" / "connector-write-available-silent-blocker.md"
    )
    if not connector_false_blocker_fixture.exists():
        errors.append(f"{connector_false_blocker_fixture.relative_to(root)} отсутствует")
    else:
        fixture_errors = validate_visible_first_answer_outcome(read(connector_false_blocker_fixture))
        if not fixture_errors:
            errors.append(
                f"{connector_false_blocker_fixture.relative_to(root)} должен быть negative fixture для false blocker при доступном GitHub connector write path, но прошел проверку"
            )

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
