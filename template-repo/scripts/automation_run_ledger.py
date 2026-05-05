#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
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
    safe_entry.setdefault("timestamp_utc", dt.datetime.now(dt.timezone.utc).isoformat())
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(safe_entry, ensure_ascii=False, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", default=".chatgpt/automation-runs/ledger.jsonl")
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
