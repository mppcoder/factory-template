#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ALLOWED_STATES = {
    "intake",
    "planning",
    "ready_for_handoff",
    "in_progress",
    "blocked",
    "external_wait",
    "verify",
    "done",
}
ALLOWED_OWNERS = {
    "internal_repo",
    "external_user",
    "external_runtime",
    "downstream_sync",
    "mixed",
}
ALLOWED_NEXT_TYPES = {"internal", "external", "blocked", "verify", "none"}
BOUNDARY_KEYS = [
    "internal_work",
    "external_user_actions",
    "external_runtime",
    "downstream_sync",
]


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise ValueError(f"некорректный YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("root должен быть YAML mapping")
    return data


def non_empty(value: Any) -> bool:
    return bool(str(value or "").strip())


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"не найден `{path}`"]
    try:
        data = load_yaml(path)
    except ValueError as exc:
        return [str(exc)]

    if data.get("schema") != "task-state-lite/v1":
        errors.append("schema должен быть `task-state-lite/v1`")
    current_state = str(data.get("current_state", "")).strip()
    owner = str(data.get("owner_boundary", "")).strip()
    if current_state not in ALLOWED_STATES:
        errors.append("current_state имеет неизвестное значение")
    if owner not in ALLOWED_OWNERS:
        errors.append("owner_boundary имеет неизвестное значение")

    next_action = data.get("next_action")
    if not isinstance(next_action, dict):
        errors.append("next_action должен быть mapping")
        next_action = {}
    next_type = str(next_action.get("type", "")).strip()
    next_summary = str(next_action.get("summary", "")).strip()
    if next_type not in ALLOWED_NEXT_TYPES:
        errors.append("next_action.type имеет неизвестное значение")
    if next_type != "none" and not next_summary:
        errors.append("next_action.summary обязателен, если next_action.type не `none`")

    blocked = data.get("blocked")
    if not isinstance(blocked, dict):
        errors.append("blocked должен быть mapping")
        blocked = {}
    blocked_status = blocked.get("status")
    blocked_reason = str(blocked.get("reason", "")).strip()
    if not isinstance(blocked_status, bool):
        errors.append("blocked.status должен быть boolean")
    if blocked_status is True and not blocked_reason:
        errors.append("blocked.reason обязателен при blocked.status=true")
    if blocked_status is False and not blocked_reason:
        errors.append("blocked.reason должен быть `not_required` или краткой причиной отсутствия блокера")
    if current_state == "blocked" and blocked_status is not True:
        errors.append("current_state=blocked требует blocked.status=true")
    if current_state == "done" and blocked_status is True:
        errors.append("current_state=done не может иметь active blocker")
    if current_state == "done" and next_type not in {"none", "verify"}:
        errors.append("current_state=done допускает только next_action.type none/verify")

    boundaries = data.get("boundaries")
    if not isinstance(boundaries, dict):
        errors.append("boundaries должен быть mapping")
        boundaries = {}
    has_boundary_note = False
    for key in BOUNDARY_KEYS:
        value = boundaries.get(key)
        if not isinstance(value, list):
            errors.append(f"boundaries.{key} должен быть list")
            continue
        if any(non_empty(item) for item in value):
            has_boundary_note = True
    if not has_boundary_note:
        errors.append("boundaries должен содержать хотя бы одну содержательную boundary-запись")

    sources = data.get("source_artifacts", [])
    if not isinstance(sources, list):
        errors.append("source_artifacts должен быть list")
    elif not any(non_empty(item) for item in sources):
        errors.append("source_artifacts должен содержать хотя бы один repo artifact")

    if owner == "external_user" and next_type != "external":
        errors.append("owner_boundary=external_user требует next_action.type=external")
    if owner == "external_runtime" and not boundaries.get("external_runtime"):
        errors.append("owner_boundary=external_runtime требует boundaries.external_runtime")
    if owner == "downstream_sync" and not boundaries.get("downstream_sync"):
        errors.append("owner_boundary=downstream_sync требует boundaries.downstream_sync")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет .chatgpt/task-state.yaml.")
    parser.add_argument("root", nargs="?", default=".", help="Корень repo или путь к task-state.yaml")
    args = parser.parse_args()

    raw = Path(args.root).expanduser()
    path = raw if raw.is_file() else raw / ".chatgpt" / "task-state.yaml"
    errors = validate(path)
    if errors:
        print("TASK STATE LITE НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1
    print("TASK STATE LITE ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
