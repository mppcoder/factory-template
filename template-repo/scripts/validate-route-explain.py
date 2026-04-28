#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


REQUIRED_FIELDS = [
    "task_class",
    "selected_profile",
    "selected_model",
    "selected_reasoning_effort",
    "selected_plan_mode_reasoning_effort",
    "evidence",
    "method",
    "live_catalog_boundary",
    "advisory_boundary",
]


def run_case(root: Path, task_text: str, expected_class: str) -> list[str]:
    proc = subprocess.run(
        [
            "python3",
            str(root / "template-repo/scripts/explain-codex-route.py"),
            "--root",
            str(root),
            "--task-text",
            task_text,
            "--json",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return [proc.stderr or proc.stdout or "route explain command failed"]
    payload = json.loads(proc.stdout)
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in payload or payload[field] in ("", [], None):
            errors.append(f"missing `{field}`")
    if payload.get("task_class") != expected_class:
        errors.append(f"expected task_class `{expected_class}`, got `{payload.get('task_class')}`")
    method = str(payload.get("method", "")).lower()
    if "semantic classifier" in method and "not a semantic classifier" not in method:
        errors.append("route explain falsely claims semantic classifier")
    if "already-open" not in str(payload.get("advisory_boundary", "")):
        errors.append("advisory boundary must mention already-open live session")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет route-explain layer.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    cases = [
        ("Проведи deep audit orchestration после Plan №5", "deep"),
        ("Реализуй build remediation validator", "build"),
        ("Запусти review verification pass", "review"),
        ("Найди docs inventory для quick update", "quick"),
    ]
    errors: list[str] = []
    for text, expected in cases:
        for error in run_case(root, text, expected):
            errors.append(f"{expected}: {error}")
    if errors:
        print("ROUTE EXPLAIN НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ROUTE EXPLAIN ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
