#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path
from typing import Any

import yaml

from factory_automation_common import now_utc


DEFAULT_ALLOWED_KINDS = ["handoff", "self_handoff", "bug", "decision", "research", "completion_followup"]
DEFAULT_ALLOWED_STATES = [
    "open",
    "codex_accepted",
    "in_progress",
    "implemented",
    "verified",
    "blocked",
    "superseded",
    "not_applicable",
    "archived",
]
HANDOFF_CHAIN = ["chatgpt_handoff", "codex_accepted", "codex_completed"]
SELF_HANDOFF_CHAIN = ["codex_self_handoff", "codex_accepted", "codex_completed"]
DEFAULT_ALLOCATION_POLICY = {
    "shared_counter_for_all_kinds": False,
    "first_chat_response_allocates_handoff_id": True,
    "visible_chat_title_requires_materialized_index_item": True,
    "dry_run_title_is_not_reserved": True,
    "unlaunched_handoff_keeps_chat_number_reserved": True,
    "allocator_blocker_required_without_write_access": True,
    "codex_self_handoff_uses_same_counter": False,
    "handoff_must_reference_chat_id": True,
    "self_handoff_must_reference_chat_id": False,
    "codex_self_handoff_uses_codex_work_index": True,
    "codex_work_index_path": ".chatgpt/codex-work-index.yaml",
}


def default_index_path(root: Path) -> Path:
    direct = root / ".chatgpt" / "chat-handoff-index.yaml"
    if direct.exists():
        return direct
    return root / "template-repo" / "template" / ".chatgpt" / "chat-handoff-index.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def slugify(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "task"


def ensure_index(data: dict[str, Any], project_code: str) -> dict[str, Any]:
    if not data:
        return {
            "schema": "chat-handoff-index/v1",
            "project_code": project_code,
            "next_chat_number": 1,
            "title_policy": {
                "canonical_format": "<PROJECT_CODE>-CH-<NNNN> <task-slug>",
                "include_status_in_title": False,
                "include_kind_in_title": False,
                "title_is_stable": True,
                "status_source_of_truth": ".chatgpt/chat-handoff-index.yaml",
                "manual_rename_required_on_status_change": False,
            },
            "allocation_policy": dict(DEFAULT_ALLOCATION_POLICY),
            "allowed_kinds": DEFAULT_ALLOWED_KINDS,
            "allowed_states": DEFAULT_ALLOWED_STATES,
            "items": [],
        }
    data.setdefault("schema", "chat-handoff-index/v1")
    data.setdefault("project_code", project_code)
    data.setdefault("next_chat_number", 1)
    data.setdefault("allowed_kinds", DEFAULT_ALLOWED_KINDS)
    data.setdefault("allowed_states", DEFAULT_ALLOWED_STATES)
    data.setdefault("items", [])
    data.setdefault(
        "title_policy",
        {
            "canonical_format": "<PROJECT_CODE>-CH-<NNNN> <task-slug>",
            "include_status_in_title": False,
            "include_kind_in_title": False,
            "title_is_stable": True,
            "status_source_of_truth": ".chatgpt/chat-handoff-index.yaml",
            "manual_rename_required_on_status_change": False,
        },
    )
    data.setdefault(
        "allocation_policy",
        dict(DEFAULT_ALLOCATION_POLICY),
    )
    allocation_policy = data.get("allocation_policy")
    if isinstance(allocation_policy, dict):
        for key, value in DEFAULT_ALLOCATION_POLICY.items():
            allocation_policy.setdefault(key, value)
    return data


def load_validator():
    path = Path(__file__).resolve().with_name("validate-chat-handoff-index.py")
    spec = importlib.util.spec_from_file_location("validate_chat_handoff_index", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Не удалось загрузить validate-chat-handoff-index.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description="Выделяет стабильный ChatGPT chat id/title из repo index.")
    parser.add_argument("--root", default=".", help="Project root for default index discovery.")
    parser.add_argument("--index", default="", help="Path to .chatgpt/chat-handoff-index.yaml or template equivalent.")
    parser.add_argument("--project-code", default="", help="Uppercase project code, e.g. FT.")
    parser.add_argument("--kind", required=True, choices=DEFAULT_ALLOWED_KINDS)
    parser.add_argument("--description", required=True, help="Short task description; will be slugified.")
    parser.add_argument("--source-type", default="chatgpt-first-answer")
    parser.add_argument("--handoff-group", default="")
    parser.add_argument("--handoff-revision", type=int, default=1)
    parser.add_argument("--handoff-register-item-id", default="")
    parser.add_argument("--state", default="open", choices=DEFAULT_ALLOWED_STATES)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true", help="Print allocation without writing the index.")
    args = parser.parse_args()

    if args.kind == "self_handoff":
        print("CHAT HANDOFF ALLOCATION FAILED")
        print("- Codex self-handoff не должен расходовать ChatGPT chat counter.")
        print("- Используйте: python3 template-repo/scripts/allocate-codex-work-id.py --description \"...\"")
        return 1

    root = Path(args.root).resolve()
    index_path = Path(args.index).resolve() if args.index else default_index_path(root)
    project_code = args.project_code or "FT"
    data = ensure_index(load_yaml(index_path), project_code)
    if args.project_code:
        data["project_code"] = args.project_code
    project_code = str(data.get("project_code") or project_code)
    next_number = int(data.get("next_chat_number") or 1)
    task_slug = slugify(args.description)
    chat_id = f"{project_code}-CH-{next_number:04d}"
    chat_title = f"{chat_id} {task_slug}"
    now = now_utc().replace("+00:00", "Z")

    item = {
        "chat_id": chat_id,
        "chat_number": next_number,
        "chat_title": chat_title,
        "task_slug": task_slug,
        "kind": args.kind,
        "state": args.state,
        "created_utc": now,
        "updated_utc": now,
        "source_type": args.source_type,
        "handoff_group": args.handoff_group or task_slug,
        "handoff_revision": args.handoff_revision,
        "handoff_register_item_id": args.handoff_register_item_id,
        "status_chain": SELF_HANDOFF_CHAIN if args.kind == "self_handoff" else HANDOFF_CHAIN,
        "evidence": args.evidence,
        "next_action": "Start the Codex handoff or close/supersede this repo reservation; do not reuse this chat number.",
    }

    data.setdefault("items", []).append(item)
    data["next_chat_number"] = next_number + 1
    validator = load_validator()
    errors = validator.validate_index(data)
    if errors:
        print("CHAT HANDOFF ALLOCATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    if not args.dry_run:
        write_yaml(index_path, data)

    if args.dry_run:
        print("DRY RUN ONLY - CHAT NUMBER NOT RESERVED")
        print("Do not show this title in the first ChatGPT answer.")
        print()
    print("ChatGPT title to copy:" if not args.dry_run else "Calculated title:")
    print(chat_title)
    print()
    print("Repo state:")
    print(f"chat_id: {chat_id}")
    print(f"kind: {args.kind}")
    print(f"state: {args.state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
