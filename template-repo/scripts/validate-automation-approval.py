#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-automation-approval: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/automation-approval.py"
    docs = [
        root / ".chatgpt/automation-approvals/README.md",
        root / "docs/operator/factory-template/automation-approval.md",
        root / "template-repo/template/docs/operator/automation-approval.md",
    ]
    if not script.exists():
        fail("missing automation-approval.py")
    text = script.read_text(encoding="utf-8")
    for doc in docs:
        if not doc.exists():
            fail(f"missing {doc}")
        text += "\n" + doc.read_text(encoding="utf-8")
    for marker in ["automation-approval/v1", "single_use", "expires_at", "status: active/consumed/expired/revoked", "public-submit", "production-deploy"]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        create = subprocess.run([sys.executable, str(script), "create", "--root", str(tmp), "--scope", "parallel-runner", "--target", "task/FT-TASK-0001", "--actor", "maint", "--actor-permission", "maintain", "--approval-id", "A1", "--single-use", "--reason", "fixture", "--write"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if create.returncode != 0:
            fail(create.stderr.strip() or "create failed")
        valid = subprocess.run([sys.executable, str(script), "validate", "--root", str(tmp), "--scope", "parallel-runner", "--target", "task/FT-TASK-0001", "--actor", "maint", "--actor-permission", "maintain", "--approval-id", "A1"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if valid.returncode != 0:
            fail(valid.stderr.strip() or "validate failed")
        consume = subprocess.run([sys.executable, str(script), "consume", "--root", str(tmp), "--scope", "parallel-runner", "--target", "task/FT-TASK-0001", "--actor", "maint", "--actor-permission", "maintain", "--approval-id", "A1", "--write"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if consume.returncode != 0:
            fail(consume.stderr.strip() or "consume failed")
        consumed = subprocess.run([sys.executable, str(script), "validate", "--root", str(tmp), "--scope", "parallel-runner", "--target", "task/FT-TASK-0001", "--actor", "maint", "--actor-permission", "maintain", "--approval-id", "A1"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if consumed.returncode == 0:
            fail("consumed approval was accepted")
        expired_path = tmp / ".chatgpt/automation-approvals/EXPIRED.json"
        expired_path.parent.mkdir(parents=True, exist_ok=True)
        expired_path.write_text(json.dumps({"schema": "automation-approval/v1", "approval_id": "EXPIRED", "action_scope": "auto-merge", "target": "PR-1", "status": "active", "expires_at": (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).isoformat()}), encoding="utf-8")
        expired = subprocess.run([sys.executable, str(script), "validate", "--root", str(tmp), "--scope", "auto-merge", "--target", "PR-1", "--actor", "maint", "--actor-permission", "maintain", "--approval-id", "EXPIRED"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if expired.returncode == 0:
            fail("expired approval was accepted")
    print("validate-automation-approval=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
