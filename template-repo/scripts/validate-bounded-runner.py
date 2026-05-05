#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import json
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-bounded-runner: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/bounded-task-runner.py"
    doc = root / "docs/operator/factory-template/bounded-runner.md"
    if not script.exists():
        fail("missing bounded-task-runner.py")
    if not doc.exists():
        fail("missing bounded runner docs")
    text = script.read_text(encoding="utf-8") + "\n" + doc.read_text(encoding="utf-8")
    for marker in [
        "--source",
        "--queue",
        "--dry-run",
        "--write",
        "--one",
        "--max-concurrency",
        "--allow-parallel",
        "--no-push",
        "--no-pr",
        "no auto-merge",
        "no production deploy",
        "security/external-secret",
        "launcher_command",
        "rollback_plan",
    ]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    script_abs = script.resolve()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        proc = subprocess.run(
            [sys.executable, str(script_abs), "--task-id", "FT-TASK-0002", "--one"],
            cwd=tmp,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            fail(proc.stderr.strip() or "dry-run smoke failed")
        if "bounded_runner_status=dry_run_planned" not in proc.stdout:
            fail("dry-run smoke did not report planned status")
        bad = subprocess.run(
            [sys.executable, str(script_abs), "--task-id", "FT-TASK-0002", "--one", "--labels", "security"],
            cwd=tmp,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if bad.returncode == 0:
            fail("security label was not refused")
        approval = tmp_path / "parallel-approval.json"
        approval.write_text(
            json.dumps(
                {
                    "schema": "automation-approval/v1",
                    "approval_id": "PARALLEL-1",
                    "action_scope": "parallel-runner",
                    "target": "task/FT-TASK-0002",
                    "status": "active",
                }
            ),
            encoding="utf-8",
        )
        # Parallel without approval must be refused even before validator checks.
        refused = subprocess.run(
            [sys.executable, str(script_abs), "--source", "task", "--task-id", "FT-TASK-0002", "--max-concurrency", "2", "--allow-parallel"],
            cwd=tmp,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if refused.returncode == 0:
            fail("parallel without approval was allowed")
    print("validate-bounded-runner=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
