#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from factory_automation_common import AutomationError, read_text, repo_root, validate_release_decision_data


def main() -> int:
    root = repo_root(sys.argv[1] if len(sys.argv) > 1 else ".")
    try:
        data = validate_release_decision_data(root)
        notes_path = root / str(data.get("notes_source"))
        text = read_text(notes_path)
        if len([line for line in text.splitlines() if line.strip()]) < 4:
            raise AutomationError(f"release notes source слишком пустой: {Path(data['notes_source'])}")
    except AutomationError as exc:
        print("RELEASE NOTES SOURCE НЕВАЛИДЕН")
        print(f"- {exc}")
        return 1
    print("RELEASE NOTES SOURCE ВАЛИДЕН")
    print(f"- {data.get('notes_source')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
