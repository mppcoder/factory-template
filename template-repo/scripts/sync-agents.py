#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


SYNC_HEADER = """<!--
SYNCED FILE - DO NOT EDIT MANUALLY
Source of truth: template-repo/AGENTS.md
This root AGENTS.md is a materialized clone for the downstream repo.
Manual edits in this clone will be overwritten by the canonical template sync flow.
-->
"""


def render_materialized_clone(source_text: str) -> str:
    body = source_text.strip()
    return f"{SYNC_HEADER}\n{body}\n"


def main() -> int:
    if len(sys.argv) not in {3, 4}:
        print("Usage: sync-agents.py <source-agents> <target-agents> [--check]")
        return 1

    source = Path(sys.argv[1]).resolve()
    target = Path(sys.argv[2]).resolve()
    check_only = len(sys.argv) == 4 and sys.argv[3] == "--check"

    if not source.exists():
        print(f"ERROR: source file not found: {source}")
        return 1

    rendered = render_materialized_clone(source.read_text(encoding="utf-8"))

    if check_only:
        if not target.exists():
            print(f"ERROR: missing materialized clone: {target}")
            return 1
        current = target.read_text(encoding="utf-8")
        if current != rendered:
            print(f"ERROR: drift detected between {source} and {target}")
            return 1
        print(f"OK: {target} is in sync with {source}")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    print(f"Synced {target} from {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
