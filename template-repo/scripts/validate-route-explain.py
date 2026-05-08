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
    "handoff_shape",
    "handoff_shape_evidence",
    "goal_first",
    "evidence",
    "method",
    "live_catalog_boundary",
    "advisory_boundary",
]


def run_case(root: Path, task_text: str, expected_class: str, expected_shape: str = "codex-task-handoff") -> list[str]:
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
    if payload.get("handoff_shape") != expected_shape:
        errors.append(f"expected handoff_shape `{expected_shape}`, got `{payload.get('handoff_shape')}`")
    method = str(payload.get("method", "")).lower()
    if "semantic classifier" in method and "not a semantic classifier" not in method:
        errors.append("route explain falsely claims semantic classifier")
    if "already-open" not in str(payload.get("advisory_boundary", "")):
        errors.append("advisory boundary must mention already-open live session")
    goal_first = payload.get("goal_first", {})
    if not isinstance(goal_first, dict):
        errors.append("goal_first должен быть mapping")
    else:
        if "does not change selected_profile" not in str(goal_first.get("profile_boundary", "")):
            errors.append("goal_first boundary must say it does not change selected_profile")
        if not goal_first.get("runtime_recommendation"):
            errors.append("goal_first must include runtime_recommendation")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет route-explain layer.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    cases = [
        ("Проведи deep audit одного routing файла, задача цельная", "deep", "codex-task-handoff"),
        ("Реализуй build remediation validator", "build", "codex-task-handoff"),
        ("Запусти review verification pass", "review", "codex-task-handoff"),
        ("Найди docs inventory для quick update", "quick", "codex-task-handoff"),
        (
            "Нужен parent orchestration: child subtasks для audit/deep, implementation/build и validators/tests",
            "review",
            "codex-task-handoff",
        ),
    ]
    errors: list[str] = []
    for text, expected, expected_shape in cases:
        for error in run_case(root, text, expected, expected_shape):
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
