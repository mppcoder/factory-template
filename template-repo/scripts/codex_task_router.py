#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from factory_automation_common import now_utc, read_text, read_yaml, write_yaml
from codex_model_catalog import configured_profiles, configured_task_classes, load_model_routing


HANDOFF_CHAIN = ["chatgpt_handoff", "codex_accepted", "codex_completed"]
SELF_HANDOFF_CHAIN = ["codex_self_handoff", "codex_accepted", "codex_completed"]
DEFAULT_CHAT_KINDS = ["handoff", "self_handoff", "bug", "decision", "research", "completion_followup"]
DEFAULT_CHAT_STATES = [
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
DEFAULT_CHAT_ALLOCATION_POLICY = {
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


def load_routing_spec(root: Path) -> dict:
    spec_path = root / "codex-routing.yaml"
    if not spec_path.exists():
        fallback = root / "template-repo" / "codex-routing.yaml"
        if fallback.exists():
            spec_path = fallback
    data = yaml.safe_load(spec_path.read_text(encoding="utf-8")) if spec_path.exists() else {}
    spec = data if isinstance(data, dict) else {}
    model_routing, _path = load_model_routing(root)
    if model_routing:
        merged_profiles = spec.get("profiles", {}) if isinstance(spec.get("profiles", {}), dict) else {}
        for name, profile in configured_profiles(model_routing, spec).items():
            base = dict(merged_profiles.get(name, {}))
            base["model"] = profile.get("model", base.get("model", ""))
            base["reasoning_effort"] = profile.get("reasoning_effort", base.get("reasoning_effort", ""))
            base["plan_mode_reasoning_effort"] = profile.get(
                "plan_mode_reasoning_effort",
                base.get("plan_mode_reasoning_effort", ""),
            )
            merged_profiles[name] = base
        spec["profiles"] = merged_profiles

        task_routes = configured_task_classes(model_routing, spec)
        task_classes = spec.get("task_classes", {}) if isinstance(spec.get("task_classes", {}), dict) else {}
        for task_class, profile_name in task_routes.items():
            meta = dict(task_classes.get(task_class, {}))
            meta["profile"] = profile_name
            task_classes[task_class] = meta
        spec["task_classes"] = task_classes
        spec["model_catalog_status"] = (model_routing.get("model_catalog", {}) or {}).get(
            "catalog_check_status",
            "unknown",
        )
        spec["model_catalog_last_checked_utc"] = (model_routing.get("model_catalog", {}) or {}).get(
            "last_checked_utc",
            "",
        )
    return spec


def read_task_text(task_file: Path | None, task_text: str | None) -> str:
    if task_text and task_text.strip():
        return task_text.strip()
    if task_file and task_file.exists():
        return task_file.read_text(encoding="utf-8", errors="ignore").strip()
    return ""


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def parse_structured_handoff(text: str) -> dict:
    if not text.strip():
        return {}
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        data = None
    if isinstance(data, dict):
        return data

    yaml_block: list[str] = []
    in_block = False
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped and not in_block:
            continue
        if stripped.startswith("#") and not in_block:
            continue
        if stripped.startswith("## ") and in_block:
            break
        looks_like_mapping = ":" in line and not stripped.startswith("```")
        looks_like_list_item = bool(yaml_block) and (line.startswith("  - ") or line.startswith("- "))
        if looks_like_mapping or looks_like_list_item or (yaml_block and line.startswith(" ")):
            yaml_block.append(line)
            in_block = True
            continue
        if in_block:
            break
    if yaml_block:
        try:
            data = yaml.safe_load("\n".join(yaml_block))
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict):
            return data

    result: dict[str, object] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        result[key] = value
    return result


def normalize_model_name(model: str) -> str:
    normalized = _normalize(model)
    if "gpt-5.5" in normalized:
        return "gpt-5.5"
    if "gpt-5.4-mini" in normalized:
        return "gpt-5.4-mini"
    if "gpt-5.4" in normalized:
        return "gpt-5.4"
    return normalized


def stringify_override(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value).strip()


def stringify_yes_no_override(value: object) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    text = stringify_override(value)
    lowered = _normalize(text)
    if lowered in {"true", "yes"}:
        return "yes"
    if lowered in {"false", "no"}:
        return "no"
    return text


def slugify_chat_task(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "task"


def default_chat_index_path(root: Path) -> Path:
    direct = root / ".chatgpt" / "chat-handoff-index.yaml"
    if direct.exists() or (root / ".chatgpt").exists():
        return direct
    return root / "template-repo" / "template" / ".chatgpt" / "chat-handoff-index.yaml"


def default_codex_work_index_path(root: Path) -> Path:
    direct = root / ".chatgpt" / "codex-work-index.yaml"
    if direct.exists() or (root / ".chatgpt").exists():
        return direct
    return root / "template-repo" / "template" / ".chatgpt" / "codex-work-index.yaml"


def ensure_chat_index(data: dict[str, Any], project_code: str) -> dict[str, Any]:
    if not data:
        data = {}
    data.setdefault("schema", "chat-handoff-index/v1")
    data.setdefault("project_code", project_code)
    data.setdefault("next_chat_number", 1)
    data.setdefault(
        "title_policy",
        {
            "canonical_format": "<PROJECT_CODE>-CH-<NNNN> <task-slug>",
            "include_status_in_title": False,
            "include_kind_in_title": False,
            "title_is_stable": True,
            "status_source_of_truth": ".chatgpt/chat-handoff-index.yaml",
            "manual_rename_required_on_status_change": False,
        },
    )
    data.setdefault(
        "allocation_policy",
        dict(DEFAULT_CHAT_ALLOCATION_POLICY),
    )
    allocation_policy = data.get("allocation_policy")
    if isinstance(allocation_policy, dict):
        for key, value in DEFAULT_CHAT_ALLOCATION_POLICY.items():
            allocation_policy.setdefault(key, value)
    data.setdefault("allowed_kinds", DEFAULT_CHAT_KINDS)
    data.setdefault("allowed_states", DEFAULT_CHAT_STATES)
    data.setdefault("items", [])
    return data


def ensure_codex_work_index(data: dict[str, Any], project_code: str) -> dict[str, Any]:
    if not data:
        data = {}
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
    data.setdefault("allowed_kinds", ["self_handoff", "direct_task", "remediation", "validation_followup"])
    data.setdefault("allowed_states", DEFAULT_CHAT_STATES)
    data.setdefault("items", [])
    return data


def project_code_from_root(root: Path) -> str:
    index = read_yaml(default_chat_index_path(root))
    configured = str(index.get("project_code") or "").strip()
    if configured:
        return configured
    letters = "".join(part[:1] for part in re.split(r"[^A-Za-z0-9]+", root.name) if part)
    return (letters or "PRJ").upper()[:6]


def chat_identity_overrides(task_text: str) -> dict[str, str]:
    data = parse_structured_handoff(task_text)
    if not isinstance(data, dict):
        return {}
    result: dict[str, str] = {}
    for key in [
        "chat_id",
        "chat_title",
        "task_slug",
        "chat_kind",
        "chat_state",
        "codex_work_id",
        "codex_work_title",
        "codex_work_state",
    ]:
        value = data.get(key)
        if value not in (None, ""):
            result[key] = str(value)
    return result


def allocate_chat_identity(root: Path, record: dict, task_text: str) -> dict:
    launch = record.get("launch", {})
    overrides = chat_identity_overrides(task_text)
    if launch.get("launch_source") == "direct-task":
        if overrides.get("codex_work_id"):
            launch["codex_work_id"] = overrides.get("codex_work_id", "")
            launch["codex_work_title"] = overrides.get("codex_work_title", "")
            launch["task_slug"] = overrides.get("task_slug", "")
            launch["codex_work_kind"] = "self_handoff"
            launch["codex_work_state"] = overrides.get("codex_work_state", "open")
            launch["codex_work_index_path"] = ".chatgpt/codex-work-index.yaml"
            return record
        work_index_path = default_codex_work_index_path(root)
        data = ensure_codex_work_index(read_yaml(work_index_path), project_code_from_root(root))
        next_number = int(data.get("next_codex_work_number") or 1)
        project_code = str(data.get("project_code") or project_code_from_root(root))
        task_slug = slugify_chat_task(str(launch.get("task_summary") or task_text.splitlines()[0] if task_text.strip() else "task"))
        work_id = f"{project_code}-CX-{next_number:04d}"
        work_title = f"{work_id} {task_slug}"
        now = now_utc().replace("+00:00", "Z")
        item = {
            "codex_work_id": work_id,
            "work_number": next_number,
            "work_title": work_title,
            "task_slug": task_slug,
            "kind": "self_handoff",
            "state": "open",
            "created_utc": now,
            "updated_utc": now,
            "source_type": "direct-task",
            "handoff_group": task_slug,
            "handoff_revision": 1,
            "handoff_register_item_id": "",
            "status_chain": SELF_HANDOFF_CHAIN,
            "evidence": ["Allocated during direct-task bootstrap before first substantive response."],
            "next_action": "Use this Codex work id in the self-handoff; do not consume ChatGPT chat numbers.",
        }
        data.setdefault("items", []).append(item)
        data["next_codex_work_number"] = next_number + 1
        write_yaml(work_index_path, data)
        launch["codex_work_id"] = work_id
        launch["codex_work_title"] = work_title
        launch["task_slug"] = task_slug
        launch["codex_work_kind"] = "self_handoff"
        launch["codex_work_state"] = "open"
        launch["codex_work_index_path"] = str(work_index_path.relative_to(root)) if work_index_path.is_relative_to(root) else str(work_index_path)
        return record
    if overrides.get("chat_id"):
        launch["chat_id"] = overrides.get("chat_id", "")
        launch["chat_title"] = overrides.get("chat_title", "")
        launch["task_slug"] = overrides.get("task_slug", "")
        launch["chat_kind"] = overrides.get("chat_kind", "handoff")
        launch["chat_state"] = overrides.get("chat_state", "open")
        launch["chat_index_path"] = ".chatgpt/chat-handoff-index.yaml"
        return record

    kind = "handoff"
    state = "open"
    index_path = default_chat_index_path(root)
    data = ensure_chat_index(read_yaml(index_path), project_code_from_root(root))
    next_number = int(data.get("next_chat_number") or 1)
    project_code = str(data.get("project_code") or project_code_from_root(root))
    task_slug = slugify_chat_task(str(launch.get("task_summary") or task_text.splitlines()[0] if task_text.strip() else "task"))
    chat_id = f"{project_code}-CH-{next_number:04d}"
    chat_title = f"{chat_id} {task_slug}"
    now = now_utc().replace("+00:00", "Z")
    item = {
        "chat_id": chat_id,
        "chat_number": next_number,
        "chat_title": chat_title,
        "task_slug": task_slug,
        "kind": kind,
        "state": state,
        "created_utc": now,
        "updated_utc": now,
        "source_type": str(launch.get("launch_source") or "direct-task"),
        "handoff_group": task_slug,
        "handoff_revision": 1,
        "handoff_register_item_id": "",
        "status_chain": SELF_HANDOFF_CHAIN if kind == "self_handoff" else HANDOFF_CHAIN,
        "evidence": [f"Allocated during {launch.get('launch_source')} bootstrap before first substantive response."],
        "next_action": "Use this stable id/title in the handoff; if Codex is not launched, keep or close/supersede this repo reservation without reusing the number.",
    }
    data.setdefault("items", []).append(item)
    data["next_chat_number"] = next_number + 1
    write_yaml(index_path, data)
    launch["chat_id"] = chat_id
    launch["chat_title"] = chat_title
    launch["task_slug"] = task_slug
    launch["chat_kind"] = kind
    launch["chat_state"] = state
    launch["chat_index_path"] = str(index_path.relative_to(root)) if index_path.is_relative_to(root) else str(index_path)
    return record


def explicit_routing_overrides(text: str) -> dict:
    data = parse_structured_handoff(text)
    if not isinstance(data, dict):
        return {}
    overrides: dict[str, object] = {}
    for key in [
        "task_class",
        "selected_profile",
        "selected_model",
        "selected_reasoning_effort",
        "selected_plan_mode_reasoning_effort",
        "apply_mode",
        "strict_launch_mode",
        "project_profile",
        "selected_scenario",
        "pipeline_stage",
        "artifacts_to_update",
        "handoff_allowed",
        "defect_capture_path",
        "handoff_shape",
    ]:
        value = data.get(key)
        if value not in (None, "", []):
            overrides[key] = value
    return overrides


def infer_task_class(spec: dict, text: str, explicit_task_class: str | None = None) -> tuple[str, list[str]]:
    task_classes = spec.get("task_classes", {})
    default_task_class = spec.get("defaults", {}).get("task_class", "build")
    if explicit_task_class:
        if explicit_task_class not in task_classes:
            raise ValueError(f"Неизвестный task class: {explicit_task_class}")
        return explicit_task_class, [f"явный override task_class: {explicit_task_class}"]

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
        return default_task_class, [f"keyword-hit не найден; fallback на default task class `{default_task_class}`"]

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    chosen, _score = ordered[0]
    return chosen, [f"keyword-hit: {hit}" for hit in reasons.get(chosen, [])]


def selected_profile(spec: dict, task_class: str) -> tuple[str, dict]:
    task_meta = (spec.get("task_classes", {}) or {}).get(task_class, {})
    profile_name = task_meta.get("profile", task_class)
    profile = (spec.get("profiles", {}) or {}).get(profile_name, {})
    if not profile:
        raise ValueError(f"Для task class `{task_class}` не найден profile `{profile_name}`")
    return profile_name, profile


def choose_profile_from_overrides(spec: dict, task_class: str, overrides: dict) -> tuple[str, dict, list[str]] | None:
    profiles = spec.get("profiles", {}) or {}
    requested_profile = str(overrides.get("selected_profile") or "").strip()
    if requested_profile and requested_profile in profiles:
        return requested_profile, profiles[requested_profile], [f"явный override selected_profile: {requested_profile}"]

    requested_model = normalize_model_name(str(overrides.get("selected_model") or "").strip())
    requested_reasoning = _normalize(str(overrides.get("selected_reasoning_effort") or "").strip())
    requested_plan_reasoning = _normalize(str(overrides.get("selected_plan_mode_reasoning_effort") or "").strip())
    candidates: list[tuple[str, dict]] = []
    for name, profile in profiles.items():
        profile_model = normalize_model_name(str(profile.get("model", "")))
        profile_reasoning = _normalize(str(profile.get("reasoning_effort", "")))
        profile_plan_reasoning = _normalize(str(profile.get("plan_mode_reasoning_effort", "")))
        if requested_model and requested_model != profile_model:
            continue
        if requested_reasoning and requested_reasoning != profile_reasoning:
            continue
        if requested_plan_reasoning and requested_plan_reasoning != profile_plan_reasoning:
            continue
        candidates.append((name, profile))

    if not candidates:
        return None

    task_meta = (spec.get("task_classes", {}) or {}).get(task_class, {})
    default_profile_name = str(task_meta.get("profile", task_class))
    for name, profile in candidates:
        if name == default_profile_name:
            reasons = [
                f"явный reasoning/model override совпал с default profile: {name}",
            ]
            return name, profile, reasons

    preferred_order = ["deep", "review", "build", "quick"]
    for preferred in preferred_order:
        for name, profile in candidates:
            if name == preferred:
                reasons = [f"явный reasoning/model override выбрал совместимый profile: {name}"]
                if requested_profile and requested_profile not in profiles:
                    reasons.append(f"requested profile `{requested_profile}` отсутствует как executable profile в routing spec")
                return name, profile, reasons

    name, profile = candidates[0]
    reasons = [f"явный reasoning/model override выбрал совместимый profile: {name}"]
    if requested_profile and requested_profile not in profiles:
        reasons.append(f"requested profile `{requested_profile}` отсутствует как executable profile в routing spec")
    return name, profile, reasons


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


def launch_artifact_path(launch_source: str) -> str:
    if launch_source == "direct-task":
        return ".chatgpt/direct-task-source.md"
    return ".chatgpt/codex-input.md"


def repo_launch_command(launch_source: str, artifact_path: str) -> str:
    return (
        f"./scripts/launch-codex-task.sh --launch-source {launch_source} "
        f"--task-file {artifact_path} --execute"
    )


def codex_profile_command(profile_name: str) -> str:
    return f"codex --profile {profile_name}"


def infer_handoff_shape(spec: dict, text: str, explicit_shape: str | None = None) -> tuple[str, list[str]]:
    allowed = set(((spec.get("routing_contract", {}) or {}).get("handoff_shape", {}) or {}).get("allowed_values", []))
    default_shape = str(((spec.get("routing_contract", {}) or {}).get("handoff_shape", {}) or {}).get("default") or "codex-task-handoff")
    if default_shape not in allowed:
        default_shape = "codex-task-handoff"

    normalized = _normalize(text)
    parent_hard_triggers = [
        ("large or roadmap-like task", ["roadmap", "многоэтап", "большая задача", "large task"]),
        ("independent child subtasks", ["child subtask", "child session", "subtasks", "подзадач", "дочерн"]),
        ("different route requirements", ["different profile", "разных профил", "разные task_class", "разные selected_profile"]),
        ("orchestration cockpit/dashboard", ["cockpit", "dashboard", "parent status tracking"]),
        ("deferred external actions", ["deferred_user_actions", "placeholder_replacements", "external-user-action", "runtime/downstream", "defer-to-final-closeout"]),
        ("explicit parent orchestration request", ["parent handoff", "parent orchestration", "orchestrator", "full orchestration", "оркестр агентов", "оркестра"]),
    ]
    reasons: list[str] = []
    if explicit_shape:
        if explicit_shape not in allowed:
            raise ValueError(f"Неизвестный handoff_shape: {explicit_shape}")
        if explicit_shape != default_shape:
            reasons.append(f"legacy requested handoff_shape `{explicit_shape}` normalized to `{default_shape}`")
        else:
            reasons.append(f"explicit neutral handoff_shape: {explicit_shape}")
    for label, needles in parent_hard_triggers:
        if any(needle in normalized for needle in needles):
            reasons.append(f"orchestration candidate hard trigger: {label}")

    if not reasons:
        reasons.append("default neutral handoff: Codex decides actual execution_mode after analysis")
    else:
        reasons.append("handoff remains neutral; actual orchestration requires Codex to launch child/subagent sessions")
    return default_shape, reasons


def build_launch_record(
    root: Path,
    launch_source: str,
    task_text: str,
    explicit_task_class: str | None = None,
) -> dict:
    spec = load_routing_spec(root)
    overrides = explicit_routing_overrides(task_text)
    requested_task_class = str(overrides.get("task_class") or "").strip()
    task_class_override = explicit_task_class
    if not task_class_override and requested_task_class in (spec.get("task_classes", {}) or {}):
        task_class_override = requested_task_class

    task_class, reasons = infer_task_class(spec, task_text, task_class_override)
    handoff_shape, handoff_shape_reasons = infer_handoff_shape(
        spec,
        task_text,
        stringify_override(overrides.get("handoff_shape")) or None,
    )
    explicit_profile = choose_profile_from_overrides(spec, task_class, overrides)
    if explicit_profile is not None:
        profile_name, profile, profile_reasons = explicit_profile
        reasons.extend(profile_reasons)
    else:
        profile_name, profile = selected_profile(spec, task_class)
    defect_path = detect_defect_path(task_text)
    project_profile = stringify_override(overrides.get("project_profile")) or gather_project_profile(root)
    selected_scenario = stringify_override(overrides.get("selected_scenario")) or gather_selected_scenario(root)
    pipeline_stage = stringify_override(overrides.get("pipeline_stage")) or gather_pipeline_stage(root)
    apply_mode = stringify_override(overrides.get("apply_mode")) or str(
        (spec.get("validation", {}) or {}).get("apply_mode_default", "manual-ui")
    )
    strict_launch_mode = stringify_override(overrides.get("strict_launch_mode")) or str(
        (spec.get("validation", {}) or {}).get("strict_launch_mode_default", "optional")
    )
    artifacts = overrides.get("artifacts_to_update")
    if isinstance(artifacts, list) and artifacts:
        artifacts_list = [str(item) for item in artifacts if str(item).strip()]
    else:
        artifacts_list = artifacts_to_update(spec, root, defect_path)
    handoff_allowed_value = stringify_yes_no_override(overrides.get("handoff_allowed")) or handoff_allowed(root)
    defect_capture_path = stringify_override(overrides.get("defect_capture_path")) or defect_path
    handoff_artifact = launch_artifact_path(launch_source)
    selected_codex_command = codex_profile_command(profile_name)
    selected_launch_command = repo_launch_command(launch_source, handoff_artifact)
    return {
        "launch": {
            "timestamp_utc": now_utc(),
            "launch_unit": spec.get("routing_contract", {}).get("launch_unit", "new-task-launch"),
            "launch_source": launch_source,
            "router_layer": "executable",
            "handoff_shape": handoff_shape,
            "handoff_shape_reasons": handoff_shape_reasons,
            "task_class": task_class,
            "task_class_reasons": reasons,
            "selected_profile": profile_name,
            "selected_model": profile.get("model", ""),
            "selected_reasoning_effort": profile.get("reasoning_effort", ""),
            "selected_plan_mode_reasoning_effort": profile.get("plan_mode_reasoning_effort", ""),
            "apply_mode": apply_mode,
            "strict_launch_mode": strict_launch_mode,
            "project_profile": project_profile,
            "selected_scenario": selected_scenario,
            "pipeline_stage": pipeline_stage,
            "artifacts_to_update": artifacts_list,
            "handoff_allowed": handoff_allowed_value,
            "defect_capture_path": defect_capture_path,
            "task_summary": task_text.splitlines()[0].strip()[:240] if task_text.strip() else "",
            "launch_boundary_rule": spec.get("routing_contract", {}).get("launch_boundary_rule", ""),
            "interactive_default_rule": spec.get("routing_contract", {}).get("interactive_default_rule", ""),
            "executable_switch_rule": spec.get("routing_contract", {}).get("executable_switch_rule", ""),
            "strict_launch_rule": spec.get("routing_contract", {}).get("strict_launch_rule", ""),
            "live_session_fallback_rule": spec.get("routing_contract", {}).get("live_session_fallback_rule", ""),
            "model_expectation_rule": spec.get("routing_contract", {}).get("model_expectation_rule", ""),
            "model_catalog_status": spec.get("model_catalog_status", "unknown"),
            "model_catalog_last_checked_utc": spec.get("model_catalog_last_checked_utc", ""),
            "model_catalog_validation_note": (
                "selected_model взят из repo-configured mapping; live availability требует проверки через `codex debug models`"
                if spec.get("model_catalog_status") != "available"
                else "selected_model совпадает с последним сохраненным snapshot repo catalog; перед внешними обещаниями повторите live catalog check"
            ),
            "advisory_layers": spec.get("routing_contract", {}).get("advisory_layers", []),
            "executable_layers": spec.get("routing_contract", {}).get("executable_layers", []),
            "launch_artifact_path": handoff_artifact,
            "launch_command": selected_launch_command,
            "codex_profile_command": selected_codex_command,
            "strict_launch_use_cases": (spec.get("validation", {}) or {}).get("strict_launch_use_cases", []),
            "troubleshooting": spec.get("validation", {}).get("troubleshooting", []),
            "direct_self_handoff_required": launch_source == "direct-task",
            "direct_self_handoff_completed": False,
            "requested_task_class": requested_task_class or None,
            "requested_handoff_shape": stringify_override(overrides.get("handoff_shape")) or None,
            "requested_selected_profile": stringify_override(overrides.get("selected_profile")) or None,
            "requested_selected_model": stringify_override(overrides.get("selected_model")) or None,
            "requested_selected_reasoning_effort": stringify_override(overrides.get("selected_reasoning_effort")) or None,
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
    handoff_shape_reasons = launch.get("handoff_shape_reasons", [])
    handoff_shape_reason_lines = "\n".join(f"- {item}" for item in handoff_shape_reasons) if handoff_shape_reasons else "- none"
    manual_ui_lines = "\n".join(
        [
            "- Откройте новый чат/окно Codex в VS Code extension.",
            f"- Вручную выберите model `{launch.get('selected_model', '')}` и reasoning `{launch.get('selected_reasoning_effort', '')}` в picker.",
            "- Только после этого вставьте handoff.",
            "- Codex должен отвечать пользователю на русском языке; английский допустим только для technical literal values.",
            "- Уже открытая live session не считается надежным auto-switch boundary.",
        ]
    )
    strict_launch_use_cases = launch.get("strict_launch_use_cases", [])
    strict_launch_lines = "\n".join(f"- {item}" for item in strict_launch_use_cases) if strict_launch_use_cases else "- none"
    troubleshooting = launch.get("troubleshooting", [])
    troubleshooting_lines = "\n".join(f"- {item}" for item in troubleshooting) if troubleshooting else "- none"
    prompt_contract = "\n".join(
        [
            "- GPT-5.5 не считать drop-in replacement для старого prompt stack.",
            "- Начинать с fresh baseline: роль/область ответственности, ожидаемый outcome, success criteria, constraints, output shape и stop rules.",
            "- Сохранять обязательные repo invariants: чтение router, defect-capture, handoff/routing/closeout rules.",
            "- Убирать лишнюю пошаговую процессность, если путь не является обязательным repo invariant.",
            "- Для tool-heavy задач явно задавать evidence requirements, validation commands и fallback/blocker behavior.",
            "- Держать stable rules выше task-specific dynamic content, чтобы prompt caching и повторное использование оставались устойчивыми.",
            "- Не вставлять current date как постоянную model instruction; даты reports/filenames фиксировать как metadata.",
        ]
    )
    return f"""# {title}

## Источник запуска
{launch.get('launch_source', '')}

## Вид handoff
{launch.get('handoff_shape', '')}

## Решение о фактическом execution mode
- owner: Codex после route receipt и анализа task graph.
- allowed modes: `single-session execution` или `orchestrated-child-sessions`.
- closeout обязателен: назвать actual execution mode и `child/subagent count`.
- rule: handoff остается одним `codex-task-handoff`; orchestration candidate signals не равны фактическому запуску child/subagent sessions.

## Стабильная identity чата и handoff
- chat_id: `{launch.get('chat_id', '')}`
- chat_title: `{launch.get('chat_title', '')}`
- task_slug: `{launch.get('task_slug', '')}`
- kind: `{launch.get('chat_kind', '')}`
- state: `{launch.get('chat_state', '')}`
- source_of_truth: `{launch.get('chat_index_path', '.chatgpt/chat-handoff-index.yaml')}`
- rule: номер выделяется из общего repo counter до первого substantive ответа; status/kind не добавляются в title.

## Evidence для вида handoff
{handoff_shape_reason_lines}

## Класс задачи
{launch.get('task_class', '')}

## Evidence для класса задачи
{reason_lines}

## Выбранный профиль
{launch.get('selected_profile', '')}

## Выбранная модель
{launch.get('selected_model', '')}

## Выбранное reasoning effort
{launch.get('selected_reasoning_effort', '')}

## Выбранное reasoning effort для plan mode
{launch.get('selected_plan_mode_reasoning_effort', '')}

## Режим применения
{launch.get('apply_mode', '')}

## Ручное применение через UI
{manual_ui_lines}

## Язык ответа Codex
Русский. Английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Строгий режим запуска
{launch.get('strict_launch_mode', '')}

## Профиль проекта
{launch.get('project_profile', '')}

## Выбранный сценарий
{launch.get('selected_scenario', '')}

## Этап pipeline
{launch.get('pipeline_stage', '')}

## Артефакты для обновления
{artifacts_lines}

## Разрешение handoff
{launch.get('handoff_allowed', '')}

## Маршрут defect-capture
{launch.get('defect_capture_path', '')}

## Правило launch boundary
{launch.get('launch_boundary_rule', '')}

## Правило интерактивного режима по умолчанию
{launch.get('interactive_default_rule', '')}

## Правило executable switch
{launch.get('executable_switch_rule', '')}

## Правило строгого запуска
{launch.get('strict_launch_rule', '')}

## Правило fallback для live session
{launch.get('live_session_fallback_rule', '')}

## Правило ожиданий по модели
{launch.get('model_expectation_rule', '')}

## Статус catalog check
{launch.get('model_catalog_status', '')}

## Последняя catalog check UTC
{launch.get('model_catalog_last_checked_utc', '')}

## Примечание по live availability
{launch.get('model_catalog_validation_note', '')}

## Базовый prompt contract для GPT-5.5
{prompt_contract}

## Путь launch artifact
`{launch.get('launch_artifact_path', '')}`

## Опциональная команда строгого запуска
`{launch.get('launch_command', '')}`

## Сценарии для строгого запуска
{strict_launch_lines}

## Прямая команда Codex за launcher
`{launch.get('codex_profile_command', '')}`

## Диагностика проблем
{troubleshooting_lines}

## Текст задачи
{task_text.strip() or '-'}"""


def render_direct_task_response(record: dict, task_text: str) -> str:
    launch = record.get("launch", {})
    artifacts = launch.get("artifacts_to_update", [])
    artifacts_lines = "\n".join(f"- {item}" for item in artifacts) if artifacts else "- none"
    compatibility_markers = "\n".join(
        [
            "- `## Self-handoff для прямой задачи`",
            "- `## Классификация`",
            "- `## Выбранный профиль проекта`",
            "- `## Выбранный сценарий`",
            "- `## Текущий этап pipeline`",
            "- `## Режим применения`",
            "- `## Ручное применение через UI`",
            "- `## Строгий режим запуска`",
            "- `## Артефакты для обновления`",
            "- `## Разрешение handoff`",
            "- `## Маршрут defect-capture`",
            "- `## Опциональная команда строгого запуска`",
            "- `## Прямая команда Codex за launcher`",
            "- `## Диагностика проблем`",
            "- `## Следующий шаг`",
        ]
    )
    return f"""## Применение в Codex UI

`apply_mode: {launch.get('apply_mode', 'manual-ui')} (default)`.

Для интерактивной работы открой новый чат/окно Codex в VS Code extension, вручную выбери model `{launch.get('selected_model', '')}` и reasoning `{launch.get('selected_reasoning_effort', '')}` в picker, затем вставь один цельный handoff block ниже.

Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же. Advisory layer сам по себе не переключает model/profile/reasoning; надежная единица маршрутизации — новый task launch. Уже открытая live session допустима только как non-canonical fallback без обещаний auto-switch.

## Строгий launch mode (опционально)

Используй launcher-first strict mode только для automation / reproducibility / shell-first запуска:

```bash
{launch.get('launch_command', '')}
```

Прямая команда profile за launcher:

```bash
{launch.get('codex_profile_command', '')}
```

## Handoff в Codex

```text
Язык ответа Codex: русский
Отвечай пользователю по-русски. Английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

Цель:
Выполнить direct-task self-handoff и продолжить работу в этом же task, если текущий live route совпадает с routing ниже. Не завершай ответ только self-handoff block и не требуй ручного продолжения пользователя для внутренней Codex-eligible работы.

Repo rules:
В рамках repo приоритет у repo rules, AGENTS, runbook и policy files репозитория. Общие рабочие инструкции применяются только там, где не противоречат правилам repo и старшим системным ограничениям среды.

Routing:
- launch_source: {launch.get('launch_source', '')}
- handoff_shape: {launch.get('handoff_shape', '')}
- execution_mode_decision_owner: Codex runtime after task graph analysis
- execution_mode_closeout_required: actual execution mode plus child/subagent count
- task_class: {launch.get('task_class', '')}
- selected_profile: {launch.get('selected_profile', '')}
- selected_model: {launch.get('selected_model', '')}
- selected_reasoning_effort: {launch.get('selected_reasoning_effort', '')}
- selected_plan_mode_reasoning_effort: {launch.get('selected_plan_mode_reasoning_effort', '')}
- apply_mode: {launch.get('apply_mode', '')}
- strict_launch_mode: {launch.get('strict_launch_mode', '')}
- project_profile: {launch.get('project_profile', '')}
- selected_scenario: {launch.get('selected_scenario', '')}
- pipeline_stage: {launch.get('pipeline_stage', '')}
- handoff_allowed: {launch.get('handoff_allowed', '')}
- defect_capture_path: {launch.get('defect_capture_path', '')}
- chat_id: {launch.get('chat_id', '')}
- chat_title: {launch.get('chat_title', '')}
- task_slug: {launch.get('task_slug', '')}
- chat_kind: {launch.get('chat_kind', '')}
- chat_state: {launch.get('chat_state', '')}
- chat_index_path: {launch.get('chat_index_path', '')}
- codex_work_id: {launch.get('codex_work_id', '')}
- codex_work_title: {launch.get('codex_work_title', '')}
- codex_work_kind: {launch.get('codex_work_kind', '')}
- codex_work_state: {launch.get('codex_work_state', '')}
- codex_work_index_path: {launch.get('codex_work_index_path', '')}

Артефакты для обновления:
{artifacts_lines}

Текст задачи:
{task_text.strip() or '-'}

Continuation rule:
Если задача пришла в уже открытую Codex-сессию и этот route совместим с текущей сессией, после видимого self-handoff продолжай remediation / implementation / verification без отдельного запроса пользователя. Остановка допустима только при реальном blocker, внешнем действии, несовместимом route или необходимости нового task launch.

Completion rule:
Перед финальным ответом сгенерируй compact project card командой `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout` и вставь ее в раздел `Карточка проекта`. Карточка должна содержать строки `Модули:` и `В работе:`. Если в конце остается следующий пользовательский или внешний шаг, финальный ответ обязан завершаться разделом `## Инструкция пользователю`. Если внешних действий нет, финальный ответ обязан явно сказать: `Внешних действий не требуется.` и добавить continuation outcome: `Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.`
```

## Совместимость validator

Этот раздел фиксирует legacy-маркеры direct-task response без создания второго handoff-блока:

{compatibility_markers}"""


def write_markdown(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path
