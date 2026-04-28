#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_CASES = [
    "blocked push",
    "remote drift",
    "protected branch",
    "branch ahead",
    "dirty state",
    "fallback instructions",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def validate_report(path: Path) -> list[str]:
    text = read_text(path)
    errors: list[str] = []
    if not text.strip():
        return [f"{path}: report пустой"]
    for case in REQUIRED_CASES:
        if case not in text.lower():
            errors.append(f"{path}: отсутствует fallback coverage case `{case}`")
    if "FACTORY_SYNC_FALLBACK_PUSH_URL" not in text:
        errors.append(f"{path}: не описан env override FACTORY_SYNC_FALLBACK_PUSH_URL")
    if "no secrets" not in text.lower() and "без secrets" not in text.lower():
        errors.append(f"{path}: не зафиксирован no secrets boundary")
    if re.search(r"(?i)(TOKEN|PASSWORD|SECRET|API_KEY)\s*=", text):
        errors.append(f"{path}: найден secret-like assignment")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate verified sync fallback evidence report.")
    parser.add_argument("report", nargs="?", default="reports/release/verified-sync-fallback-evidence.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_report(Path(args.report))
    if errors:
        print("VERIFIED SYNC FALLBACK EVIDENCE НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1
    print("VERIFIED SYNC FALLBACK EVIDENCE ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
