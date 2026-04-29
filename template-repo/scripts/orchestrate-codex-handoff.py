#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

from codex_model_catalog import compare_catalog, configured_profiles, load_live_catalog, load_model_routing
from codex_task_router import load_routing_spec
from factory_automation_common import now_utc


SCHEMA = "codex-orchestration/v1"
TASK_CLASSES = {"quick", "build", "deep", "review"}
REQUIRED_SUBTASK_FIELDS = [
    "id",
    "title",
    "task_class",
    "selected_profile",
    "selected_model",
    "selected_reasoning_effort",
    "selected_plan_mode_reasoning_effort",
    "selected_scenario",
    "prompt",
]
DEFERRED_BOUNDARIES = {"external-user-action", "runtime-action", "downstream-battle-action"}
PLACEHOLDER_RE = re.compile(r"^__[A-Z0-9_]+__$")
PLACEHOLDER_TIMINGS = {"final-user-action", "future-user-action"}
SECRET_PATTERNS = [
    re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"(?i)^[-\w]*\.env(?:\.\w+)?\s*$"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def read_yaml_or_json(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: orchestration plan должен быть mapping")
    return data


def has_secret_like_text(value: Any) -> bool:
    if isinstance(value, dict):
        return any(has_secret_like_text(item) for item in value.values())
    if isinstance(value, list):
        return any(has_secret_like_text(item) for item in value)
    text = str(value)
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-") or "subtask"


def validate_plan(data: dict[str, Any], root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")
    parent = data.get("parent")
    if not isinstance(parent, dict):
        errors.append("parent должен быть mapping")
        parent = {}
    if parent.get("handoff_shape") != "codex-task-handoff":
        errors.append("parent.handoff_shape должен быть `codex-task-handoff`")
    if parent.get("execution_mode") != "orchestrated-child-sessions":
        errors.append("parent.execution_mode должен быть `orchestrated-child-sessions`")
    if parent.get("user_actions_policy") != "defer-to-final-closeout":
        errors.append("parent.user_actions_policy должен быть `defer-to-final-closeout`")
    dumped = yaml.safe_dump(data, allow_unicode=True)
    if "Cloud Director is default" in dumped or "Codex Cloud is default" in dumped:
        errors.append("plan содержит forbidden wording: Cloud Director is default")
    if re.search(r"(?i)already-open (?:live )?session auto-switch", dumped):
        errors.append("plan содержит forbidden wording: already-open session auto-switch")
    blocks = parent.get("copy_paste_handoff_blocks")
    if isinstance(blocks, list) and len(blocks) > 1:
        errors.append("parent handoff должен быть одним цельным block; multi-block handoff запрещен")
    deferred_actions = data.get("deferred_user_actions", [])
    if deferred_actions is not None and not isinstance(deferred_actions, list):
        errors.append("deferred_user_actions должен быть list")
    placeholder_replacements = data.get("placeholder_replacements", [])
    if placeholder_replacements is not None and not isinstance(placeholder_replacements, list):
        errors.append("placeholder_replacements должен быть list")
    if isinstance(placeholder_replacements, list):
        for index, item in enumerate(placeholder_replacements, 1):
            if not isinstance(item, dict):
                errors.append(f"placeholder_replacements[{index}] должен быть mapping")
                continue
            placeholder = str(item.get("placeholder") or "")
            final_value_owner = str(item.get("final_value_owner") or "")
            replacement_timing = str(item.get("replacement_timing") or "")
            if not PLACEHOLDER_RE.match(placeholder):
                errors.append(f"placeholder_replacements[{index}].placeholder должен иметь вид `__PLACEHOLDER_NAME__`")
            if final_value_owner != "operator":
                errors.append(f"placeholder_replacements[{index}].final_value_owner должен быть `operator`")
            if replacement_timing not in PLACEHOLDER_TIMINGS:
                errors.append(
                    f"placeholder_replacements[{index}].replacement_timing должен быть одним из "
                    f"`{', '.join(sorted(PLACEHOLDER_TIMINGS))}`"
                )
    if has_secret_like_text(data):
        errors.append("plan содержит secret-like или .env-like content")
    subtasks = data.get("subtasks")
    if not isinstance(subtasks, list) or not subtasks:
        errors.append("subtasks должен быть непустым list")
        return errors, warnings

    spec = load_routing_spec(root)
    profiles = spec.get("profiles", {}) or {}
    task_routes = spec.get("task_classes", {}) or {}
    model_routing, _model_path = load_model_routing(root)
    model_profiles = configured_profiles(model_routing, spec)
    live_models, _source, live_error = load_live_catalog(None)
    if live_error:
        warnings.append(f"live model catalog unavailable: {live_error}")
    catalog_findings = compare_catalog(model_routing, live_models, spec)
    if catalog_findings.get("missing_configured_models"):
        errors.append("configured model missing from live catalog: " + ", ".join(catalog_findings["missing_configured_models"]))
    if catalog_findings.get("unsupported_reasoning"):
        errors.append("configured reasoning unsupported by live catalog")

    seen_ids: set[str] = set()
    for index, item in enumerate(subtasks, 1):
        if not isinstance(item, dict):
            errors.append(f"subtasks[{index}] должен быть mapping")
            continue
        subtask_id = str(item.get("id") or f"#{index}")
        owner_boundary = str(item.get("owner_boundary") or "internal-repo-follow-up")
        if owner_boundary in DEFERRED_BOUNDARIES:
            errors.append(
                f"subtask `{subtask_id}` имеет boundary `{owner_boundary}`; "
                "действия пользователя/runtime/downstream должны быть перенесены в deferred_user_actions"
            )
        if subtask_id in seen_ids:
            errors.append(f"duplicate subtask id `{subtask_id}`")
        seen_ids.add(subtask_id)
        for field in REQUIRED_SUBTASK_FIELDS:
            if not str(item.get(field) or "").strip():
                errors.append(f"subtask `{subtask_id}` не содержит `{field}`")
        task_class = str(item.get("task_class") or "").strip()
        profile = str(item.get("selected_profile") or "").strip()
        if task_class and task_class not in TASK_CLASSES:
            errors.append(f"subtask `{subtask_id}`: unknown task_class `{task_class}`")
        expected_profile = str((task_routes.get(task_class, {}) or {}).get("profile") or task_class)
        if task_class and profile and expected_profile != profile:
            errors.append(
                f"subtask `{subtask_id}`: selected_profile `{profile}` не совпадает с task_class route `{expected_profile}`"
            )
        if profile and profile not in profiles:
            errors.append(f"subtask `{subtask_id}`: selected_profile `{profile}` отсутствует в codex-routing.yaml")
        expected = model_profiles.get(profile, {})
        if expected:
            checks = [
                ("selected_model", "model"),
                ("selected_reasoning_effort", "reasoning_effort"),
                ("selected_plan_mode_reasoning_effort", "plan_mode_reasoning_effort"),
            ]
            for field, expected_field in checks:
                if str(item.get(field) or "") != str(expected.get(expected_field) or ""):
                    errors.append(
                        f"subtask `{subtask_id}`: `{field}` не совпадает с codex-model-routing.yaml profile `{profile}`"
                    )
        if str(item.get("selected_model") or "").strip() and not live_models:
            warnings.append(f"subtask `{subtask_id}`: selected_model requires live validation")
    return errors, warnings


def render_subtask_handoff(parent: dict[str, Any], subtask: dict[str, Any], validation_note: str) -> str:
    artifacts = subtask.get("artifacts_to_update") or []
    if isinstance(artifacts, list) and artifacts:
        artifact_lines = "\n".join(f"- {item}" for item in artifacts)
    else:
        artifact_lines = "- parent-selected artifacts or subtask-local files"
    return f"""Язык ответа Codex: русский
Отвечай пользователю по-русски. Английский допускается только для технических идентификаторов, имен файлов, команд, YAML/TOML ключей и literal values.

# Child Codex session handoff / дочерний handoff

## Parent задача
- parent_id: {parent.get('id', '')}
- parent_title: {parent.get('title', '')}
- default_context: {parent.get('default_context', 'VPS Remote SSH repo context')}

## Routing / маршрут
- task_class: {subtask.get('task_class', '')}
- selected_profile: {subtask.get('selected_profile', '')}
- selected_model: {subtask.get('selected_model', '')}
- selected_reasoning_effort: {subtask.get('selected_reasoning_effort', '')}
- selected_plan_mode_reasoning_effort: {subtask.get('selected_plan_mode_reasoning_effort', '')}
- selected_scenario: {subtask.get('selected_scenario', '')}
- model_availability: {validation_note}

## Boundary / граница
- owner_boundary: {subtask.get('owner_boundary', 'internal-repo-follow-up')}
- child session не наследует parent route by default.
- Уже открытая live session не считается reliable auto-switch.
- Не хранить secrets, `.env` content или private transcripts в repo artifacts.

## Артефакты для обновления
{artifact_lines}

## Задача
{subtask.get('prompt', '').strip()}

## Completion contract / правило завершения
Вернуть краткий result summary, changed files, verification commands, blockers and owner boundary.
"""


def render_report(
    plan_path: Path,
    report_path: Path,
    data: dict[str, Any],
    rows: list[dict[str, str]],
    errors: list[str],
    warnings: list[str],
    executed: bool,
) -> str:
    parent = data.get("parent", {}) if isinstance(data.get("parent"), dict) else {}
    deferred_actions = data.get("deferred_user_actions", []) if isinstance(data.get("deferred_user_actions", []), list) else []
    placeholder_replacements = (
        data.get("placeholder_replacements", []) if isinstance(data.get("placeholder_replacements", []), list) else []
    )
    status = "failed" if errors else ("executed" if executed else "dry-run")
    lines = [
        "# Отчет parent Codex orchestration",
        "",
        f"Generated UTC: {now_utc()}",
        f"Status: {status}",
        f"Plan: {plan_path.as_posix()}",
        f"Report: {report_path.as_posix()}",
        "Default path: VPS Remote SSH-first",
        "Cloud default: false",
        "",
        "## Parent задача",
        "",
        f"- id: `{parent.get('id', '')}`",
        f"- title: {parent.get('title', '')}",
        f"- launch_source: `{parent.get('launch_source', '')}`",
        f"- selected_scenario: `{parent.get('selected_scenario', '')}`",
        f"- apply_mode: `{parent.get('apply_mode', '')}`",
        f"- strict_launch_mode: `{parent.get('strict_launch_mode', '')}`",
        f"- user_actions_policy: `{parent.get('user_actions_policy', '')}`",
        "",
        "## Subtasks / подзадачи",
        "",
        "| Subtask | Profile | Model | Reasoning | Status | Boundary | Session file | Command |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['id']}` | `{row['profile']}` | `{row['model']}` | `{row['reasoning']}` | "
            f"{row['status']} | `{row['boundary']}` | `{row['session_file']}` | `{row['command']}` |"
        )
    lines.extend(["", "## Warnings / предупреждения", ""])
    lines.extend([f"- {item}" for item in warnings] or ["- none"])
    lines.extend(["", "## Errors / ошибки", ""])
    lines.extend([f"- {item}" for item in errors] or ["- none"])
    lines.extend(["", "## Финальные действия пользователя", ""])
    if deferred_actions:
        for item in deferred_actions:
            if isinstance(item, dict):
                lines.append(
                    f"- `{item.get('id', 'user-action')}`: {item.get('action', '')} "
                    f"(timing: `{item.get('timing', 'final-closeout')}`)"
                )
            else:
                lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.extend(["", "## Напоминания о замене placeholder values", ""])
    if placeholder_replacements:
        for item in placeholder_replacements:
            if isinstance(item, dict):
                lines.append(
                    f"- `{item.get('placeholder', '')}` -> {item.get('description', '')} "
                    f"(owner: `{item.get('final_value_owner', '')}`, timing: `{item.get('replacement_timing', '')}`)"
                )
            else:
                lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Финальный parent closeout contract",
            "",
            "- Collect child result summaries.",
            "- Separate internal repo follow-up, external user action, runtime action and downstream/battle action.",
            "- Move all user-required actions to the final closeout block.",
            "- Use safe temporary placeholders where possible and remind the operator to replace them with real data at the end.",
            "- Do not claim Cloud/App default.",
            "- Do not claim already-open session auto-switch.",
            "- If external action remains, final answer must include compact `## Инструкция пользователю`.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repo-native Codex full handoff orchestrator.")
    parser.add_argument("--root", default=".", help="Repo root")
    parser.add_argument("--plan", required=True, help="YAML/JSON orchestration plan")
    parser.add_argument("--report", help="Markdown parent report path")
    parser.add_argument("--sessions-dir", help="Directory for per-subtask handoff files")
    parser.add_argument("--execute", action="store_true", help="Launch separate Codex CLI subprocesses")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    plan_path = Path(args.plan).resolve()
    data = read_yaml_or_json(plan_path)
    report_path = Path(args.report).resolve() if args.report else root / "reports" / "orchestration" / "parent-orchestration-report.md"
    sessions_dir = Path(args.sessions_dir).resolve() if args.sessions_dir else report_path.parent / "sessions"

    errors, warnings = validate_plan(data, root)
    if errors:
        print("ORCHESTRATION PLAN НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("ORCHESTRATION WARNINGS")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    sessions_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    parent = data.get("parent", {}) if isinstance(data.get("parent"), dict) else {}
    live_note = "repo-configured; requires live validation" if warnings else "repo-configured; last catalog validation passed"
    for subtask in data.get("subtasks", []) or []:
        if not isinstance(subtask, dict):
            continue
        subtask_id = safe_id(str(subtask.get("id") or "subtask"))
        profile = str(subtask.get("selected_profile") or "")
        session_file = sessions_dir / f"{subtask_id}.md"
        session_file.write_text(render_subtask_handoff(parent, subtask, live_note), encoding="utf-8")
        command = f"codex --profile {profile} < {session_file.as_posix()}"
        status = "session-file-written"
        if args.execute and not errors:
            with session_file.open("r", encoding="utf-8") as handle:
                proc = subprocess.run(["codex", "--profile", profile], cwd=root, stdin=handle, check=False)
            status = f"executed-exit-{proc.returncode}"
        rows.append(
            {
                "id": subtask_id,
                "profile": profile,
                "model": str(subtask.get("selected_model") or ""),
                "reasoning": str(subtask.get("selected_reasoning_effort") or ""),
                "boundary": str(subtask.get("owner_boundary") or "internal-repo-follow-up"),
                "session_file": session_file.as_posix(),
                "command": command,
                "status": status,
            }
        )

    report_path.write_text(render_report(plan_path, report_path, data, rows, errors, warnings, args.execute), encoding="utf-8")
    print("ORCHESTRATION EXECUTE" if args.execute else "ORCHESTRATION DRY-RUN")
    for row in rows:
        print(f"- {row['id']}: {row['command']}")
    print(f"report={report_path}")
    print("ORCHESTRATION PLAN ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
