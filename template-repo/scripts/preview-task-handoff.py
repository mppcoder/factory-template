#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


DEFAULT_REGISTRY = "template-repo/template/.chatgpt/task-registry.yaml"
MASTER_ROUTER = "template-repo/scenario-pack/00-master-router.md"
OPEN_TERMINAL_STATUSES = {"verified", "superseded", "not_applicable", "archived"}
COUNT_STATUSES = [
    "ready_for_handoff",
    "ready_for_codex",
    "codex_running",
    "human_review",
    "blocked",
    "verified",
]


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


def find_task(registry: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = registry.get("tasks", [])
    if not isinstance(tasks, list):
        raise SystemExit("tasks должен быть list")
    for task in tasks:
        if isinstance(task, dict) and str(task.get("task_id") or "") == task_id:
            return task
    raise SystemExit(f"TASK НЕ НАЙДЕН: {task_id}")


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def bullet(items: list[Any], empty: str = "- нет") -> str:
    if not items:
        return empty
    return "\n".join(f"- {item}" for item in items)


def status_counts(registry: dict[str, Any]) -> dict[str, int]:
    tasks = registry.get("tasks", [])
    if not isinstance(tasks, list):
        tasks = []
    counts = {status: 0 for status in COUNT_STATUSES}
    counts["open_tasks"] = 0
    for task in tasks:
        if not isinstance(task, dict):
            continue
        status = str(task.get("status") or "")
        if status not in OPEN_TERMINAL_STATUSES:
            counts["open_tasks"] += 1
        if status in counts:
            counts[status] += 1
    return counts


def value(data: dict[str, Any], *keys: str, default: str = "") -> str:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    return str(current) if current is not None else default


def default_handoff_output(task_id: str) -> str:
    return f"reports/handoffs/{task_id}-codex-handoff.md"


def dashboard_line(counts: dict[str, int]) -> str:
    return (
        f"Tasks: {counts.get('ready_for_handoff', 0)} ready-for-handoff -> "
        f"{counts.get('ready_for_codex', 0)} ready-for-codex -> "
        f"{counts.get('codex_running', 0)} running -> "
        f"{counts.get('human_review', 0)} human-review"
    )


def task_bucket(status: str) -> str:
    if status in COUNT_STATUSES:
        return status
    if status in {"draft", "needs_triage"}:
        return "triage"
    if status in {"implemented", "verification_pending"}:
        return "verification"
    if status in OPEN_TERMINAL_STATUSES:
        return "terminal"
    return "unknown"


def render_preview(registry_path: Path, registry: dict[str, Any], task: dict[str, Any], handoff_output: str) -> str:
    task_id = str(task.get("task_id") or "")
    route = task.get("route", {}) if isinstance(task.get("route"), dict) else {}
    execution = task.get("execution", {}) if isinstance(task.get("execution"), dict) else {}
    dependencies = task.get("dependencies", {}) if isinstance(task.get("dependencies"), dict) else {}
    human = task.get("human_boundary", {}) if isinstance(task.get("human_boundary"), dict) else {}
    counts = status_counts(registry)
    status = str(task.get("status") or "")
    verification_commands = as_list(task.get("verification_commands"))
    if not verification_commands:
        verification_commands = [
            f"python3 template-repo/scripts/validate-task-registry.py {registry_path.as_posix()}",
            f"python3 template-repo/scripts/task-to-codex-handoff.py --registry {registry_path.as_posix()} --task-id {task_id} --output {handoff_output}",
            f"python3 template-repo/scripts/validate-codex-task-handoff.py {handoff_output}",
        ]

    lines = [
        "# Предпросмотр Codex handoff task",
        "",
        "Этот файл является preview. Он не запускает Codex, не переключает model/profile/reasoning и не является execution evidence.",
        "",
        "## Задача",
        "",
        f"- registry: `{registry_path.as_posix()}`",
        f"- task_id: `{task_id}`",
        f"- title: {task.get('title', '')}",
        f"- class/priority/status: `{task.get('class', '')}` / `{task.get('priority', '')}` / `{status}`",
        f"- source: `{value(task, 'source', 'kind')}` `{value(task, 'source', 'ref')}`",
        f"- bucket для dashboard: `{task_bucket(status)}`",
        f"- next_action: {task.get('next_action', '')}",
        "",
        "## Маршрут",
        "",
        f"- selected_project_profile: {route.get('selected_project_profile') or registry.get('description') or ''}",
        f"- selected_scenario: `{route.get('selected_scenario') or MASTER_ROUTER}`",
        f"- pipeline_stage: `{route.get('pipeline_stage') or 'implementation'}`",
        f"- handoff_allowed: `{route.get('handoff_allowed', True)}`",
        f"- handoff_shape: `{route.get('handoff_shape') or 'codex-task-handoff'}`",
        f"- selected_profile: `{route.get('selected_profile') or 'deep'}`",
        f"- selected_reasoning_effort: `{route.get('selected_reasoning_effort') or 'high'}`",
        f"- selected_model: `{route.get('selected_model') or 'repo-configured; do not assume live auto-switch'}`",
        "",
        "## Граница запуска",
        "",
        "- Advisory layer: AGENTS, scenario-pack, runbooks, `.chatgpt` guidance и generated handoff text.",
        "- Executable routing layer: Codex picker, launcher scripts, Codex CLI/app/cloud или future adapter.",
        "- Manual UI default: открыть новый Codex chat, выбрать model/reasoning в picker и вставить generated handoff.",
        "- Already-open live session: non-canonical fallback без обещаний auto-switch.",
        "",
        "## Файл handoff",
        "",
        f"- planned handoff file: `{handoff_output}`",
        "- команда генерации:",
        "",
        "```bash",
        f"python3 template-repo/scripts/task-to-codex-handoff.py --registry {registry_path.as_posix()} --task-id {task_id} --output {handoff_output}",
        "```",
        "",
        "## Предпросмотр dashboard",
        "",
        f"- open_tasks: `{counts.get('open_tasks', 0)}`",
        f"- compact line: {dashboard_line(counts)}",
        f"- текущая задача учитывается как: `{task_bucket(status)}`",
        "",
        "## Зависимости",
        "",
        "blocked_by:",
        bullet(as_list(dependencies.get("blocked_by"))),
        "",
        "unlocks:",
        bullet(as_list(dependencies.get("unlocks"))),
        "",
        "## Человеческая граница",
        "",
        f"- requires_review: `{human.get('requires_review', False)}`",
        f"- requires_secret: `{human.get('requires_secret', False)}`",
        f"- external_user_action: `{human.get('external_user_action', False)}`",
        "",
        "## Артефакты",
        "",
        bullet(as_list(task.get("artifacts_to_update"))),
        "",
        "## Команды проверки",
        "",
        bullet(verification_commands),
        "",
        "## Следующий безопасный шаг",
        "",
        f"1. Проверить preview и task status `{status}`.",
        f"2. Если task готов, сгенерировать handoff в `{handoff_output}`.",
        "3. Передать generated handoff в новый Codex chat или launcher-first path.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Показывает safe preview для Codex task handoff без запуска Codex.")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--handoff-output", default="", help="Планируемый путь generated handoff.")
    parser.add_argument("--output", default="", help="Записать preview markdown в файл. По умолчанию stdout.")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    registry = load_yaml(registry_path)
    task = find_task(registry, args.task_id)
    handoff_output = args.handoff_output or default_handoff_output(args.task_id)
    preview = render_preview(registry_path, registry, task, handoff_output)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(preview, encoding="utf-8")
        print(f"task_handoff_preview={output_path}")
    else:
        print(preview, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
