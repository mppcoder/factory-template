#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import yaml

from factory_automation_common import now_utc, read_text, read_yaml, write_yaml


def load_routing_spec(root: Path) -> dict:
    spec_path = root / "codex-routing.yaml"
    data = yaml.safe_load(spec_path.read_text(encoding="utf-8")) if spec_path.exists() else {}
    return data if isinstance(data, dict) else {}


def read_task_text(task_file: Path | None, task_text: str | None) -> str:
    if task_text and task_text.strip():
        return task_text.strip()
    if task_file and task_file.exists():
        return task_file.read_text(encoding="utf-8", errors="ignore").strip()
    return ""


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def infer_task_class(spec: dict, text: str, explicit_task_class: str | None = None) -> tuple[str, list[str]]:
    task_classes = spec.get("task_classes", {})
    default_task_class = spec.get("defaults", {}).get("task_class", "build")
    if explicit_task_class:
        if explicit_task_class not in task_classes:
            raise ValueError(f"Неизвестный task class: {explicit_task_class}")
        return explicit_task_class, [f"explicit task class override: {explicit_task_class}"]

    normalized = _normalize(text)
    scores: dict[str, int] = {}
    reasons: dict[str, list[str]] = {}
    for task_class, meta in task_classes.items():
        score = 0
        hits: list[str] = []
        for keyword in meta.get("keywords", []):
            token = _normalize(str(keyword))
            if token and token in normalized:
                score += len(token.split()) + 1
                hits.append(keyword)
        if score:
            scores[task_class] = score
            reasons[task_class] = hits

    if not scores:
        return default_task_class, [f"no keyword hit; fallback to default task class `{default_task_class}`"]

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    chosen, _score = ordered[0]
    return chosen, [f"keyword hit: {hit}" for hit in reasons.get(chosen, [])]


def selected_profile(spec: dict, task_class: str) -> tuple[str, dict]:
    task_meta = (spec.get("task_classes", {}) or {}).get(task_class, {})
    profile_name = task_meta.get("profile", task_class)
    profile = (spec.get("profiles", {}) or {}).get(profile_name, {})
    if not profile:
        raise ValueError(f"Для task class `{task_class}` не найден profile `{profile_name}`")
    return profile_name, profile


def detect_defect_path(text: str) -> str:
    normalized = _normalize(text)
    if re.search(r"\bbug\b|defect|regression|gap|unexpected|broken|ошиб|дефект|регресс|несогласован|инконсист", normalized):
        return "reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation"
    return "not-required-by-text-signal"


def gather_project_profile(root: Path) -> str:
    profile = read_yaml(root / ".chatgpt" / "project-profile.yaml")
    return str(
        profile.get("project_preset")
        or profile.get("project_title")
        or "unknown-project-profile"
    )


def gather_pipeline_stage(root: Path) -> str:
    stage = read_yaml(root / ".chatgpt" / "stage-state.yaml")
    return str((stage.get("stage") or {}).get("current") or "unknown-stage")


def gather_selected_scenario(root: Path) -> str:
    active = read_yaml(root / ".chatgpt" / "active-scenarios.yaml")
    raw = active.get("active_scenarios", active.get("active", []))
    if isinstance(raw, list) and raw:
        return str(raw[0])
    scenario_pack = active.get("scenario_pack", {})
    if isinstance(scenario_pack, dict) and scenario_pack.get("entrypoint"):
        return str(scenario_pack["entrypoint"])
    return "00-master-router.md"


def handoff_allowed(root: Path) -> str:
    stage = read_yaml(root / ".chatgpt" / "stage-state.yaml")
    policy = read_yaml(root / ".chatgpt" / "policy-status.yaml")
    allowed = bool((stage.get("gates") or {}).get("codex_handoff_allowed"))
    handoff_policy = str(policy.get("handoff_policy") or "forbidden")
    if allowed:
        return f"yes ({handoff_policy})"
    return f"no ({handoff_policy})"


def artifacts_to_update(spec: dict, root: Path, defect_path: str) -> list[str]:
    defaults = list(spec.get("defaults", {}).get("artifacts_to_update", []))
    profile = read_yaml(root / ".chatgpt" / "project-profile.yaml")
    for item in profile.get("required_artifacts", []):
        if isinstance(item, str) and item not in defaults:
            defaults.append(item)
    if defect_path != "not-required-by-text-signal":
        for rel in ["reports/bugs/", "reports/factory-feedback/"]:
            if rel not in defaults:
                defaults.append(rel)
    return defaults


def build_launch_record(
    root: Path,
    launch_source: str,
    task_text: str,
    explicit_task_class: str | None = None,
) -> dict:
    spec = load_routing_spec(root)
    task_class, reasons = infer_task_class(spec, task_text, explicit_task_class)
    profile_name, profile = selected_profile(spec, task_class)
    defect_path = detect_defect_path(task_text)
    return {
        "launch": {
            "timestamp_utc": now_utc(),
            "launch_unit": spec.get("routing_contract", {}).get("launch_unit", "new-task-launch"),
            "launch_source": launch_source,
            "router_layer": "executable",
            "task_class": task_class,
            "task_class_reasons": reasons,
            "selected_profile": profile_name,
            "selected_model": profile.get("model", ""),
            "selected_reasoning_effort": profile.get("reasoning_effort", ""),
            "selected_plan_mode_reasoning_effort": profile.get("plan_mode_reasoning_effort", ""),
            "project_profile": gather_project_profile(root),
            "selected_scenario": gather_selected_scenario(root),
            "pipeline_stage": gather_pipeline_stage(root),
            "artifacts_to_update": artifacts_to_update(spec, root, defect_path),
            "handoff_allowed": handoff_allowed(root),
            "defect_capture_path": defect_path,
            "task_summary": task_text.splitlines()[0].strip()[:240] if task_text.strip() else "",
            "launch_boundary_rule": spec.get("routing_contract", {}).get("launch_boundary_rule", ""),
            "advisory_layers": spec.get("routing_contract", {}).get("advisory_layers", []),
            "executable_layers": spec.get("routing_contract", {}).get("executable_layers", []),
            "launch_command": f"codex --profile {profile_name}",
            "direct_self_handoff_required": launch_source == "direct-task",
            "direct_self_handoff_completed": False,
        }
    }


def write_launch_record(root: Path, record: dict) -> Path:
    path = root / ".chatgpt" / "task-launch.yaml"
    write_yaml(path, record)
    return path


def render_normalized_handoff(record: dict, task_text: str, title: str) -> str:
    launch = record.get("launch", {})
    artifacts = launch.get("artifacts_to_update", [])
    artifacts_lines = "\n".join(f"- {item}" for item in artifacts) if artifacts else "- none"
    reasons = launch.get("task_class_reasons", [])
    reason_lines = "\n".join(f"- {item}" for item in reasons) if reasons else "- none"
    return f"""# {title}

## Launch source
{launch.get('launch_source', '')}

## Task class
{launch.get('task_class', '')}

## Task class evidence
{reason_lines}

## Selected profile
{launch.get('selected_profile', '')}

## Selected model
{launch.get('selected_model', '')}

## Selected reasoning effort
{launch.get('selected_reasoning_effort', '')}

## Selected plan mode reasoning
{launch.get('selected_plan_mode_reasoning_effort', '')}

## Project profile
{launch.get('project_profile', '')}

## Selected scenario
{launch.get('selected_scenario', '')}

## Pipeline stage
{launch.get('pipeline_stage', '')}

## Artifacts to update
{artifacts_lines}

## Handoff allowed
{launch.get('handoff_allowed', '')}

## Defect capture path
{launch.get('defect_capture_path', '')}

## Launch boundary rule
{launch.get('launch_boundary_rule', '')}

## Executable launch command
`{launch.get('launch_command', '')}`

## Task payload
{task_text.strip() or '-'}"""


def write_markdown(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path
