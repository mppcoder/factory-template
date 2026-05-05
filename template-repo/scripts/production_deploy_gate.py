#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from automation_run_ledger import append_entry
from permission_model import decide


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Disabled-by-default production deploy gate.")
    parser.add_argument("--target")
    parser.add_argument("--environment-approval", action="store_true")
    parser.add_argument("--safe-secrets-env", action="store_true")
    parser.add_argument("--health-check-plan")
    parser.add_argument("--rollback-plan")
    parser.add_argument("--labels", default="")
    parser.add_argument("--approval-file")
    parser.add_argument("--security-approval-file")
    parser.add_argument("--actor", default="local")
    parser.add_argument("--actor-permission", default="maintain")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--ledger")
    return parser.parse_args()


def load(path: str | None) -> dict | None:
    return json.loads(Path(path).read_text(encoding="utf-8")) if path else None


def main() -> int:
    args = parse_args()
    approval = load(args.approval_file)
    decision = decide("production-deploy", args.actor, args.actor_permission, args.target or "", approval)
    reasons: list[str] = []
    if not decision["allowed"]:
        reasons.append(decision["reason"])
    if not args.target:
        reasons.append("deploy target missing")
    if not args.environment_approval:
        reasons.append("environment approval missing")
    if not args.safe_secrets_env:
        reasons.append("secrets must come from safe environment")
    if not args.rollback_plan or not Path(args.rollback_plan).exists():
        reasons.append("rollback plan missing")
    if not args.health_check_plan or not Path(args.health_check_plan).exists():
        reasons.append("health check plan missing")
    if "security" in {x.strip() for x in args.labels.split(",")} and not args.security_approval_file:
        reasons.append("security-fix scope also required")
    allowed = not reasons
    if args.write:
        raise SystemExit("production-deploy-gate: real deploy is outside verification and requires operator approval")
    if args.ledger:
        append_entry(Path(args.ledger), {"run_id": f"deploy-{args.target or 'missing'}", "issue_or_task_id": args.target or "missing", "trigger": "production-deploy-gate", "actor": args.actor, "permission_decision": decision, "approvals": [approval.get("approval_id")] if approval else [], "deploy_status": "would_deploy" if allowed else "refused", "rollback_plan": args.rollback_plan or "", "final_status": "dry_run_plan"})
    print(json.dumps({"allowed": allowed, "reasons": reasons, "dry_run": True}, ensure_ascii=False, sort_keys=True))
    return 0 if allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
