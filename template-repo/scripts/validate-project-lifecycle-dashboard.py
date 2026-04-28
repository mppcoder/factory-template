#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "project-lifecycle-dashboard/v1"
LIFECYCLE_PHASES = {
    "idea",
    "intake",
    "spec",
    "architecture",
    "handoff",
    "execution",
    "verification",
    "release",
    "deploy",
    "operate",
    "improve",
}
STATUSES = {
    "not_started",
    "pending",
    "in_progress",
    "blocked",
    "passed",
    "completed",
    "done",
    "skipped",
    "failed",
    "not_applicable",
    "draft",
    "ready",
    "ready-for-handoff",
    "archived",
}
GREEN_STATUSES = {"passed", "completed", "done", "ready", "archived"}
OWNER_BOUNDARIES = {
    "internal-repo-follow-up",
    "external-user-action",
    "runtime-action",
    "downstream-battle-action",
    "model-mapping-blocker",
    "secret-boundary-blocker",
}
PROJECT_OWNER_BOUNDARIES = {
    "template-owned-generated-project-artifact",
    "factory-template-root",
    "project-owned",
}
CHANGE_CLASSES = {
    "small-fix",
    "feature",
    "refactor",
    "migration",
    "brownfield-audit",
    "deep",
    "quick",
    "build",
    "review",
}
PRIORITIES = {"low", "medium", "high", "critical"}
REQUIRED_TOP_LEVEL = [
    "project",
    "lifecycle_phase",
    "active_change",
    "stage_gates",
    "multi_step_execution",
    "handoff_orchestration",
    "release_readiness",
    "deploy_runtime",
    "post_release_improvement",
    "external_actions_ledger",
    "recommended_next_step",
    "fallback_next_step",
]
SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")
POSITIVE_AUTOSWITCH_RE = re.compile(
    r"(?i)(advisory|handoff|scenario|project instruction).{0,80}(auto[- ]?switch|switches model|switches profile|switches reasoning)"
)
RU_POSITIVE_AUTOSWITCH_RE = re.compile(
    r"(?i)(advisory|handoff|сценари|инструкц|project).{0,100}(автоматически переключает|сам переключает|переключает model|переключает profile|переключает reasoning)"
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def as_mapping(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"`{key}` должен быть mapping")
        return {}
    return value


def as_list(data: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"`{key}` должен быть list")
        return []
    return value


def has_evidence(item: dict[str, Any]) -> bool:
    evidence = item.get("evidence")
    if isinstance(evidence, list) and evidence:
        return True
    if isinstance(evidence, str) and evidence.strip():
        return True
    reason = item.get("accepted_reason") or item.get("reason")
    return bool(str(reason or "").strip())


def status_of(item: dict[str, Any], default: str = "") -> str:
    return str(item.get("status") or default).strip()


def validate_status(value: str, path: str, errors: list[str]) -> None:
    if value and value not in STATUSES:
        errors.append(f"{path} имеет неизвестный status `{value}`")


def validate_boundary(value: str, path: str, errors: list[str]) -> None:
    if value not in OWNER_BOUNDARIES:
        errors.append(f"{path} должен быть одним из: {', '.join(sorted(OWNER_BOUNDARIES))}")


def validate_green_evidence(item: dict[str, Any], path: str, errors: list[str]) -> None:
    status = status_of(item)
    if status in GREEN_STATUSES and not has_evidence(item):
        errors.append(f"{path} отмечен `{status}`, но не содержит evidence или accepted_reason")


def validate_dashboard(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"`{key}` обязателен")

    dumped = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    if SECRET_RE.search(dumped) or "-----BEGIN" in dumped:
        errors.append("dashboard содержит secret-like content")
    for line in dumped.splitlines():
        lowered = line.lower()
        if POSITIVE_AUTOSWITCH_RE.search(line) and "does not" not in lowered and "not " not in lowered:
            errors.append("dashboard содержит false auto-switch claim для advisory/routing layer")
        if RU_POSITIVE_AUTOSWITCH_RE.search(line) and "не переключает" not in lowered and "нельзя" not in lowered:
            errors.append("dashboard содержит false auto-switch claim для advisory/routing layer")

    project = as_mapping(data, "project", errors)
    for field in ["name", "slug", "profile", "lifecycle_state", "current_mode", "owner_boundary"]:
        if not str(project.get(field) or "").strip():
            errors.append(f"project.{field} обязателен")
    if str(project.get("owner_boundary") or "") not in PROJECT_OWNER_BOUNDARIES:
        errors.append("project.owner_boundary имеет неизвестное значение")

    lifecycle = as_mapping(data, "lifecycle_phase", errors)
    current_phase = str(lifecycle.get("current") or "")
    if current_phase not in LIFECYCLE_PHASES:
        errors.append("lifecycle_phase.current должен быть lifecycle phase")
    allowed = lifecycle.get("allowed", [])
    if isinstance(allowed, list) and allowed:
        unknown = [str(item) for item in allowed if str(item) not in LIFECYCLE_PHASES]
        if unknown:
            errors.append("lifecycle_phase.allowed содержит неизвестные phases: " + ", ".join(unknown))

    change = as_mapping(data, "active_change", errors)
    if str(change.get("class") or "") not in CHANGE_CLASSES:
        errors.append("active_change.class имеет неизвестное значение")
    if str(change.get("priority") or "") not in PRIORITIES:
        errors.append("active_change.priority должен быть low/medium/high/critical")
    validate_status(status_of(change), "active_change.status", errors)
    validate_boundary(str(change.get("owner_boundary") or ""), "active_change.owner_boundary", errors)
    validate_green_evidence(change, "active_change", errors)

    gates = as_list(data, "stage_gates", errors)
    required_gates = {
        "intake",
        "classification",
        "reuse_reality_check",
        "spec",
        "tech_spec",
        "handoff_allowed",
        "execution",
        "verification",
        "done",
    }
    seen_gates: set[str] = set()
    for index, gate in enumerate(gates, 1):
        if not isinstance(gate, dict):
            errors.append(f"stage_gates[{index}] должен быть mapping")
            continue
        gate_id = str(gate.get("id") or "")
        seen_gates.add(gate_id)
        if not gate_id:
            errors.append(f"stage_gates[{index}].id обязателен")
        if not str(gate.get("title") or "").strip():
            errors.append(f"stage_gates[{index}].title обязателен")
        validate_status(status_of(gate), f"stage_gates[{gate_id}].status", errors)
        validate_green_evidence(gate, f"stage_gates[{gate_id}]", errors)
    missing_gates = sorted(required_gates - seen_gates)
    if missing_gates:
        errors.append("stage_gates не содержит обязательные gates: " + ", ".join(missing_gates))

    execution = as_mapping(data, "multi_step_execution", errors)
    if not isinstance(execution.get("current_wave"), int):
        errors.append("multi_step_execution.current_wave должен быть integer")
    waves = execution.get("waves", [])
    if not isinstance(waves, list) or not waves:
        errors.append("multi_step_execution.waves должен быть непустым list")
    else:
        for wave_index, wave in enumerate(waves, 1):
            if not isinstance(wave, dict):
                errors.append(f"multi_step_execution.waves[{wave_index}] должен быть mapping")
                continue
            wave_id = str(wave.get("id") or f"#{wave_index}")
            validate_status(status_of(wave), f"wave {wave_id}.status", errors)
            validate_green_evidence(wave, f"wave {wave_id}", errors)
            tasks = wave.get("tasks", [])
            if not isinstance(tasks, list):
                errors.append(f"wave {wave_id}.tasks должен быть list")
                continue
            for task_index, task in enumerate(tasks, 1):
                if not isinstance(task, dict):
                    errors.append(f"wave {wave_id}.tasks[{task_index}] должен быть mapping")
                    continue
                task_id = str(task.get("id") or f"#{task_index}")
                validate_status(status_of(task), f"task {task_id}.status", errors)
                if str(task.get("owner_boundary") or ""):
                    validate_boundary(str(task.get("owner_boundary") or ""), f"task {task_id}.owner_boundary", errors)
                validate_green_evidence(task, f"task {task_id}", errors)
    next_task = execution.get("next_task")
    if not isinstance(next_task, dict) or not str(next_task.get("action") or "").strip():
        errors.append("multi_step_execution.next_task.action обязателен")
    elif str(next_task.get("owner_boundary") or ""):
        validate_boundary(str(next_task.get("owner_boundary") or ""), "multi_step_execution.next_task.owner_boundary", errors)
    final_verification = execution.get("final_verification")
    if not isinstance(final_verification, dict):
        errors.append("multi_step_execution.final_verification должен быть mapping")
    else:
        validate_status(status_of(final_verification), "multi_step_execution.final_verification.status", errors)
        validate_green_evidence(final_verification, "multi_step_execution.final_verification", errors)

    orchestration = as_mapping(data, "handoff_orchestration", errors)
    boundary_text = str(orchestration.get("route_explanation_boundary") or "").lower()
    if not boundary_text:
        errors.append("handoff_orchestration.route_explanation_boundary обязателен")
    if "не переключ" not in boundary_text and "does not" not in boundary_text:
        errors.append("handoff_orchestration.route_explanation_boundary должен явно запрещать advisory auto-switch claim")

    release = as_mapping(data, "release_readiness", errors)
    validate_status(status_of(release), "release_readiness.status", errors)
    validate_status(str(release.get("verification_state") or ""), "release_readiness.verification_state", errors)
    validate_green_evidence(release, "release_readiness", errors)

    runtime = as_mapping(data, "deploy_runtime", errors)
    validate_status(status_of(runtime), "deploy_runtime.status", errors)
    validate_green_evidence(runtime, "deploy_runtime", errors)

    post_release = as_mapping(data, "post_release_improvement", errors)
    for key in ["incidents", "feedback", "learning_proposals", "backlog_candidates"]:
        if not isinstance(post_release.get(key, []), list):
            errors.append(f"post_release_improvement.{key} должен быть list")

    for index, action in enumerate(as_list(data, "external_actions_ledger", errors), 1):
        if not isinstance(action, dict):
            errors.append(f"external_actions_ledger[{index}] должен быть mapping")
            continue
        boundary = str(action.get("owner_boundary") or "")
        if boundary not in OWNER_BOUNDARIES - {"internal-repo-follow-up"}:
            errors.append(f"external_actions_ledger[{index}].owner_boundary должен быть external/runtime/downstream/model/secret boundary")
        if not str(action.get("action") or "").strip():
            errors.append(f"external_actions_ledger[{index}].action обязателен")

    for key in ["recommended_next_step", "fallback_next_step"]:
        item = as_mapping(data, key, errors)
        validate_boundary(str(item.get("owner_boundary") or ""), f"{key}.owner_boundary", errors)
        if not str(item.get("action") or "").strip():
            errors.append(f"{key}.action обязателен")
        validate_green_evidence(item, key, errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует Project Lifecycle Dashboard YAML.")
    parser.add_argument("path", nargs="?", default="template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml")
    args = parser.parse_args()

    path = Path(args.path)
    errors = validate_dashboard(load_yaml(path))
    if errors:
        print("PROJECT LIFECYCLE DASHBOARD НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PROJECT LIFECYCLE DASHBOARD ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
