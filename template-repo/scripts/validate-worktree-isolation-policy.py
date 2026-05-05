#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-worktree-isolation-policy: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    paths = [
        root / "docs/operator/factory-template/worktree-isolation-policy.md",
        root / "template-repo/template/docs/operator/worktree-isolation-policy.md",
        root / "docs/operator/factory-template/bounded-runner.md",
        root / "template-repo/template/docs/operator/bounded-runner.md",
        root / "template-repo/scripts/bounded-task-runner.py",
    ]
    text = ""
    for path in paths:
        if not path.exists():
            fail(f"missing {path}")
        text += "\n" + path.read_text(encoding="utf-8")
    for marker in [
        "branch per issue/task",
        "worktree per issue/task",
        "lock file",
        "run state",
        "cleanup policy",
        "parallel execution is refused",
        "--max-concurrency",
        "worktree isolation",
    ]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    print("validate-worktree-isolation-policy=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
