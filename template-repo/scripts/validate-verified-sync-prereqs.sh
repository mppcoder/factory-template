#!/usr/bin/env python3
from __future__ import annotations

import sys

from factory_automation_common import AutomationError, repo_root, validate_verify_prereqs


def main() -> int:
    root = repo_root(sys.argv[1] if len(sys.argv) > 1 else ".")
    try:
        task_index, git_meta = validate_verify_prereqs(root)
    except AutomationError as exc:
        print("VERIFIED SYNC PREREQS НЕ ПРОЙДЕНЫ")
        print(f"- {exc}")
        return 1
    change = task_index.get("change", {})
    print("VERIFIED SYNC PREREQS ПРОЙДЕНЫ")
    print(f"- change_id: {change.get('id')}")
    print(f"- branch: {git_meta.get('branch')}")
    print(f"- remote: {git_meta.get('push_url')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
