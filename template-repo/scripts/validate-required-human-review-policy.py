#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-required-human-review-policy: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    docs = [
        root / "docs/operator/factory-template/required-human-review-policy.md",
        root / "template-repo/template/docs/operator/required-human-review-policy.md",
    ]
    text = ""
    for doc in docs:
        if not doc.exists():
            fail(f"missing {doc}")
        text += "\n" + doc.read_text(encoding="utf-8")
    for marker in [
        "auto-merge",
        "production deploy",
        "security issue autofix",
        "public external report submit",
        "parallel runner above 1",
        "approval must be explicit",
        "approval must match action scope",
        "approval must be logged",
        "comments from untrusted users do not approve",
    ]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    print("validate-required-human-review-policy=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
