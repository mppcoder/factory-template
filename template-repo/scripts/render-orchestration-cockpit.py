#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from factory_automation_common import now_utc
from validate_orchestration_cockpit_import import load_validator


validator = load_validator()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def bullet(items: list[Any], empty: str = "- none") -> str:
    lines: list[str] = []
    for item in items:
        if isinstance(item, dict):
            item_id = item.get("id") or item.get("placeholder") or "item"
            text = item.get("action") or item.get("description") or item.get("reason") or ""
            boundary = item.get("owner_boundary")
            suffix = f" (`{boundary}`)" if boundary else ""
            lines.append(f"- `{item_id}`: {text}{suffix}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines) if lines else empty


def render(data: dict[str, Any]) -> str:
    parent = data.get("parent", {}) if isinstance(data.get("parent"), dict) else {}
    route = data.get("route_receipt", {}) if isinstance(data.get("route_receipt"), dict) else {}
    next_action = data.get("next_action", {}) if isinstance(data.get("next_action"), dict) else {}
    lines = [
        "# Orchestration cockpit lite / лёгкая панель оркестрации",
        "",
        f"Generated UTC: `{now_utc()}`",
        "",
        f"Status: `{parent.get('status', '')}`",
        f"Parent: `{parent.get('id', '')}`",
        f"Title: {parent.get('title', '')}",
        "",
        "## Route receipt / подтверждение маршрута",
        "",
        f"- handoff_shape: `{route.get('handoff_shape', '')}`",
        f"- task_class: `{route.get('task_class', '')}`",
        f"- selected_profile: `{route.get('selected_profile', '')}`",
        f"- selected_model: `{route.get('selected_model', '')}`",
        f"- selected_reasoning_effort: `{route.get('selected_reasoning_effort', '')}`",
        f"- selected_plan_mode_reasoning_effort: `{route.get('selected_plan_mode_reasoning_effort', '')}`",
        f"- explanation: {route.get('route_explanation', '')}",
        "",
        "## Child tasks / дочерние задачи",
        "",
        "| Child | Class | Profile | Model | Reasoning | Status | Boundary |",
        "|---|---|---|---|---|---|---|",
    ]
    for child in data.get("child_tasks", []) or []:
        if not isinstance(child, dict):
            continue
        lines.append(
            f"| `{child.get('id', '')}` | `{child.get('task_class', '')}` | `{child.get('selected_profile', '')}` | "
            f"`{child.get('selected_model', '')}` | `{child.get('selected_reasoning_effort', '')}` | "
            f"`{child.get('status', '')}` | `{child.get('owner_boundary', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Blockers / блокеры",
            "",
            bullet(data.get("blockers", []) or []),
            "",
            "## Deferred user actions / отложенные действия пользователя",
            "",
            bullet(data.get("deferred_user_actions", []) or []),
            "",
            "## Placeholder replacements / замены placeholder",
            "",
            bullet(data.get("placeholder_replacements", []) or []),
            "",
            "## Next action / следующее действие",
            "",
            f"- `{next_action.get('owner_boundary', '')}`: {next_action.get('action', '')}",
            "",
            "## Continuation outcome / итог продолжения",
            "",
            str(data.get("continuation_outcome") or ""),
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Рендерит orchestration-cockpit-lite markdown.")
    parser.add_argument("--input", default="template-repo/template/.chatgpt/orchestration-cockpit.yaml")
    parser.add_argument("--output", default="reports/orchestration/orchestration-cockpit.md")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    data = load_yaml(input_path)
    errors = validator.validate_cockpit(data)
    if errors:
        print("ORCHESTRATION COCKPIT НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render(data), encoding="utf-8")
    print(f"cockpit_report={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
