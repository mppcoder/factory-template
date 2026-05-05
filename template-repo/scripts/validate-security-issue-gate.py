#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-security-issue-gate: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/security_issue_gate.py"
    docs = [root / "SECURITY.md", root / "template-repo/template/SECURITY.md", root / "docs/operator/factory-template/security-issue-gate.md", root / "template-repo/template/docs/operator/security-issue-gate.md"]
    text = script.read_text(encoding="utf-8") if script.exists() else ""
    for doc in docs:
        if not doc.exists():
            fail(f"missing {doc}")
        text += "\n" + doc.read_text(encoding="utf-8")
    for marker in ["public security issue autofix refused", "private report channel", "approval scope `security-fix`", "no public logs"]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    public = subprocess.run([sys.executable, str(script), "--channel", "public-issue", "--labels", "security"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if public.returncode == 0:
        fail("public security issue was allowed")
    with tempfile.TemporaryDirectory() as tmp_raw:
        approval = Path(tmp_raw) / "approval.json"
        approval.write_text(json.dumps({"schema": "automation-approval/v1", "approval_id": "S1", "action_scope": "security-fix", "target": "security/private", "status": "active"}), encoding="utf-8")
        private = subprocess.run([sys.executable, str(script), "--channel", "private", "--approval-file", str(approval), "--actor-permission", "maintain"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if private.returncode != 0:
            fail(private.stderr.strip() or "private placeholder refused")
    print("validate-security-issue-gate=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
