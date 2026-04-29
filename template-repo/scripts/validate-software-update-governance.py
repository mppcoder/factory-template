#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


INVENTORY_SCHEMA = "software-inventory/v1"
WATCHLIST_SCHEMA = "software-update-watchlist/v1"
READINESS_SCHEMA = "software-update-readiness/v1"
AUTO_UPDATE_POLICY = "manual-approved-upgrade"
IMPACT_CLASSIFICATIONS = {
    "not_relevant",
    "monitor_only",
    "security_relevant",
    "feature_relevant",
    "breaking_change_risk",
    "runtime_conflict_risk",
    "upgrade_candidate",
    "blocked",
}
OWNER_BOUNDARIES = {
    "internal-repo-follow-up",
    "external-user-action",
    "runtime-action",
    "downstream-battle-action",
    "secret-boundary-blocker",
}
GREEN_STATUSES = {"passed", "completed", "done", "ready", "archived"}
SECRET_RE = re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+")
LATEST_IMAGE_RE = re.compile(r"(?im)^\s*image:\s*['\"]?[^#\s'\"]+:latest['\"]?\s*(?:#.*)?$")
UNTAGGED_IMAGE_RE = re.compile(r"(?im)^\s*image:\s*['\"]?[^#\s:'\"]+/[^#\s:'\"]+['\"]?\s*(?:#.*)?$")
FLOATING_ACTION_RE = re.compile(r"(?im)^\s*uses:\s*[^@\s]+/(?:[^@\s]+)@(main|master)\s*(?:#.*)?$")
FROM_FLOATING_RE = re.compile(r"(?im)^\s*FROM\s+[^@\s:]+(?:\s+AS\s+\S+)?\s*$")
FORBIDDEN_PROMISES = [
    re.compile(r"(?i)background monitoring"),
    re.compile(r"(?i)automatic upgrade"),
    re.compile(r"(?i)auto-upgrade"),
    re.compile(r"(?i)автоматическ[а-я ]+обнов"),
    re.compile(r"(?i)фон(овый|овая|овое|овые) мониторинг"),
]


def load_yaml(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"отсутствует `{path}`")
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        errors.append(f"`{path}` должен быть YAML mapping")
        return {}
    dumped = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    if SECRET_RE.search(dumped) or "-----BEGIN" in dumped:
        errors.append(f"`{path}` содержит secret-like content")
    return data


def as_mapping(data: dict[str, Any], key: str, path: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{path}.{key} должен быть mapping")
        return {}
    return value


def as_list(data: dict[str, Any], key: str, path: str, errors: list[str]) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"{path}.{key} должен быть list")
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


def validate_action(item: Any, path: str, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"{path} должен быть mapping")
        return
    boundary = str(item.get("owner_boundary") or "")
    if boundary not in OWNER_BOUNDARIES:
        errors.append(f"{path}.owner_boundary имеет неизвестное значение")
    if not str(item.get("action") or "").strip():
        errors.append(f"{path}.action обязателен")
    if str(item.get("status") or "") in GREEN_STATUSES and not has_evidence(item):
        errors.append(f"{path} отмечен green без evidence/accepted_reason")


def validate_inventory(root: Path, data: dict[str, Any], errors: list[str]) -> None:
    path = ".chatgpt/software-inventory.yaml"
    if data.get("schema") != INVENTORY_SCHEMA:
        errors.append(f"{path}.schema должен быть `{INVENTORY_SCHEMA}`")
    if data.get("auto_update_policy") != AUTO_UPDATE_POLICY:
        errors.append(f"{path}.auto_update_policy должен быть `{AUTO_UPDATE_POLICY}`")
    if data.get("auto_install_without_approval") != "forbidden":
        errors.append(f"{path}.auto_install_without_approval должен быть `forbidden`")
    if data.get("strict_controlled_mode") is not True:
        errors.append(f"{path}.strict_controlled_mode должен быть true")

    baseline = as_mapping(data, "baseline", path, errors)
    for key in ["status", "recorded_at", "evidence", "os", "package_manager", "runtime_stack", "github_actions", "docker_images", "package_lockfiles", "critical_runtime_dependencies"]:
        if key not in baseline:
            errors.append(f"{path}.baseline.{key} обязателен")
    if str(baseline.get("status") or "") in GREEN_STATUSES and not has_evidence(baseline):
        errors.append(f"{path}.baseline отмечен green без evidence/accepted_reason")

    os_data = as_mapping(baseline, "os", f"{path}.baseline", errors)
    for key in ["distro_name", "version", "codename", "provider_image_id", "kernel", "selected_ubuntu_lts_release", "later_package_update_state"]:
        if key not in os_data:
            errors.append(f"{path}.baseline.os.{key} обязателен")

    package_manager = as_mapping(baseline, "package_manager", f"{path}.baseline", errors)
    unattended = as_mapping(package_manager, "unattended_upgrades", f"{path}.baseline.package_manager", errors)
    for key in ["installed", "enabled", "apt_timers", "policy_exception"]:
        if key not in unattended:
            errors.append(f"{path}.baseline.package_manager.unattended_upgrades.{key} обязателен")
    if not isinstance(package_manager.get("sources", []), list):
        errors.append(f"{path}.baseline.package_manager.sources должен быть list")

    for key in ["docker_version", "docker_compose_version", "node_version", "python_version"]:
        if key not in as_mapping(baseline, "runtime_stack", f"{path}.baseline", errors):
            errors.append(f"{path}.baseline.runtime_stack.{key} обязателен")
    if not isinstance(baseline.get("package_lockfiles", []), list):
        errors.append(f"{path}.baseline.package_lockfiles должен быть list")
    if not isinstance(baseline.get("critical_runtime_dependencies", []), list):
        errors.append(f"{path}.baseline.critical_runtime_dependencies должен быть list")


def validate_watchlist(data: dict[str, Any], errors: list[str]) -> None:
    path = ".chatgpt/software-update-watchlist.yaml"
    if data.get("schema") != WATCHLIST_SCHEMA:
        errors.append(f"{path}.schema должен быть `{WATCHLIST_SCHEMA}`")
    if not str(data.get("check_cadence") or "").strip():
        errors.append(f"{path}.check_cadence обязателен")
    if not isinstance(data.get("relevant_findings_count", 0), int):
        errors.append(f"{path}.relevant_findings_count должен быть integer")
    components = as_list(data, "watched_components", path, errors)
    if not components:
        errors.append(f"{path}.watched_components должен быть непустым")
    for index, component in enumerate(components, 1):
        if not isinstance(component, dict):
            errors.append(f"{path}.watched_components[{index}] должен быть mapping")
            continue
        prefix = f"{path}.watched_components[{component.get('id') or index}]"
        for key in [
            "id",
            "name",
            "official_docs_source",
            "release_notes_source",
            "security_advisory_source",
            "issue_tracker_source",
            "secondary_signals",
            "check_cadence",
            "last_checked_at",
            "last_relevant_finding",
            "project_impact_classification",
        ]:
            if key not in component:
                errors.append(f"{prefix}.{key} обязателен")
        for source_key in ["official_docs_source", "release_notes_source", "security_advisory_source", "issue_tracker_source"]:
            source = component.get(source_key)
            if not isinstance(source, dict) or not str(source.get("name") or "").strip() or not str(source.get("url") or "").startswith("https://"):
                errors.append(f"{prefix}.{source_key} должен содержать name и https url")
        classification = str(component.get("project_impact_classification") or "")
        if classification not in IMPACT_CLASSIFICATIONS:
            errors.append(f"{prefix}.project_impact_classification неизвестен: `{classification}`")


def validate_readiness(data: dict[str, Any], errors: list[str]) -> None:
    path = ".chatgpt/software-update-readiness.yaml"
    if data.get("schema") != READINESS_SCHEMA:
        errors.append(f"{path}.schema должен быть `{READINESS_SCHEMA}`")
    if data.get("auto_update_policy") != AUTO_UPDATE_POLICY:
        errors.append(f"{path}.auto_update_policy должен быть `{AUTO_UPDATE_POLICY}`")
    if data.get("auto_upgrade_allowed") is not False:
        errors.append(f"{path}.auto_upgrade_allowed должен быть false")
    if data.get("user_approval_required") is not True:
        errors.append(f"{path}.user_approval_required должен быть true")
    if not isinstance(data.get("relevant_findings_count", 0), int):
        errors.append(f"{path}.relevant_findings_count должен быть integer")
    if str(data.get("status") or "") in GREEN_STATUSES and not has_evidence(data):
        errors.append(f"{path} отмечен green без evidence/accepted_reason")
    validate_action(data.get("next_safe_action"), f"{path}.next_safe_action", errors)
    validate_action(data.get("fallback_action"), f"{path}.fallback_action", errors)
    if not isinstance(data.get("blockers", []), list):
        errors.append(f"{path}.blockers должен быть list")

    proposal = as_mapping(data, "upgrade_proposal", path, errors)
    for key in [
        "current_version",
        "target_version",
        "reason",
        "project_relevance",
        "affected_layers",
        "required_backups",
        "restore_rollback_plan",
        "test_matrix",
        "user_approval_gate",
        "rollout_plan",
        "post_upgrade_monitoring",
        "fallback_decision",
        "evidence",
    ]:
        if key not in proposal:
            errors.append(f"{path}.upgrade_proposal.{key} обязателен")
    approval = as_mapping(proposal, "user_approval_gate", f"{path}.upgrade_proposal", errors)
    if approval.get("required") is not True:
        errors.append(f"{path}.upgrade_proposal.user_approval_gate.required должен быть true")


def validate_dashboard(data: dict[str, Any], errors: list[str]) -> None:
    dashboard = data.get("software_update_governance")
    if not isinstance(dashboard, dict):
        errors.append("project-lifecycle-dashboard.yaml должен содержать software_update_governance")
        return
    if dashboard.get("auto_update_policy") != AUTO_UPDATE_POLICY:
        errors.append("dashboard software_update_governance.auto_update_policy должен быть manual-approved-upgrade")
    if not isinstance(dashboard.get("relevant_findings_count", 0), int):
        errors.append("dashboard software_update_governance.relevant_findings_count должен быть integer")
    for key in ["baseline_status", "last_update_intelligence_check", "upgrade_proposal_status", "next_safe_action", "fallback_action", "blockers", "source_artifacts"]:
        if key not in dashboard:
            errors.append(f"dashboard software_update_governance.{key} обязателен")
    validate_action(dashboard.get("next_safe_action"), "dashboard software_update_governance.next_safe_action", errors)
    validate_action(dashboard.get("fallback_action"), "dashboard software_update_governance.fallback_action", errors)


def validate_no_fake_promises(root: Path, errors: list[str]) -> None:
    paths = [
        root / "docs/operator/software-update-governance.md",
        root / "template-repo/template/reports/software-updates/README.md",
    ]
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PROMISES:
            match = pattern.search(text)
            if match:
                window = text[max(0, match.start() - 120) : match.end() + 120].lower()
                if "не " not in window and "not " not in window and "без реального" not in window:
                    errors.append(f"`{path}` содержит возможное обещание fake monitoring/auto-upgrade: {match.group(0)}")


def validate_floating_production_refs(root: Path, errors: list[str]) -> None:
    candidates: list[Path] = []
    for rel in ["deploy", ".github/workflows", "template-repo/template/deploy"]:
        base = root / rel
        if base.exists():
            candidates.extend([p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in {".yml", ".yaml", ".dockerfile"}])
            candidates.extend([p for p in base.rglob("Dockerfile*") if p.is_file()])
    for path in sorted(set(candidates)):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if LATEST_IMAGE_RE.search(text):
            errors.append(f"`{path}` содержит production-critical Docker image с `:latest`")
        if UNTAGGED_IMAGE_RE.search(text):
            errors.append(f"`{path}` содержит Docker image без явного tag/digest")
        if FLOATING_ACTION_RE.search(text):
            errors.append(f"`{path}` содержит GitHub Actions floating ref `@main`/`@master`")
        if FROM_FLOATING_RE.search(text):
            errors.append(f"`{path}` содержит Dockerfile FROM без tag/digest")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    inventory = load_yaml(root / ".chatgpt/software-inventory.yaml", errors)
    watchlist = load_yaml(root / ".chatgpt/software-update-watchlist.yaml", errors)
    readiness = load_yaml(root / ".chatgpt/software-update-readiness.yaml", errors)

    if inventory:
        validate_inventory(root, inventory, errors)
    if watchlist:
        validate_watchlist(watchlist, errors)
    if readiness:
        validate_readiness(readiness, errors)

    dashboard_path = root / ".chatgpt/project-lifecycle-dashboard.yaml"
    if not dashboard_path.exists():
        dashboard_path = root / "template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml"
    dashboard = load_yaml(dashboard_path, errors)
    if dashboard:
        validate_dashboard(dashboard, errors)

    readme = root / "reports/software-updates/README.md"
    if not readme.exists():
        readme = root / "template-repo/template/reports/software-updates/README.md"
    if not readme.exists():
        errors.append("отсутствует reports/software-updates/README.md")
    elif SECRET_RE.search(readme.read_text(encoding="utf-8")):
        errors.append("reports/software-updates/README.md содержит secret-like content")

    validate_no_fake_promises(root, errors)
    validate_floating_production_refs(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидирует controlled software update governance artifacts.")
    parser.add_argument("root", nargs="?", default=".", help="Factory root или generated project root.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    errors = validate(root)
    if errors:
        print("SOFTWARE UPDATE GOVERNANCE НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("SOFTWARE UPDATE GOVERNANCE ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
