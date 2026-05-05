#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


SCAN_PATHS = [
    ".chatgpt/task-registry.yaml",
    ".chatgpt/handoff-implementation-register.yaml",
    "template-repo/template/.chatgpt/task-registry.yaml",
    "template-repo/template/.chatgpt/handoff-implementation-register.yaml",
    "reports/task-queue.md",
    "reports/continuous-backlog-readout.md",
    "RELEASE_NOTES.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    today = dt.date.today().isoformat()
    output = Path(args.output) if args.output else root / "reports" / "curator" / f"{today}-curator-proposals.md"
    evidence = [path for path in SCAN_PATHS if (root / path).exists()]
    text = f"""# Factory curator proposals / предложения куратора

Дата: {today}

## Policy / политика

Curator is read-only by default. No hidden self-learning is allowed; every learning must become a repo-reviewed artifact before it can change behavior.

## Evidence / подтверждения

{chr(10).join(f"- `{path}`" for path in evidence)}

## Proposal 1 / предложение 1

- evidence: task queue and release notes are the active automation control plane.
- proposal: keep issue-autofix, bounded runner, Symphony-compatible spec and advanced automation gates in the same quick validation contour.
- risk: validator drift can make future automation look safer than it is.
- suggested validation: run `bash template-repo/scripts/verify-all.sh quick` and the advanced automation validators before release-facing closeout.

## Proposal 2 / предложение 2

- evidence: generated projects receive repo-owned docs and scripts.
- proposal: add downstream smoke coverage whenever a new automation workflow or support surface is added.
- risk: factory-only paths can leak into generated repos.
- suggested validation: generate a temp project and check `.github`, `WORKFLOW.md`, support docs and `SECURITY.md`.

## Write mode / режим записи

`--write` may create a curator-class FT-TASK in a future increment, but this MVP does not mutate the repo except for this proposal report.
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"curator_report={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
