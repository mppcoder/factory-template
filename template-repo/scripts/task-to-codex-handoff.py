#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
        raise SystemExit(f"Registry not found: {path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"Registry YAML error: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("Registry root must be mapping")
    return data


def find_task(registry: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = registry.get("tasks", [])
    if not isinstance(tasks, list):
        raise SystemExit("Registry tasks must be list")
    for task in tasks:
        if isinstance(task, dict) and str(task.get("task_id") or "") == task_id:
            return task
    raise SystemExit(f"Task not found: {task_id}")


def list_block(title: str, values: Any, *, empty: str = "- none") -> list[str]:
    lines = [f"{title}:"]
    if isinstance(values, list) and values:
        lines.extend(f"- {item}" for item in values)
    elif isinstance(values, dict) and values:
        lines.extend(f"- {key}: {value}" for key, value in values.items())
    else:
        lines.append(empty)
    return lines


def bool_text(value: Any, default: bool = False) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "true" if default else "false"


def render_handoff(registry: dict[str, Any], task: dict[str, Any]) -> str:
    route = task.get("route", {}) if isinstance(task.get("route"), dict) else {}
    execution = task.get("execution", {}) if isinstance(task.get("execution"), dict) else {}
    dependencies = task.get("dependencies", {}) if isinstance(task.get("dependencies"), dict) else {}
    human = task.get("human_boundary", {}) if isinstance(task.get("human_boundary"), dict) else {}
    outputs = task.get("outputs_required", [])
    artifacts = task.get("artifacts_to_update", [])
    verification = task.get("verification_commands", [])

    selected_scenario = str(route.get("selected_scenario") or MASTER_ROUTER)
    if selected_scenario != MASTER_ROUTER:
        read_instruction = (
            f"Обязательное первое действие: открой и прочитай `{MASTER_ROUTER}`, затем прочитай route target "
            f"`{selected_scenario}`, если router туда отправит."
        )
    else:
        read_instruction = f"Обязательное первое действие: открой и прочитай `{MASTER_ROUTER}`."

    lines: list[str] = [
        "Ты Codex. launch_source=task-registry-handoff.",
        "",
        read_instruction,
        "После чтения выведи короткий route receipt и только потом переходи к реализации.",
        "",
        "Route receipt values:",
        f"selected_project_profile: {route.get('selected_project_profile') or registry.get('description') or 'factory-template task'}",
        f"selected_scenario: {selected_scenario}",
        f"pipeline_stage: {route.get('pipeline_stage') or 'implementation'}",
        "artifacts_to_update:",
    ]
    if isinstance(artifacts, list) and artifacts:
        lines.extend(f"- {item}" for item in artifacts)
    else:
        lines.append("- Заполни из задачи после чтения repo-router.")
    lines.extend(
        [
            f"handoff_allowed: {bool_text(route.get('handoff_allowed'), True)}",
            f"handoff_shape: {route.get('handoff_shape') or 'codex-task-handoff'}",
            "goal_contract:",
            f"  normalized_goal: {task.get('goal') or task.get('next_action') or 'Выполнить задачу из task registry.'}",
            "  definition_of_done:",
            "    - Evidence satisfies the task goal and acceptance criteria.",
            "  evidence_required:",
            "    - Verification report and targeted command output.",
            "  scope:",
            "    - Task registry item scope.",
            "  non_goals:",
            "    - Production/destructive/secrets actions unless explicitly approved.",
            "  proxy_signal_denylist:",
            "    - tests passed alone",
            "    - file exists alone",
            "    - commit exists alone",
            "    - green dashboard alone",
            "    - validator passed alone",
            "goal_runtime_recommendation: goal_first_contract_only",
            "codex_goal_live_validation_required: true",
            f"task_class: {task.get('class') or 'feature'}",
            f"selected_profile: {route.get('selected_profile') or 'deep'}",
            f"selected_reasoning_effort: {route.get('selected_reasoning_effort') or 'high'}",
            f"selected_model: {route.get('selected_model') or 'repo-configured; do not assume live auto-switch'}",
            "",
            "Routing and execution boundary:",
            "- Advisory layer: AGENTS, scenario-pack, runbooks, `.chatgpt` guidance and this handoff text.",
            "- Executable routing layer: named profiles, launcher scripts, Codex picker, Codex CLI, Codex app, Codex cloud or future adapter.",
            "- Не утверждай, что advisory text переключает model/profile/reasoning внутри уже открытой Codex-сессии.",
            "- Manual UI default: открыть новый Codex app или VS Code Codex extension chat, выбрать model/reasoning в picker, затем вставить handoff.",
            "- planned_execution_mode: Codex decides after task graph analysis; do not claim orchestrated-child-sessions unless child/subagent sessions are actually used.",
            "- goal first нормализует цель до route; Codex /goal runtime optional/live-gated и не включается advisory text.",
            "- Не закрывай goal по proxy signals alone; сравни evidence с DoD.",
            "",
            "Task:",
            f"task_id: {task.get('task_id')}",
            f"title: {task.get('title')}",
            f"goal: {task.get('goal') or task.get('next_action') or 'Выполнить задачу из task registry.'}",
            f"source_kind: {(task.get('source') or {}).get('kind') if isinstance(task.get('source'), dict) else ''}",
            f"source_ref: {(task.get('source') or {}).get('ref') if isinstance(task.get('source'), dict) else ''}",
            "",
            "Execution preferences:",
            f"preferred_surface: {execution.get('preferred_surface') or 'codex_app'}",
            f"workspace_mode: {execution.get('workspace_mode') or 'repo_root_or_per_task_worktree'}",
        ]
    )
    lines.extend(list_block("allowed_surfaces", execution.get("allowed_surfaces", [])))
    lines.append("")
    lines.extend(list_block("outputs_required", outputs))
    lines.append("")
    lines.extend(list_block("dependencies.blocked_by", dependencies.get("blocked_by", [])))
    lines.extend(list_block("dependencies.unlocks", dependencies.get("unlocks", [])))
    lines.extend(
        [
            "",
            "Human boundary:",
            f"requires_review: {bool_text(human.get('requires_review'))}",
            f"requires_secret: {bool_text(human.get('requires_secret'))}",
            f"external_user_action: {bool_text(human.get('external_user_action'))}",
            "- Если external_user_action=true, не выполняй это действие за пользователя и вынеси его в final closeout.",
            "- Не добавляй secrets, tokens, passwords, private keys, private repo URLs или raw sensitive logs в публичные issue/PR/docs.",
            "",
            "Verification commands:",
        ]
    )
    if isinstance(verification, list) and verification:
        lines.extend(f"- {cmd}" for cmd in verification)
    else:
        lines.extend(
            [
                f"- {python_script_command('validate-task-registry.py')} {default_registry()}",
                f"- {verify_all_command()}",
            ]
        )
    lines.extend(
        [
            "",
            "Closeout requirements:",
            "- В финальном ответе пиши по-русски.",
            "- Укажи actual_execution_mode и child/subagent count.",
            "- Перечисли, что изменено, какие проверки запускались и их результат.",
            "- Перед финальным closeout обязательно выполни: git status --short --branch",
            "- Если repo dirty, branch ahead, commit/push невозможны или verify blocked, явно назови sync/blocker.",
            "- Не заявляй full Symphony daemon, background worker, Telegram/Slack bot, web app, database, auto-merge или auto-deploy, если они реально не реализованы.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Генерирует единый copy-paste Codex handoff из task-registry.yaml.")
    parser.add_argument("--registry", required=True, help="Путь к task-registry.yaml")
    parser.add_argument("--task-id", required=True, help="Например FT-TASK-0001")
    parser.add_argument("--output", required=True, help="Куда записать generated handoff")
    args = parser.parse_args()

    registry = load_yaml(Path(args.registry))
    task = find_task(registry, args.task_id)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_handoff(registry, task), encoding="utf-8")
    print(f"codex_handoff={output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
