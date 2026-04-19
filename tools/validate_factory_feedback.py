#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


PLACEHOLDER_PREFIXES = ("<!--", "Подсказка:", "Пример:")


def meaningful_lines(text: str) -> list[str]:
    out: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line in {"-", "*"}:
            continue
        if any(line.startswith(prefix) for prefix in PLACEHOLDER_PREFIXES):
            continue
        out.append(line)
    return out


def extract_section(text: str, section: str) -> str:
    lines = text.splitlines()
    capture = False
    buf: list[str] = []
    for raw in lines:
        line = raw.rstrip("\n")
        if line.strip() == section:
            capture = True
            continue
        if capture and line.strip().startswith("## "):
            break
        if capture:
            buf.append(line)
    return "\n".join(buf).strip()


def validate_file(path: Path, kind: str) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        errors.append(f"Не найден {path.name}")
        return errors
    text = path.read_text(encoding="utf-8", errors="ignore")
    if len(meaningful_lines(text)) < 4:
        errors.append(f"{path.name}: слишком мало содержательных строк")

    if kind == "task":
        sections = [
            "## Основание",
            "## Источник feedback",
            "## Что нужно изменить в фабрике",
            "## Критерии готовности",
        ]
    else:
        sections = [
            "## Где найдено",
            "## Что ожидалось",
            "## Что произошло фактически",
            "## Что нужно исправить в фабрике",
        ]
    for section in sections:
        body = extract_section(text, section)
        if not meaningful_lines(body):
            errors.append(f"{path.name}: пустая или шаблонная секция {section}")

    if kind == "bug":
        if not re.search(r"обход|workaround|временн", text, flags=re.I):
            errors.append(f"{path.name}: не описан временный обход")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Использование: validate_factory_feedback.py <корень-working-project>")
        return 1
    root = Path(sys.argv[1]).resolve()
    feedback = root / "meta-feedback"
    if not feedback.exists():
        print(f"FACTORY FEEDBACK НЕВАЛИДЕН")
        print(f"- Не найден каталог meta-feedback в {root}")
        return 1

    errors: list[str] = []
    errors.extend(validate_file(feedback / "factory-task.md", "task"))
    errors.extend(validate_file(feedback / "factory-bug-report.md", "bug"))
    if errors:
        print("FACTORY FEEDBACK НЕВАЛИДЕН")
        for err in errors:
            print(f"- {err}")
        return 1
    print("FACTORY FEEDBACK ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
