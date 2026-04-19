#!/usr/bin/env python3
from __future__ import annotations
import filecmp
import json
import sys
from pathlib import Path

WATCH_DIRS = ["bootstrap", "template-repo/scenario-pack", "template-repo/template", "template-repo/scripts"]

def compare_dirs(factory: Path, project: Path):
    report = []
    for rel in WATCH_DIRS:
        a = factory / rel
        b = project / rel
        if not a.exists() or not b.exists():
            report.append({"path": rel, "status": "missing", "factory_exists": a.exists(), "project_exists": b.exists()})
            continue
        cmp = filecmp.dircmp(a, b)
        report.append({"path": rel, "left_only": cmp.left_only, "right_only": cmp.right_only, "diff_files": cmp.diff_files, "funny_files": cmp.funny_files})
    return report

def main() -> int:
    if len(sys.argv) != 3:
        print("Использование: check-template-drift.py <корень-фабрики> <корень-проекта>")
        return 1
    factory = Path(sys.argv[1]).resolve()
    project = Path(sys.argv[2]).resolve()
    print(json.dumps({"factory": str(factory), "project": str(project), "drift": compare_dirs(factory, project)}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
