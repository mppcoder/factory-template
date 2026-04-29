#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
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


CHAT_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*-CH-[0-9]{4}$")
TASK_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CHAT_STATES = {
    "open",
    "codex_accepted",
    "in_progress",
    "implemented",
    "verified",
    "blocked",
    "superseded",
    "not_applicable",
    "archived",
}
CHAT_STATUS_TOKENS = {"OPEN", "CODEX", "DONE", "BLOCKED", "SUPERSEDED", "VOID", "VERIFIED", "ARCHIVED"}
CHAT_KIND_TOKENS = {"HO", "SELFHO", "BUG", "DECISION", "RESEARCH"}


def validate_list(value: Any, path: str, errors: list[str]) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"{path} должен быть list")
        return []
    return value


def title_has_token(title: str, tokens: set[str]) -> str:
    title_tokens = {part.upper() for part in re.split(r"[^A-Za-z0-9]+", title) if part}
    for token in sorted(tokens):
        if token in title_tokens:
            return token
    return ""


def validate_optional_chat_link(item: dict[str, Any], item_id: str, errors: list[str]) -> None:
    chat_id = str(item.get("chat_id") or "").strip()
    chat_title = str(item.get("chat_title") or "").strip()
    task_slug = str(item.get("task_slug") or "").strip()
    chat_state = str(item.get("chat_state") or "").strip()
    chat_index_item_id = str(item.get("chat_index_item_id") or "").strip()
    if not any([chat_id, chat_title, task_slug, chat_state, chat_index_item_id]):
        return
    if not chat_id:
        errors.append(f"items[{item_id}].chat_id обязателен, если заполнены chat_* поля")
    elif not CHAT_ID_RE.match(chat_id):
        errors.append(f"items[{item_id}].chat_id должен соответствовать стабильному формату PROJECT-CH-0001")
    if not task_slug:
        errors.append(f"items[{item_id}].task_slug обязателен, если заполнены chat_* поля")
    elif not TASK_SLUG_RE.match(task_slug):
        errors.append(f"items[{item_id}].task_slug должен быть lowercase kebab-case")
    if chat_id and task_slug and chat_title != f"{chat_id} {task_slug}":
        errors.append(f'items[{item_id}].chat_title должен быть ровно "{chat_id} {task_slug}"')
    if chat_title:
        status_token = title_has_token(chat_title, CHAT_STATUS_TOKENS)
        if status_token:
            errors.append(f"items[{item_id}].chat_title содержит status token `{status_token}`")
        kind_token = title_has_token(chat_title, CHAT_KIND_TOKENS)
        if kind_token:
            errors.append(f"items[{item_id}].chat_title содержит kind token `{kind_token}`")
    if chat_state and chat_state not in CHAT_STATES:
        errors.append(f"items[{item_id}].chat_state неизвестен: `{chat_state}`")


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

    replacement_policy = data.get("replacement_policy")
    if replacement_policy is not None:
        if not isinstance(replacement_policy, dict):
            errors.append("replacement_policy должен быть mapping")
            replacement_policy = {}
        for key in ["same_chat_same_task_single_active", "superseded_requires_replacement_link", "replacement_reason_required"]:
            if replacement_policy.get(key) is not True:
                errors.append(f"replacement_policy.{key} должен быть true")

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
        for field in [
            "id",
            "title",
            "handoff_group",
            "source_type",
            "task_class",
            "status",
            "priority",
            "calculated_priority",
            "owner_boundary",
            "next_action",
        ]:
            if not str(item.get(field) or "").strip():
                errors.append(f"items[{item_id}].{field} обязателен")
        if not isinstance(item.get("handoff_revision"), int) or item.get("handoff_revision", 0) < 1:
            errors.append(f"items[{item_id}].handoff_revision должен быть positive integer")
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
        validate_optional_chat_link(item, item_id, errors)

        depends_on = validate_list(item.get("depends_on"), f"items[{item_id}].depends_on", errors)
        blocks = validate_list(item.get("blocks"), f"items[{item_id}].blocks", errors)
        replaces = validate_list(item.get("replaces"), f"items[{item_id}].replaces", errors)
        validate_list(item.get("artifacts_to_update"), f"items[{item_id}].artifacts_to_update", errors)
        validate_list(item.get("evidence"), f"items[{item_id}].evidence", errors)
        for dep_id in depends_on:
            if str(dep_id) not in by_id:
                errors.append(f"items[{item_id}].depends_on содержит неизвестный id `{dep_id}`")
        for blocked_id in blocks:
            if str(blocked_id) not in by_id:
                errors.append(f"items[{item_id}].blocks содержит неизвестный id `{blocked_id}`")
        for replaced_id in replaces:
            replaced = by_id.get(str(replaced_id))
            if replaced is None:
                errors.append(f"items[{item_id}].replaces содержит неизвестный id `{replaced_id}`")
                continue
            if status_of(replaced) not in {"superseded", "not_applicable", "archived"}:
                errors.append(f"items[{item_id}].replaces указывает на `{replaced_id}`, но замененный item не списан")
            if str(replaced.get("superseded_by") or "") != item_id:
                errors.append(f"items[{replaced_id}].superseded_by должен ссылаться на `{item_id}`")

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
        if status == "superseded":
            if not str(item.get("superseded_by") or "").strip():
                errors.append(f"items[{item_id}] отмечен superseded без superseded_by")
            elif str(item.get("superseded_by")) not in by_id:
                errors.append(f"items[{item_id}].superseded_by содержит неизвестный id `{item.get('superseded_by')}`")
            else:
                replacement = by_id[str(item.get("superseded_by"))]
                replacement_replaces = {str(replaced_id) for replaced_id in replacement.get("replaces", []) or []}
                if item_id not in replacement_replaces:
                    errors.append(f"items[{item_id}].superseded_by указывает на replacement, который не содержит `{item_id}` в replaces")
            if not str(item.get("replacement_reason") or item.get("closeout_reason") or "").strip():
                errors.append(f"items[{item_id}] отмечен superseded без replacement_reason или closeout_reason")
            if not has_evidence(item):
                errors.append(f"items[{item_id}] отмечен superseded без evidence")
        if status == "archived" and not has_evidence(item):
            errors.append(f"items[{item_id}] archived требует evidence после verified/not_applicable closeout")

    groups: dict[str, list[str]] = {}
    for item in items:
        group = str(item.get("handoff_group") or "").strip()
        if not group or status_of(item) in {"verified", "not_applicable", "superseded", "archived"}:
            continue
        groups.setdefault(group, []).append(str(item.get("id") or ""))
    for group, active_ids in sorted(groups.items()):
        if len(active_ids) > 1:
            errors.append(
                f"handoff_group `{group}` содержит несколько активных handoff items: {', '.join(active_ids)}; "
                "старые handoff нужно списать как superseded/not_applicable"
            )

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
