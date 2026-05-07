#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from task_control_paths import default_registry, python_script_command, verify_all_command

MASTER_ROUTER = "template-repo/scenario-pack/00-master-router.md"


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        raise SystemExit(f"TASK REGISTRY НЕ НАЙДЕН: {path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"TASK REGISTRY YAML НЕ ЧИТАЕТСЯ: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("TASK REGISTRY НЕВАЛИДЕН: root должен быть mapping")
    return data


def save_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def current_max_task_number(registry: dict[str, Any], project_code: str) -> int:
    pattern = re.compile(rf"^{re.escape(project_code)}-TASK-(\d{{4}})$")
    numbers: list[int] = []
    tasks = registry.get("tasks", [])
    if isinstance(tasks, list):
        for task in tasks:
            if not isinstance(task, dict):
                continue
            match = pattern.fullmatch(str(task.get("task_id") or ""))
            if match:
                numbers.append(int(match.group(1)))
    return max(numbers or [0])


def next_task_number(registry: dict[str, Any], project_code: str) -> int:
    configured = registry.get("next_task_number")
    max_seen = current_max_task_number(registry, project_code)
    if isinstance(configured, int) and configured > max_seen:
        return configured
    return max_seen + 1


def task_id(project_code: str, number: int) -> str:
    return f"{project_code}-TASK-{number:04d}"


def default_task(args: argparse.Namespace, registry: dict[str, Any], new_task_id: str) -> dict[str, Any]:
    task_class = args.task_class
    allowed_classes = registry.get("allowed_classes", [])
    if isinstance(allowed_classes, list) and task_class not in {str(item) for item in allowed_classes}:
        raise SystemExit(f"task class `{task_class}` не входит в allowed_classes")
    allowed_statuses = registry.get("allowed_statuses", [])
    if isinstance(allowed_statuses, list) and args.status not in {str(item) for item in allowed_statuses}:
        raise SystemExit(f"status `{args.status}` не входит в allowed_statuses")
    return {
        "task_id": new_task_id,
        "title": args.title,
        "goal": args.goal or args.title,
        "class": task_class,
        "priority": args.priority,
        "status": args.status,
        "source": {
            "kind": args.source_kind,
            "ref": args.source_ref,
        },
        "route": {
            "selected_project_profile": args.selected_project_profile,
            "selected_scenario": args.selected_scenario,
            "pipeline_stage": args.pipeline_stage,
            "handoff_allowed": True,
            "handoff_shape": "codex-task-handoff",
            "selected_profile": args.selected_profile,
            "selected_reasoning_effort": args.selected_reasoning_effort,
            "selected_model": args.selected_model,
        },
        "execution": {
            "preferred_surface": args.preferred_surface,
            "allowed_surfaces": [
                "codex_app",
                "vscode_remote_ssh_codex_extension",
                "codex_cli",
                "codex_cloud",
                "symphony_like_runner",
            ],
            "workspace_mode": "repo_root_or_per_task_worktree",
        },
        "dependencies": {
            "blocked_by": [],
            "unlocks": [],
        },
        "artifacts_to_update": [],
        "outputs_required": [
            "codex_handoff",
            "verification_evidence",
            "dashboard_update",
            "closeout_summary",
        ],
        "human_boundary": {
            "requires_review": args.requires_review,
            "requires_secret": False,
            "external_user_action": args.external_user_action,
        },
        "verification_commands": [
            f"{python_script_command('validate-task-registry.py')} {args.registry}",
            verify_all_command(),
        ],
        "evidence": [],
        "next_action": args.next_action,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Выделяет следующий PROJECT_CODE-TASK id. Не использует и не меняет CH/CX counters."
    )
    parser.add_argument("--registry", default=default_registry())
    parser.add_argument("--append-draft", action="store_true", help="Добавить draft task и увеличить next_task_number.")
    parser.add_argument("--title", default="Draft universal Codex task")
    parser.add_argument("--goal", default="")
    parser.add_argument("--task-class", default="feature")
    parser.add_argument("--priority", default="medium")
    parser.add_argument("--status", default="draft")
    parser.add_argument("--source-kind", default="manual")
    parser.add_argument("--source-ref", default="")
    parser.add_argument("--selected-project-profile", default="factory-template self-improvement / automation-orchestration implementation")
    parser.add_argument("--selected-scenario", default=MASTER_ROUTER)
    parser.add_argument("--pipeline-stage", default="implementation")
    parser.add_argument("--selected-profile", default="deep")
    parser.add_argument("--selected-reasoning-effort", default="high")
    parser.add_argument("--selected-model", default="repo-configured; do not assume live auto-switch")
    parser.add_argument("--preferred-surface", default="codex_app")
    parser.add_argument("--requires-review", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--external-user-action", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--next-action", default="Generate Codex handoff when the task is ready.")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    registry = load_yaml(registry_path)
    project_code = str(registry.get("project_code") or "FT")
    number = next_task_number(registry, project_code)
    new_task_id = task_id(project_code, number)

    if args.append_draft:
        tasks = registry.setdefault("tasks", [])
        if not isinstance(tasks, list):
            raise SystemExit("tasks должен быть list")
        tasks.append(default_task(args, registry, new_task_id))
        registry["next_task_number"] = number + 1
        save_yaml(registry_path, registry)
        print(f"allocated_task_id={new_task_id}")
        print(f"registry_updated={registry_path}")
    else:
        print(f"next_task_id={new_task_id}")
        print("dry_run=true")
        print(f"Use --append-draft to reserve this {project_code}-TASK id in the registry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
