#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_FIELDS = {
    "issue_or_task_id",
    "trigger",
    "actor",
    "gate_result",
    "handoff_path",
    "branch",
    "launcher_command",
    "verification_commands_results",
    "pr_url",
    "blockers",
    "final_status",
    "timestamp_utc",
}


def fail(msg: str) -> None:
    raise SystemExit(f"validate-automation-run-ledger: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    for path in [
        root / ".chatgpt/automation-runs/README.md",
        root / "template-repo/scripts/automation_run_ledger.py",
        root / "docs/operator/factory-template/automation-audit-log.md",
    ]:
        if not path.exists():
            fail(f"missing {path}")
    docs = (root / ".chatgpt/automation-runs/README.md").read_text(encoding="utf-8")
    docs += "\n" + (root / "docs/operator/factory-template/automation-audit-log.md").read_text(encoding="utf-8")
    for marker in sorted(REQUIRED_FIELDS - {"timestamp_utc"}):
        if marker not in docs:
            fail(f"ledger field missing from docs: {marker}")
    if "no secrets" not in docs or "append-only" not in docs:
        fail("ledger docs must state append-only and no secrets")

    with tempfile.TemporaryDirectory() as tmp_raw:
        ledger = Path(tmp_raw) / "ledger.jsonl"
        proc = subprocess.run(
            [
                sys.executable,
                str((root / "template-repo/scripts/automation_run_ledger.py").resolve()),
                "--ledger",
                str(ledger),
                "--issue",
                "101",
                "--trigger",
                "validator-smoke",
                "--actor",
                "maintainer",
                "--gate-result",
                "eligible",
                "--handoff-path",
                "codex-input.md",
                "--branch",
                "codex/issue-101",
                "--launcher-command",
                "bounded-task-runner --dry-run",
                "--verification",
                "quick=pass",
                "--final-status",
                "dry_run_complete",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            fail(proc.stderr or "ledger helper failed")
        line = ledger.read_text(encoding="utf-8").strip()
        entry = json.loads(line)
        missing = sorted(REQUIRED_FIELDS - set(entry))
        if missing:
            fail("ledger entry missing fields: " + ", ".join(missing))
        if "API_KEY=" in line or "password=" in line:
            fail("ledger contains secret-like value")
    print("validate-automation-run-ledger=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
