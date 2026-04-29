#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "handoff-implementation-register/v1"
TERMINAL_STATUSES = {"verified", "not_applicable", "archived"}
EVIDENCE_REQUIRED_STATUSES = {"implemented", "verified", "not_applicable", "archived"}
ACTIVE_STATUSES = {"captured", "handoff_issued", "self_handoff_created", "queued", "ready", "in_progress", "blocked"}
DEFAULT_ALLOWED_STATUSES = {
    "captured",
    "handoff_issued",
    "self_handoff_created",
    "queued",
    "ready",
    "in_progress",
    "implemented",
    "verified",
    "blocked",
    "not_applicable",
    "archived",
}
PRIORITIES = ["low", "medium", "high", "critical"]
SOURCE_TYPES = {"chatgpt-handoff", "codex-self-handoff", "self-handoff", "direct-task", "manual-entry"}
TASK_CLASSES = {"quick", "build", "deep", "review", "small-fix", "feature", "refactor", "migration"}
OWNER_BOUNDARIES = {
    "internal-repo-follow-up",
    "external-user-action",
    "runtime-action",
    "downstream-battle-action",
    "model-mapping-blocker",
    "secret-boundary-blocker",
}
SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def status_of(item: dict[str, Any]) -> str:
    return str(item.get("status") or "").strip()


def priority_index(priority: str) -> int:
    try:
        return PRIORITIES.index(priority)
    except ValueError:
        return PRIORITIES.index("medium")


def priority_at(index: int) -> str:
    return PRIORITIES[max(0, min(index, len(PRIORITIES) - 1))]


def has_evidence(item: dict[str, Any]) -> bool:
    evidence = item.get("evidence")
    if isinstance(evidence, list) and any(str(entry).strip() for entry in evidence):
        return True
    if isinstance(evidence, str) and evidence.strip():
        return True
    return False


def has_accepted_reason(item: dict[str, Any]) -> bool:
    return bool(str(item.get("accepted_reason") or item.get("closeout_reason") or "").strip())


def is_terminal(item: dict[str, Any]) -> bool:
    return status_of(item) in TERMINAL_STATUSES


def item_map(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("id")): item for item in items if str(item.get("id") or "").strip()}


def normalized_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    raw_items = data.get("items", [])
    return [item for item in raw_items if isinstance(item, dict)] if isinstance(raw_items, list) else []


def blocker_count(item: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> int:
    item_id = str(item.get("id") or "")
    blocked_ids: set[str] = set()
    for blocked_id in item.get("blocks", []) or []:
        target = by_id.get(str(blocked_id))
        if target and not is_terminal(target):
            blocked_ids.add(str(blocked_id))
    for other_id, other in by_id.items():
        if item_id in {str(dep) for dep in other.get("depends_on", []) or []} and not is_terminal(other):
            blocked_ids.add(other_id)
    return len(blocked_ids)


def calculated_priority(item: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> str:
    base = priority_index(str(item.get("priority") or "medium"))
    count = blocker_count(item, by_id)
    if count >= 1:
        base += 1
    if count >= 2:
        base += 1
    return priority_at(base)


def unresolved_dependencies(item: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> list[str]:
    unresolved: list[str] = []
    for dep_id in item.get("depends_on", []) or []:
        dependency = by_id.get(str(dep_id))
        if dependency and not is_terminal(dependency):
            unresolved.append(str(dep_id))
    return unresolved


def effective_status(item: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> str:
    if status_of(item) in TERMINAL_STATUSES:
        return status_of(item)
    if unresolved_dependencies(item, by_id):
        return "blocked"
    return status_of(item) or "captured"


def parse_dt(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        normalized = text.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def is_stale(item: dict[str, Any], *, now: datetime | None = None, max_age_days: int = 14) -> bool:
    if status_of(item) in TERMINAL_STATUSES:
        return False
    if not has_evidence(item):
        return True
    updated = parse_dt(item.get("updated_at"))
    if updated is None:
        return True
    current = now or datetime.now(timezone.utc)
    return (current - updated).days > max_age_days


def sorted_queue_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = item_map(items)
    return sorted(
        items,
        key=lambda item: (
            -priority_index(calculated_priority(item, by_id)),
            -blocker_count(item, by_id),
            str(item.get("id") or ""),
        ),
    )

