#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue")
    parser.add_argument("--task-id")
    parser.add_argument("--branch", default="")
    parser.add_argument("--pr-url", default="")
    parser.add_argument("--output", required=True)
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
- task status reset: move FT-TASK back to `blocked` or `ready_for_handoff` with reason.
- run.yaml correction: write a new corrected run state; keep previous ledger entries append-only.
- no main rewrite: never use force-push or history rewrite on `main`.
"""
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"rollback_plan={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
