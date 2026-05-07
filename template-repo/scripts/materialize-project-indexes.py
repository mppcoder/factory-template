#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path
from typing import Any

import yaml

from project_naming import validate_project_code


CHAT_DEFAULT_POLICY = {
    "canonical_format": "<PROJECT_CODE>-CH-<NNNN> <task-slug>",
    "include_status_in_title": False,
    "include_kind_in_title": False,
    "title_is_stable": True,
    "status_source_of_truth": ".chatgpt/chat-handoff-index.yaml",
    "manual_rename_required_on_status_change": False,
}
CHAT_DEFAULT_ALLOCATION = {
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
CHAT_ALLOWED_KINDS = ["handoff", "self_handoff", "bug", "decision", "research", "completion_followup"]
CHAT_ALLOWED_STATES = [
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
CODEX_DEFAULT_POLICY = {
    "canonical_format": "<PROJECT_CODE>-CX-<NNNN> <task-slug>",
    "independent_from_chat_handoff_index": True,
    "status_source_of_truth": ".chatgpt/codex-work-index.yaml",
}
CODEX_ALLOWED_KINDS = ["self_handoff", "direct_task", "remediation", "validation_followup"]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def load_validator(script_name: str, module_name: str):
    path = Path(__file__).resolve().with_name(script_name)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Не удалось загрузить {script_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def materialize_chat_index(path: Path, project_code: str) -> None:
    data = load_yaml(path)
    data["schema"] = "chat-handoff-index/v1"
    data["project_code"] = project_code
    data["next_chat_number"] = 1
    data["title_policy"] = data.get("title_policy") if isinstance(data.get("title_policy"), dict) else {}
    for key, value in CHAT_DEFAULT_POLICY.items():
        data["title_policy"][key] = value
    data["allocation_policy"] = data.get("allocation_policy") if isinstance(data.get("allocation_policy"), dict) else {}
    for key, value in CHAT_DEFAULT_ALLOCATION.items():
        data["allocation_policy"][key] = value
    data["allowed_kinds"] = data.get("allowed_kinds") if isinstance(data.get("allowed_kinds"), list) else CHAT_ALLOWED_KINDS
    data["allowed_states"] = data.get("allowed_states") if isinstance(data.get("allowed_states"), list) else CHAT_ALLOWED_STATES
    data["items"] = []
    errors = load_validator("validate-chat-handoff-index.py", "validate_chat_handoff_index").validate_index(data)
    if errors:
        raise SystemExit("CHAT HANDOFF INDEX MATERIALIZATION FAILED\n- " + "\n- ".join(errors))
    write_yaml(path, data)


def materialize_codex_index(path: Path, project_code: str) -> None:
    data = load_yaml(path)
    data["schema"] = "codex-work-index/v1"
    data["project_code"] = project_code
    data["next_codex_work_number"] = 1
    data["id_policy"] = data.get("id_policy") if isinstance(data.get("id_policy"), dict) else {}
    for key, value in CODEX_DEFAULT_POLICY.items():
        data["id_policy"][key] = value
    data["allowed_kinds"] = data.get("allowed_kinds") if isinstance(data.get("allowed_kinds"), list) else CODEX_ALLOWED_KINDS
    data["allowed_states"] = data.get("allowed_states") if isinstance(data.get("allowed_states"), list) else CHAT_ALLOWED_STATES
    data["items"] = []
    errors = load_validator("validate-codex-work-index.py", "validate_codex_work_index").validate_index(data)
    if errors:
        raise SystemExit("CODEX WORK INDEX MATERIALIZATION FAILED\n- " + "\n- ".join(errors))
    write_yaml(path, data)


def update_stage_state(path: Path, project_code: str) -> None:
    data = load_yaml(path)
    project = data.setdefault("project", {})
    if isinstance(project, dict):
        project["code"] = project_code
    write_yaml(path, data)


def update_project_origin(path: Path, project_code: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else "# Происхождение проекта\n"
    block = f"## PROJECT_CODE\n{project_code}\n"
    pattern = re.compile(r"##\s+PROJECT_CODE\s*\n[^\n]*(?:\n|$)", re.IGNORECASE)
    if pattern.search(text):
        text = pattern.sub(block, text)
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += f"\n{block}"
    path.write_text(text, encoding="utf-8")


def update_task_registry(path: Path, project_code: str) -> None:
    if not path.exists():
        return
    data = load_yaml(path)
    if not data:
        return
    data["project_code"] = project_code
    policy = data.setdefault("task_id_policy", {})
    if isinstance(policy, dict):
        policy["canonical_format"] = f"{project_code}-TASK-NNNN"
        policy["source_of_truth"] = ".chatgpt/task-registry.yaml"
    max_number = 0
    for task in data.get("tasks", []) or []:
        if not isinstance(task, dict):
            continue
        task_id = str(task.get("task_id") or "")
        match = re.match(r"^[A-Z][A-Z0-9]*-TASK-(\d{4})$", task_id)
        if match:
            number = int(match.group(1))
            max_number = max(max_number, number)
            task["task_id"] = f"{project_code}-TASK-{number:04d}"
            replace_ft_task_refs(task, project_code)
    if isinstance(data.get("next_task_number"), int):
        data["next_task_number"] = max(int(data["next_task_number"]), max_number + 1)
    write_yaml(path, data)


def replace_ft_task_refs(value: Any, project_code: str) -> Any:
    if isinstance(value, dict):
        for key, child in list(value.items()):
            value[key] = replace_ft_task_refs(child, project_code)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            value[index] = replace_ft_task_refs(child, project_code)
    elif isinstance(value, str):
        return re.sub(r"\bFT-TASK-(\d{4})\b", rf"{project_code}-TASK-\1", value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize repo-local ChatGPT/Codex indexes for a generated project.")
    parser.add_argument("--root", default=".", help="Generated project root.")
    parser.add_argument("--project-code", required=True, help="Per-project uppercase code, e.g. NGIS.")
    parser.add_argument("--allow-ft", action="store_true", help="Allow FT for factory-template only.")
    args = parser.parse_args()

    project_code = args.project_code.strip().upper()
    errors = validate_project_code(project_code, allow_ft=args.allow_ft)
    if errors:
        print("PROJECT INDEX MATERIALIZATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    root = Path(args.root).resolve()
    chat = root / ".chatgpt"
    materialize_chat_index(chat / "chat-handoff-index.yaml", project_code)
    materialize_codex_index(chat / "codex-work-index.yaml", project_code)
    update_stage_state(chat / "stage-state.yaml", project_code)
    update_project_origin(chat / "project-origin.md", project_code)
    update_task_registry(chat / "task-registry.yaml", project_code)
    print(f"PROJECT INDEXES MATERIALIZED: project_code={project_code}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
