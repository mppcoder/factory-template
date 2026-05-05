#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_LABELS = {
    "agent:ready",
    "agent:claimed",
    "agent:running",
    "agent:blocked",
    "agent:pr-opened",
    "agent:human-review",
    "status:needs-info",
    "security",
    "external-secret",
    "needs-human",
    "blocked",
    "risk:high",
}


def fail(msg: str) -> None:
    raise SystemExit(f"validate-issue-autofix-labels: {msg}")


def labels_from_manifest(path: Path) -> set[str]:
    if not path.exists():
        fail(f"missing labels manifest: {path}")
    return set(re.findall(r"(?m)^-\s+name:\s*([A-Za-z0-9:_-]+)\s*$", path.read_text(encoding="utf-8")))


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    labels = labels_from_manifest(root / ".github" / "labels.yml")
    missing = sorted(REQUIRED_LABELS - labels)
    if missing:
        fail("labels manifest missing: " + ", ".join(missing))

    sources = [
        root / "template-repo/scripts/issue-autofix-gate.py",
        root / ".github/workflows/issue-autofix.yml",
        root / "docs/operator/factory-template/issue-autofix-permission-model.md",
        root / "docs/support-automation.md",
        root / "template-repo/template/docs/operator/issue-autofix-permission-model.md",
    ]
    joined = "\n".join(path.read_text(encoding="utf-8") for path in sources if path.exists())
    for label in REQUIRED_LABELS:
        if label not in joined:
            fail(f"label is not documented/used consistently: {label}")
    if "dry-run by default" not in joined or "no live label mutation" not in joined:
        fail("label sync dry-run/no-live-mutation boundary is not documented")
    print("validate-issue-autofix-labels=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
