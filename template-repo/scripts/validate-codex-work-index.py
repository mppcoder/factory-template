#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "codex-work-index/v1"
WORK_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*-CX-[0-9]{4}$")
TASK_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")
ALLOWED_KINDS = {"self_handoff", "direct_task", "remediation", "validation_followup"}
ALLOWED_STATES = {"open", "codex_accepted", "in_progress", "implemented", "verified", "blocked", "superseded", "not_applicable", "archived"}
STATUS_CHAIN = ["codex_self_handoff", "codex_accepted", "codex_completed"]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def has_evidence(item: dict[str, Any]) -> bool:
    evidence = item.get("evidence")
    return isinstance(evidence, list) and any(str(entry).strip() for entry in evidence)


def has_reason(item: dict[str, Any]) -> bool:
    return bool(str(item.get("accepted_reason") or item.get("replacement_reason") or item.get("closeout_reason") or "").strip())


def validate_item(item: dict[str, Any], index: int, project_code: str, errors: list[str]) -> None:
    path = f"items[{index}]"
    required = [
        "codex_work_id",
        "work_number",
        "work_title",
        "task_slug",
        "kind",
        "state",
        "created_utc",
        "updated_utc",
        "source_type",
        "handoff_group",
        "handoff_revision",
        "handoff_register_item_id",
        "status_chain",
        "evidence",
        "next_action",
    ]
    for field in required:
        if field not in item:
            errors.append(f"{path}.{field} обязателен")

    work_id = str(item.get("codex_work_id") or "")
    if not WORK_ID_RE.match(work_id):
        errors.append(f"{path}.codex_work_id должен соответствовать PROJECT-CX-0001")
    elif project_code and not work_id.startswith(f"{project_code}-CX-"):
        errors.append(f"{path}.codex_work_id должен начинаться с `{project_code}-CX-`")
    if "-CH-" in work_id or "chat_id" in item:
        errors.append(f"{path} не должен смешивать Codex CX и ChatGPT CH поля")

    work_number = item.get("work_number")
    if not isinstance(work_number, int) or work_number < 1:
        errors.append(f"{path}.work_number должен быть positive integer")
    elif WORK_ID_RE.match(work_id):
        suffix = int(work_id.rsplit("-", 1)[1])
        if suffix != work_number:
            errors.append(f"{path}.work_number должен совпадать с номером в codex_work_id")

    task_slug = str(item.get("task_slug") or "")
    if not TASK_SLUG_RE.match(task_slug):
        errors.append(f"{path}.task_slug должен быть lowercase kebab-case")
    if str(item.get("work_title") or "") != f"{work_id} {task_slug}":
        errors.append(f'{path}.work_title должен быть ровно "{work_id} {task_slug}"')
    if str(item.get("kind") or "") not in ALLOWED_KINDS:
        errors.append(f"{path}.kind неизвестен")
    state = str(item.get("state") or "")
    if state not in ALLOWED_STATES:
        errors.append(f"{path}.state неизвестен")
    if item.get("status_chain") != STATUS_CHAIN:
        errors.append(f"{path}.status_chain должен быть {STATUS_CHAIN}")
    if not isinstance(item.get("handoff_revision"), int) or item.get("handoff_revision", 0) < 1:
        errors.append(f"{path}.handoff_revision должен быть positive integer")
    if not isinstance(item.get("evidence"), list):
        errors.append(f"{path}.evidence должен быть list")
    if not str(item.get("next_action") or "").strip():
        errors.append(f"{path}.next_action обязателен")
    if state in {"verified", "archived"} and not has_evidence(item):
        errors.append(f"{path} state `{state}` требует evidence")
    if state == "superseded" and not (str(item.get("replacement_work_id") or "").strip() or has_reason(item)):
        errors.append(f"{path} superseded требует replacement_work_id или accepted/replacement reason")
    if state == "not_applicable" and not has_reason(item):
        errors.append(f"{path} not_applicable требует accepted_reason")


def validate_index(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")
    dumped = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    if SECRET_RE.search(dumped) or "-----BEGIN" in dumped:
        errors.append("codex work index содержит secret-like content")
    project_code = str(data.get("project_code") or "")
    if not re.match(r"^[A-Z][A-Z0-9]*$", project_code):
        errors.append("project_code должен быть uppercase code")
    next_number = data.get("next_codex_work_number")
    if not isinstance(next_number, int) or next_number < 1:
        errors.append("next_codex_work_number должен быть positive integer")
        next_number = 0
    policy = data.get("id_policy")
    if not isinstance(policy, dict):
        errors.append("id_policy должен быть mapping")
    else:
        expected = {
            "canonical_format": "<PROJECT_CODE>-CX-<NNNN> <task-slug>",
            "independent_from_chat_handoff_index": True,
            "status_source_of_truth": ".chatgpt/codex-work-index.yaml",
        }
        for key, value in expected.items():
            if policy.get(key) != value:
                errors.append(f"id_policy.{key} должен быть `{value}`")

    items = data.get("items", [])
    if not isinstance(items, list):
        errors.append("items должен быть list")
        items = []
    seen_ids: set[str] = set()
    seen_numbers: set[int] = set()
    max_number = 0
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"items[{index}] должен быть mapping")
            continue
        validate_item(item, index, project_code, errors)
        work_id = str(item.get("codex_work_id") or "")
        if work_id in seen_ids:
            errors.append(f"items[{index}].codex_work_id повторяется: `{work_id}`")
        seen_ids.add(work_id)
        work_number = item.get("work_number")
        if isinstance(work_number, int):
            if work_number in seen_numbers:
                errors.append(f"items[{index}].work_number повторяется: `{work_number}`")
            seen_numbers.add(work_number)
            max_number = max(max_number, work_number)
    if isinstance(next_number, int) and next_number <= max_number:
        errors.append("next_codex_work_number должен быть больше всех work_number")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует Codex work index.")
    parser.add_argument("path")
    args = parser.parse_args()
    errors = validate_index(load_yaml(Path(args.path)))
    if errors:
        print("CODEX WORK INDEX НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CODEX WORK INDEX ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
