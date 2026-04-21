#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
import yaml


PLACEHOLDER_TOKEN = "<replace-with-project-folder-id>"
DRIVE_PREFIX = "https://drive.google.com/drive/folders/"


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    path = root / ".chatgpt" / "google-drive-sources.yaml"
    if not path.exists():
        print(f"ОШИБКА: отсутствует {path}")
        return 1

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    block = data.get("google_drive_sources", {})
    if not isinstance(block, dict):
        print("ОШИБКА: google_drive_sources должен быть mapping")
        return 1

    folder_url = str(block.get("folder_url", "")).strip()
    if not folder_url:
        print("ОШИБКА: folder_url пустой")
        return 1
    if not folder_url.startswith(DRIVE_PREFIX):
        print(f"ОШИБКА: folder_url должен начинаться с {DRIVE_PREFIX}")
        return 1
    if PLACEHOLDER_TOKEN in folder_url:
        print("ОШИБКА: folder_url всё ещё содержит placeholder и не подходит для реального Sources contour")
        return 1
    if "<" in folder_url:
        print("ОШИБКА: folder_url содержит незаменённый placeholder")
        return 1

    for key in ["delete_stale", "dry_run", "supports_all_drives"]:
        if key not in block:
            print(f"ОШИБКА: отсутствует ключ {key}")
            return 1

    print(f"Google Drive Sources config валиден: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
