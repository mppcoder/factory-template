#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from automation_run_ledger import append_entry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue")
    parser.add_argument("--task-id")
    parser.add_argument("--branch", default="")
    parser.add_argument("--pr-url", default="")
    parser.add_argument("--label", default="")
    parser.add_argument("--task-status", default="")
    parser.add_argument("--deploy-id", default="")
    parser.add_argument("--public-submit-url", default="")
    parser.add_argument("--security-report-id", default="")
    parser.add_argument("--output", required=True)
    parser.add_argument("--ledger")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ident = args.issue or args.task_id or "manual-run"
    text = f"""# Automation rollback dry-run plan

- run: `{ident}`
- branch: `{args.branch or 'not-created'}`
- pr_url: `{args.pr_url or 'not-created'}`
- failed run: stop runner, mark `agent:blocked`, append ledger blocker.
- bad branch: close PR if present, delete automation branch after review, do not rewrite `main`.
- bad PR: convert to draft or close; leave audit trail and verification output.
- label reset: remove `agent:running`, keep `agent:blocked` until human review clears it.
- wrong labels: dry-run removal/addition plan only; live label mutation requires explicit approval.
- task status reset: move FT-TASK back to `blocked` or `ready_for_handoff` with reason.
- wrong task status: dry-run status correction plan only; append new state, never erase history.
- failed deploy: stop rollout, run health check, follow environment rollback procedure after human deploy approval.
- bad public submit: prepare correction/close/update plan; no public mutation without public-submit approval.
- security false positive: close private security workflow with sanitized audit entry and no public disclosure.
- run.yaml correction: write a new corrected run state; keep previous ledger entries append-only.
- no main rewrite: never use force-push or history rewrite on `main`.
- destructive cleanup requires explicit destructive-rollback approval.
"""
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if args.ledger:
        append_entry(
            Path(args.ledger),
            {
                "run_id": f"rollback-{ident}",
                "issue_or_task_id": ident,
                "trigger": "rollback-plan",
                "actor": "local",
                "permission_decision": "dry-run-plan-only",
                "commands": ["dry-run rollback plan generated"],
                "rollback_plan": str(path),
                "final_status": "rollback_plan_created",
            },
        )
    print(f"rollback_plan={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
