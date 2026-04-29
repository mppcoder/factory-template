#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from orchestrate_codex_handoff_import import load_orchestrator


orchestrator = load_orchestrator()
PLACEHOLDER_MARKERS = ["__PARENT_HANDOFF_ID__", "__CHILD_TASK_ID__", "__ARTIFACT_PATH__", "__CHILD_PROMPT__"]


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def validate_template(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for marker in PLACEHOLDER_MARKERS:
        if marker not in text:
            errors.append(f"template не содержит placeholder `{marker}`")
    if "schema: codex-orchestration/v1" not in text:
        errors.append("template не содержит `schema: codex-orchestration/v1`")
    if "handoff_shape: codex-task-handoff" not in text:
        errors.append("template не содержит `handoff_shape: codex-task-handoff`")
    if "execution_mode: orchestrated-child-sessions" not in text:
        errors.append("template не содержит `execution_mode: orchestrated-child-sessions`")
    if "user_actions_policy: defer-to-final-closeout" not in text:
        errors.append("template не содержит defer-to-final-closeout")
    if "future-user-action" not in text:
        errors.append("template не содержит future-user-action placeholder timing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует parent orchestration plan или template.")
    parser.add_argument("--root", default=".", help="Repo root")
    parser.add_argument("--plan", default="tests/codex-orchestration/fixtures/valid/parent-plan.yaml")
    parser.add_argument("--template", default="template-repo/template/.chatgpt/parent-orchestration-plan.yaml.template")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    plan_path = (root / args.plan).resolve() if not Path(args.plan).is_absolute() else Path(args.plan)
    template_path = (root / args.template).resolve() if not Path(args.template).is_absolute() else Path(args.template)

    errors = validate_template(template_path)
    plan = load_yaml(plan_path)
    plan_errors, warnings = orchestrator.validate_plan(plan, root)
    errors.extend(plan_errors)

    if errors:
        print("PARENT ORCHESTRATION PLAN НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PARENT ORCHESTRATION PLAN ВАЛИДЕН")
    for warning in warnings:
        print(f"- warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
