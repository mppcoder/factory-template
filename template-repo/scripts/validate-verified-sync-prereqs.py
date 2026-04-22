#!/usr/bin/env python3
from __future__ import annotations

import sys

from factory_automation_common import AutomationError, changed_paths, repo_root, resolve_sync_plan


def main() -> int:
    root = repo_root(sys.argv[1] if len(sys.argv) > 1 else ".")
    try:
        paths = changed_paths(root)
        if not paths:
            print("VERIFIED SYNC PREREQS ПРОЙДЕНЫ")
            print("- mode: no-op")
            print("- change_id: none")
            return 0
        plan = resolve_sync_plan(root, paths)
    except AutomationError as exc:
        print("VERIFIED SYNC PREREQS НЕ ПРОЙДЕНЫ")
        print(f"- {exc}")
        return 1
    change = plan.get("change", {})
    print("VERIFIED SYNC PREREQS ПРОЙДЕНЫ")
    print(f"- mode: {plan.get('mode')}")
    print(f"- change_id: {change.get('id')}")
    print(f"- branch: {plan.get('branch')}")
    print(f"- remote: {plan.get('push_url')}")
    print(f"- commit_message: {plan.get('commit_message')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
