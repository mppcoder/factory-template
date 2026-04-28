#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def load_routing(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    return load_yaml(root / "template-repo" / "codex-routing.yaml"), load_yaml(root / "template-repo" / "codex-model-routing.yaml")


def match_task_class(text: str, routing: dict[str, Any], explicit: str | None) -> tuple[str, list[str]]:
    task_classes = routing.get("task_classes", {}) or {}
    if explicit:
        return explicit, ["explicit task_class field"]
    lowered = text.lower()
    matches: list[tuple[str, str]] = []
    for task_class, spec in task_classes.items():
        for keyword in spec.get("keywords", []) or []:
            kw = str(keyword).lower()
            if kw and kw in lowered:
                matches.append((str(task_class), str(keyword)))
    if matches:
        priority = ["review", "deep", "build", "quick"]
        for candidate in priority:
            hit = [kw for cls, kw in matches if cls == candidate]
            if hit:
                return candidate, [f"keyword `{item}`" for item in hit[:5]]
    default_class = str((routing.get("defaults", {}) or {}).get("task_class") or "build")
    return default_class, ["default route"]


def explain(root: Path, task_text: str, explicit_task_class: str | None = None) -> dict[str, Any]:
    routing, model_routing = load_routing(root)
    task_class, evidence = match_task_class(task_text, routing, explicit_task_class)
    task_routes = routing.get("task_classes", {}) or {}
    profile = str((task_routes.get(task_class, {}) or {}).get("profile") or task_class)
    profiles = model_routing.get("profile_routes", {}) or {}
    route = profiles.get(profile, {}) or {}
    catalog = model_routing.get("model_catalog", {}) or {}
    catalog_status = str(catalog.get("catalog_check_status") or "unknown")
    live_boundary = "last catalog validation passed" if catalog_status == "available" else "requires live validation"
    return {
        "task_class": task_class,
        "selected_profile": profile,
        "selected_model": route.get("selected_model", ""),
        "selected_reasoning_effort": route.get("selected_reasoning_effort", ""),
        "selected_plan_mode_reasoning_effort": route.get("selected_plan_mode_reasoning_effort", ""),
        "evidence": evidence,
        "method": "deterministic keyword/rule-based routing; not a semantic classifier",
        "live_catalog_boundary": live_boundary,
        "advisory_boundary": "advisory handoff text does not switch an already-open live session",
    }


def render_markdown(payload: dict[str, Any]) -> str:
    evidence = "\n".join(f"- {item}" for item in payload["evidence"])
    return f"""# Route explanation / объяснение маршрута

## Route receipt / подтверждение маршрута

- task_class: `{payload['task_class']}`
- selected_profile: `{payload['selected_profile']}`
- selected_model: `{payload['selected_model']}`
- selected_reasoning_effort: `{payload['selected_reasoning_effort']}`
- selected_plan_mode_reasoning_effort: `{payload['selected_plan_mode_reasoning_effort']}`

## Evidence / evidence маршрута

{evidence}

## Boundary / граница

- method: {payload['method']}
- live_catalog_boundary: {payload['live_catalog_boundary']}
- advisory_boundary: {payload['advisory_boundary']}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Объясняет deterministic Codex route selection.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--task-text", default="")
    parser.add_argument("--task-class", choices=["quick", "build", "deep", "review"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = explain(Path(args.root).resolve(), args.task_text, args.task_class)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
