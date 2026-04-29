#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "standards-gates/v1"
PROFILES = {"solo_lightweight", "commercial_production", "custom"}
GREEN_STATUSES = {"passed", "completed", "done", "ready"}
ALLOWED_STATUSES = GREEN_STATUSES | {"pending", "in_progress", "blocked", "failed", "not_applicable", "skipped"}
OWNER_BOUNDARIES = {
    "internal-repo-follow-up",
    "external-user-action",
    "runtime-action",
    "downstream-battle-action",
    "model-mapping-blocker",
    "secret-boundary-blocker",
}
CERTIFICATION_RE = re.compile(r"(?i)\b(certified|certification|сертифиц|сертификат|formally compliant|formal compliance)\b")
CURRENT_STATUSES = {
    "current_published",
    "current_final",
    "current_stable_release",
    "current_w3c_recommendation",
    "current_dora_guidance",
    "current_practice_baseline",
}
STALE_STATUSES = {"stale", "unknown", "needs_review", "revision_pending", "current_with_revision_pending"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def resolve_path(value: str) -> Path:
    path = Path(value)
    if path.is_dir():
        candidates = [
            path / ".chatgpt" / "standards-gates.yaml",
            path / "template-repo" / "template" / ".chatgpt" / "standards-gates.yaml",
            path / "template" / ".chatgpt" / "standards-gates.yaml",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
    return path


def has_evidence(item: dict[str, Any]) -> bool:
    evidence = item.get("evidence")
    if isinstance(evidence, list) and evidence:
        return True
    if isinstance(evidence, str) and evidence.strip():
        return True
    return bool(str(item.get("accepted_reason") or item.get("reason") or "").strip())


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")

    profile = str(data.get("selected_profile") or "")
    if profile not in PROFILES:
        errors.append("selected_profile должен быть solo_lightweight, commercial_production или custom")

    claims = data.get("project_claims")
    if not isinstance(claims, dict):
        errors.append("project_claims должен быть mapping")
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
            errors.append(f"project_claims.{field} должен быть boolean")
    claim_evidence = claims.get("claim_evidence", [])
    if not isinstance(claim_evidence, list):
        errors.append("project_claims.claim_evidence должен быть list")

    dumped = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    if CERTIFICATION_RE.search(dumped) and not str(data.get("false_compliance_boundary") or "").strip():
        errors.append("certification/compliance wording найден без false_compliance_boundary")
    if (claims.get("formal_certification_claim") or claims.get("compliance_claim")) and not claim_evidence:
        errors.append("formal certification/compliance claim requires claim_evidence")
    if (claims.get("production_target") or claims.get("commercial_claim")) and profile == "solo_lightweight":
        errors.append("production/commercial claim cannot use solo_lightweight profile only")

    versions = data.get("standard_versions", [])
    if not isinstance(versions, list):
        errors.append("standard_versions должен быть list")
    else:
        for index, item in enumerate(versions, 1):
            if not isinstance(item, dict):
                errors.append(f"standard_versions[{index}] должен быть mapping")
                continue
            status = str(item.get("version_status") or "")
            current_claim = bool(item.get("dashboard_current_claim"))
            if current_claim and status in STALE_STATUSES:
                errors.append(
                    f"standard_versions[{item.get('standard_ref', index)}] has stale/revision-pending status but dashboard_current_claim=true"
                )
            if status and status not in CURRENT_STATUSES | STALE_STATUSES:
                errors.append(f"standard_versions[{item.get('standard_ref', index)}].version_status неизвестен: `{status}`")

    gates = data.get("gates", [])
    if not isinstance(gates, list) or not gates:
        errors.append("gates должен быть непустым list")
        return errors

    by_id: dict[str, dict[str, Any]] = {}
    for index, gate in enumerate(gates, 1):
        if not isinstance(gate, dict):
            errors.append(f"gates[{index}] должен быть mapping")
            continue
        gate_id = str(gate.get("id") or "")
        if not gate_id:
            errors.append(f"gates[{index}].id обязателен")
            continue
        by_id[gate_id] = gate
        status = str(gate.get("status") or "")
        if status not in ALLOWED_STATUSES:
            errors.append(f"gate `{gate_id}` имеет неизвестный status `{status}`")
        if status in GREEN_STATUSES and not has_evidence(gate):
            errors.append(f"gate `{gate_id}` отмечен `{status}`, но не содержит evidence или accepted_reason")
        if status == "not_applicable" and not str(gate.get("accepted_reason") or "").strip():
            errors.append(f"gate `{gate_id}` отмечен not_applicable без accepted_reason")
        if not isinstance(gate.get("standard_refs"), list) or not gate.get("standard_refs"):
            errors.append(f"gate `{gate_id}` должен содержать standard_refs")
        required_for = gate.get("required_for_profile")
        if not isinstance(required_for, list) or not required_for:
            errors.append(f"gate `{gate_id}` должен содержать required_for_profile")
        else:
            unknown_profiles = [str(item) for item in required_for if str(item) not in PROFILES]
            if unknown_profiles:
                errors.append(f"gate `{gate_id}` содержит неизвестные required_for_profile: {', '.join(unknown_profiles)}")
        boundary = str(gate.get("owner_boundary") or "")
        if boundary not in OWNER_BOUNDARIES:
            errors.append(f"gate `{gate_id}` имеет неизвестный owner_boundary `{boundary}`")

    if (claims.get("production_target") or claims.get("commercial_claim")) and profile == "commercial_production":
        required = [
            "security_minimum_checked",
            "web_security_checked",
            "accessibility_minimum_checked",
            "operations_health_baseline",
            "false_compliance_checked",
        ]
        for gate_id in required:
            gate = by_id.get(gate_id)
            if not gate:
                errors.append(f"commercial_production requires gate `{gate_id}`")
            elif str(gate.get("status") or "") not in GREEN_STATUSES:
                errors.append(f"commercial_production gate `{gate_id}` must be passed/ready/done/completed")

    if claims.get("ai_app") or claims.get("ai_ready_for_users"):
        gate = by_id.get("ai_safety_gate")
        if not gate:
            errors.append("AI app requires `ai_safety_gate`")
        elif claims.get("ai_ready_for_users") and str(gate.get("status") or "") not in GREEN_STATUSES:
            errors.append("AI app ready for users requires passed `ai_safety_gate`")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует standards-gates.yaml.")
    parser.add_argument("path", nargs="?", default="template-repo/template/.chatgpt/standards-gates.yaml")
    args = parser.parse_args()

    path = resolve_path(args.path)
    errors = validate(load_yaml(path))
    if errors:
        print("STANDARDS GATES НЕВАЛИДНЫ")
        for error in errors:
            print(f"- {error}")
        return 1
    print("STANDARDS GATES ВАЛИДНЫ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
