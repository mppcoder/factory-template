#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-production-deploy-gate: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/production_deploy_gate.py"
    docs = [root / "docs/operator/factory-template/production-deploy-gate.md", root / "template-repo/template/docs/operator/production-deploy-gate.md"]
    text = script.read_text(encoding="utf-8") if script.exists() else ""
    for doc in docs:
        if not doc.exists():
            fail(f"missing {doc}")
        text += "\n" + doc.read_text(encoding="utf-8")
    for marker in ["default disabled", "approval scope `production-deploy`", "environment approval", "health check plan", "never print secrets"]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        rollback = tmp / "rollback.md"
        health = tmp / "health.md"
        rollback.write_text("rollback\n", encoding="utf-8")
        health.write_text("health\n", encoding="utf-8")
        approval = tmp / "approval.json"
        approval.write_text(json.dumps({"schema": "automation-approval/v1", "approval_id": "PD1", "action_scope": "production-deploy", "target": "prod-vps", "status": "active"}), encoding="utf-8")
        ok = subprocess.run([sys.executable, str(script), "--target", "prod-vps", "--environment-approval", "--safe-secrets-env", "--rollback-plan", str(rollback), "--health-check-plan", str(health), "--approval-file", str(approval)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if ok.returncode != 0 or "secret" in ok.stdout.lower() and "safe" not in ok.stdout.lower():
            fail(ok.stderr.strip() or "positive deploy fixture failed")
        missing = subprocess.run([sys.executable, str(script), "--target", "prod-vps", "--rollback-plan", str(rollback), "--health-check-plan", str(health)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if missing.returncode == 0:
            fail("missing approval/env was allowed")
        no_target = subprocess.run([sys.executable, str(script), "--environment-approval", "--safe-secrets-env", "--rollback-plan", str(rollback), "--health-check-plan", str(health), "--approval-file", str(approval)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if no_target.returncode == 0:
            fail("missing target was allowed")
    print("validate-production-deploy-gate=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
