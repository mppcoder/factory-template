#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from automation_run_ledger import append_entry


SCOPES = {
    "issue-fix",
    "high-risk",
    "auto-merge",
    "production-deploy",
    "security-fix",
    "public-submit",
    "parallel-runner",
    "destructive-rollback",
    "secret-access",
    "release-publication",
}
TRUSTED = {"admin", "maintain", "write", "trusted-bot"}


def fail(msg: str) -> None:
    raise SystemExit(f"automation-approval: {msg}")


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def approval_dir(root: Path) -> Path:
    return root / ".chatgpt/automation-approvals"


def approval_path(root: Path, approval_id: str) -> Path:
    return approval_dir(root) / f"{approval_id}.json"


def load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing approval: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid approval json: {exc}")
    return data if isinstance(data, dict) else {}


def validate_record(record: dict[str, Any], scope: str, target: str) -> tuple[bool, str]:
    if record.get("schema") != "automation-approval/v1":
        return False, "schema mismatch"
    if record.get("action_scope") != scope:
        return False, "scope mismatch"
    if str(record.get("target", "")) != str(target):
        return False, "target mismatch"
    status = record.get("status", "active")
    if status != "active":
        return False, f"approval is {status}"
    expires_at = record.get("expires_at")
    if expires_at:
        try:
            expiry = dt.datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        except ValueError:
            return False, "invalid expiry"
        if expiry <= dt.datetime.now(dt.timezone.utc):
            return False, "approval expired"
    return True, "approval valid"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Approval artifact CLI. Dry-run by default.")
    parser.add_argument("command", choices=["create", "validate", "consume"])
    parser.add_argument("--root", default=".")
    parser.add_argument("--scope", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--actor", default="unknown")
    parser.add_argument("--actor-permission", default="unknown")
    parser.add_argument("--approval-id")
    parser.add_argument("--expires-at")
    parser.add_argument("--single-use", action="store_true")
    parser.add_argument("--reason", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--ledger")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if args.scope not in SCOPES:
        fail("invalid scope")
    if args.actor_permission not in TRUSTED:
        fail("approval cannot be created or consumed by read/unknown actor")
    approval_id = args.approval_id or f"approval-{args.scope}-{args.target}".replace("/", "-").replace(":", "-")
    path = approval_path(root, approval_id)

    if args.command == "create":
        record = {
            "schema": "automation-approval/v1",
            "approval_id": approval_id,
            "action_scope": args.scope,
            "actor": args.actor,
            "actor_permission": args.actor_permission,
            "target": args.target,
            "expires_at": args.expires_at,
            "single_use": bool(args.single_use),
            "reason": args.reason,
            "created_at": now(),
            "consumed_at": None,
            "status": "active",
            "evidence": args.evidence,
        }
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if args.ledger:
                append_entry(Path(args.ledger), {"run_id": approval_id, "issue_or_task_id": args.target, "trigger": "approval-create", "actor": args.actor, "permission_decision": "approval-created", "approvals": [approval_id], "final_status": "approval_active"})
        print(f"approval_record={json.dumps(record, ensure_ascii=False, sort_keys=True)}")
        print(f"approval_path={path}")
        return 0

    record = load(path)
    ok, reason = validate_record(record, args.scope, args.target)
    if not ok:
        fail(reason)
    if args.command == "consume":
        if args.write:
            record["status"] = "consumed" if record.get("single_use") else "active"
            record["consumed_at"] = now()
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if args.ledger:
                append_entry(Path(args.ledger), {"run_id": approval_id, "issue_or_task_id": args.target, "trigger": "approval-consume", "actor": args.actor, "permission_decision": "approval-consumed", "approvals": [approval_id], "final_status": "approval_consumed"})
        print(f"approval_consumed={approval_id if args.write else 'dry-run'}")
        return 0
    print(f"approval_valid={approval_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
