#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


DEFAULT_REGISTRY = "template-repo/template/.chatgpt/task-registry.yaml"
ALLOCATOR = "template-repo/scripts/allocate-task-id.py"
MASTER_ROUTER = "template-repo/scenario-pack/00-master-router.md"
CLASS_LABELS = {
    "task:bug": "bug",
    "task:feature": "feature",
    "task:docs": "docs",
    "task:research": "research",
    "task:audit": "audit",
    "task:release": "release",
    "task:downstream-sync": "downstream_sync",
    "task:curator": "curator",
}


def load_structured_issue(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    elif path.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(text) or {}
    else:
        data = parse_markdown_issue(text)
    if not isinstance(data, dict):
        raise SystemExit("Issue draft должен быть mapping/object")
    return data


def parse_markdown_issue(text: str) -> dict[str, Any]:
    fields: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{2,4}\s+(.+?)\s*$", line)
        if match:
            if current is not None:
                fields[current] = "\n".join(buffer).strip()
            current = match.group(1).strip()
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        fields[current] = "\n".join(buffer).strip()
    return {"fields": fields}


def load_registry(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit("Registry root must be mapping")
    return data


def infer_class(issue: dict[str, Any], explicit: str) -> str:
    if explicit:
        return explicit
    labels = issue.get("labels", [])
    if isinstance(labels, str):
        labels = [item.strip() for item in labels.split(",")]
    if isinstance(labels, list):
        for label in labels:
            task_class = CLASS_LABELS.get(str(label))
            if task_class:
                return task_class
    title = str(issue.get("title") or "")
    lowered = title.lower()
    if "bug" in lowered or "ошиб" in lowered:
        return "bug"
    if "docs" in lowered or "док" in lowered:
        return "docs"
    if "research" in lowered or "исслед" in lowered:
        return "research"
    if "audit" in lowered or "проверк" in lowered:
        return "audit"
    if "release" in lowered or "релиз" in lowered:
        return "release"
    if "downstream" in lowered:
        return "downstream_sync"
    if "curator" in lowered:
        return "curator"
    return "feature"


def issue_field(issue: dict[str, Any], *names: str) -> str:
    direct_names = {name.lower() for name in names}
    for key, value in issue.items():
        if str(key).lower() in direct_names and not isinstance(value, (dict, list)):
            return str(value).strip()
    fields = issue.get("fields", {})
    if isinstance(fields, dict):
        for key, value in fields.items():
            key_lower = str(key).lower()
            if key_lower in direct_names or any(name.lower() in key_lower for name in names):
                return str(value).strip()
    return ""


def derive_goal(issue: dict[str, Any], task_class: str) -> str:
    candidates = [
        "goal",
        "цель",
        "expected result",
        "ожидаемый результат",
        "expected behavior",
        "ожидаемое поведение",
        "question",
        "вопрос",
        "audit scope",
        "scope проверки",
        "problem or sync need",
        "проблема или потребность синхронизации",
        "proposal",
        "предлагаемый reusable artifact",
    ]
    for candidate in candidates:
        value = issue_field(issue, candidate)
        if value:
            return value
    title = str(issue.get("title") or "").strip()
    return title or f"Process GitHub issue as `{task_class}` task."


def source_ref(issue: dict[str, Any], fallback: str) -> str:
    for key in ["html_url", "url", "issue_url", "source_ref", "ref"]:
        value = str(issue.get(key) or "").strip()
        if value:
            return value
    number = str(issue.get("number") or "").strip()
    return f"GitHub issue #{number}" if number else fallback


def ensure_no_secret_like_text(issue: dict[str, Any]) -> None:
    dumped = yaml.safe_dump(issue, allow_unicode=True, sort_keys=False)
    secret_re = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")
    if secret_re.search(dumped) or "-----BEGIN" in dumped:
        raise SystemExit("Issue draft похож на secret-containing input. Сначала отредактируйте данные.")


def run_allocator(args: argparse.Namespace, issue: dict[str, Any], task_class: str, goal: str, ref: str) -> str:
    cmd = [
        sys.executable,
        ALLOCATOR,
        "--registry",
        args.registry,
        "--append-draft",
        "--title",
        str(issue.get("title") or args.title or f"GitHub issue {task_class} task"),
        "--goal",
        goal,
        "--task-class",
        task_class,
        "--priority",
        args.priority,
        "--status",
        args.status,
        "--source-kind",
        "github_issue",
        "--source-ref",
        ref,
        "--next-action",
        args.next_action,
    ]
    if args.no_requires_review:
        cmd.append("--no-requires-review")
    if args.external_user_action:
        cmd.append("--external-user-action")
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    print(result.stdout, end="")
    match = re.search(r"allocated_task_id=([A-Z]+-TASK-\d{4})", result.stdout)
    if not match:
        raise SystemExit("Allocator did not return allocated_task_id")
    return match.group(1)


def append_issue_context(registry_path: Path, task_id: str, issue: dict[str, Any], args: argparse.Namespace) -> None:
    registry = load_registry(registry_path)
    tasks = registry.get("tasks", [])
    if not isinstance(tasks, list):
        raise SystemExit("Registry tasks must be list")
    task = next((item for item in tasks if isinstance(item, dict) and item.get("task_id") == task_id), None)
    if not isinstance(task, dict):
        raise SystemExit(f"Allocated task not found: {task_id}")
    affected_layer = issue_field(issue, "affected_layer", "затронутый слой")
    codex_involvement = issue_field(issue, "codex_involvement", "ожидаемое участие codex")
    evidence = issue_field(issue, "evidence", "context", "контекст", "redacted evidence", "отредактированное evidence")
    if affected_layer:
        task["affected_layer"] = affected_layer
    if codex_involvement:
        task["codex_involvement"] = codex_involvement
    if evidence:
        task["context"] = evidence
    task["artifacts_to_update"] = args.artifacts_to_update or []
    task["verification_commands"] = [
        f"python3 template-repo/scripts/validate-task-registry.py {args.registry}",
        f"python3 template-repo/scripts/task-to-codex-handoff.py --registry {args.registry} --task-id {task_id} --output reports/handoffs/{task_id}-codex-handoff.md",
        f"python3 template-repo/scripts/validate-codex-task-handoff.py reports/handoffs/{task_id}-codex-handoff.md",
    ]
    registry_path.write_text(yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Создает task-registry entry из sanitized GitHub Issue JSON/YAML/Markdown draft. Не обращается к GitHub API."
    )
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--issue-file", required=True, help="JSON/YAML/Markdown draft from GitHub Issue or issue form.")
    parser.add_argument("--task-class", default="", help="Override task class.")
    parser.add_argument("--title", default="")
    parser.add_argument("--priority", default="medium")
    parser.add_argument("--status", default="needs_triage")
    parser.add_argument("--next-action", default="Triage issue, complete route fields, then generate Codex handoff.")
    parser.add_argument("--no-requires-review", action="store_true")
    parser.add_argument("--external-user-action", action="store_true")
    parser.add_argument("--artifacts-to-update", action="append", default=[])
    args = parser.parse_args()

    issue_path = Path(args.issue_file)
    issue = load_structured_issue(issue_path)
    if args.title and not issue.get("title"):
        issue["title"] = args.title
    ensure_no_secret_like_text(issue)
    task_class = infer_class(issue, args.task_class)
    goal = derive_goal(issue, task_class)
    ref = source_ref(issue, issue_path.as_posix())
    task_id = run_allocator(args, issue, task_class, goal, ref)
    append_issue_context(Path(args.registry), task_id, issue, args)
    print(f"issue_to_task_bridge=ok task_id={task_id}")
    print(f"next_handoff_command=python3 template-repo/scripts/task-to-codex-handoff.py --registry {args.registry} --task-id {task_id} --output reports/handoffs/{task_id}-codex-handoff.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
