#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import yaml


PLACEHOLDER_TOKEN = "<replace-with-project-folder-id>"
DRIVE_PREFIX = "https://drive.google.com/drive/folders/"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate google-drive-sources.yaml config.")
    parser.add_argument("config_path", help="Path to .chatgpt/google-drive-sources.yaml")
    parser.add_argument(
        "--allow-placeholder",
        action="store_true",
        help="Allow placeholder folder URL for template skeleton files.",
    )
    args = parser.parse_args()

    path = Path(args.config_path)
    if not path.exists():
        print(f"ОШИБКА: отсутствует конфиг Google Drive Sources: {path}")
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

    has_placeholder = PLACEHOLDER_TOKEN in folder_url
    if has_placeholder and not args.allow_placeholder:
        print("ОШИБКА: folder_url всё ещё содержит placeholder и не подходит для реального Sources contour")
        return 1
    if not has_placeholder and "<" in folder_url:
        print("ОШИБКА: folder_url содержит незаменённый placeholder")
        return 1

    if "delete_stale" not in block or "dry_run" not in block or "supports_all_drives" not in block:
        print("ОШИБКА: google_drive_sources должен содержать delete_stale, dry_run и supports_all_drives")
        return 1

    print(f"Google Drive Sources config валиден: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
