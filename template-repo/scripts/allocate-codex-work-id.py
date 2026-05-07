#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path
from typing import Any

import yaml

from factory_automation_common import now_utc


STATUS_CHAIN = ["codex_self_handoff", "codex_accepted", "codex_completed"]
DEFAULT_ALLOWED_STATES = ["open", "codex_accepted", "in_progress", "implemented", "verified", "blocked", "superseded", "not_applicable", "archived"]
DEFAULT_ALLOWED_KINDS = ["self_handoff", "direct_task", "remediation", "validation_followup"]


def default_index_path(root: Path) -> Path:
    direct = root / ".chatgpt" / "codex-work-index.yaml"
    if direct.exists() or (root / ".chatgpt").exists():
        return direct
    return root / "template-repo" / "template" / ".chatgpt" / "codex-work-index.yaml"


def project_code_from_root(root: Path) -> str:
    for path in [
        root / ".chatgpt" / "codex-work-index.yaml",
        root / ".chatgpt" / "task-registry.yaml",
        root / ".chatgpt" / "stage-state.yaml",
    ]:
        data = load_yaml(path)
        if path.name == "stage-state.yaml":
            project = data.get("project") if isinstance(data.get("project"), dict) else {}
            configured = str(project.get("code") or "").strip() if isinstance(project, dict) else ""
        else:
            configured = str(data.get("project_code") or "").strip()
        if configured:
            return configured
    return "FT" if root.name == "factory-template" else "PRJ"


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
            "schema": "codex-work-index/v1",
            "project_code": project_code,
            "next_codex_work_number": 1,
            "id_policy": {
                "canonical_format": "<PROJECT_CODE>-CX-<NNNN> <task-slug>",
                "independent_from_chat_handoff_index": True,
                "status_source_of_truth": ".chatgpt/codex-work-index.yaml",
            },
            "allowed_kinds": DEFAULT_ALLOWED_KINDS,
            "allowed_states": DEFAULT_ALLOWED_STATES,
            "items": [],
        }
    data.setdefault("schema", "codex-work-index/v1")
    data.setdefault("project_code", project_code)
    data.setdefault("next_codex_work_number", 1)
    data.setdefault(
        "id_policy",
        {
            "canonical_format": "<PROJECT_CODE>-CX-<NNNN> <task-slug>",
            "independent_from_chat_handoff_index": True,
            "status_source_of_truth": ".chatgpt/codex-work-index.yaml",
        },
    )
    data.setdefault("allowed_kinds", DEFAULT_ALLOWED_KINDS)
    data.setdefault("allowed_states", DEFAULT_ALLOWED_STATES)
    data.setdefault("items", [])
    return data


def load_validator():
    path = Path(__file__).resolve().with_name("validate-codex-work-index.py")
    spec = importlib.util.spec_from_file_location("validate_codex_work_index", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Не удалось загрузить validate-codex-work-index.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description="Выделяет отдельный Codex work id без расходования ChatGPT chat counter.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--index", default="")
    parser.add_argument("--project-code", default="")
    parser.add_argument("--kind", default="self_handoff", choices=DEFAULT_ALLOWED_KINDS)
    parser.add_argument("--description", required=True)
    parser.add_argument("--source-type", default="direct-task")
    parser.add_argument("--handoff-group", default="")
    parser.add_argument("--handoff-revision", type=int, default=1)
    parser.add_argument("--handoff-register-item-id", default="")
    parser.add_argument("--state", default="open", choices=DEFAULT_ALLOWED_STATES)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    index_path = Path(args.index).resolve() if args.index else default_index_path(root)
    data = ensure_index(load_yaml(index_path), args.project_code or project_code_from_root(root))
    if args.project_code:
        data["project_code"] = args.project_code
    project_code = str(data.get("project_code") or args.project_code or project_code_from_root(root))
    next_number = int(data.get("next_codex_work_number") or 1)
    task_slug = slugify(args.description)
    work_id = f"{project_code}-CX-{next_number:04d}"
    work_title = f"{work_id} {task_slug}"
    now = now_utc().replace("+00:00", "Z")
    item = {
        "codex_work_id": work_id,
        "work_number": next_number,
        "work_title": work_title,
        "task_slug": task_slug,
        "kind": args.kind,
        "state": args.state,
        "created_utc": now,
        "updated_utc": now,
        "source_type": args.source_type,
        "handoff_group": args.handoff_group or task_slug,
        "handoff_revision": args.handoff_revision,
        "handoff_register_item_id": args.handoff_register_item_id,
        "status_chain": STATUS_CHAIN,
        "evidence": args.evidence,
        "next_action": "Accept in Codex or update repo state before implementation.",
    }
    data.setdefault("items", []).append(item)
    data["next_codex_work_number"] = next_number + 1
    errors = load_validator().validate_index(data)
    if errors:
        print("CODEX WORK ALLOCATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    if not args.dry_run:
        write_yaml(index_path, data)

    print("Codex work title:")
    print(work_title)
    print()
    print("Repo state:")
    print(f"codex_work_id: {work_id}")
    print(f"kind: {args.kind}")
    print(f"state: {args.state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
