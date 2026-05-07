#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def load_validator(script_name: str, module_name: str):
    path = Path(__file__).resolve().with_name(script_name)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Не удалось загрузить {script_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def origin_project_code(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    match = re.search(r"##\s+PROJECT_CODE\s*\n([A-Z][A-Z0-9]*)", text)
    return match.group(1) if match else ""


def expected_project_code(root: Path) -> tuple[str, list[str]]:
    sources: list[tuple[str, str]] = []
    stage = load_yaml(root / ".chatgpt" / "stage-state.yaml")
    project = stage.get("project") if isinstance(stage.get("project"), dict) else {}
    if isinstance(project, dict) and project.get("code"):
        sources.append((".chatgpt/stage-state.yaml project.code", str(project.get("code"))))
    registry = load_yaml(root / ".chatgpt" / "task-registry.yaml")
    if registry.get("project_code"):
        sources.append((".chatgpt/task-registry.yaml project_code", str(registry.get("project_code"))))
    origin_code = origin_project_code(root / ".chatgpt" / "project-origin.md")
    if origin_code:
        sources.append((".chatgpt/project-origin.md PROJECT_CODE", origin_code))

    if not sources and root.name == "factory-template":
        chat_index = load_yaml(root / ".chatgpt" / "chat-handoff-index.yaml")
        if str(chat_index.get("project_code") or "") == "FT":
            return "FT", []
    if not sources:
        return "", ["project identity config missing: expected project_code in stage-state, task-registry or project-origin"]
    normalized = [(label, value.strip()) for label, value in sources]
    values = {value for _label, value in normalized}
    if len(values) > 1:
        details = ", ".join(f"{label}={value}" for label, value in normalized)
        return "", [f"project_code identity mismatch across config: {details}"]
    return normalized[0][1], []


def validate_chat_index(path: Path, expected_code: str, errors: list[str]) -> None:
    data = load_yaml(path)
    if not data:
        errors.append(f"missing chat handoff index: {path}")
        return
    for error in load_validator("validate-chat-handoff-index.py", "validate_chat_handoff_index").validate_index(data):
        errors.append(f"chat-handoff-index: {error}")
    project_code = str(data.get("project_code") or "")
    if project_code != expected_code:
        errors.append(f"chat-handoff-index project_code `{project_code}` должен совпадать с project identity `{expected_code}`")
    seen_ids: set[str] = set()
    seen_numbers: set[int] = set()
    max_number = 0
    for index, item in enumerate(data.get("items", []) or [], 1):
        if not isinstance(item, dict):
            continue
        chat_id = str(item.get("chat_id") or "")
        if "-CX-" in chat_id or item.get("codex_work_id"):
            errors.append(f"chat-handoff-index items[{index}] смешивает CH и CX поля")
        if chat_id and not chat_id.startswith(f"{expected_code}-CH-"):
            errors.append(f"chat-handoff-index items[{index}].chat_id должен начинаться с `{expected_code}-CH-`")
        if chat_id in seen_ids:
            errors.append(f"chat-handoff-index duplicate chat_id `{chat_id}`")
        seen_ids.add(chat_id)
        number = item.get("chat_number")
        if isinstance(number, int):
            if number in seen_numbers:
                errors.append(f"chat-handoff-index duplicate chat_number `{number}`")
            seen_numbers.add(number)
            max_number = max(max_number, number)
    next_number = data.get("next_chat_number")
    if isinstance(next_number, int) and next_number <= max_number:
        errors.append("chat-handoff-index next_chat_number должен быть больше всех chat_number")


def validate_codex_index(path: Path, expected_code: str, errors: list[str]) -> None:
    data = load_yaml(path)
    if not data:
        errors.append(f"missing codex work index: {path}")
        return
    for error in load_validator("validate-codex-work-index.py", "validate_codex_work_index").validate_index(data):
        errors.append(f"codex-work-index: {error}")
    project_code = str(data.get("project_code") or "")
    if project_code != expected_code:
        errors.append(f"codex-work-index project_code `{project_code}` должен совпадать с project identity `{expected_code}`")
    seen_ids: set[str] = set()
    seen_numbers: set[int] = set()
    max_number = 0
    for index, item in enumerate(data.get("items", []) or [], 1):
        if not isinstance(item, dict):
            continue
        work_id = str(item.get("codex_work_id") or "")
        if "-CH-" in work_id or item.get("chat_id"):
            errors.append(f"codex-work-index items[{index}] смешивает CX и CH поля")
        if work_id and not work_id.startswith(f"{expected_code}-CX-"):
            errors.append(f"codex-work-index items[{index}].codex_work_id должен начинаться с `{expected_code}-CX-`")
        if work_id in seen_ids:
            errors.append(f"codex-work-index duplicate codex_work_id `{work_id}`")
        seen_ids.add(work_id)
        number = item.get("work_number")
        if isinstance(number, int):
            if number in seen_numbers:
                errors.append(f"codex-work-index duplicate work_number `{number}`")
            seen_numbers.add(number)
            max_number = max(max_number, number)
    next_number = data.get("next_codex_work_number")
    if isinstance(next_number, int) and next_number <= max_number:
        errors.append("codex-work-index next_codex_work_number должен быть больше всех codex_work_number")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate per-project ChatGPT/Codex index identity.")
    parser.add_argument("root", nargs="?", default=".", help="Project root.")
    parser.add_argument("--allow-ft", action="store_true", help="Allow FT identity for factory-template.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []
    expected_code, identity_errors = expected_project_code(root)
    errors.extend(identity_errors)
    if expected_code == "FT" and not args.allow_ft:
        errors.append("project_code `FT` is factory-only and forbidden for downstream project identity")
    if expected_code:
        validate_chat_index(root / ".chatgpt" / "chat-handoff-index.yaml", expected_code, errors)
        validate_codex_index(root / ".chatgpt" / "codex-work-index.yaml", expected_code, errors)

    if errors:
        print("PROJECT INDEX IDENTITY НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PROJECT INDEX IDENTITY ВАЛИДЕН: project_code={expected_code}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
