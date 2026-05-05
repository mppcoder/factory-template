#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


DEFAULT_REGISTRY = "template-repo/template/.chatgpt/task-registry.yaml"
DEFAULT_DASHBOARD = "template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml"
TERMINAL_STATUSES = {"verified", "superseded", "not_applicable", "archived"}
EVIDENCE_REQUIRED_STATUSES = {
    "implemented",
    "verification_pending",
    "human_review",
    "verified",
    "archived",
}
COUNT_STATUSES = [
    "ready_for_handoff",
    "ready_for_codex",
    "codex_running",
    "human_review",
    "blocked",
    "verified",
]
ALLOWED_TRANSITIONS = {
    "draft": {"needs_triage", "ready_for_handoff", "blocked", "superseded", "not_applicable", "archived"},
    "needs_triage": {"draft", "ready_for_handoff", "blocked", "superseded", "not_applicable", "archived"},
    "ready_for_handoff": {"ready_for_codex", "needs_triage", "blocked", "superseded", "not_applicable", "archived"},
    "ready_for_codex": {"codex_running", "ready_for_handoff", "blocked", "superseded", "not_applicable", "archived"},
    "codex_running": {"implemented", "blocked", "human_review", "superseded"},
    "implemented": {"verification_pending", "human_review", "ready_for_codex", "blocked", "superseded", "archived"},
    "verification_pending": {"verified", "human_review", "implemented", "blocked", "superseded", "archived"},
    "human_review": {"verified", "verification_pending", "implemented", "blocked", "superseded", "archived"},
    "blocked": {"needs_triage", "ready_for_handoff", "ready_for_codex", "codex_running", "superseded", "not_applicable", "archived"},
    "verified": {"archived"},
    "superseded": {"archived"},
    "not_applicable": {"archived"},
    "archived": set(),
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        raise SystemExit(f"YAML file not found: {path}")
    except yaml.YAMLError as exc:
        raise SystemExit(f"YAML parse error in {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit(f"YAML root must be mapping: {path}")
    return data


def save_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def find_task(registry: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = registry.get("tasks", [])
    if not isinstance(tasks, list):
        raise SystemExit("registry.tasks должен быть list")
    for task in tasks:
        if isinstance(task, dict) and str(task.get("task_id") or "") == task_id:
            return task
    raise SystemExit(f"TASK НЕ НАЙДЕН: {task_id}")


def allowed_statuses(registry: dict[str, Any]) -> set[str]:
    statuses = registry.get("allowed_statuses", [])
    if not isinstance(statuses, list):
        raise SystemExit("allowed_statuses должен быть list")
    return {str(status) for status in statuses}


def evidence_list(task: dict[str, Any]) -> list[Any]:
    evidence = task.get("evidence")
    if evidence is None:
        task["evidence"] = []
        return task["evidence"]
    if not isinstance(evidence, list):
        raise SystemExit("task.evidence должен быть list для status update")
    return evidence


def status_counts(registry: dict[str, Any]) -> dict[str, int]:
    tasks = registry.get("tasks", [])
    if not isinstance(tasks, list):
        tasks = []
    counts = {status: 0 for status in COUNT_STATUSES}
    counts["open_tasks"] = 0
    for task in tasks:
        if not isinstance(task, dict):
            continue
        status = str(task.get("status") or "")
        if status not in TERMINAL_STATUSES:
            counts["open_tasks"] += 1
        if status in counts:
            counts[status] += 1
    return counts


def sync_dashboard(dashboard_path: Path, registry: dict[str, Any], registry_path: Path, evidence_paths: list[str]) -> None:
    dashboard = load_yaml(dashboard_path)
    control = dashboard.setdefault("universal_task_control", {})
    if not isinstance(control, dict):
        raise SystemExit("dashboard.universal_task_control должен быть mapping")
    counts = status_counts(registry)
    control["status"] = "in_progress" if counts["open_tasks"] else "pending"
    control["registry_path"] = registry_path.as_posix()
    for key, value in counts.items():
        control[key] = value
    control["next_action"] = "Generate or update Codex handoff for the next ready task."
    control["fallback_next_action"] = "Keep task in triage until route, evidence and human boundary are clear."
    evidence = control.setdefault("evidence", [])
    if not isinstance(evidence, list):
        raise SystemExit("dashboard.universal_task_control.evidence должен быть list")
    for path in evidence_paths:
        if path and path not in evidence:
            evidence.append(path)
    save_yaml(dashboard_path, dashboard)


def validate_transition(current: str, target: str, *, force: bool) -> None:
    if current == target:
        raise SystemExit(f"Task уже имеет status `{target}`")
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if target not in allowed and not force:
        allowed_text = ", ".join(sorted(allowed)) or "none"
        raise SystemExit(f"Переход `{current}` -> `{target}` запрещен. Allowed: {allowed_text}. Use --force только с явным reason.")


def apply_update(args: argparse.Namespace, registry: dict[str, Any], task: dict[str, Any]) -> list[str]:
    current = str(task.get("status") or "")
    target = args.status
    if target not in allowed_statuses(registry):
        raise SystemExit(f"status `{target}` не входит в registry.allowed_statuses")
    validate_transition(current, target, force=args.force)
    if not args.reason.strip():
        raise SystemExit("--reason обязателен для status transition")
    if target == "verified" and not args.confirm_verified:
        raise SystemExit("status `verified` требует --confirm-verified")
    evidence_items = list(args.evidence or [])
    if target in EVIDENCE_REQUIRED_STATUSES and not evidence_items and not args.accepted_reason:
        raise SystemExit(f"status `{target}` требует --evidence или --accepted-reason")
    if target == "blocked":
        dependencies = task.setdefault("dependencies", {})
        if not isinstance(dependencies, dict):
            raise SystemExit("task.dependencies должен быть mapping")
        blocked_by = dependencies.setdefault("blocked_by", [])
        if not isinstance(blocked_by, list):
            raise SystemExit("task.dependencies.blocked_by должен быть list")
        if not blocked_by and "block" not in args.reason.lower() and "блок" not in args.reason.lower():
            raise SystemExit("status `blocked` требует dependencies.blocked_by или reason с явным blocker")

    task["status"] = target
    task["last_status_change"] = {
        "from": current,
        "to": target,
        "changed_at_utc": now_utc(),
        "reason": args.reason,
    }
    if args.next_action:
        task["next_action"] = args.next_action
    if args.accepted_reason:
        task["accepted_reason"] = args.accepted_reason
    evidence = evidence_list(task)
    for item in evidence_items:
        if item not in evidence:
            evidence.append(item)
    return [str(item) for item in evidence_items]


def main() -> int:
    parser = argparse.ArgumentParser(description="Безопасно меняет status FT-TASK и при необходимости пересчитывает dashboard counters.")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--dashboard", default=DEFAULT_DASHBOARD)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--next-action", default="")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--accepted-reason", default="")
    parser.add_argument("--sync-dashboard", action="store_true")
    parser.add_argument("--confirm-verified", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--write", action="store_true", help="Без этого флага команда только показывает dry-run.")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    dashboard_path = Path(args.dashboard)
    registry = load_yaml(registry_path)
    task = find_task(registry, args.task_id)
    current = str(task.get("status") or "")

    if not args.write:
        validate_transition(current, args.status, force=args.force)
        print("dry_run=true")
        print(f"task_id={args.task_id}")
        print(f"status_transition={current}->{args.status}")
        print(f"sync_dashboard={args.sync_dashboard}")
        print("Use --write to apply this transition.")
        return 0

    evidence_paths = apply_update(args, registry, task)
    save_yaml(registry_path, registry)
    if args.sync_dashboard:
        sync_dashboard(dashboard_path, registry, registry_path, [registry_path.as_posix(), *evidence_paths])
    print("task_status_updated=true")
    print(f"task_id={args.task_id}")
    print(f"status_transition={current}->{args.status}")
    print(f"registry_updated={registry_path}")
    if args.sync_dashboard:
        print(f"dashboard_updated={dashboard_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
