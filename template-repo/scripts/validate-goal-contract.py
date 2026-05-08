#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ALLOWED_TRIGGERS = {
    "explicit_goal_command",
    "inferred_from_task",
    "handoff",
    "direct_codex_task",
}
ALLOWED_RUNTIME_RECOMMENDATIONS = {
    "goal_first_contract_only",
    "manual_review",
    "codex_goal_candidate",
    "codex_goal_enabled",
    "codex_goal_enabled_after_live_validation",
    "requires_feedback_setup",
    "not_recommended",
}
ALLOWED_GOAL_STATUSES = {
    "achieved",
    "unmet",
    "budget_limited",
    "tool_limited",
    "blocked",
    "not_applicable",
}
PROXY_SIGNALS = {
    "tests passed alone",
    "file exists alone",
    "commit exists alone",
    "green dashboard alone",
    "validator passed alone",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(nonempty(item) for item in value)
    return value is not None


def normalized_items(value: Any) -> list[str]:
    return [str(item).strip() for item in as_list(value) if str(item).strip()]


def is_proxy_only(items: list[str]) -> bool:
    if not items:
        return False
    lowered = [item.lower() for item in items]
    return all(any(proxy in item for proxy in PROXY_SIGNALS) for item in lowered)


def validate_contract(data: dict[str, Any], template_mode: bool = False) -> list[str]:
    errors: list[str] = []
    contract = as_dict(data.get("goal_contract"))
    if not contract:
        return ["YAML должен содержать mapping `goal_contract`"]

    if contract.get("version") != "goal-contract/v1":
        errors.append("goal_contract.version должен быть `goal-contract/v1`")

    source = as_dict(contract.get("goal_command_source"))
    outcome = as_dict(contract.get("outcome"))
    boundaries = as_dict(contract.get("boundaries"))
    validation = as_dict(contract.get("validation"))
    runtime = as_dict(contract.get("runtime"))
    continuation = as_dict(contract.get("continuation"))
    closeout = as_dict(contract.get("closeout"))
    intake = as_dict(contract.get("intake"))

    trigger = str(source.get("goal_first_trigger") or "").strip()
    if trigger and trigger not in ALLOWED_TRIGGERS:
        errors.append(f"goal_first_trigger `{trigger}` недопустим")

    clarification_required = bool(intake.get("clarification_required"))
    if clarification_required and not str(intake.get("clarifying_question") or "").strip():
        errors.append("clarification_required требует intake.clarifying_question")

    if not template_mode:
        if not nonempty(source.get("normalized_goal")):
            errors.append("goal_command_source.normalized_goal обязателен")
        if not clarification_required and not nonempty(outcome.get("definition_of_done")):
            errors.append("outcome.definition_of_done обязателен для не-vague goal")
        if not nonempty(outcome.get("evidence_required")):
            errors.append("outcome.evidence_required обязателен")
        if not nonempty(boundaries.get("scope")):
            errors.append("boundaries.scope обязателен")
        if not nonempty(boundaries.get("non_goals")):
            errors.append("boundaries.non_goals обязателен")

    for field in ["destructive_actions_allowed", "production_actions_allowed", "secrets_allowed"]:
        if field not in boundaries:
            errors.append(f"boundaries.{field} обязателен")
        elif boundaries.get(field) is not False:
            errors.append(f"boundaries.{field} должен быть false by default")

    denylist = set(normalized_items(validation.get("proxy_signal_denylist")))
    for proxy in PROXY_SIGNALS:
        if proxy not in denylist:
            errors.append(f"validation.proxy_signal_denylist не содержит `{proxy}`")
    if "evidence satisfies DoD" not in str(validation.get("goal_achievement_rule") or ""):
        errors.append("validation.goal_achievement_rule должен запрещать proxy-only closure")

    evidence_required = normalized_items(outcome.get("evidence_required"))
    if is_proxy_only(evidence_required):
        errors.append("outcome.evidence_required не может состоять только из proxy signals")

    runtime_rec = str(runtime.get("goal_runtime_recommendation") or "").strip()
    if runtime_rec and runtime_rec not in ALLOWED_RUNTIME_RECOMMENDATIONS:
        errors.append(f"runtime.goal_runtime_recommendation `{runtime_rec}` недопустим")
    if runtime_rec in {"codex_goal_enabled", "codex_goal_enabled_after_live_validation"}:
        if not str(runtime.get("codex_goal_live_validation_evidence") or "").strip():
            errors.append("codex_goal_enabled требует runtime.codex_goal_live_validation_evidence")
        if not runtime.get("tool_feedback_ready"):
            errors.append("codex_goal_enabled требует runtime.tool_feedback_ready: true")
    if runtime_rec == "requires_feedback_setup" and runtime.get("tool_feedback_ready"):
        errors.append("requires_feedback_setup несовместим с tool_feedback_ready: true")

    budget = as_dict(runtime.get("budget_guardrails"))
    stop_when = set(normalized_items(budget.get("stop_when")))
    for stop in ["budget_limited", "tool_limited", "quota_wall", "goal_drift", "unsafe_action"]:
        if stop not in stop_when:
            errors.append(f"runtime.budget_guardrails.stop_when не содержит `{stop}`")

    if not as_dict(runtime.get("pause_resume_policy")).get("user_controls_lifecycle"):
        errors.append("runtime.pause_resume_policy.user_controls_lifecycle должен быть true")
    if not as_dict(contract.get("side_channel")).get("must_not_mutate_goal_without_confirmation"):
        errors.append("side_channel.must_not_mutate_goal_without_confirmation должен быть true")

    if "if_budget_limited" not in continuation:
        errors.append("continuation.if_budget_limited обязателен")

    status = str(closeout.get("goal_status") or "not_applicable").strip()
    if status not in ALLOWED_GOAL_STATUSES:
        errors.append(f"closeout.goal_status `{status}` недопустим")
    evidence_vs_dod = normalized_items(closeout.get("evidence_vs_dod"))
    if status == "achieved":
        if not evidence_vs_dod:
            errors.append("achieved требует closeout.evidence_vs_dod")
        if closeout.get("proxy_signal_closure_used") is not False:
            errors.append("achieved запрещен при proxy_signal_closure_used")
        if is_proxy_only(evidence_vs_dod):
            errors.append("achieved не может опираться только на proxy signals")
    if status == "budget_limited":
        summary = as_dict(closeout.get("continuation_summary"))
        for field in ["done", "remaining", "blockers", "next_recommended_goal"]:
            if not nonempty(summary.get(field)):
                errors.append(f"budget_limited требует closeout.continuation_summary.{field}")

    if clarification_required and runtime_rec in {"codex_goal_enabled", "codex_goal_enabled_after_live_validation"}:
        errors.append("vague goal requiring clarification не может быть codex_goal_enabled")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate goal-contract YAML.")
    parser.add_argument("path")
    parser.add_argument("--template", action="store_true", help="Allow empty template placeholders while validating schema/guardrails.")
    args = parser.parse_args()

    path = Path(args.path)
    errors = validate_contract(load_yaml(path), template_mode=args.template)
    if errors:
        print("GOAL CONTRACT НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("GOAL CONTRACT ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
