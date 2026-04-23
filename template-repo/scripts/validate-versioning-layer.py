#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")


def fail(message: str) -> None:
    print(message)
    raise SystemExit(1)


def heading_value(text: str, heading: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == heading and index + 1 < len(lines):
            return lines[index + 1].strip().replace("\r", "")
    return ""


def main() -> int:
    root_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    root = root_arg.parent if root_arg.is_file() else root_arg

    required = [
        root / "README.md",
        root / "VERSION.md",
        root / "CHANGELOG.md",
        root / "CURRENT_FUNCTIONAL_STATE.md",
    ]
    for path in required:
        if not path.is_file():
            fail(f"ОШИБКА: отсутствует {path}")

    origin = root / ".chatgpt" / "project-origin.md"
    version_file = root / "VERSION.md"
    if origin.is_file() and version_file.is_file():
        origin_text = origin.read_text(encoding="utf-8")
        version_text = version_file.read_text(encoding="utf-8")
        factory_origin = heading_value(origin_text, "## Версия фабрики")
        factory_version = heading_value(version_text, "## Версия фабрики-источника")
        if factory_origin and factory_version and factory_origin != factory_version:
            fail("ОШИБКА: версия фабрики в project-origin.md не совпадает с VERSION.md")

    for path in (root / "VERSION.md", root / "CHANGELOG.md", root / "CURRENT_FUNCTIONAL_STATE.md"):
        text = path.read_text(encoding="utf-8")
        if not CYRILLIC_RE.search(text):
            fail(f"ОШИБКА: файл {path} не содержит русскоязычного содержания")

    print("VERSIONING LAYER ПРОЙДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
