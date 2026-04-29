#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "orchestration-cockpit/v1"
PARENT_STATUSES = {"planned", "validated", "dry-run", "executing", "completed", "blocked"}
CHILD_STATUSES = {"planned", "session-file-written", "executed", "blocked", "skipped"}
OWNER_BOUNDARIES = {
    "internal-repo-follow-up",
    "external-user-action",
    "runtime-action",
    "downstream-battle-action",
    "model-mapping-blocker",
    "secret-boundary-blocker",
}
TASK_CLASSES = {"quick", "build", "deep", "review"}
PLACEHOLDER_RE = re.compile(r"^__[A-Z0-9_]+__$")
SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def nonempty_mapping(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"`{key}` должен быть mapping")
        return {}
    return value


def validate_cockpit(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")
    dumped = yaml.safe_dump(data, allow_unicode=True)
    if SECRET_RE.search(dumped) or "-----BEGIN" in dumped:
        errors.append("cockpit содержит secret-like content")

    parent = nonempty_mapping(data, "parent", errors)
    parent_status = str(parent.get("status") or "")
    if parent_status not in PARENT_STATUSES:
        errors.append("parent.status должен быть одним из " + ", ".join(sorted(PARENT_STATUSES)))
    for field in ["id", "title", "launch_source", "handoff_shape", "selected_scenario", "apply_mode", "strict_launch_mode"]:
        if not str(parent.get(field) or "").strip():
            errors.append(f"parent.{field} обязателен")
    if str(parent.get("handoff_shape") or "") != "parent-orchestration-handoff":
        errors.append("parent.handoff_shape должен быть parent-orchestration-handoff")

    route = nonempty_mapping(data, "route_receipt", errors)
    if str(route.get("handoff_shape") or "") != "parent-orchestration-handoff":
        errors.append("route_receipt.handoff_shape должен быть parent-orchestration-handoff")
    task_class = str(route.get("task_class") or "")
    if task_class not in TASK_CLASSES:
        errors.append("route_receipt.task_class должен быть quick/build/deep/review")
    for field in [
        "selected_profile",
        "selected_model",
        "selected_reasoning_effort",
        "selected_plan_mode_reasoning_effort",
        "route_explanation",
    ]:
        if not str(route.get(field) or "").strip():
            errors.append(f"route_receipt.{field} обязателен")
    explanation = str(route.get("route_explanation") or "").lower()
    if "deterministic" not in explanation and "keyword" not in explanation and "rule" not in explanation:
        errors.append("route_receipt.route_explanation должен явно назвать deterministic/keyword/rule-based evidence")
    if "live catalog" not in explanation:
        errors.append("route_receipt.route_explanation должен упоминать live catalog validation boundary")

    child_tasks = data.get("child_tasks")
    if not isinstance(child_tasks, list) or not child_tasks:
        errors.append("child_tasks должен быть непустым list")
    else:
        for index, child in enumerate(child_tasks, 1):
            if not isinstance(child, dict):
                errors.append(f"child_tasks[{index}] должен быть mapping")
                continue
            child_id = str(child.get("id") or f"#{index}")
            for field in ["id", "title", "task_class", "selected_profile", "selected_model", "selected_reasoning_effort", "status", "owner_boundary"]:
                if not str(child.get(field) or "").strip():
                    errors.append(f"child `{child_id}` не содержит `{field}`")
            if str(child.get("task_class") or "") not in TASK_CLASSES:
                errors.append(f"child `{child_id}`: unknown task_class")
            if str(child.get("status") or "") not in CHILD_STATUSES:
                errors.append(f"child `{child_id}`: unknown status")
            if str(child.get("owner_boundary") or "") not in OWNER_BOUNDARIES:
                errors.append(f"child `{child_id}`: unknown owner_boundary")

    blockers = data.get("blockers", [])
    if blockers is not None and not isinstance(blockers, list):
        errors.append("blockers должен быть list")
    for index, blocker in enumerate(blockers or [], 1):
        if not isinstance(blocker, dict):
            errors.append(f"blockers[{index}] должен быть mapping")
            continue
        if str(blocker.get("owner_boundary") or "") not in OWNER_BOUNDARIES:
            errors.append(f"blockers[{index}].owner_boundary unknown")

    for index, item in enumerate(data.get("placeholder_replacements", []) or [], 1):
        if not isinstance(item, dict):
            errors.append(f"placeholder_replacements[{index}] должен быть mapping")
            continue
        if not PLACEHOLDER_RE.match(str(item.get("placeholder") or "")):
            errors.append(f"placeholder_replacements[{index}].placeholder должен иметь вид `__PLACEHOLDER__`")
        if str(item.get("final_value_owner") or "") != "operator":
            errors.append(f"placeholder_replacements[{index}].final_value_owner должен быть `operator`")
        if str(item.get("replacement_timing") or "") not in {"final-user-action", "future-user-action"}:
            errors.append(f"placeholder_replacements[{index}].replacement_timing invalid")

    next_action = nonempty_mapping(data, "next_action", errors)
    if str(next_action.get("owner_boundary") or "") not in OWNER_BOUNDARIES:
        errors.append("next_action.owner_boundary unknown")
    if not str(next_action.get("action") or "").strip():
        errors.append("next_action.action обязателен")
    if not str(data.get("continuation_outcome") or "").strip():
        errors.append("continuation_outcome обязателен")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует orchestration-cockpit-lite YAML.")
    parser.add_argument("path", nargs="?", default="template-repo/template/.chatgpt/orchestration-cockpit.yaml")
    args = parser.parse_args()

    path = Path(args.path)
    errors = validate_cockpit(load_yaml(path))
    if errors:
        print("ORCHESTRATION COCKPIT НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ORCHESTRATION COCKPIT ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
