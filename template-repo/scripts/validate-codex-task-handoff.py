#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_SNIPPETS = {
    "launch_source": "launch_source=task-registry-handoff",
    "master_router": "template-repo/scenario-pack/00-master-router.md",
    "handoff_shape": "handoff_shape: codex-task-handoff",
    "verification": "Verification commands:",
    "closeout": "Closeout requirements:",
    "git_status": "git status --short --branch",
}
ROUTE_FIELDS = [
    "selected_project_profile:",
    "selected_scenario:",
    "pipeline_stage:",
    "artifacts_to_update:",
    "handoff_allowed:",
    "handoff_shape:",
    "task_class:",
    "selected_profile:",
    "selected_reasoning_effort:",
]


def validate_handoff(text: str) -> list[str]:
    errors: list[str] = []
    for name, snippet in REQUIRED_SNIPPETS.items():
        if snippet not in text:
            errors.append(f"missing {name}: `{snippet}`")
    for field in ROUTE_FIELDS:
        if field not in text:
            errors.append(f"missing route field `{field}`")
    if "Advisory layer" not in text or "Executable routing layer" not in text:
        errors.append("missing advisory/executable routing boundary")
    if "actual_execution_mode" not in text:
        errors.append("missing actual_execution_mode closeout requirement")
    if "child/subagent count" not in text:
        errors.append("missing child/subagent count closeout requirement")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует generated Codex task handoff.")
    parser.add_argument("handoff_path", help="Путь к generated handoff markdown")
    args = parser.parse_args()

    path = Path(args.handoff_path)
    if not path.exists():
        print(f"CODEX TASK HANDOFF НЕ НАЙДЕН: {path}")
        return 1
    errors = validate_handoff(path.read_text(encoding="utf-8"))
    if errors:
        print("CODEX TASK HANDOFF НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"CODEX TASK HANDOFF OK: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
