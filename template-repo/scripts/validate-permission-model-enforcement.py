#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-permission-model-enforcement: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/permission_model.py"
    if not script.exists():
        fail("missing permission_model.py")
    proc = subprocess.run([sys.executable, str(script), "fixture"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        fail(proc.stderr.strip() or "fixture mode failed")
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        approval = tmp / "approval.json"
        approval.write_text(json.dumps({"schema": "automation-approval/v1", "approval_id": "A1", "action_scope": "high-risk", "target": "issue/9", "status": "active"}), encoding="utf-8")
        ok = subprocess.run([sys.executable, str(script), "check", "--scope", "high-risk", "--target", "issue/9", "--actor", "maint", "--actor-permission", "maintain", "--approval-file", str(approval)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if ok.returncode != 0:
            fail(ok.stderr.strip() or "matching approval refused")
        no = subprocess.run([sys.executable, str(script), "check", "--scope", "high-risk", "--target", "issue/9", "--actor", "maint", "--actor-permission", "maintain"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if no.returncode == 0:
            fail("high-risk without approval was allowed")
        read = subprocess.run([sys.executable, str(script), "check", "--scope", "issue-fix", "--target", "issue/1", "--actor", "reader", "--actor-permission", "read"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if read.returncode == 0:
            fail("read actor was allowed")
    print("validate-permission-model-enforcement=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
