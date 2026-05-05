#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from automation_run_ledger import append_entry
from permission_model import decide


def fail(msg: str) -> None:
    raise SystemExit(f"auto-merge-gate: {msg}")


def load(path: str | None) -> dict | None:
    return json.loads(Path(path).read_text(encoding="utf-8")) if path else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Disabled-by-default auto-merge gate.")
    parser.add_argument("--pr", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--checks", choices=["green", "red", "pending"], default="pending")
    parser.add_argument("--labels", default="")
    parser.add_argument("--conflicts", action="store_true")
    parser.add_argument("--human-review-unresolved", action="store_true")
    parser.add_argument("--rollback-plan", required=True)
    parser.add_argument("--approval-file")
    parser.add_argument("--actor", default="local")
    parser.add_argument("--actor-permission", default="maintain")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--ledger")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reasons: list[str] = []
    labels = {x.strip() for x in args.labels.split(",") if x.strip()}
    approval = load(args.approval_file)
    decision = decide("auto-merge", args.actor, args.actor_permission, args.pr, approval)
    if not decision["allowed"]:
        reasons.append(decision["reason"])
    if not args.branch.startswith("codex/"):
        reasons.append("PR must come from automation branch")
    if args.checks != "green":
        reasons.append("checks are not green")
    if labels & {"security", "external-secret"}:
        reasons.append("security/external-secret labels require refusal")
    if args.human_review_unresolved or "needs-human" in labels:
        reasons.append("unresolved human review")
    if args.conflicts:
        reasons.append("merge conflicts")
    if not Path(args.rollback_plan).exists():
        reasons.append("rollback plan missing")
    allowed = not reasons
    if args.write and not allowed:
        fail("; ".join(reasons))
    if args.write:
        fail("real merge intentionally not implemented in verification substrate")
    if args.ledger:
        append_entry(Path(args.ledger), {"run_id": f"auto-merge-{args.pr}", "issue_or_task_id": args.pr, "trigger": "auto-merge-gate", "actor": args.actor, "permission_decision": decision, "approvals": [approval.get("approval_id")] if approval else [], "branch": args.branch, "rollback_plan": args.rollback_plan, "final_status": "would_merge" if allowed else "refused"})
    print(json.dumps({"allowed": allowed, "reasons": reasons, "dry_run": True}, ensure_ascii=False, sort_keys=True))
    return 0 if allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
