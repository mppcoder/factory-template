#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / "meta-template-project" / "incoming-learnings"
PROCESSED = INCOMING / "processed"
BACKLOG = ROOT / "meta-template-project" / "FACTORY_BACKLOG.md"
GAPS = ROOT / "meta-template-project" / "TEMPLATE_GAPS.md"
ACCEPTED = ROOT / "meta-template-project" / "accepted-patterns"
REJECTED = ROOT / "meta-template-project" / "rejected-patterns"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Triage incoming learnings into recommended factory destinations.")
    parser.add_argument("--dry-run", action="store_true", help="Print recommendations without writing anything")
    parser.add_argument("--apply", action="store_true", help="Apply the recommended triage actions")
    return parser.parse_args()


def classify(text: str) -> tuple[str, str]:
    lower = text.lower()
    if "исправлено" in lower or "fixed" in lower or "принят" in lower:
        return "accepted-pattern", "Есть признаки уже принятого или подтвержденного решения."
    if "отклон" in lower or "rejected" in lower or "не делать" in lower:
        return "rejected-pattern", "Есть признаки явного отклонения или запрета."
    if "не хватает" in lower or "gap" in lower or "пробел" in lower:
        return "template-gap", "Есть признаки пробела шаблона."
    return "backlog", "По умолчанию отправляется в FACTORY_BACKLOG.md как новая задача или сигнал."


def meaningful_feedback_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("## "):
        return False
    if stripped.startswith("<!--") and stripped.endswith("-->"):
        return False
    return True


def generic_heading(line: str) -> bool:
    stripped = line.strip().lower()
    return stripped in {
        "# задача на доработку фабрики",
        "# отчет об ошибке фабрики",
    }


def extract_title(text: str, path: Path) -> str:
    lines = text.splitlines()
    preferred_sections = [
        "## Краткий заголовок",
        "## Что нужно изменить в фабрике",
        "## Что ожидалось",
        "## Что произошло фактически",
        "## Основание",
    ]
    for section in preferred_sections:
        for idx, raw in enumerate(lines):
            if raw.strip() != section:
                continue
            for candidate in lines[idx + 1:]:
                line = candidate.strip()
                if not line or line.startswith("## "):
                    break
                if not meaningful_feedback_line(line):
                    continue
                return line
    for line in lines:
        line = line.strip()
        if line.startswith("# ") and not generic_heading(line):
            return line[2:]
    return f"Требует ручного triage: {path.name}"


def append_if_missing(target: Path, entry_id: str, content: str) -> None:
    text = target.read_text(encoding="utf-8") if target.exists() else ""
    if entry_id in text:
        return
    suffix = "" if text.endswith("\n") or not text else "\n"
    target.write_text(text + suffix + content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.dry_run and args.apply:
        print("ОШИБКА: используйте либо --dry-run, либо --apply")
        return 1
    files = sorted(
        p for p in INCOMING.glob("*.md")
        if p.name not in {"README.md", "INDEX.md"}
    )
    if not files:
        print("Во incoming-learnings нет файлов для triage.")
        return 0

    print("Рекомендации по triage incoming learnings:")
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        target, reason = classify(text)
        title = extract_title(text, path)
        entry_id = f"`{path.name}`"
        if target == "accepted-pattern":
            dest = ACCEPTED / path.name
        elif target == "rejected-pattern":
            dest = REJECTED / path.name
        elif target == "template-gap":
            dest = GAPS
        else:
            dest = BACKLOG
        print(f"- {path.name}")
        print(f"  -> recommended target: {dest}")
        print(f"  -> reason: {reason}")
        if args.apply:
            if target == "accepted-pattern":
                ACCEPTED.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    path.rename(dest)
            elif target == "rejected-pattern":
                REJECTED.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    path.rename(dest)
            elif target == "template-gap":
                append_if_missing(
                    GAPS,
                    entry_id,
                    f"- {entry_id}: {title}\n  source: `meta-template-project/incoming-learnings/{path.name}`\n",
                )
                archive = PROCESSED / "template-gap" / path.name
                archive.parent.mkdir(parents=True, exist_ok=True)
                if not archive.exists():
                    path.rename(archive)
            else:
                append_if_missing(
                    BACKLOG,
                    entry_id,
                    f"- {entry_id}: {title}\n",
                )
                archive = PROCESSED / "backlog" / path.name
                archive.parent.mkdir(parents=True, exist_ok=True)
                if not archive.exists():
                    path.rename(archive)
    if args.apply:
        print("TRIAGE COMPLETE (applied).")
    else:
        print("TRIAGE COMPLETE (dry recommendation only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
