#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-automation-rollback: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    docs = [
        root / "docs/operator/factory-template/automation-rollback.md",
        root / "template-repo/template/docs/operator/automation-rollback.md",
    ]
    text = ""
    for path in docs:
        if not path.exists():
            fail(f"missing {path}")
        text += "\n" + path.read_text(encoding="utf-8")
    for marker in [
        "failed run",
        "bad branch",
        "bad PR",
        "label reset",
        "task status reset",
        "run.yaml correction",
        "no main rewrite",
    ]:
        if marker not in text:
            fail(f"missing rollback marker: {marker}")
    with tempfile.TemporaryDirectory() as tmp_raw:
        out = Path(tmp_raw) / "rollback.md"
        proc = subprocess.run(
            [
                sys.executable,
                str((root / "template-repo/scripts/automation-rollback-plan.py").resolve()),
                "--issue",
                "101",
                "--branch",
                "codex/issue-101",
                "--output",
                str(out),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0 or "no main rewrite" not in out.read_text(encoding="utf-8"):
            fail(proc.stderr or "rollback helper failed")
    print("validate-automation-rollback=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
