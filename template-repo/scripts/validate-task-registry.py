#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from task_control_paths import default_registry

SCHEMA = "factory-task-registry/v1"
TERMINAL_EVIDENCE_STATUSES = {
    "implemented",
    "verification_pending",
    "human_review",
    "verified",
    "archived",
}


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        raise SystemExit(f"TASK REGISTRY НЕ НАЙДЕН: {path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"TASK REGISTRY YAML НЕ ЧИТАЕТСЯ: {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("TASK REGISTRY НЕВАЛИДЕН: root должен быть YAML mapping")
    return data


def has_evidence_or_reason(task: dict[str, Any]) -> bool:
    evidence = task.get("evidence")
    if isinstance(evidence, list) and evidence:
        return True
    if isinstance(evidence, str) and evidence.strip():
        return True
    return bool(str(task.get("accepted_reason") or task.get("reason") or "").strip())


def task_id_pattern(project_code: str) -> re.Pattern[str]:
    code = re.escape(project_code or "FT")
    return re.compile(rf"^{code}-TASK-\d{{4}}$")


def scenario_exists(registry_path: Path, scenario: str) -> bool:
    scenario_path = Path(scenario)
    candidates = [scenario_path, Path.cwd() / scenario_path]
    if registry_path.is_absolute():
        for parent in registry_path.parents:
            candidates.append(parent / scenario_path)
    else:
        resolved = registry_path.resolve()
        for parent in resolved.parents:
            candidates.append(parent / scenario_path)
    return any(candidate.exists() for candidate in candidates)


def validate_registry(data: dict[str, Any], registry_path: Path) -> list[str]:
    errors: list[str] = []
    schema = data.get("schema")
    if schema != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`, сейчас `{schema}`")

    project_code = str(data.get("project_code") or "FT").strip()
    allowed_classes = data.get("allowed_classes")
    allowed_statuses = data.get("allowed_statuses")
    tasks = data.get("tasks")

    if not project_code:
        errors.append("project_code обязателен")
        project_code = "FT"
    if not isinstance(allowed_classes, list) or not allowed_classes:
        errors.append("allowed_classes должен быть непустым list")
        allowed_classes = []
    if not isinstance(allowed_statuses, list) or not allowed_statuses:
        errors.append("allowed_statuses должен быть непустым list")
        allowed_statuses = []
    if not isinstance(tasks, list):
        errors.append("tasks должен быть list")
        tasks = []

    allowed_class_set = {str(item) for item in allowed_classes}
    allowed_status_set = {str(item) for item in allowed_statuses}
    id_re = task_id_pattern(project_code)
    seen_ids: set[str] = set()
    seen_numbers: list[int] = []

    for index, task in enumerate(tasks, 1):
        path = f"tasks[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{path} должен быть mapping")
            continue

        task_id = str(task.get("task_id") or "")
        match = id_re.fullmatch(task_id)
        if not match:
            errors.append(f"{path}.task_id должен быть формата `{project_code}-TASK-0001`, сейчас `{task_id}`")
        else:
            seen_numbers.append(int(task_id.rsplit("-", 1)[1]))
        if task_id in seen_ids:
            errors.append(f"{path}.task_id повторяется: `{task_id}`")
        seen_ids.add(task_id)

        task_class = str(task.get("class") or "")
        if task_class not in allowed_class_set:
            errors.append(f"{path}.class `{task_class}` не входит в allowed_classes")

        status = str(task.get("status") or "")
        if status not in allowed_status_set:
            errors.append(f"{path}.status `{status}` не входит в allowed_statuses")

        route = task.get("route")
        if not isinstance(route, dict):
            errors.append(f"{path}.route должен быть mapping")
            route = {}
        if str(route.get("handoff_shape") or "") != "codex-task-handoff":
            errors.append(f"{path}.route.handoff_shape должен быть `codex-task-handoff`")
        if status not in {"draft", "needs_triage", "not_applicable", "archived", "superseded"}:
            scenario = str(route.get("selected_scenario") or "")
            if not scenario:
                errors.append(f"{path}.route.selected_scenario обязателен для routable task")
            elif not scenario_exists(registry_path, scenario):
                errors.append(f"{path}.route.selected_scenario указывает на несуществующий файл: `{scenario}`")

        dependencies = task.get("dependencies")
        if not isinstance(dependencies, dict):
            errors.append(f"{path}.dependencies должен быть mapping")
            dependencies = {}
        blocked_by = dependencies.get("blocked_by", [])
        if not isinstance(blocked_by, list):
            errors.append(f"{path}.dependencies.blocked_by должен быть list")
            blocked_by = []
        if status == "blocked":
            next_action = str(task.get("next_action") or task.get("blocker") or "").lower()
            if not blocked_by and "block" not in next_action and "блок" not in next_action:
                errors.append(f"{path} status=blocked требует dependencies.blocked_by или явный blocker/next_action")

        if status in TERMINAL_EVIDENCE_STATUSES and not has_evidence_or_reason(task):
            errors.append(f"{path} status `{status}` требует evidence или accepted_reason")

        human = task.get("human_boundary")
        if not isinstance(human, dict):
            errors.append(f"{path}.human_boundary должен быть mapping")
            human = {}
        if human.get("external_user_action") is True:
            if str(task.get("next_action") or "").strip() == "" and not has_evidence_or_reason(task):
                errors.append(f"{path}.human_boundary.external_user_action=true нельзя оставлять без next_action/evidence")
        for flag in ["requires_review", "requires_secret", "external_user_action"]:
            if flag in human and not isinstance(human.get(flag), bool):
                errors.append(f"{path}.human_boundary.{flag} должен быть boolean")

    next_task_number = data.get("next_task_number")
    max_seen = max(seen_numbers or [0])
    if not isinstance(next_task_number, int) or next_task_number < 1:
        errors.append("next_task_number должен быть positive integer")
    elif next_task_number <= max_seen:
        errors.append(f"next_task_number `{next_task_number}` должен быть больше max task number `{max_seen}`")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует Universal Codex task registry.")
    parser.add_argument("registry_path", nargs="?", default=default_registry(), help="Путь к task-registry.yaml")
    args = parser.parse_args()

    path = Path(args.registry_path)
    data = load_yaml(path)
    errors = validate_registry(data, path)
    if errors:
        print("TASK REGISTRY НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    tasks = data.get("tasks", [])
    print(f"TASK REGISTRY OK: schema={SCHEMA}, tasks={len(tasks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
