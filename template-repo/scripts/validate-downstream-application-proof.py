#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PASSED_STATUSES = {"passed", "pass"}
BLOCKED_STATUSES = {"blocked", "not_run", "not-run", "pending"}
PLACEHOLDER_MARKERS = {
    "",
    "unknown",
    "todo",
    "tbd",
    "missing",
    "not_run",
    "not-run",
    "{{integer_minutes}}",
    "{{integer_count}}",
    "{{integer_count_or_none}}",
}
REQUIRED_PASSED_FIELDS = {
    "downstream_repo",
    "app_image",
    "runtime_target",
    "healthcheck_url",
    "healthcheck_result",
    "migrations",
    "backup_result",
    "restore_result",
    "rollback_result",
    "sanitized_transcript",
    "secrets_boundary",
    "time_to_first_handoff_minutes",
    "handoff_rework_loops",
    "manual_interventions",
    "external_blockers",
    "deploy_result",
}
REQUIRED_EVIDENCE_KEYS = {
    "app_image_evidence",
    "healthcheck_evidence",
    "migrations_evidence",
    "backup_evidence",
    "restore_evidence",
    "rollback_evidence",
    "transcript_evidence",
    "secrets_boundary_evidence",
    "scorecard_evidence",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw in text.splitlines():
        match = re.match(r"^\s*([a-z0-9_]+):\s*(.*?)\s*$", raw)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def is_placeholder(value: str) -> bool:
    clean = value.strip().lower()
    return (
        clean in PLACEHOLDER_MARKERS
        or clean.startswith("{{")
        or clean.endswith("}}")
        or "placeholder" in clean
    )


def require_int(field: str, value: str, errors: list[str]) -> None:
    if not re.fullmatch(r"\d+", value.strip()):
        errors.append(f"`{field}` должен быть целым числом")


def validate_report(path: Path) -> list[str]:
    text = read_text(path)
    fields = parse_fields(text)
    errors: list[str] = []
    if not text.strip():
        return [f"{path}: report пустой"]

    status = fields.get("proof_status", "").lower()
    if status not in PASSED_STATUSES | BLOCKED_STATUSES:
        errors.append("`proof_status` должен быть `passed`, `blocked` или `not_run`")

    if status in PASSED_STATUSES:
        for field in sorted(REQUIRED_PASSED_FIELDS):
            if field not in fields:
                errors.append(f"missing field `{field}`")
            elif is_placeholder(fields[field]):
                errors.append(f"`{field}` содержит placeholder или пустое значение")

        app_image = fields.get("app_image", "")
        if app_image == "factory-template-placeholder-app:local":
            errors.append("passed proof не может использовать `factory-template-placeholder-app:local`")
        for field in ["healthcheck_result", "backup_result", "restore_result", "rollback_result", "deploy_result"]:
            if fields.get(field, "").lower() not in {"pass", "passed"}:
                errors.append(f"`{field}` должен быть pass/passed для passed proof")
        if fields.get("migrations", "").lower() not in {"pass", "passed", "not_applicable"}:
            errors.append("`migrations` должен быть pass/passed/not_applicable")
        if fields.get("sanitized_transcript", "").lower() not in {"included", "attached"}:
            errors.append("`sanitized_transcript` должен быть included/attached")
        if fields.get("secrets_boundary", "").lower() not in {"confirmed", "pass", "passed"}:
            errors.append("`secrets_boundary` должен быть confirmed/pass/passed")
        for field in ["time_to_first_handoff_minutes", "handoff_rework_loops", "manual_interventions", "external_blockers"]:
            require_int(field, fields.get(field, ""), errors)
        for key in sorted(REQUIRED_EVIDENCE_KEYS):
            value = fields.get(key, "")
            if is_placeholder(value) or len(value) < 8:
                errors.append(f"missing evidence `{key}`")
        if "```text" not in text:
            errors.append("sanitized transcript должен быть в fenced `text` block")
    else:
        if not fields.get("blocker_reason") or is_placeholder(fields.get("blocker_reason", "")):
            errors.append("blocked/not_run report должен содержать `blocker_reason`")
        for overclaim in ["deploy_result", "healthcheck_result", "backup_result", "restore_result", "rollback_result"]:
            if fields.get(overclaim, "").lower() in {"pass", "passed"}:
                errors.append(f"blocked/not_run report не может claim `{overclaim}: pass`")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет downstream application proof report и novice scorecard evidence.")
    parser.add_argument("reports", nargs="+", help="Markdown reports to validate.")
    args = parser.parse_args()

    errors: list[str] = []
    for item in args.reports:
        path = Path(item)
        if not path.exists():
            errors.append(f"report not found: {path}")
            continue
        errors.extend(f"{path}: {error}" for error in validate_report(path))

    if errors:
        print("DOWNSTREAM APPLICATION PROOF НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1

    print("DOWNSTREAM APPLICATION PROOF ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    sys.exit(main())

