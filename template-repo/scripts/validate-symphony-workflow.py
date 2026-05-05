#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-symphony-workflow: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    paths = ["WORKFLOW.md", "template-repo/template/WORKFLOW.md", "docs/operator/factory-template/symphony-compatible-workflow.md"]
    for path in paths:
        full = root / path
        if not full.exists():
            fail(f"missing {path}")
        text = full.read_text(encoding="utf-8")
        for marker in [
            "tracker",
            "control plane",
            "max concurrency",
            "terminal states",
            "no auto-merge",
            "no pull_request_target",
            "external boundary",
            "00-master-router.md",
            "codex-task-handoff",
        ]:
            if marker not in text:
                fail(f"{path} missing marker: {marker}")
    print("validate-symphony-workflow=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
