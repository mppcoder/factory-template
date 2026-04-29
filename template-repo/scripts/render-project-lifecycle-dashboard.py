#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

import yaml

from factory_automation_common import now_utc, read_text, read_yaml


def detect_repo_root() -> Path:
    script = Path(__file__).resolve()
    for parent in script.parents:
        if (parent / "template-repo" / "scripts").exists() and (parent / "README.md").exists():
            return parent
        if (parent / "scripts").exists() and (parent / ".chatgpt").exists():
            return parent
    return Path.cwd().resolve()


def default_dashboard_path(root: Path) -> Path:
    source_path = root / "template-repo" / "template" / ".chatgpt" / "project-lifecycle-dashboard.yaml"
    if source_path.exists():
        return source_path
    return root / ".chatgpt" / "project-lifecycle-dashboard.yaml"


def load_validator():
    script = Path(__file__).resolve()
    path = script.with_name("validate-project-lifecycle-dashboard.py")
    spec = importlib.util.spec_from_file_location("validate_project_lifecycle_dashboard", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Не удалось загрузить validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def value(data: dict[str, Any], *keys: str, default: str = "") -> str:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    if current is None:
        return default
    return str(current)


def list_value(data: dict[str, Any], *keys: str) -> list[Any]:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return []
        current = current.get(key)
    return current if isinstance(current, list) else []


def bullet(items: list[Any], empty: str = "- нет") -> str:
    lines: list[str] = []
    for item in items:
        if isinstance(item, dict):
            item_id = item.get("id") or item.get("title") or item.get("path") or "item"
            status = f" `{item.get('status')}`" if item.get("status") else ""
            boundary = f" (`{item.get('owner_boundary')}`)" if item.get("owner_boundary") else ""
            text = item.get("action") or item.get("title") or item.get("summary") or item.get("reason") or item.get("path") or ""
            lines.append(f"- `{item_id}`{status}: {text}{boundary}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines) if lines else empty


def evidence_text(item: dict[str, Any]) -> str:
    evidence = item.get("evidence")
    if isinstance(evidence, list) and evidence:
        return ", ".join(f"`{entry}`" for entry in evidence)
    if isinstance(evidence, str) and evidence.strip():
        return f"`{evidence}`"
    reason = item.get("accepted_reason") or item.get("reason")
    if reason:
        return str(reason)
    return ""


def optional_context(root: Path, dashboard_path: Path) -> dict[str, Any]:
    chatgpt_dir = dashboard_path.parent
    task_state = read_yaml(chatgpt_dir / "task-state.yaml")
    stage_state = read_yaml(chatgpt_dir / "stage-state.yaml")
    task_index = read_yaml(chatgpt_dir / "task-index.yaml")
    cockpit = read_yaml(chatgpt_dir / "orchestration-cockpit.yaml")
    verify_summary = read_text(root / "VERIFY_SUMMARY.md")
    current_state = read_text(root / "CURRENT_FUNCTIONAL_STATE.md")
    runtime_reports = {
        "dry_run": read_text(root / ".factory-runtime" / "reports" / "deploy-dry-run-latest.txt"),
        "deploy": read_text(root / ".factory-runtime" / "reports" / "deploy-last-run.txt"),
    }
    return {
        "task_state": task_state,
        "stage_state": stage_state,
        "task_index": task_index,
        "cockpit": cockpit,
        "verify_summary": verify_summary,
        "current_state_present": bool(current_state.strip()),
        "runtime_reports": runtime_reports,
    }


def resolved_project(data: dict[str, Any], context: dict[str, Any]) -> dict[str, str]:
    stage_project = context.get("stage_state", {}).get("project", {}) if isinstance(context.get("stage_state"), dict) else {}
    stage_lifecycle = context.get("stage_state", {}).get("lifecycle", {}) if isinstance(context.get("stage_state"), dict) else {}
    return {
        "name": value(data, "project", "name") or str(stage_project.get("name") or ""),
        "slug": value(data, "project", "slug") or str(stage_project.get("slug") or ""),
        "profile": value(data, "project", "profile"),
        "lifecycle_state": value(data, "project", "lifecycle_state") or str(stage_lifecycle.get("lifecycle_state") or ""),
        "current_mode": value(data, "project", "current_mode") or str(stage_project.get("mode") or ""),
        "factory_producer_owned_layer": value(data, "project", "factory_producer_owned_layer"),
    }


def resolved_change(data: dict[str, Any], context: dict[str, Any]) -> dict[str, str]:
    task_change = context.get("task_index", {}).get("change", {}) if isinstance(context.get("task_index"), dict) else {}
    dashboard_change = data.get("active_change", {}) if isinstance(data.get("active_change"), dict) else {}
    result: dict[str, str] = {}
    for key in ["id", "title", "class", "priority", "status"]:
        result[key] = str(dashboard_change.get(key) or task_change.get(key) or "")
    result["owner_boundary"] = str(dashboard_change.get("owner_boundary") or "internal-repo-follow-up")
    return result


def render(data: dict[str, Any], root: Path, dashboard_path: Path) -> str:
    context = optional_context(root, dashboard_path)
    project = resolved_project(data, context)
    change = resolved_change(data, context)
    lifecycle = data.get("lifecycle_phase", {}) if isinstance(data.get("lifecycle_phase"), dict) else {}
    stage = context.get("stage_state", {}).get("stage", {}) if isinstance(context.get("stage_state"), dict) else {}
    task_state = context.get("task_state", {}) if isinstance(context.get("task_state"), dict) else {}
    execution = data.get("multi_step_execution", {}) if isinstance(data.get("multi_step_execution"), dict) else {}
    orchestration = data.get("handoff_orchestration", {}) if isinstance(data.get("handoff_orchestration"), dict) else {}
    release = data.get("release_readiness", {}) if isinstance(data.get("release_readiness"), dict) else {}
    runtime = data.get("deploy_runtime", {}) if isinstance(data.get("deploy_runtime"), dict) else {}
    standards = data.get("standards_navigator", {}) if isinstance(data.get("standards_navigator"), dict) else {}
    software_updates = data.get("software_update_governance", {}) if isinstance(data.get("software_update_governance"), dict) else {}
    post_release = data.get("post_release_improvement", {}) if isinstance(data.get("post_release_improvement"), dict) else {}
    runbook_packages = data.get("runbook_packages", []) if isinstance(data.get("runbook_packages"), list) else []
    recommended = data.get("recommended_next_step", {}) if isinstance(data.get("recommended_next_step"), dict) else {}
    fallback = data.get("fallback_next_step", {}) if isinstance(data.get("fallback_next_step"), dict) else {}

    gates = list_value(data, "stage_gates")
    waves = execution.get("waves", []) if isinstance(execution.get("waves"), list) else []
    cockpit = context.get("cockpit", {}) if isinstance(context.get("cockpit"), dict) else {}
    cockpit_parent = cockpit.get("parent", {}) if isinstance(cockpit.get("parent"), dict) else {}
    cockpit_route = cockpit.get("route_receipt", {}) if isinstance(cockpit.get("route_receipt"), dict) else {}

    lines = [
        "# Панель жизненного цикла проекта / `project-lifecycle-dashboard`",
        "",
        f"Generated UTC: `{now_utc()}`",
        f"Source: `{dashboard_path}`",
        "",
        "## Сейчас",
        "",
        f"- Проект: `{project['name']}` (`{project['slug']}`)",
        f"- Профиль: `{project['profile']}`",
        f"- Lifecycle state: `{project['lifecycle_state']}`",
        f"- Текущий mode: `{project['current_mode']}`",
        f"- Factory producer layer: `{project['factory_producer_owned_layer']}`",
        f"- Фаза: `{lifecycle.get('current', '')}` -> next `{lifecycle.get('next', '')}`",
        f"- Stage file говорит: current `{stage.get('current', '')}`, next `{stage.get('next', '')}`",
        "",
        "## Активное изменение",
        "",
        f"- id: `{change['id']}`",
        f"- title: {change['title']}",
        f"- class/priority/status: `{change['class']}` / `{change['priority']}` / `{change['status']}`",
        f"- boundary: `{change['owner_boundary']}`",
        f"- task-state next action: {value(task_state, 'next_action', 'summary')}",
        "",
            "## Гейты этапов",
        "",
        "| Gate | Status | Evidence / reason |",
        "|---|---|---|",
    ]
    for gate in gates:
        if isinstance(gate, dict):
            lines.append(f"| `{gate.get('id', '')}` {gate.get('title', '')} | `{gate.get('status', '')}` | {evidence_text(gate)} |")

    lines.extend(
        [
            "",
            "## Многошаговое выполнение",
            "",
            f"- current wave: `{execution.get('current_wave', '')}`",
            f"- completed tasks: `{', '.join(map(str, execution.get('completed_tasks', []) or [])) or 'none'}`",
            f"- blocked tasks: `{', '.join(map(str, execution.get('blocked_tasks', []) or [])) or 'none'}`",
            f"- next task: `{value(execution, 'next_task', 'id')}` - {value(execution, 'next_task', 'action')}",
            f"- final verification: `{value(execution, 'final_verification', 'status')}` {evidence_text(execution.get('final_verification', {}) if isinstance(execution.get('final_verification'), dict) else {})}",
            f"- archive allowed: `{value(execution, 'archive_to_work_completed', 'allowed')}`; {value(execution, 'archive_to_work_completed', 'reason')}",
            "",
            "| Wave | Status | Tasks |",
            "|---|---|---|",
        ]
    )
    for wave in waves:
        if not isinstance(wave, dict):
            continue
        tasks = []
        for task in wave.get("tasks", []) or []:
            if isinstance(task, dict):
                tasks.append(f"`{task.get('id', '')}` `{task.get('status', '')}`")
        lines.append(f"| `{wave.get('id', '')}` {wave.get('title', '')} | `{wave.get('status', '')}` | {', '.join(tasks) or 'none'} |")

    lines.extend(
        [
            "",
            "## Передача и оркестрация",
            "",
            f"- parent handoff: `{value(orchestration, 'parent_handoff', 'id') or cockpit_parent.get('id', '')}` `{value(orchestration, 'parent_handoff', 'status') or cockpit_parent.get('status', '')}`",
            f"- selected profile/model/reasoning: `{orchestration.get('selected_profile') or cockpit_route.get('selected_profile', '')}` / `{orchestration.get('selected_model') or cockpit_route.get('selected_model', '')}` / `{orchestration.get('selected_reasoning_effort') or cockpit_route.get('selected_reasoning_effort', '')}`",
            f"- route boundary: {orchestration.get('route_explanation_boundary', '')}",
            "",
            "## Пакеты операторских сценариев",
            "",
            "| Package | Phase | Gates | Blockers | Next action |",
            "|---|---|---|---|---|",
        ]
    )
    for package in runbook_packages:
        if not isinstance(package, dict):
            continue
        gates_text = ", ".join(f"`{gate}`" for gate in package.get("gates", []) or [])
        blockers_text = ", ".join(map(str, package.get("blockers", []) or [])) or "none"
        lines.append(
            f"| `{package.get('id', '')}` | `{package.get('current_phase', '')}` | {gates_text} | {blockers_text} | {package.get('next_action', '')} |"
        )

    lines.extend(
        [
            "",
            "## Готовность релиза",
            "",
            f"- version: `{release.get('version', '')}`",
            f"- status: `{release.get('status', '')}`",
            f"- verification: `{release.get('verification_state', '')}`",
            f"- changelog/release notes/scorecard: `{release.get('changelog', '')}` / `{release.get('release_notes', '')}` / `{release.get('scorecard', '')}`",
            f"- VERIFY_SUMMARY present: `{bool(context.get('verify_summary'))}`",
            "",
            "## Развертывание и выполнение",
            "",
            f"- status: `{runtime.get('status', '')}`",
            f"- preset: `{runtime.get('preset', '')}`",
            f"- operator source: `{runtime.get('operator_dashboard_source', '')}`",
            f"- dry-run report present: `{bool(context.get('runtime_reports', {}).get('dry_run'))}`",
            f"- deploy report present: `{bool(context.get('runtime_reports', {}).get('deploy'))}`",
            f"- boundary: {runtime.get('boundary', '')}",
            "",
            "## Навигатор стандартов",
            "",
            f"- profile: `{standards.get('selected_profile', '')}`",
            f"- lifecycle backbone: `{value(standards, 'lifecycle_backbone', 'standard_ref')}` `{value(standards, 'lifecycle_backbone', 'selected_version')}` (`{value(standards, 'lifecycle_backbone', 'version_status')}`)",
            f"- gate summary: `{value(standards, 'gate_summary', 'passed')}/{value(standards, 'gate_summary', 'total')}` passed; missing `{value(standards, 'gate_summary', 'missing')}`; blocking `{value(standards, 'gate_summary', 'blocking')}`",
            f"- current phase standards: `{value(standards, 'current_phase_required_standards', 'phase')}` -> {', '.join(map(str, list_value(standards, 'current_phase_required_standards', 'standard_refs'))) or 'none'}",
            f"- missing evidence: `{', '.join(map(str, standards.get('missing_standards_evidence', []) or [])) or 'none'}`",
            f"- next standards action: {value(standards, 'next_safe_standards_action', 'action')}",
            f"- monitoring: `{value(standards, 'monitoring_status', 'status')}`; proposal_required `{value(standards, 'monitoring_status', 'proposal_required')}`",
            f"- allowed to advance phase: `{standards.get('allowed_to_advance_phase', '')}`",
            f"- boundary: {standards.get('false_compliance_boundary', '')}",
            "",
            "## Управление обновлениями",
            "",
            f"- baseline status: `{software_updates.get('baseline_status', '')}`",
            f"- auto-update policy: `{software_updates.get('auto_update_policy', '')}`",
            f"- last intelligence check: `{software_updates.get('last_update_intelligence_check', '') or 'not recorded'}`",
            f"- relevant findings: `{software_updates.get('relevant_findings_count', 0)}`",
            f"- upgrade proposal: `{software_updates.get('upgrade_proposal_status', '')}`",
            f"- blockers: `{', '.join(map(str, software_updates.get('blockers', []) or [])) or 'none'}`",
            f"- next safe action: {value(software_updates, 'next_safe_action', 'action')}",
            f"- fallback action: {value(software_updates, 'fallback_action', 'action')}",
            "",
            "## Улучшения после релиза",
            "",
            f"- incidents: `{len(post_release.get('incidents', []) or [])}`",
            f"- feedback: `{len(post_release.get('feedback', []) or [])}`",
            f"- learning proposals: `{len(post_release.get('learning_proposals', []) or [])}`",
            f"- backlog candidates: `{len(post_release.get('backlog_candidates', []) or [])}`",
            "",
            "## Реестр внешних действий",
            "",
            bullet(data.get("external_actions_ledger", []) or [], empty="- внешних/manual действий сейчас нет"),
            "",
            "## Следующий шаг",
            "",
            f"- Recommended (`{recommended.get('owner_boundary', '')}`): {recommended.get('action', '')}",
            f"- Fallback (`{fallback.get('owner_boundary', '')}`): {fallback.get('action', '')}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Рендерит repo-native Project Lifecycle Dashboard в Markdown.")
    parser.add_argument("--root", default="", help="Project root. По умолчанию определяется автоматически.")
    parser.add_argument("--input", default="", help="Dashboard YAML. По умолчанию `.chatgpt/project-lifecycle-dashboard.yaml` или template source.")
    parser.add_argument("--output", default="reports/project-lifecycle-dashboard.md", help="Markdown output path.")
    parser.add_argument("--stdout", action="store_true", help="Печатать Markdown в stdout вместо записи файла.")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else detect_repo_root()
    input_path = Path(args.input).resolve() if args.input else default_dashboard_path(root)
    data = load_yaml(input_path)
    validator = load_validator()
    errors = validator.validate_dashboard(data)
    if errors:
        print("PROJECT LIFECYCLE DASHBOARD НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1

    rendered = render(data, root, input_path)
    if args.stdout:
        print(rendered, end="")
    else:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"lifecycle_dashboard={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
