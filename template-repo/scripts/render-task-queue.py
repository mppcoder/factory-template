#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from task_control_paths import default_registry, python_script_command

DEFAULT_OUTPUT = "reports/task-queue.md"
TERMINAL_STATUSES = {"verified", "superseded", "not_applicable", "archived"}
STATUS_ORDER = {
    "blocked": 0,
    "ready_for_codex": 1,
    "ready_for_handoff": 2,
    "codex_running": 3,
    "human_review": 4,
    "verification_pending": 5,
    "implemented": 6,
    "needs_triage": 7,
    "draft": 8,
    "verified": 20,
    "superseded": 21,
    "not_applicable": 22,
    "archived": 23,
}


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


def tasks(registry: dict[str, Any]) -> list[dict[str, Any]]:
    items = registry.get("tasks", [])
    if not isinstance(items, list):
        raise SystemExit("registry.tasks должен быть list")
    return [item for item in items if isinstance(item, dict)]


def task_sort_key(task: dict[str, Any]) -> tuple[int, str]:
    status = str(task.get("status") or "")
    return (STATUS_ORDER.get(status, 99), str(task.get("task_id") or ""))


def command(task_id: str, registry_path: Path, kind: str) -> str:
    registry = registry_path.as_posix()
    if kind == "preview":
        return (
            f"{python_script_command('preview-task-handoff.py')} --registry {registry} "
            f"--task-id {task_id} --output reports/handoffs/{task_id}-preview.md"
        )
    if kind == "prepare":
        return f"{python_script_command('prepare-task-pack.py')} --registry {registry} --task-id {task_id} --write"
    if kind == "ready":
        return (
            f"{python_script_command('prepare-task-pack.py')} --registry {registry} --task-id {task_id} "
            "--mark-ready-for-codex --sync-dashboard --write"
        )
    return ""


def evidence_text(task: dict[str, Any]) -> str:
    evidence = task.get("evidence", [])
    if isinstance(evidence, list) and evidence:
        return ", ".join(f"`{item}`" for item in evidence)
    accepted = str(task.get("accepted_reason") or "").strip()
    return accepted or "none"


def human_boundary_text(task: dict[str, Any]) -> str:
    human = task.get("human_boundary", {})
    if not isinstance(human, dict):
        return "unknown"
    flags = []
    if human.get("requires_review") is True:
        flags.append("review")
    if human.get("requires_secret") is True:
        flags.append("secret")
    if human.get("external_user_action") is True:
        flags.append("external")
    return ", ".join(flags) if flags else "none"


def blocked_by_text(task: dict[str, Any]) -> str:
    dependencies = task.get("dependencies", {})
    if not isinstance(dependencies, dict):
        return "unknown"
    blocked_by = dependencies.get("blocked_by", [])
    if isinstance(blocked_by, list) and blocked_by:
        return ", ".join(f"`{item}`" for item in blocked_by)
    return "none"


def counts_by_status(items: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for task in items:
        status = str(task.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def render_queue(registry_path: Path, registry: dict[str, Any]) -> str:
    items = sorted(tasks(registry), key=task_sort_key)
    counts = counts_by_status(items)
    open_count = sum(1 for task in items if str(task.get("status") or "") not in TERMINAL_STATUSES)
    ready_handoff = counts.get("ready_for_handoff", 0)
    ready_codex = counts.get("ready_for_codex", 0)
    running = counts.get("codex_running", 0)
    review = counts.get("human_review", 0)

    lines = [
        "# Очередь Universal Codex задач",
        "",
        "Этот отчет является read-only control plane. Он не запускает Codex, не меняет registry и не переключает model/profile/reasoning.",
        "",
        "## Сводка",
        "",
        f"- registry: `{registry_path.as_posix()}`",
        f"- schema: `{registry.get('schema', '')}`",
        f"- project_code: `{registry.get('project_code', '')}`",
        f"- next_task_number: `{registry.get('next_task_number', '')}`",
        f"- open_tasks: `{open_count}`",
        f"- compact line: Tasks: {ready_handoff} ready-for-handoff -> {ready_codex} ready-for-codex -> {running} running -> {review} human-review",
        "",
        "## Статусы",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in sorted(counts.items(), key=lambda item: STATUS_ORDER.get(item[0], 99)):
        lines.append(f"| `{status}` | {count} |")

    lines.extend(
        [
            "",
            "## Очередь",
            "",
            "| Task | Class | Status | Human boundary | Blocked by | Next action | Evidence |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for task in items:
        task_id = str(task.get("task_id") or "")
        lines.append(
            f"| `{task_id}` {task.get('title', '')} | `{task.get('class', '')}` | `{task.get('status', '')}` | "
            f"{human_boundary_text(task)} | {blocked_by_text(task)} | {task.get('next_action', '')} | {evidence_text(task)} |"
        )

    lines.extend(["", "## Команды подготовки", ""])
    for task in items:
        task_id = str(task.get("task_id") or "")
        status = str(task.get("status") or "")
        if status in TERMINAL_STATUSES:
            lines.extend(
                [
                    f"### `{task_id}`",
                    "",
                    f"- status: `{status}`",
                    "- terminal task: команды подготовки не нужны.",
                    "",
                ]
            )
            continue
        lines.extend(
            [
                f"### `{task_id}`",
                "",
                f"- status: `{status}`",
                "- preview:",
                "",
                "```bash",
                command(task_id, registry_path, "preview"),
                "```",
                "",
                "- prepare pack:",
                "",
                "```bash",
                command(task_id, registry_path, "prepare"),
                "```",
                "",
                "- mark ready for Codex after review:",
                "",
                "```bash",
                command(task_id, registry_path, "ready"),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Рендерит read-only Markdown очередь Universal Codex задач.")
    parser.add_argument("--registry", default=default_registry())
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    rendered = render_queue(registry_path, load_yaml(registry_path))
    if args.stdout:
        print(rendered, end="")
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"task_queue={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
