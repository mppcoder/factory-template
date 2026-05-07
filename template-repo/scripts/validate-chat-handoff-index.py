#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "chat-handoff-index/v1"
CHAT_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*-CH-[0-9]{4}$")
TASK_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")
STATUS_TITLE_TOKENS = {
    "OPEN",
    "DONE",
    "BLOCKED",
    "SUPERSEDED",
    "VOID",
    "VERIFIED",
    "ARCHIVED",
}
KIND_TITLE_TOKENS = {"HO", "SELFHO", "BUG", "DECISION", "RESEARCH"}
HANDOFF_CHAIN = ["chatgpt_handoff", "codex_accepted", "codex_completed"]
SELF_HANDOFF_CHAIN = ["codex_self_handoff", "codex_accepted", "codex_completed"]
OTHER_ALLOWED_CHAINS = [HANDOFF_CHAIN, SELF_HANDOFF_CHAIN]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def has_evidence(item: dict[str, Any]) -> bool:
    evidence = item.get("evidence")
    return isinstance(evidence, list) and any(str(entry).strip() for entry in evidence)


def has_reason(item: dict[str, Any]) -> bool:
    return bool(str(item.get("accepted_reason") or item.get("replacement_reason") or item.get("closeout_reason") or "").strip())


def validate_policy(data: dict[str, Any], errors: list[str]) -> None:
    policy = data.get("title_policy")
    if not isinstance(policy, dict):
        errors.append("title_policy должен быть mapping")
        return
    expected = {
        "canonical_format": "<PROJECT_CODE>-CH-<NNNN> <task-slug>",
        "include_status_in_title": False,
        "include_kind_in_title": False,
        "title_is_stable": True,
        "status_source_of_truth": ".chatgpt/chat-handoff-index.yaml",
        "manual_rename_required_on_status_change": False,
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            errors.append(f"title_policy.{key} должен быть `{value}`")

    allocation_policy = data.get("allocation_policy")
    if not isinstance(allocation_policy, dict):
        errors.append("allocation_policy должен быть mapping")
        return
    allocation_expected = {
        "shared_counter_for_all_kinds": False,
        "first_chat_response_allocates_handoff_id": True,
        "visible_chat_title_requires_materialized_index_item": True,
        "dry_run_title_is_not_reserved": True,
        "unlaunched_handoff_keeps_chat_number_reserved": True,
        "repo_local_allocator_attempt_first": True,
        "github_connector_write_fallback": True,
        "github_connector_write_requires_confirm_fetch": True,
        "blocker_forbidden_when_confirmed_write_path_available": True,
        "allocator_blocker_required_without_write_access": True,
        "codex_self_handoff_uses_same_counter": False,
        "handoff_must_reference_chat_id": True,
        "self_handoff_must_reference_chat_id": False,
        "codex_self_handoff_uses_codex_work_index": True,
        "codex_work_index_path": ".chatgpt/codex-work-index.yaml",
    }
    for key, value in allocation_expected.items():
        if allocation_policy.get(key) != value:
            errors.append(f"allocation_policy.{key} должен быть `{value}`")


def title_has_forbidden_token(title: str, tokens: set[str]) -> str:
    title_tokens = {part.upper() for part in re.split(r"[^A-Za-z0-9]+", title) if part}
    for token in sorted(tokens):
        if token in title_tokens:
            return token
    return ""


def validate_item(
    item: dict[str, Any],
    index: int,
    allowed_kinds: set[str],
    allowed_states: set[str],
    project_code: str,
    errors: list[str],
) -> None:
    item_path = f"items[{index}]"
    required = [
        "chat_id",
        "chat_number",
        "chat_title",
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
            errors.append(f"{item_path}.{field} обязателен")

    chat_id = str(item.get("chat_id") or "")
    if not CHAT_ID_RE.match(chat_id):
        errors.append(f"{item_path}.chat_id должен соответствовать ^[A-Z][A-Z0-9]*-CH-[0-9]{{4}}$")
    elif project_code and not chat_id.startswith(f"{project_code}-CH-"):
        errors.append(f"{item_path}.chat_id должен начинаться с `{project_code}-CH-`")
    if "-CX-" in chat_id or "codex_work_id" in item:
        errors.append(f"{item_path} не должен смешивать ChatGPT CH и Codex CX поля")

    chat_number = item.get("chat_number")
    if not isinstance(chat_number, int) or chat_number < 1:
        errors.append(f"{item_path}.chat_number должен быть positive integer")
    elif CHAT_ID_RE.match(chat_id):
        suffix = int(chat_id.rsplit("-", 1)[1])
        if suffix != chat_number:
            errors.append(f"{item_path}.chat_number должен совпадать с номером в chat_id")

    task_slug = str(item.get("task_slug") or "")
    if not TASK_SLUG_RE.match(task_slug):
        errors.append(f"{item_path}.task_slug должен быть lowercase kebab-case")

    chat_title = str(item.get("chat_title") or "")
    if chat_title != f"{chat_id} {task_slug}":
        errors.append(f'{item_path}.chat_title должен быть ровно "{chat_id} {task_slug}"')
    status_token = title_has_forbidden_token(chat_title, STATUS_TITLE_TOKENS)
    if status_token:
        errors.append(f"{item_path}.chat_title содержит status token `{status_token}`")
    kind_token = title_has_forbidden_token(chat_title, KIND_TITLE_TOKENS)
    if kind_token:
        errors.append(f"{item_path}.chat_title содержит kind token `{kind_token}`")

    kind = str(item.get("kind") or "")
    if kind not in allowed_kinds:
        errors.append(f"{item_path}.kind неизвестен: `{kind}`")
    state = str(item.get("state") or "")
    if state not in allowed_states:
        errors.append(f"{item_path}.state неизвестен: `{state}`")
    if not isinstance(item.get("handoff_revision"), int) or item.get("handoff_revision", 0) < 1:
        errors.append(f"{item_path}.handoff_revision должен быть positive integer")
    if not isinstance(item.get("evidence"), list):
        errors.append(f"{item_path}.evidence должен быть list")
    if not str(item.get("next_action") or "").strip():
        errors.append(f"{item_path}.next_action обязателен")

    chain = item.get("status_chain")
    expected_chain = SELF_HANDOFF_CHAIN if kind == "self_handoff" else HANDOFF_CHAIN if kind == "handoff" else None
    if not isinstance(chain, list):
        errors.append(f"{item_path}.status_chain должен быть list")
    else:
        normalized_chain = [str(entry) for entry in chain]
        if expected_chain is not None and normalized_chain != expected_chain:
            errors.append(f"{item_path}.status_chain для kind `{kind}` должен быть {', '.join(expected_chain)}")
        elif expected_chain is None and normalized_chain not in OTHER_ALLOWED_CHAINS:
            errors.append(f"{item_path}.status_chain должен быть одним из разрешенных handoff chains")

    if state in {"verified", "archived"} and not has_evidence(item):
        errors.append(f"{item_path} state `{state}` требует evidence")
    if state == "superseded" and not (str(item.get("replacement_chat_id") or "").strip() or has_reason(item)):
        errors.append(f"{item_path} superseded требует replacement_chat_id или accepted/replacement reason")
    if state == "not_applicable" and not has_reason(item):
        errors.append(f"{item_path} not_applicable требует accepted_reason")


def validate_index(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")
    dumped = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    if SECRET_RE.search(dumped) or "-----BEGIN" in dumped:
        errors.append("chat handoff index содержит secret-like content")

    project_code = str(data.get("project_code") or "")
    if not re.match(r"^[A-Z][A-Z0-9]*$", project_code):
        errors.append("project_code должен быть uppercase code")
    next_chat_number = data.get("next_chat_number")
    if not isinstance(next_chat_number, int) or next_chat_number < 1:
        errors.append("next_chat_number должен быть positive integer")
        next_chat_number = 0
    validate_policy(data, errors)

    allowed_kinds_raw = data.get("allowed_kinds", [])
    allowed_states_raw = data.get("allowed_states", [])
    if not isinstance(allowed_kinds_raw, list) or not allowed_kinds_raw:
        errors.append("allowed_kinds должен быть непустым list")
        allowed_kinds_raw = []
    if not isinstance(allowed_states_raw, list) or not allowed_states_raw:
        errors.append("allowed_states должен быть непустым list")
        allowed_states_raw = []
    allowed_kinds = {str(kind) for kind in allowed_kinds_raw}
    allowed_states = {str(state) for state in allowed_states_raw}

    items_raw = data.get("items", [])
    if not isinstance(items_raw, list):
        errors.append("items должен быть list")
        items_raw = []

    seen_ids: set[str] = set()
    seen_numbers: set[int] = set()
    max_number = 0
    for index, item in enumerate(items_raw, 1):
        if not isinstance(item, dict):
            errors.append(f"items[{index}] должен быть mapping")
            continue
        validate_item(item, index, allowed_kinds, allowed_states, project_code, errors)
        chat_id = str(item.get("chat_id") or "")
        if chat_id in seen_ids:
            errors.append(f"items[{index}].chat_id повторяется: `{chat_id}`")
        seen_ids.add(chat_id)
        chat_number = item.get("chat_number")
        if isinstance(chat_number, int):
            if chat_number in seen_numbers:
                errors.append(f"items[{index}].chat_number повторяется: `{chat_number}`")
            seen_numbers.add(chat_number)
            max_number = max(max_number, chat_number)

    if isinstance(next_chat_number, int) and next_chat_number <= max_number:
        errors.append("next_chat_number должен быть больше всех existing chat_number")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует repo-first ChatGPT chat handoff index.")
    parser.add_argument("path", nargs="?", default="template-repo/template/.chatgpt/chat-handoff-index.yaml")
    args = parser.parse_args()

    path = Path(args.path)
    errors = validate_index(load_yaml(path))
    if errors:
        print("CHAT HANDOFF INDEX НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CHAT HANDOFF INDEX ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
