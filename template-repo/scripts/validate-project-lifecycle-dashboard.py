#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "project-lifecycle-dashboard/v1"
LIFECYCLE_PHASES = {
    "idea",
    "intake",
    "spec",
    "architecture",
    "handoff",
    "execution",
    "verification",
    "release",
    "deploy",
    "operate",
    "improve",
}
STATUSES = {
    "not_started",
    "pending",
    "in_progress",
    "blocked",
    "passed",
    "completed",
    "done",
    "skipped",
    "failed",
    "not_applicable",
    "draft",
    "ready",
    "ready-for-handoff",
    "archived",
}
GREEN_STATUSES = {"passed", "completed", "done", "ready", "archived"}
BEGINNER_STATUSES = {
    "pending",
    "in_progress",
    "blocked",
    "passed",
    "failed",
    "completed",
    "not_applicable",
}
OWNER_BOUNDARIES = {
    "internal-repo-follow-up",
    "external-user-action",
    "runtime-action",
    "downstream-battle-action",
    "model-mapping-blocker",
    "secret-boundary-blocker",
}
VISUAL_SURFACES = {
    "chatgpt-mini-card",
    "codex-execution-card",
    "markdown-dashboard",
}
VISUAL_CARD_FIELDS = {
    "project",
    "lifecycle_chain",
    "module_readiness_chain",
    "active_handoff_lines",
}
CODEX_CARD_SECTIONS = {"route_receipt", "progress", "blockers", "next", "external"}
ORCHESTRATION_PARENT_STATUSES = {
    "not_started",
    "planned",
    "validated",
    "dry-run",
    "executing",
    "completed",
    "blocked",
    "failed",
}
ORCHESTRATION_CHILD_STATUSES = {
    "planned",
    "session-file-written",
    "executed",
    "blocked",
    "skipped",
    "completed",
    "failed",
}
ORCHESTRATION_GREEN_STATUSES = {"executed", "completed", "passed", "done"}
RUNBOOK_PACKAGE_IDS = {
    "01-factory-template",
    "02-greenfield-product",
    "03-brownfield-with-repo-to-greenfield",
    "04-brownfield-without-repo-to-greenfield",
}
DEFAULT_DECISION_MODES = {
    "not_selected",
    "global-defaults",
    "confirm-each-default",
    "manual",
}
RUNBOOK_DEFAULT_DECISION_FIELDS = [
    "default_decision_mode",
    "defaults_count",
    "overrides_count",
    "unresolved_decisions_count",
    "next_decision",
    "readiness_to_generate_handoff",
]
PROJECT_OWNER_BOUNDARIES = {
    "template-owned-generated-project-artifact",
    "factory-template-root",
    "project-owned",
}
CHANGE_CLASSES = {
    "small-fix",
    "feature",
    "refactor",
    "migration",
    "brownfield-audit",
    "brownfield-stabilization",
    "deep",
    "quick",
    "build",
    "review",
}
PRIORITIES = {"low", "medium", "high", "critical"}
REQUIRED_TOP_LEVEL = [
    "project",
    "lifecycle_phase",
    "active_change",
    "stage_gates",
    "multi_step_execution",
    "handoff_orchestration",
    "module_readiness",
    "beginner_visual_surfaces",
    "release_readiness",
    "deploy_runtime",
    "standards_navigator",
    "software_update_governance",
    "post_release_improvement",
    "external_actions_ledger",
    "recommended_next_step",
    "fallback_next_step",
]
SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")
POSITIVE_AUTOSWITCH_RE = re.compile(
    r"(?i)(advisory|handoff|scenario|project instruction).{0,80}(auto[- ]?switch|switches model|switches profile|switches reasoning)"
)
RU_POSITIVE_AUTOSWITCH_RE = re.compile(
    r"(?i)(advisory|handoff|сценари|инструкц|project).{0,100}(автоматически переключает|сам переключает|переключает model|переключает profile|переключает reasoning)"
)
NO_USER_ACTION_RE = re.compile(r"(?i)^\s*(ничего|не требуется|нет|none|not required|no user action required)\s*$")
HEAVY_DEFAULT_UI_RE = re.compile(
    r"(?i)(default|по умолчанию|обязательн).{0,100}(web app|daemon|sqlite|telegram|websocket|live[- ]?refresh|background worker)"
)
SOFTWARE_UPDATE_POLICIES = {"manual-approved-upgrade"}
SOFTWARE_PROPOSAL_STATUSES = {
    "not_started",
    "draft",
    "pending",
    "blocked",
    "ready",
    "approved",
    "rejected",
    "completed",
}
SOFTWARE_BOUNDARIES = {
    "internal-repo-follow-up",
    "external-user-action",
    "runtime-action",
    "downstream-battle-action",
    "secret-boundary-blocker",
}
STANDARDS_PROFILES = {"solo_lightweight", "commercial_production", "custom"}
STANDARDS_GREEN_STATUSES = GREEN_STATUSES
STANDARDS_VERSION_CURRENT = {
    "current_published",
    "current_final",
    "current_stable_release",
    "current_w3c_recommendation",
    "current_dora_guidance",
    "current_practice_baseline",
}
STANDARDS_VERSION_STALE = {"stale", "unknown", "needs_review", "revision_pending", "current_with_revision_pending"}
HANDOFF_IMPLEMENTATION_ARTIFACT = ".chatgpt/handoff-implementation-register.yaml"
CHAT_HANDOFF_INDEX_ARTIFACT = ".chatgpt/chat-handoff-index.yaml"
CHAT_ID_IN_TEXT_RE = re.compile(r"\b([A-Z][A-Z0-9]*-CH-[0-9]{4})\b")
MODULE_STATUSES = {"completed", "passed", "verified", "in_progress", "pending", "blocked", "failed", "not_applicable"}
MODULE_GREEN_STATUSES = {"completed", "passed", "verified"}
REQUIRED_MODULE_IDS = {"lifecycle", "core", "security", "ui_a11y", "quality", "websec", "ops", "ai"}
MODULE_SOURCE_REFS = {
    "active_change",
    "stage_gates",
    "multi_step_execution",
    "final_verification",
    "deploy_runtime",
    "software_update_governance",
}
FALSE_COMPLIANCE_RE = re.compile(r"(?i)\b(certified|certification|compliant|compliance)\b")
UNIVERSAL_TASK_STATUSES = {
    "pending",
    "unknown",
    "in_progress",
    "blocked",
    "passed",
    "completed",
    "verified",
}
UNIVERSAL_TASK_GREEN_STATUSES = {"passed", "completed", "verified"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def load_handoff_implementation_validator():
    script = Path(__file__).resolve().with_name("validate-handoff-implementation-register.py")
    spec = importlib.util.spec_from_file_location("validate_handoff_implementation_register", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Не удалось загрузить validate-handoff-implementation-register.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def resolve_source_artifact(dashboard_path: Path, artifact: str) -> Path | None:
    candidates: list[Path] = []
    artifact_path = Path(artifact)
    if artifact.startswith(".chatgpt/"):
        candidates.append(dashboard_path.parent / artifact.removeprefix(".chatgpt/"))
    candidates.append(dashboard_path.parent / artifact_path)
    for parent in dashboard_path.resolve().parents:
        candidates.append(parent / artifact_path)
        candidates.append(parent / "template-repo" / "template" / artifact_path)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def dashboard_project_root(dashboard_path: Path) -> Path:
    if dashboard_path.parent.name == ".chatgpt":
        return dashboard_path.parent.parent
    return dashboard_path.parent


def validate_generated_project_state_alignment(
    data: dict[str, Any], dashboard_path: Path | None, errors: list[str]
) -> None:
    if dashboard_path is None:
        return
    project = data.get("project", {}) if isinstance(data.get("project"), dict) else {}
    project_slug = str(project.get("slug") or "")
    if "{{" in project_slug or "}}" in project_slug:
        return
    root = dashboard_project_root(dashboard_path)
    chat_dir = root / ".chatgpt"

    active_change = data.get("active_change", {}) if isinstance(data.get("active_change"), dict) else {}
    active_id = str(active_change.get("id") or "")
    chat_match = CHAT_ID_IN_TEXT_RE.search(active_id)
    if chat_match:
        index_path = chat_dir / "chat-handoff-index.yaml"
        if index_path.exists():
            index = load_yaml(index_path)
            known_ids = {
                str(item.get("chat_id") or "")
                for item in index.get("items", [])
                if isinstance(item, dict)
            }
            if chat_match.group(1) not in known_ids:
                errors.append(
                    "generated dashboard active_change ссылается на ChatGPT handoff id, "
                    "которого нет в .chatgpt/chat-handoff-index.yaml"
                )

    stage_path = chat_dir / "stage-state.yaml"
    task_state_path = chat_dir / "task-state.yaml"
    if stage_path.exists() and task_state_path.exists():
        stage = load_yaml(stage_path)
        task_state = load_yaml(task_state_path)
        gates = stage.get("gates", {}) if isinstance(stage.get("gates"), dict) else {}
        if gates.get("done_complete") is True and str(task_state.get("current_state") or "") == "intake":
            errors.append("stage-state done_complete=true несовместим с task-state current_state=intake")


def registry_standard_ids(data: dict[str, Any], dashboard_path: Path | None) -> set[str]:
    standards = data.get("standards_navigator", {}) if isinstance(data.get("standards_navigator"), dict) else {}
    registry_ref = str(standards.get("standards_registry") or "")
    if not dashboard_path or not registry_ref:
        return set()
    registry_path = resolve_source_artifact(dashboard_path, registry_ref)
    if registry_path is None:
        return set()
    registry = load_yaml(registry_path)
    standards_map = registry.get("standards", {})
    if not isinstance(standards_map, dict):
        return set()
    return {str(key) for key in standards_map}


def standards_gate_ids(data: dict[str, Any]) -> set[str]:
    standards = data.get("standards_navigator", {}) if isinstance(data.get("standards_navigator"), dict) else {}
    gates = standards.get("gates", []) if isinstance(standards, dict) else []
    return {str(gate.get("id")) for gate in gates if isinstance(gate, dict) and str(gate.get("id") or "").strip()}


def as_mapping(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"`{key}` должен быть mapping")
        return {}
    return value


def as_list(data: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"`{key}` должен быть list")
        return []
    return value


def has_evidence(item: dict[str, Any]) -> bool:
    evidence = item.get("evidence")
    if isinstance(evidence, list) and evidence:
        return True
    if isinstance(evidence, str) and evidence.strip():
        return True
    reason = item.get("accepted_reason") or item.get("reason")
    return bool(str(reason or "").strip())


def status_of(item: dict[str, Any], default: str = "") -> str:
    return str(item.get("status") or default).strip()


def validate_status(value: str, path: str, errors: list[str]) -> None:
    if value and value not in STATUSES:
        errors.append(f"{path} имеет неизвестный status `{value}`")


def validate_boundary(value: str, path: str, errors: list[str]) -> None:
    if value not in OWNER_BOUNDARIES:
        errors.append(f"{path} должен быть одним из: {', '.join(sorted(OWNER_BOUNDARIES))}")


def validate_green_evidence(item: dict[str, Any], path: str, errors: list[str]) -> None:
    status = status_of(item)
    if status in GREEN_STATUSES and not has_evidence(item):
        errors.append(f"{path} отмечен `{status}`, но не содержит evidence или accepted_reason")


def validate_software_action(item: Any, path: str, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"{path} должен быть mapping")
        return
    boundary = str(item.get("owner_boundary") or "")
    if boundary not in SOFTWARE_BOUNDARIES:
        errors.append(f"{path}.owner_boundary должен быть одним из: {', '.join(sorted(SOFTWARE_BOUNDARIES))}")
    if not str(item.get("action") or "").strip():
        errors.append(f"{path}.action обязателен")
    validate_green_evidence(item, path, errors)


def validate_standards_navigator(item: Any, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append("standards_navigator должен быть mapping")
        return
    profile = str(item.get("selected_profile") or "")
    if profile not in STANDARDS_PROFILES:
        errors.append("standards_navigator.selected_profile должен быть solo_lightweight/commercial_production/custom")
    for field in ["standards_registry", "stage_map", "gates_source", "false_compliance_boundary"]:
        if not str(item.get(field) or "").strip():
            errors.append(f"standards_navigator.{field} обязателен")
    boundary = str(item.get("false_compliance_boundary") or "").lower()
    if "certification" not in boundary and "сертифика" not in boundary:
        errors.append("standards_navigator.false_compliance_boundary должен явно запрещать certification/compliance overclaim")

    backbone = item.get("lifecycle_backbone")
    if not isinstance(backbone, dict):
        errors.append("standards_navigator.lifecycle_backbone должен быть mapping")
        backbone = {}
    if str(backbone.get("standard_ref") or "") != "iso_12207":
        errors.append("standards_navigator.lifecycle_backbone.standard_ref должен быть iso_12207")
    version_status = str(backbone.get("version_status") or "")
    source_status = str(backbone.get("source_verification_status") or "")
    if version_status in STANDARDS_VERSION_STALE and source_status in STANDARDS_VERSION_CURRENT:
        errors.append("standards_navigator.lifecycle_backbone stale/revision-pending version cannot claim current source status")
    if version_status == "current_with_revision_pending" and backbone.get("verify_current_gate") is not True:
        errors.append("standards_navigator.lifecycle_backbone current_with_revision_pending требует verify_current_gate=true")

    phase_req = item.get("current_phase_required_standards")
    if not isinstance(phase_req, dict):
        errors.append("standards_navigator.current_phase_required_standards должен быть mapping")
        phase_req = {}
    for field in ["phase", "standard_refs", "required_gates"]:
        if field not in phase_req:
            errors.append(f"standards_navigator.current_phase_required_standards.{field} обязателен")
    if not isinstance(phase_req.get("standard_refs", []), list) or not phase_req.get("standard_refs", []):
        errors.append("standards_navigator.current_phase_required_standards.standard_refs должен быть непустым list")
    if not isinstance(phase_req.get("required_gates", []), list) or not phase_req.get("required_gates", []):
        errors.append("standards_navigator.current_phase_required_standards.required_gates должен быть непустым list")

    summary = item.get("gate_summary")
    if not isinstance(summary, dict):
        errors.append("standards_navigator.gate_summary должен быть mapping")
        summary = {}
    for field in ["total", "passed", "missing", "blocking"]:
        if not isinstance(summary.get(field), int) or summary.get(field) < 0:
            errors.append(f"standards_navigator.gate_summary.{field} должен быть non-negative integer")

    gates = item.get("gates", [])
    if not isinstance(gates, list) or not gates:
        errors.append("standards_navigator.gates должен быть непустым list")
        gates = []
    gate_ids: set[str] = set()
    for index, gate in enumerate(gates, 1):
        if not isinstance(gate, dict):
            errors.append(f"standards_navigator.gates[{index}] должен быть mapping")
            continue
        gate_id = str(gate.get("id") or "")
        gate_ids.add(gate_id)
        if not gate_id:
            errors.append(f"standards_navigator.gates[{index}].id обязателен")
        status = status_of(gate)
        validate_status(status, f"standards_navigator.gates[{gate_id}].status", errors)
        if status in STANDARDS_GREEN_STATUSES and not has_evidence(gate):
            errors.append(f"standards_navigator.gates[{gate_id}] отмечен `{status}`, но не содержит evidence или accepted_reason")
        if status == "not_applicable" and not str(gate.get("accepted_reason") or "").strip():
            errors.append(f"standards_navigator.gates[{gate_id}] отмечен not_applicable без accepted_reason")
        if not isinstance(gate.get("standard_refs"), list) or not gate.get("standard_refs"):
            errors.append(f"standards_navigator.gates[{gate_id}].standard_refs должен быть непустым list")
    for required_gate in phase_req.get("required_gates", []) if isinstance(phase_req.get("required_gates"), list) else []:
        if str(required_gate) not in gate_ids:
            errors.append(f"standards_navigator.current phase requires missing gate `{required_gate}`")

    missing = item.get("missing_standards_evidence", [])
    if not isinstance(missing, list):
        errors.append("standards_navigator.missing_standards_evidence должен быть list")
        missing = []
    allowed_to_advance = item.get("allowed_to_advance_phase")
    if not isinstance(allowed_to_advance, bool):
        errors.append("standards_navigator.allowed_to_advance_phase должен быть boolean")
    if allowed_to_advance and (missing or int(summary.get("blocking") or 0) > 0):
        errors.append("standards_navigator.allowed_to_advance_phase=true при missing/blocking standards evidence")

    action = item.get("next_safe_standards_action")
    if not isinstance(action, dict):
        errors.append("standards_navigator.next_safe_standards_action должен быть mapping")
    else:
        validate_software_action(action, "standards_navigator.next_safe_standards_action", errors)

    monitoring = item.get("monitoring_status")
    if not isinstance(monitoring, dict):
        errors.append("standards_navigator.monitoring_status должен быть mapping")
        monitoring = {}
    if not str(monitoring.get("watchlist") or "").strip():
        errors.append("standards_navigator.monitoring_status.watchlist обязателен")
    if str(monitoring.get("status") or "") not in {"current", "stale", "proposal-needed", "unknown"}:
        errors.append("standards_navigator.monitoring_status.status неизвестен")
    if monitoring.get("proposal_required") is not None and not isinstance(monitoring.get("proposal_required"), bool):
        errors.append("standards_navigator.monitoring_status.proposal_required должен быть boolean")
    if str(monitoring.get("status") or "") == "stale" and monitoring.get("proposal_required") is not True:
        errors.append("stale standards monitoring requires proposal_required=true")

    claims = item.get("claims")
    if not isinstance(claims, dict):
        errors.append("standards_navigator.claims должен быть mapping")
        claims = {}
    for field in [
        "production_target",
        "commercial_claim",
        "ai_app",
        "ai_ready_for_users",
        "formal_certification_claim",
        "compliance_claim",
    ]:
        if field not in claims or not isinstance(claims.get(field), bool):
            errors.append(f"standards_navigator.claims.{field} должен быть boolean")
    claim_evidence = claims.get("claim_evidence", [])
    if not isinstance(claim_evidence, list):
        errors.append("standards_navigator.claims.claim_evidence должен быть list")
        claim_evidence = []
    if (claims.get("production_target") or claims.get("commercial_claim")) and profile == "solo_lightweight":
        errors.append("standards_navigator production/commercial claim requires commercial_production or custom profile")
    if (claims.get("formal_certification_claim") or claims.get("compliance_claim")) and not claim_evidence:
        errors.append("standards_navigator certification/compliance claim requires evidence")
    if claims.get("ai_ready_for_users"):
        ai_gate = next((gate for gate in gates if isinstance(gate, dict) and gate.get("id") == "ai_safety_gate"), None)
        if not ai_gate:
            errors.append("standards_navigator AI app ready requires ai_safety_gate")
        elif status_of(ai_gate) not in STANDARDS_GREEN_STATUSES:
            errors.append("standards_navigator AI app ready requires passed ai_safety_gate")


def validate_orchestration_execution_claims(item: Any, errors: list[str]) -> None:
    if not isinstance(item, dict):
        return
    parent = item.get("parent_handoff")
    if isinstance(parent, dict):
        parent_status = str(parent.get("status") or "")
        if parent_status and parent_status not in ORCHESTRATION_PARENT_STATUSES:
            errors.append("handoff_orchestration.parent_handoff.status неизвестен")
        if parent_status in ORCHESTRATION_GREEN_STATUSES and not has_evidence(parent):
            errors.append("handoff_orchestration.parent_handoff отмечен completed/executed без execution evidence или accepted_reason")

    children = item.get("child_tasks", [])
    if children is None:
        return
    if not isinstance(children, list):
        errors.append("handoff_orchestration.child_tasks должен быть list")
        return
    for index, child in enumerate(children, 1):
        if not isinstance(child, dict):
            errors.append(f"handoff_orchestration.child_tasks[{index}] должен быть mapping")
            continue
        child_id = str(child.get("id") or index)
        child_status = str(child.get("status") or "")
        if child_status and child_status not in ORCHESTRATION_CHILD_STATUSES:
            errors.append(f"handoff_orchestration.child_tasks[{child_id}].status неизвестен")
        if str(child.get("owner_boundary") or ""):
            validate_boundary(str(child.get("owner_boundary") or ""), f"handoff_orchestration.child_tasks[{child_id}].owner_boundary", errors)
        if child_status in ORCHESTRATION_GREEN_STATUSES and not has_evidence(child):
            errors.append(f"handoff_orchestration.child_tasks[{child_id}] отмечен `{child_status}`, но не содержит execution evidence или accepted_reason")


def validate_handoff_implementation_control(item: Any, data: dict[str, Any], dashboard_path: Path | None, errors: list[str]) -> None:
    source_artifacts = data.get("source_artifacts", [])
    source_set = {str(source) for source in source_artifacts} if isinstance(source_artifacts, list) else set()
    references_register = HANDOFF_IMPLEMENTATION_ARTIFACT in source_set
    if item is None and not references_register:
        return
    if not isinstance(item, dict):
        errors.append("handoff_implementation_control должен быть mapping")
        return
    if item.get("enabled") is not True:
        errors.append("handoff_implementation_control.enabled должен быть true")
    source_artifact = str(item.get("source_artifact") or "")
    if source_artifact != HANDOFF_IMPLEMENTATION_ARTIFACT:
        errors.append("handoff_implementation_control.source_artifact должен ссылаться на .chatgpt/handoff-implementation-register.yaml")
    if HANDOFF_IMPLEMENTATION_ARTIFACT not in source_set:
        errors.append("source_artifacts должен содержать .chatgpt/handoff-implementation-register.yaml")
    if str(item.get("queue_policy") or "") != "deterministic_dependency_priority_calculation":
        errors.append("handoff_implementation_control.queue_policy должен быть deterministic_dependency_priority_calculation")
    route_boundary = str(item.get("route_boundary") or "").lower()
    if "не переключ" not in route_boundary and "does not" not in route_boundary:
        errors.append("handoff_implementation_control.route_boundary должен явно запрещать handoff/register auto-switch claim")
    closeout_policy = str(item.get("closeout_policy") or "").lower()
    if "silent" not in closeout_policy and "не удал" not in closeout_policy:
        errors.append("handoff_implementation_control.closeout_policy должен запрещать silent deletion/drop")
    summary = item.get("summary")
    if not isinstance(summary, dict):
        errors.append("handoff_implementation_control.summary должен быть mapping")
    else:
        for key in ["open_items", "blocked_items", "implemented_not_verified", "stale_items_without_recent_evidence"]:
            if key not in summary or not isinstance(summary.get(key), int) or summary.get(key) < 0:
                errors.append(f"handoff_implementation_control.summary.{key} должен быть non-negative integer")

    if dashboard_path is not None and source_artifact:
        register_path = resolve_source_artifact(dashboard_path, source_artifact)
        if register_path is None:
            errors.append(f"handoff_implementation_control source artifact не найден: `{source_artifact}`")
        else:
            validator = load_handoff_implementation_validator()
            for register_error in validator.validate_register(load_yaml(register_path)):
                errors.append(f"handoff_implementation_control register invalid: {register_error}")


def validate_universal_task_control(item: Any, dashboard_path: Path | None, errors: list[str]) -> None:
    if item is None:
        return
    if not isinstance(item, dict):
        errors.append("universal_task_control должен быть mapping")
        return
    status = str(item.get("status") or "unknown")
    if status not in UNIVERSAL_TASK_STATUSES:
        errors.append("universal_task_control.status неизвестен")
    registry_path = str(item.get("registry_path") or "")
    if not registry_path:
        errors.append("universal_task_control.registry_path обязателен")
    for key in [
        "open_tasks",
        "ready_for_handoff",
        "ready_for_codex",
        "codex_running",
        "human_review",
        "blocked",
        "verified",
    ]:
        if key not in item or not isinstance(item.get(key), int) or item.get(key) < 0:
            errors.append(f"universal_task_control.{key} должен быть non-negative integer")
    if not str(item.get("next_action") or "").strip():
        errors.append("universal_task_control.next_action обязателен")
    if not str(item.get("fallback_next_action") or "").strip():
        errors.append("universal_task_control.fallback_next_action обязателен")
    evidence = item.get("evidence", [])
    if evidence is not None and not isinstance(evidence, list):
        errors.append("universal_task_control.evidence должен быть list")
        evidence = []
    accepted_reason = str(item.get("accepted_reason") or item.get("reason") or "").strip()
    if status in UNIVERSAL_TASK_GREEN_STATUSES and not evidence and not accepted_reason:
        errors.append("universal_task_control green status требует evidence или accepted_reason")


def validate_module_readiness(item: Any, data: dict[str, Any], dashboard_path: Path | None, errors: list[str]) -> None:
    visual = data.get("beginner_visual_surfaces", {}) if isinstance(data.get("beginner_visual_surfaces"), dict) else {}
    chatgpt_card = visual.get("chatgpt_mini_card", {}) if isinstance(visual.get("chatgpt_mini_card"), dict) else {}
    if not isinstance(item, dict):
        if chatgpt_card.get("enabled") is True:
            errors.append("module_readiness обязателен, когда включена beginner ChatGPT visual card")
        return

    if str(item.get("selected_profile") or "") not in STANDARDS_PROFILES:
        errors.append("module_readiness.selected_profile должен быть solo_lightweight/commercial_production/custom")
    policy = str(item.get("false_green_policy") or "")
    if not policy:
        errors.append("module_readiness.false_green_policy обязателен")
    lowered_policy = policy.lower()
    if "not compliance" not in lowered_policy and "not certification" not in lowered_policy and "не compliance" not in lowered_policy and "не certification" not in lowered_policy:
        errors.append("module_readiness.false_green_policy должен запрещать compliance/certification overclaim")

    required_modules = item.get("required_modules", [])
    if not isinstance(required_modules, list):
        errors.append("module_readiness.required_modules должен быть list")
        required_modules = []
    required_set = {str(module_id) for module_id in required_modules}
    missing_required = sorted(REQUIRED_MODULE_IDS - required_set)
    if missing_required:
        errors.append("module_readiness.required_modules не содержит: " + ", ".join(missing_required))

    modules = item.get("modules", [])
    if not isinstance(modules, list):
        errors.append("module_readiness.modules должен быть list")
        modules = []
    registry_ids = registry_standard_ids(data, dashboard_path)
    gate_ids = standards_gate_ids(data)
    seen: set[str] = set()
    for index, module in enumerate(modules, 1):
        if not isinstance(module, dict):
            errors.append(f"module_readiness.modules[{index}] должен быть mapping")
            continue
        module_id = str(module.get("id") or "")
        if not module_id:
            errors.append(f"module_readiness.modules[{index}].id обязателен")
        if module_id in seen:
            errors.append(f"module_readiness.modules содержит повторяющийся id `{module_id}`")
        seen.add(module_id)
        if not str(module.get("label") or "").strip():
            errors.append(f"module_readiness.modules[{module_id}].label обязателен")
        status = str(module.get("status") or "")
        if status not in MODULE_STATUSES:
            errors.append(f"module_readiness.modules[{module_id}].status неизвестен: `{status}`")
        if status in MODULE_GREEN_STATUSES and not has_evidence(module):
            errors.append(f"module_readiness.modules[{module_id}] green status `{status}` требует evidence или accepted_reason")
        if module_id == "ai" and status == "not_applicable" and not str(module.get("accepted_reason") or "").strip():
            errors.append("module_readiness.modules[ai] not_applicable требует accepted_reason")

        standard_refs = module.get("standard_refs", [])
        if not isinstance(standard_refs, list):
            errors.append(f"module_readiness.modules[{module_id}].standard_refs должен быть list")
            standard_refs = []
        for standard_ref in standard_refs:
            if registry_ids and str(standard_ref) not in registry_ids:
                errors.append(f"module_readiness.modules[{module_id}].standard_refs содержит неизвестный standard_ref `{standard_ref}`")

        gate_refs = module.get("gate_refs", [])
        if not isinstance(gate_refs, list):
            errors.append(f"module_readiness.modules[{module_id}].gate_refs должен быть list")
            gate_refs = []
        for gate_ref in gate_refs:
            if gate_ids and str(gate_ref) not in gate_ids:
                errors.append(f"module_readiness.modules[{module_id}].gate_refs содержит неизвестный gate_ref `{gate_ref}`")

        source_refs = module.get("source_refs", [])
        if not isinstance(source_refs, list):
            errors.append(f"module_readiness.modules[{module_id}].source_refs должен быть list")
            source_refs = []
        for source_ref in source_refs:
            if str(source_ref) not in MODULE_SOURCE_REFS:
                errors.append(f"module_readiness.modules[{module_id}].source_refs содержит неизвестный source_ref `{source_ref}`")
        if status in MODULE_GREEN_STATUSES and "software_update_governance" in {str(ref) for ref in source_refs}:
            software = data.get("software_update_governance", {}) if isinstance(data.get("software_update_governance"), dict) else {}
            if str(software.get("baseline_status") or "") not in GREEN_STATUSES:
                errors.append(
                    f"module_readiness.modules[{module_id}] green status `{status}` "
                    "ссылается на pending software_update_governance"
                )

        claim = str(module.get("claim") or "")
        if claim and FALSE_COMPLIANCE_RE.search(claim):
            errors.append(f"module_readiness.modules[{module_id}].claim содержит false compliance/certification wording")

    missing_modules = sorted(REQUIRED_MODULE_IDS - seen)
    if missing_modules:
        errors.append("module_readiness.modules не содержит: " + ", ".join(missing_modules))


def validate_beginner_visual_surfaces(item: Any, data: dict[str, Any], errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append("beginner_visual_surfaces должен быть mapping")
        return

    if item.get("no_heavy_default_ui") is not True:
        errors.append("beginner_visual_surfaces.no_heavy_default_ui должен быть true")
    default_surfaces = item.get("default_surfaces", [])
    if not isinstance(default_surfaces, list):
        errors.append("beginner_visual_surfaces.default_surfaces должен быть list")
        default_surfaces = []
    default_set = {str(surface) for surface in default_surfaces}
    missing_surfaces = sorted(VISUAL_SURFACES - default_set)
    if missing_surfaces:
        errors.append("beginner_visual_surfaces.default_surfaces не содержит: " + ", ".join(missing_surfaces))
    heavy_surfaces = [
        surface
        for surface in default_set
        if re.search(r"(?i)(web|daemon|sqlite|telegram|websocket|worker|background|live)", surface)
    ]
    if heavy_surfaces:
        errors.append("beginner_visual_surfaces.default_surfaces содержит heavy default UI promise: " + ", ".join(sorted(heavy_surfaces)))
    boundary = str(item.get("heavy_ui_boundary") or "")
    if not boundary:
        errors.append("beginner_visual_surfaces.heavy_ui_boundary обязателен")
    if HEAVY_DEFAULT_UI_RE.search(boundary) and not re.search(r"(?i)(not default|not default promises|не является default|не по умолчанию|не default)", boundary):
        errors.append("beginner_visual_surfaces.heavy_ui_boundary содержит heavy default UI promise")
    if "project-lifecycle-dashboard.yaml" not in str(item.get("source_of_truth") or ""):
        errors.append("beginner_visual_surfaces.source_of_truth должен ссылаться на project-lifecycle-dashboard.yaml")

    statuses = item.get("status_vocabulary", [])
    if not isinstance(statuses, list):
        errors.append("beginner_visual_surfaces.status_vocabulary должен быть list")
        statuses = []
    status_set = {str(status) for status in statuses}
    missing_statuses = sorted(BEGINNER_STATUSES - status_set)
    if missing_statuses:
        errors.append("beginner_visual_surfaces.status_vocabulary не содержит: " + ", ".join(missing_statuses))

    boundaries = item.get("owner_boundaries", [])
    if not isinstance(boundaries, list):
        errors.append("beginner_visual_surfaces.owner_boundaries должен быть list")
        boundaries = []
    boundary_set = {str(boundary) for boundary in boundaries}
    missing_boundaries = sorted(OWNER_BOUNDARIES - boundary_set)
    if missing_boundaries:
        errors.append("beginner_visual_surfaces.owner_boundaries не содержит: " + ", ".join(missing_boundaries))

    chatgpt_card = item.get("chatgpt_mini_card")
    if not isinstance(chatgpt_card, dict):
        errors.append("beginner_visual_surfaces.chatgpt_mini_card должен быть mapping")
        chatgpt_card = {}
    if chatgpt_card.get("enabled") is not True:
        errors.append("beginner_visual_surfaces.chatgpt_mini_card.enabled должен быть true")
    if chatgpt_card.get("renders_from_dashboard_yaml") is not True:
        errors.append("beginner_visual_surfaces.chatgpt_mini_card должен рендериться из dashboard YAML")
    if not str(chatgpt_card.get("template") or "").endswith("visual-status-card.md.template"):
        errors.append("beginner_visual_surfaces.chatgpt_mini_card.template должен ссылаться на visual-status-card.md.template")
    if str(chatgpt_card.get("user_action_policy") or "") != "derive_from_external_actions_ledger":
        errors.append("beginner_visual_surfaces.chatgpt_mini_card.user_action_policy должен быть derive_from_external_actions_ledger")
    fields = chatgpt_card.get("required_fields", [])
    if not isinstance(fields, list):
        errors.append("beginner_visual_surfaces.chatgpt_mini_card.required_fields должен быть list")
        fields = []
    missing_fields = sorted(VISUAL_CARD_FIELDS - {str(field) for field in fields})
    if missing_fields:
        errors.append("beginner_visual_surfaces.chatgpt_mini_card.required_fields не содержит: " + ", ".join(missing_fields))
    external_actions = data.get("external_actions_ledger", [])
    if isinstance(external_actions, list) and external_actions:
        user_action_value = str(chatgpt_card.get("user_action_required") or "")
        if NO_USER_ACTION_RE.match(user_action_value):
            errors.append("chatgpt mini card не может говорить, что пользователю ничего не требуется, если external_actions_ledger не пуст")

    codex_card = item.get("codex_execution_card")
    if not isinstance(codex_card, dict):
        errors.append("beginner_visual_surfaces.codex_execution_card должен быть mapping")
        codex_card = {}
    if codex_card.get("enabled") is not True:
        errors.append("beginner_visual_surfaces.codex_execution_card.enabled должен быть true")
    if codex_card.get("renders_from_dashboard_yaml") is not True:
        errors.append("beginner_visual_surfaces.codex_execution_card должен рендериться из dashboard YAML")
    if not str(codex_card.get("template") or "").endswith("codex-execution-card.md.template"):
        errors.append("beginner_visual_surfaces.codex_execution_card.template должен ссылаться на codex-execution-card.md.template")
    if str(codex_card.get("execution_evidence_policy") or "") != "green_status_requires_evidence_or_accepted_reason":
        errors.append("beginner_visual_surfaces.codex_execution_card.execution_evidence_policy должен требовать evidence для green status")
    sections = codex_card.get("required_sections", [])
    if not isinstance(sections, list):
        errors.append("beginner_visual_surfaces.codex_execution_card.required_sections должен быть list")
        sections = []
    missing_sections = sorted(CODEX_CARD_SECTIONS - {str(section) for section in sections})
    if missing_sections:
        errors.append("beginner_visual_surfaces.codex_execution_card.required_sections не содержит: " + ", ".join(missing_sections))

    markdown_dashboard = item.get("markdown_dashboard")
    if not isinstance(markdown_dashboard, dict):
        errors.append("beginner_visual_surfaces.markdown_dashboard должен быть mapping")
        markdown_dashboard = {}
    if markdown_dashboard.get("enabled") is not True:
        errors.append("beginner_visual_surfaces.markdown_dashboard.enabled должен быть true")
    if markdown_dashboard.get("renders_from_dashboard_yaml") is not True:
        errors.append("beginner_visual_surfaces.markdown_dashboard должен рендериться из dashboard YAML")
    if str(markdown_dashboard.get("output") or "") != "reports/project-lifecycle-dashboard.md":
        errors.append("beginner_visual_surfaces.markdown_dashboard.output должен быть reports/project-lifecycle-dashboard.md")


def validate_dashboard(data: dict[str, Any], dashboard_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"`{key}` обязателен")

    dumped = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    if SECRET_RE.search(dumped) or "-----BEGIN" in dumped:
        errors.append("dashboard содержит secret-like content")
    for line in dumped.splitlines():
        lowered = line.lower()
        if POSITIVE_AUTOSWITCH_RE.search(line) and "does not" not in lowered and "not " not in lowered:
            errors.append("dashboard содержит false auto-switch claim для advisory/routing layer")
        if RU_POSITIVE_AUTOSWITCH_RE.search(line) and "не переключает" not in lowered and "нельзя" not in lowered:
            errors.append("dashboard содержит false auto-switch claim для advisory/routing layer")

    project = as_mapping(data, "project", errors)
    for field in ["name", "slug", "profile", "lifecycle_state", "current_mode", "owner_boundary"]:
        if not str(project.get(field) or "").strip():
            errors.append(f"project.{field} обязателен")
    if str(project.get("owner_boundary") or "") not in PROJECT_OWNER_BOUNDARIES:
        errors.append("project.owner_boundary имеет неизвестное значение")
    validate_generated_project_state_alignment(data, dashboard_path, errors)

    lifecycle = as_mapping(data, "lifecycle_phase", errors)
    current_phase = str(lifecycle.get("current") or "")
    if current_phase not in LIFECYCLE_PHASES:
        errors.append("lifecycle_phase.current должен быть lifecycle phase")
    allowed = lifecycle.get("allowed", [])
    if isinstance(allowed, list) and allowed:
        unknown = [str(item) for item in allowed if str(item) not in LIFECYCLE_PHASES]
        if unknown:
            errors.append("lifecycle_phase.allowed содержит неизвестные phases: " + ", ".join(unknown))

    change = as_mapping(data, "active_change", errors)
    if str(change.get("class") or "") not in CHANGE_CLASSES:
        errors.append("active_change.class имеет неизвестное значение")
    if str(change.get("priority") or "") not in PRIORITIES:
        errors.append("active_change.priority должен быть low/medium/high/critical")
    validate_status(status_of(change), "active_change.status", errors)
    validate_boundary(str(change.get("owner_boundary") or ""), "active_change.owner_boundary", errors)
    validate_green_evidence(change, "active_change", errors)

    gates = as_list(data, "stage_gates", errors)
    required_gates = {
        "intake",
        "classification",
        "reuse_reality_check",
        "spec",
        "tech_spec",
        "handoff_allowed",
        "execution",
        "verification",
        "done",
    }
    seen_gates: set[str] = set()
    for index, gate in enumerate(gates, 1):
        if not isinstance(gate, dict):
            errors.append(f"stage_gates[{index}] должен быть mapping")
            continue
        gate_id = str(gate.get("id") or "")
        seen_gates.add(gate_id)
        if not gate_id:
            errors.append(f"stage_gates[{index}].id обязателен")
        if not str(gate.get("title") or "").strip():
            errors.append(f"stage_gates[{index}].title обязателен")
        validate_status(status_of(gate), f"stage_gates[{gate_id}].status", errors)
        validate_green_evidence(gate, f"stage_gates[{gate_id}]", errors)
    missing_gates = sorted(required_gates - seen_gates)
    if missing_gates:
        errors.append("stage_gates не содержит обязательные gates: " + ", ".join(missing_gates))

    execution = as_mapping(data, "multi_step_execution", errors)
    if not isinstance(execution.get("current_wave"), int):
        errors.append("multi_step_execution.current_wave должен быть integer")
    waves = execution.get("waves", [])
    if not isinstance(waves, list) or not waves:
        errors.append("multi_step_execution.waves должен быть непустым list")
    else:
        for wave_index, wave in enumerate(waves, 1):
            if not isinstance(wave, dict):
                errors.append(f"multi_step_execution.waves[{wave_index}] должен быть mapping")
                continue
            wave_id = str(wave.get("id") or f"#{wave_index}")
            validate_status(status_of(wave), f"wave {wave_id}.status", errors)
            validate_green_evidence(wave, f"wave {wave_id}", errors)
            tasks = wave.get("tasks", [])
            if not isinstance(tasks, list):
                errors.append(f"wave {wave_id}.tasks должен быть list")
                continue
            for task_index, task in enumerate(tasks, 1):
                if not isinstance(task, dict):
                    errors.append(f"wave {wave_id}.tasks[{task_index}] должен быть mapping")
                    continue
                task_id = str(task.get("id") or f"#{task_index}")
                validate_status(status_of(task), f"task {task_id}.status", errors)
                if str(task.get("owner_boundary") or ""):
                    validate_boundary(str(task.get("owner_boundary") or ""), f"task {task_id}.owner_boundary", errors)
                validate_green_evidence(task, f"task {task_id}", errors)
    next_task = execution.get("next_task")
    if not isinstance(next_task, dict) or not str(next_task.get("action") or "").strip():
        errors.append("multi_step_execution.next_task.action обязателен")
    elif str(next_task.get("owner_boundary") or ""):
        validate_boundary(str(next_task.get("owner_boundary") or ""), "multi_step_execution.next_task.owner_boundary", errors)
    final_verification = execution.get("final_verification")
    if not isinstance(final_verification, dict):
        errors.append("multi_step_execution.final_verification должен быть mapping")
    else:
        validate_status(status_of(final_verification), "multi_step_execution.final_verification.status", errors)
        validate_green_evidence(final_verification, "multi_step_execution.final_verification", errors)

    orchestration = as_mapping(data, "handoff_orchestration", errors)
    boundary_text = str(orchestration.get("route_explanation_boundary") or "").lower()
    if not boundary_text:
        errors.append("handoff_orchestration.route_explanation_boundary обязателен")
    if "не переключ" not in boundary_text and "does not" not in boundary_text:
        errors.append("handoff_orchestration.route_explanation_boundary должен явно запрещать advisory auto-switch claim")
    validate_orchestration_execution_claims(orchestration, errors)
    validate_handoff_implementation_control(data.get("handoff_implementation_control"), data, dashboard_path, errors)
    validate_universal_task_control(data.get("universal_task_control"), dashboard_path, errors)
    validate_module_readiness(data.get("module_readiness"), data, dashboard_path, errors)
    source_artifacts = data.get("source_artifacts", [])
    if isinstance(source_artifacts, list) and CHAT_HANDOFF_INDEX_ARTIFACT not in {str(source) for source in source_artifacts}:
        errors.append("source_artifacts должен содержать .chatgpt/chat-handoff-index.yaml")

    validate_beginner_visual_surfaces(data.get("beginner_visual_surfaces"), data, errors)

    runbook_packages = data.get("runbook_packages")
    if runbook_packages is not None:
        if not isinstance(runbook_packages, list):
            errors.append("runbook_packages должен быть list")
        else:
            seen_packages: set[str] = set()
            for index, package in enumerate(runbook_packages, 1):
                if not isinstance(package, dict):
                    errors.append(f"runbook_packages[{index}] должен быть mapping")
                    continue
                package_id = str(package.get("id") or "")
                seen_packages.add(package_id)
                if package_id not in RUNBOOK_PACKAGE_IDS:
                    errors.append(f"runbook_packages[{index}].id неизвестен: `{package_id}`")
                for field in ["path", "current_phase", "current_step", "active_contour", "checklist_path", "next_action", "owner_boundary"]:
                    if not str(package.get(field) or "").strip():
                        errors.append(f"runbook_packages[{package_id or index}].{field} обязателен")
                for field in RUNBOOK_DEFAULT_DECISION_FIELDS:
                    if field not in package:
                        errors.append(f"runbook_packages[{package_id or index}].{field} обязателен")
                if str(package.get("default_decision_mode") or "") not in DEFAULT_DECISION_MODES:
                    errors.append(f"runbook_packages[{package_id or index}].default_decision_mode неизвестен")
                for int_field in ["defaults_count", "overrides_count", "unresolved_decisions_count"]:
                    if int_field in package and not isinstance(package.get(int_field), int):
                        errors.append(f"runbook_packages[{package_id or index}].{int_field} должен быть integer")
                if "readiness_to_generate_handoff" in package and not isinstance(package.get("readiness_to_generate_handoff"), bool):
                    errors.append(f"runbook_packages[{package_id or index}].readiness_to_generate_handoff должен быть boolean")
                if "next_decision" in package and not str(package.get("next_decision") or "").strip():
                    errors.append(f"runbook_packages[{package_id or index}].next_decision обязателен")
                if package_id == "02-greenfield-product":
                    for field in [
                        "intake_channel",
                        "trigger_command",
                        "battle_repo_created_by",
                        "chatgpt_project_ui_owner",
                        "repo_first_instruction_prepared_by",
                        "repo_first_instruction_pasted_by",
                    ]:
                        if not str(package.get(field) or "").strip():
                            errors.append(f"runbook_packages[{package_id}].{field} обязателен")
                    if str(package.get("intake_channel") or "") != "factory-template-chatgpt-project":
                        errors.append("runbook_packages[02-greenfield-product].intake_channel должен быть factory-template-chatgpt-project")
                    if str(package.get("trigger_command") or "") != "новый проект":
                        errors.append("runbook_packages[02-greenfield-product].trigger_command должен быть `новый проект`")
                    if str(package.get("battle_repo_created_by") or "") != "codex":
                        errors.append("runbook_packages[02-greenfield-product].battle_repo_created_by должен быть codex")
                    if str(package.get("chatgpt_project_ui_owner") or "") != "user":
                        errors.append("runbook_packages[02-greenfield-product].chatgpt_project_ui_owner должен быть user")
                    if str(package.get("repo_first_instruction_prepared_by") or "") != "codex":
                        errors.append("runbook_packages[02-greenfield-product].repo_first_instruction_prepared_by должен быть codex")
                    if str(package.get("repo_first_instruction_pasted_by") or "") != "user":
                        errors.append("runbook_packages[02-greenfield-product].repo_first_instruction_pasted_by должен быть user")
                    for bool_field in ["handoff_ready", "codex_takeover_ready", "battle_chatgpt_project_created"]:
                        if not isinstance(package.get(bool_field), bool):
                            errors.append(f"runbook_packages[02-greenfield-product].{bool_field} должен быть boolean")
                if str(package.get("active_contour") or "") not in {
                    "not_selected",
                    "codex-app-remote-ssh",
                    "vscode-remote-ssh-codex-extension",
                }:
                    errors.append(f"runbook_packages[{package_id or index}].active_contour неизвестен")
                if not isinstance(package.get("takeover_ready"), bool):
                    errors.append(f"runbook_packages[{package_id or index}].takeover_ready должен быть boolean")
                if str(package.get("owner_boundary") or "") != "internal-repo-follow-up":
                    errors.append(f"runbook_packages[{package_id or index}].owner_boundary должен быть internal-repo-follow-up")
                if not isinstance(package.get("gates"), list) or not package.get("gates"):
                    errors.append(f"runbook_packages[{package_id or index}].gates должен быть непустым list")
                if not isinstance(package.get("blockers"), list):
                    errors.append(f"runbook_packages[{package_id or index}].blockers должен быть list")
            missing_packages = sorted(RUNBOOK_PACKAGE_IDS - seen_packages)
            if missing_packages:
                errors.append("runbook_packages не содержит packages: " + ", ".join(missing_packages))

    release = as_mapping(data, "release_readiness", errors)
    validate_status(status_of(release), "release_readiness.status", errors)
    validate_status(str(release.get("verification_state") or ""), "release_readiness.verification_state", errors)
    validate_green_evidence(release, "release_readiness", errors)

    runtime = as_mapping(data, "deploy_runtime", errors)
    validate_status(status_of(runtime), "deploy_runtime.status", errors)
    validate_green_evidence(runtime, "deploy_runtime", errors)

    validate_standards_navigator(data.get("standards_navigator"), errors)

    software = as_mapping(data, "software_update_governance", errors)
    baseline_status = str(software.get("baseline_status") or "")
    validate_status(baseline_status, "software_update_governance.baseline_status", errors)
    if baseline_status in GREEN_STATUSES and not has_evidence(software):
        errors.append("software_update_governance baseline отмечен green, но не содержит evidence или accepted_reason")
    policy = str(software.get("auto_update_policy") or "")
    if policy not in SOFTWARE_UPDATE_POLICIES:
        errors.append("software_update_governance.auto_update_policy должен быть manual-approved-upgrade")
    proposal_status = str(software.get("upgrade_proposal_status") or "")
    if proposal_status not in SOFTWARE_PROPOSAL_STATUSES:
        errors.append("software_update_governance.upgrade_proposal_status имеет неизвестное значение")
    findings = software.get("relevant_findings_count")
    if not isinstance(findings, int) or findings < 0:
        errors.append("software_update_governance.relevant_findings_count должен быть non-negative integer")
    if "last_update_intelligence_check" not in software:
        errors.append("software_update_governance.last_update_intelligence_check обязателен")
    validate_software_action(software.get("next_safe_action"), "software_update_governance.next_safe_action", errors)
    validate_software_action(software.get("fallback_action"), "software_update_governance.fallback_action", errors)
    if not isinstance(software.get("blockers", []), list):
        errors.append("software_update_governance.blockers должен быть list")
    source_artifacts = software.get("source_artifacts", [])
    if not isinstance(source_artifacts, list):
        errors.append("software_update_governance.source_artifacts должен быть list")
    else:
        required_sources = {
            ".chatgpt/software-inventory.yaml",
            ".chatgpt/software-update-watchlist.yaml",
            ".chatgpt/software-update-readiness.yaml",
            "reports/software-updates/README.md",
        }
        missing_sources = sorted(required_sources - {str(item) for item in source_artifacts})
        if missing_sources:
            errors.append("software_update_governance.source_artifacts не содержит: " + ", ".join(missing_sources))

    post_release = as_mapping(data, "post_release_improvement", errors)
    for key in ["incidents", "feedback", "learning_proposals", "backlog_candidates"]:
        if not isinstance(post_release.get(key, []), list):
            errors.append(f"post_release_improvement.{key} должен быть list")

    for index, action in enumerate(as_list(data, "external_actions_ledger", errors), 1):
        if not isinstance(action, dict):
            errors.append(f"external_actions_ledger[{index}] должен быть mapping")
            continue
        boundary = str(action.get("owner_boundary") or "")
        if boundary not in OWNER_BOUNDARIES - {"internal-repo-follow-up"}:
            errors.append(f"external_actions_ledger[{index}].owner_boundary должен быть external/runtime/downstream/model/secret boundary")
        if not str(action.get("action") or "").strip():
            errors.append(f"external_actions_ledger[{index}].action обязателен")

    for key in ["recommended_next_step", "fallback_next_step"]:
        item = as_mapping(data, key, errors)
        validate_boundary(str(item.get("owner_boundary") or ""), f"{key}.owner_boundary", errors)
        if not str(item.get("action") or "").strip():
            errors.append(f"{key}.action обязателен")
        validate_green_evidence(item, key, errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует Project Lifecycle Dashboard YAML.")
    parser.add_argument("path", nargs="?", default="template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml")
    args = parser.parse_args()

    path = Path(args.path)
    errors = validate_dashboard(load_yaml(path), path)
    if errors:
        print("PROJECT LIFECYCLE DASHBOARD НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PROJECT LIFECYCLE DASHBOARD ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
