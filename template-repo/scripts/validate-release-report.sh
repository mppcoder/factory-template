#!/usr/bin/env python3
from __future__ import annotations

import sys

from factory_automation_common import AutomationError, read_yaml, release_report_path, repo_root


def main() -> int:
    root = repo_root(sys.argv[1] if len(sys.argv) > 1 else ".")
    path = release_report_path(root)
    data = read_yaml(path)
    try:
        if not path.exists():
            raise AutomationError("release report еще не создан")
        for field in ["timestamp", "decision", "status"]:
            if not str(data.get(field, "")).strip():
                raise AutomationError(f"release report не содержит поле `{field}`")
        status = str(data.get("status"))
        if status in {"published", "already-published"}:
            if not str(data.get("tag", "")).strip():
                raise AutomationError("published report должен содержать tag")
        if status == "published" and not str(data.get("release_url", "")).strip():
            raise AutomationError("published report должен содержать release_url")
        if status == "manual-fallback":
            if not str(data.get("reason", "")).strip():
                raise AutomationError("manual-fallback report должен содержать reason")
            if not data.get("manual_actions"):
                raise AutomationError("manual-fallback report должен содержать manual_actions")
    except AutomationError as exc:
        print("RELEASE REPORT НЕВАЛИДЕН")
        print(f"- {exc}")
        return 1
    print("RELEASE REPORT ВАЛИДЕН")
    print(f"- status: {data.get('status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
