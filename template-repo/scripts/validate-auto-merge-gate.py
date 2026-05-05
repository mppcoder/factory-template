#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-auto-merge-gate: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/auto_merge_gate.py"
    docs = [root / "docs/operator/factory-template/auto-merge-gate.md", root / "template-repo/template/docs/operator/auto-merge-gate.md"]
    text = script.read_text(encoding="utf-8") if script.exists() else ""
    for doc in docs:
        if not doc.exists():
            fail(f"missing {doc}")
        text += "\n" + doc.read_text(encoding="utf-8")
    for marker in ["default disabled", "approval scope `auto-merge`", "checks green", "rollback plan", "no security labels"]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        rollback = tmp / "rollback.md"
        rollback.write_text("rollback plan\n", encoding="utf-8")
        approval = tmp / "approval.json"
        approval.write_text(json.dumps({"schema": "automation-approval/v1", "approval_id": "AM1", "action_scope": "auto-merge", "target": "PR-1", "status": "active"}), encoding="utf-8")
        ok = subprocess.run([sys.executable, str(script), "--pr", "PR-1", "--branch", "codex/issue-1", "--checks", "green", "--rollback-plan", str(rollback), "--approval-file", str(approval)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if ok.returncode != 0:
            fail(ok.stderr.strip() or "positive fixture failed")
        for args in [
            ["--checks", "red"],
            ["--labels", "security"],
            ["--conflicts"],
            ["--human-review-unresolved"],
        ]:
            bad = subprocess.run([sys.executable, str(script), "--pr", "PR-1", "--branch", "codex/issue-1", "--rollback-plan", str(rollback), "--approval-file", str(approval), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            if bad.returncode == 0:
                fail(f"negative fixture allowed: {args}")
        no_approval = subprocess.run([sys.executable, str(script), "--pr", "PR-1", "--branch", "codex/issue-1", "--checks", "green", "--rollback-plan", str(rollback)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if no_approval.returncode == 0:
            fail("missing approval allowed")
    print("validate-auto-merge-gate=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
