#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml


REQUIRED_FIELDS = [
    "launch_source",
    "task_class",
    "selected_profile",
    "selected_model",
    "selected_reasoning_effort",
    "project_profile",
    "selected_scenario",
    "pipeline_stage",
    "artifacts_to_update",
    "handoff_allowed",
    "defect_capture_path",
    "launch_command",
]


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    path = root / ".chatgpt" / "task-launch.yaml"
    if not path.exists():
        print("CODEX ROUTING НЕВАЛИДЕН")
        print("- Не найден .chatgpt/task-launch.yaml")
        return 1

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    launch = data.get("launch", {})
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
      if not launch.get(field):
          errors.append(f"Отсутствует обязательное поле launch.{field}")

    if launch.get("launch_source") == "direct-task":
        self_handoff = root / ".chatgpt" / "direct-task-self-handoff.md"
        if not self_handoff.exists():
            errors.append("Для direct-task отсутствует .chatgpt/direct-task-self-handoff.md")
        if not launch.get("direct_self_handoff_completed"):
            errors.append("Для direct-task не отмечен direct_self_handoff_completed")

    normalized = root / ".chatgpt" / "normalized-codex-handoff.md"
    if not normalized.exists():
        errors.append("Отсутствует .chatgpt/normalized-codex-handoff.md")

    command = str(launch.get("launch_command", ""))
    profile = str(launch.get("selected_profile", ""))
    if profile and f"--profile {profile}" not in command:
        errors.append("launch_command не фиксирует selected_profile через --profile")

    if errors:
        print("CODEX ROUTING НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1

    print("CODEX ROUTING ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
