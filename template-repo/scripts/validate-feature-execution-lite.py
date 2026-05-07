#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


VALID_STATUSES = {"planned", "in_progress", "blocked", "done"}
DONE_FEATURE_STATUSES = {"done", "done_complete", "completed", "archived"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def template_root(root: Path) -> Path:
    if (root / "work-templates" / "execution-plan.md.template").exists():
        return root / "work-templates"
    if (root / "template-repo" / "template" / "work-templates").exists():
        return root / "template-repo" / "template" / "work-templates"
    if (root / "template" / "work-templates").exists():
        return root / "template" / "work-templates"
    return root / "template-repo" / "template" / "work-templates"


def append_missing_fragment_errors(path: Path, fragments: list[str], errors: list[str], root: Path) -> None:
    if not path.exists():
        errors.append(f"structural drift: не найден `{rel(path, root)}`")
        return
    text = read_text(path)
    for fragment in fragments:
        if fragment not in text:
            errors.append(f"structural drift: `{rel(path, root)}` не содержит `{fragment}`")


def validate_templates(root: Path, errors: list[str]) -> None:
    base = template_root(root)
    append_missing_fragment_errors(
        base / "execution-plan.md.template",
        ["# План выполнения Lite", "## Волны", "## Правило эскалации", "## Чеклист закрытия"],
        errors,
        root,
    )
    append_missing_fragment_errors(
        base / "checkpoint.yaml.template",
        ["schema: feature-execution-lite/v1", "final_verification:", "boundaries:", "max_review_rounds:"],
        errors,
        root,
    )
    append_missing_fragment_errors(
        base / "decisions.md.template",
        ["execution_wave:", "review_rounds:", "boundary:", "verification:"],
        errors,
        root,
    )
    append_missing_fragment_errors(
        base / "tasks" / "task.md.template",
        ["wave: {{TASK_WAVE}}", "reviewers:", "reviewer_hints:", "## Verify-smoke", "## Verify-user"],
        errors,
        root,
    )


def yaml_load(path: Path, errors: list[str], root: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(read_text(path)) or {}
    except Exception as exc:
        errors.append(f"invalid yaml: `{rel(path, root)}`: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"invalid yaml: `{rel(path, root)}` должен содержать mapping")
        return {}
    return data


def parse_frontmatter(path: Path, errors: list[str], root: Path) -> dict[str, Any]:
    text = read_text(path)
    if not text.startswith("---"):
        errors.append(f"missing frontmatter: `{rel(path, root)}`")
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append(f"invalid frontmatter: `{rel(path, root)}`")
        return {}
    try:
        data = yaml.safe_load(parts[1]) or {}
    except Exception as exc:
        errors.append(f"invalid frontmatter yaml: `{rel(path, root)}`: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"invalid frontmatter: `{rel(path, root)}` должен содержать mapping")
        return {}
    return data


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped or stripped in {"[]", "- []"}:
            return []
        return [item.strip() for item in re.split(r"[, ]+", stripped.strip("[]")) if item.strip()]
    return [str(value).strip()]


def checkpoint_path(workspace: Path) -> Path:
    for candidate in [workspace / "logs" / "checkpoint.yaml", workspace / "logs" / "checkpoint.yml"]:
        if candidate.exists():
            return candidate
    return workspace / "logs" / "checkpoint.yaml"


def is_advanced_workspace(workspace: Path) -> bool:
    return (
        checkpoint_path(workspace).exists()
        or (workspace / "logs" / "execution-plan.md").exists()
        or "feature-execution-lite" in read_text(workspace / "README.md")
    )


def has_non_placeholder_section(text: str, heading: str) -> bool:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return False
    for line in match.group(1).splitlines():
        cleaned = line.strip(" -*\t")
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if "{{" in cleaned or "}}" in cleaned:
            continue
        if lowered in {"нет", "none", "не требуется", "not required"}:
            continue
        if "пока не указ" in lowered or "пока не заполн" in lowered:
            continue
        return True
    return False


def validate_decisions(workspace: Path, errors: list[str], root: Path) -> None:
    path = workspace / "decisions.md"
    if not path.exists():
        errors.append(f"missing decisions: `{rel(path, root)}`")
        return
    text = read_text(path)
    for fragment in ["# Decisions Log", "## Записи"]:
        if fragment not in text:
            errors.append(f"invalid decisions: `{rel(path, root)}` не содержит `{fragment}`")


def validate_tasks(workspace: Path, errors: list[str], root: Path) -> dict[str, dict[str, Any]]:
    tasks_dir = workspace / "tasks"
    task_files = sorted(tasks_dir.glob("T-*.md")) if tasks_dir.exists() else []
    if not task_files:
        if not (tasks_dir / "task.template.md").exists():
            errors.append(f"missing tasks: `{rel(tasks_dir, root)}` не содержит `T-*.md` или `task.template.md`")
        return {}

    tasks: dict[str, dict[str, Any]] = {}
    for path in task_files:
        fm = parse_frontmatter(path, errors, root)
        task_id = str(fm.get("task_id") or path.stem).strip()
        tasks[task_id] = {"path": path, "frontmatter": fm}

        status = str(fm.get("status", "")).strip()
        if status not in VALID_STATUSES:
            errors.append(f"invalid task status: `{rel(path, root)}` status должен быть одним из {sorted(VALID_STATUSES)}")

        wave = fm.get("wave")
        if not isinstance(wave, int) or wave < 1:
            errors.append(f"invalid wave: `{rel(path, root)}` должен иметь positive integer `wave`")

        verify = set(normalize_list(fm.get("verify")))
        text = read_text(path)
        has_smoke = has_non_placeholder_section(text, "Verify-smoke")
        has_user = has_non_placeholder_section(text, "Verify-user")
        if "smoke" in verify and not has_smoke:
            errors.append(f"missing verify-smoke: `{rel(path, root)}` frontmatter требует `smoke`, но секция пустая")
        if "user" in verify and not has_user:
            errors.append(f"missing verify-user: `{rel(path, root)}` frontmatter требует `user`, но секция пустая")
        if status == "done" and not (has_smoke or has_user):
            errors.append(f"done without verification: `{rel(path, root)}` закрыта без Verify-smoke или Verify-user")

    for task_id, item in tasks.items():
        path = item["path"]
        fm = item["frontmatter"]
        wave = fm.get("wave")
        for dep in normalize_list(fm.get("depends_on")):
            if dep not in tasks:
                errors.append(f"unknown dependency: `{rel(path, root)}` зависит от `{dep}`, но такой задачи нет")
                continue
            dep_wave = tasks[dep]["frontmatter"].get("wave")
            if isinstance(wave, int) and isinstance(dep_wave, int) and dep_wave >= wave:
                errors.append(
                    f"invalid wave dependency: `{rel(path, root)}` wave={wave} зависит от `{dep}` wave={dep_wave}; "
                    "dependency должна быть в более ранней wave"
                )

    return tasks


def validate_checkpoint(workspace: Path, tasks: dict[str, dict[str, Any]], errors: list[str], root: Path) -> None:
    path = checkpoint_path(workspace)
    if not path.exists():
        errors.append(f"missing checkpoint: `{rel(path, root)}`")
        return
    data = yaml_load(path, errors, root)
    for key in ["schema", "feature_status", "last_completed_wave", "next_wave", "max_review_rounds", "tasks", "final_verification", "boundaries"]:
        if key not in data:
            errors.append(f"invalid checkpoint: `{rel(path, root)}` не содержит `{key}`")
    if data.get("schema") != "feature-execution-lite/v1":
        errors.append(f"invalid checkpoint: `{rel(path, root)}` должен иметь schema `feature-execution-lite/v1`")
    if data.get("max_review_rounds") not in {1, 2, 3}:
        errors.append(f"invalid checkpoint: `{rel(path, root)}` max_review_rounds должен быть 1..3")

    checkpoint_tasks = data.get("tasks") if isinstance(data.get("tasks"), dict) else {}
    for task_id in tasks:
        if task_id not in checkpoint_tasks:
            errors.append(f"checkpoint gap: `{rel(path, root)}` не содержит task `{task_id}`")

    final = data.get("final_verification") if isinstance(data.get("final_verification"), dict) else {}
    feature_status = str(data.get("feature_status", "")).strip()
    if feature_status in DONE_FEATURE_STATUSES:
        if final.get("status") != "passed":
            errors.append(f"done without final verification: `{rel(path, root)}` feature_status={feature_status}, но final_verification.status != passed")
        for task_id, task_data in checkpoint_tasks.items():
            if isinstance(task_data, dict) and task_data.get("status") != "done":
                errors.append(f"done with open task: `{rel(path, root)}` task `{task_id}` status != done")

    boundaries = data.get("boundaries") if isinstance(data.get("boundaries"), dict) else {}
    for key in ["internal_work_remaining", "external_user_action_required", "runtime_backlog"]:
        if key not in boundaries:
            errors.append(f"boundary gap: `{rel(path, root)}` не содержит boundaries.{key}")


def discover_workspaces(root: Path) -> list[Path]:
    out: list[Path] = []
    for base in [root / "template-repo" / "work" / "features", root / "work" / "features"]:
        if not base.exists():
            continue
        for child in sorted(base.iterdir()):
            if child.is_dir() and is_advanced_workspace(child):
                out.append(child)
    return out


def validate_workspace(workspace: Path, require_advanced: bool, errors: list[str], root: Path) -> None:
    if not workspace.exists():
        errors.append(f"workspace not found: `{rel(workspace, root)}`")
        return
    if not require_advanced and not is_advanced_workspace(workspace):
        return
    validate_decisions(workspace, errors, root)
    tasks = validate_tasks(workspace, errors, root)
    validate_checkpoint(workspace, tasks, errors, root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate optional feature-execution-lite artifacts.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root. Defaults to current directory.")
    parser.add_argument("--workspace", action="append", help="Feature workspace to validate. May be passed multiple times.")
    parser.add_argument("--require-advanced", action="store_true", help="Require checkpoint/execution artifacts for provided workspace.")
    parser.add_argument("--skip-template-check", action="store_true", help="Skip factory template structural checks.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []

    if not args.skip_template_check:
        validate_templates(root, errors)

    workspaces = [Path(item).expanduser().resolve() for item in args.workspace or []]
    if not workspaces and not args.workspace:
        workspaces = discover_workspaces(root)
    for workspace in workspaces:
        validate_workspace(workspace, args.require_advanced or bool(args.workspace), errors, root)

    if errors:
        print("FEATURE EXECUTION LITE НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1

    print("FEATURE EXECUTION LITE ВАЛИДЕН")
    if not workspaces:
        print("workspace_audit=skipped (no advanced feature workspaces found)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
