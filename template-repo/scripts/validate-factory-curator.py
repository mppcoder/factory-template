#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-factory-curator: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/factory-curator.py"
    docs = [
        root / "docs/operator/factory-template/factory-curator.md",
        root / "template-repo/template/docs/operator/factory-curator.md",
    ]
    if not script.exists():
        fail("missing factory-curator.py")
    for doc in docs:
        if not doc.exists():
            fail(f"missing {doc}")
        text = doc.read_text(encoding="utf-8")
        for marker in ["no hidden self-learning", "read-only by default", "repo-reviewed artifact"]:
            if marker not in text:
                fail(f"{doc} missing marker: {marker}")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "curator.md"
        proc = subprocess.run([sys.executable, str(script), str(root), "--output", str(out)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            fail(proc.stderr.strip() or "curator smoke failed")
        report = out.read_text(encoding="utf-8")
        for marker in ["Evidence", "proposal", "risk", "suggested validation"]:
            if marker not in report:
                fail(f"curator report missing marker: {marker}")
    print("validate-factory-curator=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
