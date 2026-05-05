#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret|private[_ -]?key)\s*[:=]\s*\S+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = Path(args.proposal)
    text = source.read_text(encoding="utf-8")
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        raise SystemExit("refusing secret-like curator proposal")
    draft = f"""schema: factory-task-draft/v1
source_kind: curator-proposal
source_ref: {source.as_posix()}
status: draft
task_class: docs
title: Curator proposal review
handoff_allowed: false
review_required: true
auto_apply: false
release_note_required: true
summary: >
  Repo-reviewed curator proposal converted to an FT-TASK draft. Human review is
  required before handoff, implementation, validator changes or release notes.
"""
    out = Path(args.output)
    if args.write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(draft, encoding="utf-8")
        print(f"curator_task_draft={out}")
    else:
        print("dry_run=true")
        print(draft)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
