#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-public-submit-gate: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/public_submit_gate.py"
    docs = [root / "docs/operator/factory-template/public-submit-gate.md", root / "template-repo/template/docs/operator/public-submit-gate.md"]
    text = script.read_text(encoding="utf-8") if script.exists() else ""
    for doc in docs:
        if not doc.exists():
            fail(f"missing {doc}")
        text += "\n" + doc.read_text(encoding="utf-8")
    for marker in ["default disabled", "approval scope `public-submit`", "redaction validator", "consent artifact", "no secrets"]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        body = tmp / "body.md"
        consent = tmp / "consent.md"
        approval = tmp / "approval.json"
        body.write_text("Redacted public report.\n", encoding="utf-8")
        consent.write_text("consent granted\n", encoding="utf-8")
        approval.write_text(json.dumps({"schema": "automation-approval/v1", "approval_id": "P1", "action_scope": "public-submit", "target": "owner/repo", "status": "active"}), encoding="utf-8")
        ok = subprocess.run([sys.executable, str(script), "--body", str(body), "--target-repo", "owner/repo", "--consent-file", str(consent), "--approval-file", str(approval)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if ok.returncode != 0:
            fail(ok.stderr.strip() or "redacted fixture refused")
        bad_body = tmp / "bad.md"
        bad_body.write_text("api_key=example\n", encoding="utf-8")
        bad = subprocess.run([sys.executable, str(script), "--body", str(bad_body), "--target-repo", "owner/repo", "--consent-file", str(consent), "--approval-file", str(approval)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if bad.returncode == 0:
            fail("secret-like fixture accepted")
        missing_consent = subprocess.run([sys.executable, str(script), "--body", str(body), "--target-repo", "owner/repo", "--approval-file", str(approval)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if missing_consent.returncode == 0:
            fail("missing consent accepted")
    print("validate-public-submit-gate=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
