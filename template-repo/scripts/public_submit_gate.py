#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from automation_run_ledger import append_entry
from permission_model import decide


SECRET_RE = re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*\S+")
PRIVATE_URL_RE = re.compile(r"https?://(?:localhost|127\.0\.0\.1|10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)")


def load(path: str | None) -> dict | None:
    return json.loads(Path(path).read_text(encoding="utf-8")) if path else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Disabled-by-default public external submit gate.")
    parser.add_argument("--body", required=True)
    parser.add_argument("--target-repo")
    parser.add_argument("--consent-file")
    parser.add_argument("--approval-file")
    parser.add_argument("--allow-raw-logs", action="store_true")
    parser.add_argument("--actor", default="local")
    parser.add_argument("--actor-permission", default="maintain")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--ledger")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    body = Path(args.body).read_text(encoding="utf-8")
    approval = load(args.approval_file)
    decision = decide("public-submit", args.actor, args.actor_permission, args.target_repo or "", approval)
    reasons: list[str] = []
    if not decision["allowed"]:
        reasons.append(decision["reason"])
    if not args.target_repo:
        reasons.append("target repo missing")
    if not args.consent_file or not Path(args.consent_file).exists():
        reasons.append("consent artifact missing")
    if SECRET_RE.search(body):
        reasons.append("secret-like content refused")
    if PRIVATE_URL_RE.search(body):
        reasons.append("private URL refused")
    if "RAW LOG" in body and not args.allow_raw_logs:
        reasons.append("raw logs require explicit sanitized allowance")
    allowed = not reasons
    if args.write:
        raise SystemExit("public-submit-gate: real public submit is outside verification and requires operator approval")
    preview = body[:1200]
    if args.ledger:
        append_entry(Path(args.ledger), {"run_id": f"public-submit-{args.target_repo or 'missing'}", "issue_or_task_id": args.target_repo or "missing", "trigger": "public-submit-gate", "actor": args.actor, "permission_decision": decision, "approvals": [approval.get("approval_id")] if approval else [], "public_submit_status": "would_submit" if allowed else "refused", "final_status": "dry_run_preview"})
    print(json.dumps({"allowed": allowed, "reasons": reasons, "preview": preview, "dry_run": True}, ensure_ascii=False, sort_keys=True))
    return 0 if allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
