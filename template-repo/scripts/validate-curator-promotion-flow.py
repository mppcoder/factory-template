#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-curator-promotion-flow: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    docs = [
        root / "docs/operator/factory-template/curator-promotion-flow.md",
        root / "template-repo/template/docs/operator/curator-promotion-flow.md",
    ]
    text = ""
    for path in docs:
        if not path.exists():
            fail(f"missing {path}")
        text += "\n" + path.read_text(encoding="utf-8")
    for marker in [
        "curator proposal",
        "FT-TASK draft",
        "review",
        "handoff",
        "implementation",
        "validator",
        "release note",
        "no hidden self-learning",
        "do not auto-apply",
    ]:
        if marker not in text:
            fail(f"missing curator promotion marker: {marker}")
    fixture = root / "tests/factory-curator/proposal.md"
    if not fixture.exists():
        fail("missing curator proposal fixture")
    with tempfile.TemporaryDirectory() as tmp_raw:
        out = Path(tmp_raw) / "task-draft.yaml"
        proc = subprocess.run(
            [
                sys.executable,
                str((root / "template-repo/scripts/curator-proposal-to-task.py").resolve()),
                "--proposal",
                str(fixture),
                "--output",
                str(out),
                "--write",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            fail(proc.stderr or "curator proposal conversion failed")
        draft = out.read_text(encoding="utf-8")
        if "auto_apply: false" not in draft or "handoff_allowed: false" not in draft:
            fail("curator draft is not review-gated")
    print("validate-curator-promotion-flow=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
