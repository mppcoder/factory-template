#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-advanced-automation-gates: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    paths = [
        "docs/operator/factory-template/full-advanced-automation-gates.md",
        "template-repo/template/docs/operator/full-advanced-automation-gates.md",
    ]
    for path in paths:
        full = root / path
        if not full.exists():
            fail(f"missing {path}")
        text = full.read_text(encoding="utf-8")
        for marker in [
            "dry-run issue dispatch",
            "gated issue-autofix",
            "PR creation",
            "human review",
            "auto-merge default",
            "production deploy",
            "security issue autofix",
            "pull_request_target",
            "worktree isolation",
            "audit log",
            "agent:blocked",
            "runner `--dry-run`",
        ]:
            if marker not in text:
                fail(f"{path} missing marker: {marker}")
    print("validate-advanced-automation-gates=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
