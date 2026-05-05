#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from automation_run_ledger import append_entry


TRUSTED_ROLES = {"admin", "maintain", "write", "trusted-bot"}
REFUSED_ROLES = {"read", "unknown", ""}
SCOPES = {
    "issue-fix",
    "high-risk",
    "auto-merge",
    "production-deploy",
    "security-fix",
    "public-submit",
    "parallel-runner",
}
DANGEROUS_SCOPES = SCOPES - {"issue-fix"}


def fail(msg: str) -> None:
    raise SystemExit(f"permission-model: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing approval artifact: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid approval json: {exc}")
    return data if isinstance(data, dict) else {}


def github_permission(actor: str, repo: str) -> str:
    if not os.environ.get("GH_TOKEN"):
        fail("gh mode requires GH_TOKEN")
    proc = subprocess.run(
        ["gh", "api", f"repos/{repo}/collaborators/{actor}/permission", "--jq", ".permission"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(proc.stderr.strip() or "gh permission lookup failed")
    return proc.stdout.strip() or "unknown"


def decide(scope: str, actor: str, actor_permission: str, target: str, approval: dict[str, Any] | None = None) -> dict[str, Any]:
    if scope not in SCOPES:
        return {"allowed": False, "reason": "invalid scope", "scope": scope}
    role = (actor_permission or "unknown").strip()
    if role in REFUSED_ROLES or role not in TRUSTED_ROLES:
        return {"allowed": False, "reason": "actor permission refused", "scope": scope, "actor": actor, "actor_permission": role}
    if scope in DANGEROUS_SCOPES:
        if not approval:
            return {"allowed": False, "reason": "missing explicit approval artifact", "scope": scope, "actor": actor, "actor_permission": role}
        if approval.get("action_scope") != scope:
            return {"allowed": False, "reason": "approval scope mismatch", "scope": scope, "approval_scope": approval.get("action_scope")}
        if str(approval.get("target", "")) != str(target):
            return {"allowed": False, "reason": "approval target mismatch", "scope": scope, "target": target}
        if approval.get("status") not in {"active", None}:
            return {"allowed": False, "reason": "approval is not active", "scope": scope, "status": approval.get("status")}
    return {"allowed": True, "reason": "permission and approval requirements satisfied", "scope": scope, "actor": actor, "actor_permission": role}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Offline-first permission model enforcement.")
    parser.add_argument("command", choices=["check", "fixture"])
    parser.add_argument("--scope", default="issue-fix")
    parser.add_argument("--target", default="local")
    parser.add_argument("--actor", default="unknown")
    parser.add_argument("--actor-permission", default="unknown")
    parser.add_argument("--approval-file")
    parser.add_argument("--gh-repo")
    parser.add_argument("--ledger")
    return parser.parse_args()


def run_fixtures() -> int:
    active = {
        "schema": "automation-approval/v1",
        "approval_id": "APPROVAL-fixture",
        "action_scope": "parallel-runner",
        "target": "task/FT-TASK-0001",
        "status": "active",
    }
    cases = [
        (decide("issue-fix", "dev", "write", "issue/1"), True),
        (decide("issue-fix", "reader", "read", "issue/1"), False),
        (decide("high-risk", "dev", "write", "issue/2"), False),
        (decide("parallel-runner", "maint", "maintain", "task/FT-TASK-0001", active), True),
        (decide("parallel-runner", "maint", "maintain", "task/OTHER", active), False),
    ]
    for decision, expected in cases:
        if bool(decision["allowed"]) != expected:
            fail(f"fixture failed: {decision}")
    print("permission_model_fixtures=ok")
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "fixture":
        return run_fixtures()
    role = github_permission(args.actor, args.gh_repo) if args.gh_repo else args.actor_permission
    approval = load_json(Path(args.approval_file)) if args.approval_file else None
    decision = decide(args.scope, args.actor, role, args.target, approval)
    if args.ledger:
        append_entry(
            Path(args.ledger),
            {
                "run_id": f"permission-{args.scope}-{args.target}",
                "issue_or_task_id": args.target,
                "trigger": "permission-model",
                "actor": args.actor,
                "permission_decision": decision,
                "approvals": [approval.get("approval_id")] if approval else [],
                "gate_result": "allowed" if decision["allowed"] else "refused",
                "final_status": "permission_checked",
            },
        )
    print(json.dumps(decision, ensure_ascii=False, sort_keys=True))
    return 0 if decision["allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
