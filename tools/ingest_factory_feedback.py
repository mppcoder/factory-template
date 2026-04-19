#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / "meta-template-project" / "incoming-learnings"
INDEX = INCOMING / "INDEX.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest factory feedback from a working project into meta-template-project/incoming-learnings.")
    parser.add_argument("source_project", help="Path to working project root that contains meta-feedback/")
    parser.add_argument("--dry-run", action="store_true", help="Show planned actions without writing files")
    parser.add_argument("--allow-incomplete", action="store_true", help="Allow ingest even if factory feedback validator fails")
    return parser.parse_args()


def ensure_index(dry_run: bool) -> None:
    if INDEX.exists():
        return
    content = "# Incoming Learnings Index\n\n"
    if not dry_run:
        INDEX.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    source_root = Path(args.source_project).resolve()
    feedback_dir = source_root / "meta-feedback"
    if not feedback_dir.exists():
        print(f"ОШИБКА: не найден каталог meta-feedback в {source_root}")
        return 1

    validator = ROOT / "tools" / "validate_factory_feedback.py"
    rc = subprocess.run(
        [sys.executable, str(validator), str(source_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    if rc.returncode != 0 and not args.allow_incomplete:
        print(rc.stdout.strip())
        print("ОШИБКА: ingest остановлен, потому что factory feedback не прошел валидацию.")
        print("Подсказка: используйте --allow-incomplete только если осознанно ingest'ите сырой feedback.")
        return 1
    if rc.returncode != 0 and args.allow_incomplete:
        print(rc.stdout.strip())
        print("ПРЕДУПРЕЖДЕНИЕ: ingest продолжен с --allow-incomplete.")

    candidates = [
        feedback_dir / "factory-task.md",
        feedback_dir / "factory-bug-report.md",
    ]
    existing = [p for p in candidates if p.exists()]
    if not existing:
        print(f"ОШИБКА: в {feedback_dir} не найдены factory-task.md или factory-bug-report.md")
        return 1

    date_prefix = dt.date.today().isoformat()
    slug = source_root.name
    ensure_index(args.dry_run)
    planned: list[tuple[Path, Path]] = []
    for src in existing:
        dst = INCOMING / f"{date_prefix}-{slug}-{src.name}"
        planned.append((src, dst))

    print("План ingest factory feedback:")
    for src, dst in planned:
        print(f"- {src} -> {dst}")

    if args.dry_run:
        print("DRY RUN: файлы не записывались.")
        return 0

    INCOMING.mkdir(parents=True, exist_ok=True)
    for src, dst in planned:
        shutil.copy2(src, dst)

    status = "validated" if rc.returncode == 0 else "allow-incomplete"
    entry_lines = [
        f"## {date_prefix} / {slug}",
        "",
    ]
    for _, dst in planned:
        entry_lines.append(f"- `{dst.name}`")
    entry_lines.extend(
        [
            f"- source project: `{source_root}`",
            f"- ingest mode: `{status}`",
            "",
        ]
    )
    with INDEX.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(entry_lines))

    print(f"Factory feedback ingested into: {INCOMING}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
