#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PROMPT_SECTIONS = [
    "## Целевой результат",
    "## Критерии успеха",
    "## Ограничения",
    "## Требования к доказательствам",
    "## Форма результата",
    "## Правила остановки",
    "## Динамические поля задачи",
]

CONTRACT_MARKERS = [
    "Базовый prompt contract для GPT-5.5",
    "drop-in replacement",
    "success criteria",
    "evidence requirements",
    "output shape",
    "stop rules",
]

OFFICIAL_SOURCE_MARKERS = [
    "https://developers.openai.com/api/docs/guides/latest-model",
    "https://developers.openai.com/api/docs/guides/prompt-guidance",
    "https://developers.openai.com/api/docs/guides/prompt-optimizer",
    "https://help.openai.com/en/articles/11909943-gpt-53-and-gpt-55-in-chatgpt",
]

FORBIDDEN_PATTERNS = [
    (re.compile(r"think step by step", re.I), "forbidden legacy reasoning phrase"),
    (re.compile(r"\bas an AI\b", re.I), "forbidden generic model-disclaimer phrase"),
    (re.compile(r"^\s*(current date|текущая дата)\s*:", re.I | re.M), "static current-date instruction"),
]

CRITICAL_PROMPT_FILES = [
    ".chatgpt/codex-input.md",
    ".chatgpt/codex-context.md",
    ".chatgpt/codex-task-pack.md",
    ".chatgpt/normalized-codex-handoff.md",
    "template-repo/template/.chatgpt/codex-input.md",
    "template-repo/template/.chatgpt/codex-task-pack.md",
    "template-repo/scripts/create-codex-task-pack.py",
    "template-repo/scripts/codex_task_router.py",
    "template-repo/scenario-pack/15-handoff-to-codex.md",
    "template-repo/scenario-pack/17-direct-task-self-handoff.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def require_contains(errors: list[str], root: Path, rel_path: str, markers: list[str]) -> None:
    path = root / rel_path
    text = read_text(path)
    if not text.strip():
        errors.append(f"{rel_path}: файл отсутствует или пуст")
        return
    for marker in markers:
        if marker not in text:
            errors.append(f"{rel_path}: missing `{marker}`")


def check_forbidden(errors: list[str], root: Path) -> None:
    for rel_path in CRITICAL_PROMPT_FILES:
        path = root / rel_path
        text = read_text(path)
        if not text:
            continue
        for pattern, label in FORBIDDEN_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(f"{rel_path}: {label}: `{match.group(0)}`")


def check_current_handoff(errors: list[str], root: Path) -> None:
    text = read_text(root / ".chatgpt" / "codex-input.md")
    if "CODEX HANDOFF — GPT-5.5 PROMPT MIGRATION FOR FACTORY-TEMPLATE" not in text:
        errors.append(".chatgpt/codex-input.md: stale or wrong handoff title")
    if "DOWNSTREAM MULTI-CYCLE SYNC PROOF" in text:
        errors.append(".chatgpt/codex-input.md: stale downstream sync handoff still present")
    for marker in [
        "launch_source: chatgpt-handoff",
        "selected_profile: deep",
        "selected_model: gpt-5.5",
        "selected_reasoning_effort: high",
        "Язык ответа Codex: русский",
    ]:
        if marker not in text:
            errors.append(f".chatgpt/codex-input.md: missing `{marker}`")


def check_reports(errors: list[str], root: Path) -> None:
    migration_report = root / "reports" / "prompt-migration" / "2026-04-28-gpt-5-5-prompt-migration-report.md"
    inventory_report = root / "reports" / "prompt-migration" / "2026-04-28-gpt-5-5-prompt-inventory.md"
    for path in [migration_report, inventory_report]:
        if not read_text(path).strip():
            errors.append(f"{rel(path, root)}: report missing or empty")
    report_text = read_text(migration_report)
    for marker in OFFICIAL_SOURCE_MARKERS:
        if marker not in report_text:
            errors.append(f"{rel(migration_report, root)}: missing official source `{marker}`")
    for marker in ["source map", "gap map", "remediation", "verification"]:
        if marker not in report_text.lower():
            errors.append(f"{rel(migration_report, root)}: missing report section marker `{marker}`")


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет GPT-5.5 prompt contract для factory-template.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    check_current_handoff(errors, root)
    require_contains(errors, root, "template-repo/template/.chatgpt/codex-input.md", REQUIRED_PROMPT_SECTIONS)
    require_contains(errors, root, "template-repo/template/.chatgpt/codex-task-pack.md", CONTRACT_MARKERS)
    require_contains(errors, root, "template-repo/scripts/create-codex-task-pack.py", CONTRACT_MARKERS)
    require_contains(errors, root, "template-repo/scripts/codex_task_router.py", ["Базовый prompt contract для GPT-5.5", "drop-in replacement"])
    require_contains(errors, root, "template-repo/scenario-pack/15-handoff-to-codex.md", ["handoff receipt", "не является self-handoff"])
    check_forbidden(errors, root)
    check_reports(errors, root)

    if errors:
        print("GPT-5.5 prompt contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GPT-5.5 prompt contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
