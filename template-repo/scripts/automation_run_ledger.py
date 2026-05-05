#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret|private[_ -]?key)\s*[:=]\s*\S+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def scrub(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): scrub(v) for k, v in value.items()}
    if isinstance(value, list):
        return [scrub(v) for v in value]
    text = str(value)
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED-SECRET-LIKE-CONTENT]", text)
    return text


def append_entry(ledger: Path, entry: dict[str, Any]) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    safe_entry = scrub(entry)
    safe_entry.setdefault("schema", "automation-run-ledger-entry/v1")
    safe_entry.setdefault("run_id", safe_entry.get("issue_or_task_id", "unknown"))
    safe_entry.setdefault("parent_run_id", "")
    safe_entry.setdefault("issue_or_task_id", safe_entry.get("run_id", "unknown"))
    safe_entry.setdefault("actor", "unknown")
    safe_entry.setdefault("trigger", "manual")
    safe_entry.setdefault("permission_decision", safe_entry.get("gate_result", "unknown"))
    safe_entry.setdefault("approvals", [])
    safe_entry.setdefault("worktree", "")
    safe_entry.setdefault("branch", "")
    safe_entry.setdefault("commands", [safe_entry.get("launcher_command", "")])
    safe_entry.setdefault("verification", safe_entry.get("verification_commands_results", "pending"))
    safe_entry.setdefault("pr_url", "")
    safe_entry.setdefault("deploy_status", "")
    safe_entry.setdefault("public_submit_status", "")
    safe_entry.setdefault("rollback_plan", "")
    safe_entry.setdefault("blockers", "")
    safe_entry.setdefault("final_status", "pending")
    safe_entry.setdefault("timestamp_utc", dt.datetime.now(dt.timezone.utc).isoformat())
    previous_hash = ""
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    previous_hash = json.loads(line).get("current_entry_hash", "") or hashlib.sha256(line.encode("utf-8")).hexdigest()
                except json.JSONDecodeError:
                    previous_hash = hashlib.sha256(line.encode("utf-8")).hexdigest()
    safe_entry.setdefault("previous_entry_hash", previous_hash)
    payload = dict(safe_entry)
    payload.pop("current_entry_hash", None)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    safe_entry["current_entry_hash"] = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(safe_entry, ensure_ascii=False, sort_keys=True) + "\n")


def validate_entries(ledger: Path) -> list[str]:
    errors: list[str] = []
    previous_hash = ""
    for index, line in enumerate(ledger.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {index}: invalid json: {exc}")
            continue
        for field in [
            "run_id",
            "parent_run_id",
            "issue_or_task_id",
            "actor",
            "trigger",
            "permission_decision",
            "approvals",
            "worktree",
            "branch",
            "commands",
            "verification",
            "rollback_plan",
            "final_status",
            "timestamp_utc",
        ]:
            if field not in entry:
                errors.append(f"line {index}: missing {field}")
        if any(pattern.search(line) for pattern in SECRET_PATTERNS):
            errors.append(f"line {index}: secret-like string")
        if "current_entry_hash" in entry:
            if entry.get("previous_entry_hash", "") != previous_hash:
                errors.append(f"line {index}: hash chain previous mismatch")
            payload = dict(entry)
            current = payload.pop("current_entry_hash")
            expected = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
            if current != expected:
                errors.append(f"line {index}: current hash mismatch")
            previous_hash = current
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", default=".chatgpt/automation-runs/ledger.jsonl")
    parser.add_argument("command", nargs="?", choices=["append", "validate"], default="append")
    parser.add_argument("--issue")
    parser.add_argument("--task-id")
    parser.add_argument("--trigger", default="manual")
    parser.add_argument("--actor", default="unknown")
    parser.add_argument("--gate-result", default="unknown")
    parser.add_argument("--handoff-path", default="")
    parser.add_argument("--branch", default="")
    parser.add_argument("--launcher-command", default="")
    parser.add_argument("--verification", default="pending")
    parser.add_argument("--pr-url", default="")
    parser.add_argument("--blockers", default="")
    parser.add_argument("--final-status", default="pending")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "validate":
        errors = validate_entries(Path(args.ledger))
        if errors:
            raise SystemExit("automation_run_ledger: " + "; ".join(errors))
        print(f"automation_run_ledger_valid={args.ledger}")
        return 0
    append_entry(
        Path(args.ledger),
        {
            "issue_or_task_id": args.issue or args.task_id or "unknown",
            "trigger": args.trigger,
            "actor": args.actor,
            "gate_result": args.gate_result,
            "handoff_path": args.handoff_path,
            "branch": args.branch,
            "launcher_command": args.launcher_command,
            "verification_commands_results": args.verification,
            "pr_url": args.pr_url,
            "blockers": args.blockers,
            "final_status": args.final_status,
        },
    )
    print(f"automation_run_ledger={args.ledger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
