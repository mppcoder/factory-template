#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from handoff_implementation_common import (
    DEFAULT_ALLOWED_STATUSES,
    EVIDENCE_REQUIRED_STATUSES,
    OWNER_BOUNDARIES,
    PRIORITIES,
    SCHEMA,
    SECRET_RE,
    SOURCE_TYPES,
    TASK_CLASSES,
    calculated_priority,
    effective_status,
    has_accepted_reason,
    has_evidence,
    item_map,
    load_yaml,
    normalized_items,
    status_of,
    unresolved_dependencies,
)


def validate_list(value: Any, path: str, errors: list[str]) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"{path} должен быть list")
        return []
    return value


def validate_register(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")

    dumped = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    if SECRET_RE.search(dumped) or "-----BEGIN" in dumped:
        errors.append("handoff implementation register содержит secret-like content")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        errors.append("scope должен быть mapping")
        scope = {}
    if not str(scope.get("project") or "").strip():
        errors.append("scope.project обязателен")
    if str(scope.get("owner_boundary") or "") != "template-owned-generated-project-artifact":
        errors.append("scope.owner_boundary должен быть template-owned-generated-project-artifact")

    queue_policy = data.get("queue_policy")
    if not isinstance(queue_policy, dict):
        errors.append("queue_policy должен быть mapping")
        queue_policy = {}
    for key in ["dependency_first", "blockers_raise_priority", "stale_visible_cards", "silent_drop_forbidden"]:
        if queue_policy.get(key) is not True:
            errors.append(f"queue_policy.{key} должен быть true")

    statuses = data.get("statuses")
    if not isinstance(statuses, dict):
        errors.append("statuses должен быть mapping")
        statuses = {}
    allowed = statuses.get("allowed", [])
    if not isinstance(allowed, list):
        errors.append("statuses.allowed должен быть list")
        allowed = []
    allowed_set = {str(status) for status in allowed}
    missing = sorted(DEFAULT_ALLOWED_STATUSES - allowed_set)
    if missing:
        errors.append("statuses.allowed не содержит: " + ", ".join(missing))

    raw_items = data.get("items", [])
    if not isinstance(raw_items, list):
        errors.append("items должен быть list")
        raw_items = []
    items = normalized_items(data)
    by_id = item_map(items)
    if len(by_id) != len(items):
        errors.append("items содержит пустые или повторяющиеся id")

    for index, item in enumerate(raw_items, 1):
        if not isinstance(item, dict):
            errors.append(f"items[{index}] должен быть mapping")
            continue
        item_id = str(item.get("id") or f"#{index}")
        for field in ["id", "title", "source_type", "task_class", "status", "priority", "calculated_priority", "owner_boundary", "next_action"]:
            if not str(item.get(field) or "").strip():
                errors.append(f"items[{item_id}].{field} обязателен")
        if str(item.get("source_type") or "") not in SOURCE_TYPES:
            errors.append(f"items[{item_id}].source_type неизвестен")
        if str(item.get("task_class") or "") not in TASK_CLASSES:
            errors.append(f"items[{item_id}].task_class неизвестен")
        status = status_of(item)
        if status not in allowed_set:
            errors.append(f"items[{item_id}].status неизвестен: `{status}`")
        if str(item.get("priority") or "") not in PRIORITIES:
            errors.append(f"items[{item_id}].priority должен быть low/medium/high/critical")
        if str(item.get("calculated_priority") or "") not in PRIORITIES:
            errors.append(f"items[{item_id}].calculated_priority должен быть low/medium/high/critical")
        expected_priority = calculated_priority(item, by_id)
        if str(item.get("calculated_priority") or "") != expected_priority:
            errors.append(
                f"items[{item_id}].calculated_priority должен быть `{expected_priority}` "
                "по deterministic dependency/priority calculation"
            )
        if str(item.get("owner_boundary") or "") not in OWNER_BOUNDARIES:
            errors.append(f"items[{item_id}].owner_boundary неизвестен")

        depends_on = validate_list(item.get("depends_on"), f"items[{item_id}].depends_on", errors)
        blocks = validate_list(item.get("blocks"), f"items[{item_id}].blocks", errors)
        validate_list(item.get("artifacts_to_update"), f"items[{item_id}].artifacts_to_update", errors)
        validate_list(item.get("evidence"), f"items[{item_id}].evidence", errors)
        for dep_id in depends_on:
            if str(dep_id) not in by_id:
                errors.append(f"items[{item_id}].depends_on содержит неизвестный id `{dep_id}`")
        for blocked_id in blocks:
            if str(blocked_id) not in by_id:
                errors.append(f"items[{item_id}].blocks содержит неизвестный id `{blocked_id}`")

        unresolved = unresolved_dependencies(item, by_id)
        if unresolved and status not in {"blocked", "verified", "not_applicable", "archived"}:
            errors.append(
                f"items[{item_id}] зависит от незакрытых задач ({', '.join(unresolved)}), "
                "но не помечен status: blocked"
            )
        if status == "ready" and effective_status(item, by_id) == "blocked":
            errors.append(f"items[{item_id}] ошибочно показан как ready при незакрытых dependencies")

        if status in EVIDENCE_REQUIRED_STATUSES and not (has_evidence(item) or has_accepted_reason(item)):
            errors.append(f"items[{item_id}] отмечен `{status}`, но не содержит evidence или accepted_reason")
        if status == "not_applicable":
            if not has_accepted_reason(item):
                errors.append(f"items[{item_id}] отмечен not_applicable без closeout_reason или accepted_reason")
            if not (has_evidence(item) or str(item.get("accepted_reason") or "").strip()):
                errors.append(f"items[{item_id}] отмечен not_applicable без evidence или accepted_reason")
        if status == "archived" and not has_evidence(item):
            errors.append(f"items[{item_id}] archived требует evidence после verified/not_applicable closeout")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует register жизненного цикла handoff/self-handoff задач.")
    parser.add_argument("path", nargs="?", default="template-repo/template/.chatgpt/handoff-implementation-register.yaml")
    args = parser.parse_args()

    path = Path(args.path)
    errors = validate_register(load_yaml(path))
    if errors:
        print("HANDOFF IMPLEMENTATION REGISTER НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("HANDOFF IMPLEMENTATION REGISTER ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
