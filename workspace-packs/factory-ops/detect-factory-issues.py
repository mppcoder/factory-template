#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

KEYWORDS = [
    "фабрик", "template", "шаблон", "launcher", "scenario", "сценар",
    "classification", "project-origin", "task pack", "codex-task-pack",
    "feedback", "дрейф", "drift", "preset", "валидац"
]

def scan_text(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
    except Exception:
        return []
    hits = []
    for kw in KEYWORDS:
        if kw in text:
            hits.append(kw)
    return sorted(set(hits))

def main() -> int:
    if len(sys.argv) != 2:
        print("Использование: detect-factory-issues.py <корень-проекта>")
        return 1
    root = Path(sys.argv[1]).resolve()
    findings = []
    for rel in ["CURRENT_FUNCTIONAL_STATE.md", ".chatgpt/verification-report.md", ".chatgpt/done-report.md", ".chatgpt/reality-check.md", ".chatgpt/classification.md"]:
        p = root / rel
        if p.exists():
            hits = scan_text(p)
            if hits:
                findings.append({"path": str(p), "hits": hits})
    print(json.dumps({"project": str(root), "factory_issue_signals": findings, "suggestion": "Проверьте, не относится ли проблема к фабрике, а не к конкретному проекту."}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
