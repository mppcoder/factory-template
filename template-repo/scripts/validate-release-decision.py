#!/usr/bin/env python3
from __future__ import annotations

import sys

from factory_automation_common import AutomationError, repo_root, validate_release_decision_data


def main() -> int:
    root = repo_root(sys.argv[1] if len(sys.argv) > 1 else ".")
    try:
        data = validate_release_decision_data(root)
    except AutomationError as exc:
        print("RELEASE DECISION НЕВАЛИДЕН")
        print(f"- {exc}")
        return 1
    print("RELEASE DECISION ВАЛИДЕН")
    print(f"- decision: {data.get('decision')}")
    print(f"- version: {data.get('version')}")
    print(f"- notes_source: {data.get('notes_source')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
