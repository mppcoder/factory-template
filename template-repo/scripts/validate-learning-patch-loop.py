#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


ALLOWED_STATUSES = {"proposed", "not_required"}
OVERCLAIM_STATUSES = {"applied", "done", "completed", "fixed", "merged"}
PLACEHOLDER_RE = re.compile(r"<[^>]+>|\{\{[^}]+\}\}|кратко опишите|опишите", re.I)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def field(text: str, name: str) -> str:
    match = re.search(rf"(?im)^\s*{re.escape(name)}\s*:\s*(.+?)\s*$", text)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def meaningful(value: str) -> bool:
    clean = value.strip()
    return bool(clean) and not PLACEHOLDER_RE.search(clean)


def meaningful_lines(text: str) -> list[str]:
    out: list[str] = []
    in_comment = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("<!--"):
            in_comment = True
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if not line or line.startswith("#"):
            continue
        if PLACEHOLDER_RE.search(line):
            continue
        out.append(line)
    return out


def bug_is_reusable(text: str) -> bool:
    markers = [
        field(text, "reusable").lower(),
        field(text, "factory_feedback_required").lower(),
        field(text, "learning_patch_required").lower(),
    ]
    return any(value in {"true", "yes", "да", "required"} for value in markers)


def inline_learning_satisfied(text: str) -> bool:
    status = field(text, "learning_patch_status").lower()
    if status in {"required", "proposed"}:
        return False
    if status == "not_required":
        return meaningful(field(text, "learning_patch_reason"))
    return False


def proposal_source(text: str) -> str:
    return field(text, "source_bug")


def validate_proposal(path: Path, root: Path, errors: list[str]) -> None:
    text = read_text(path)
    status = field(text, "status").lower()
    if status in OVERCLAIM_STATUSES:
        errors.append(f"{rel(path, root)}: proposal overclaim status `{status}`")
        return
    if status not in ALLOWED_STATUSES:
        errors.append(f"{rel(path, root)}: status должен быть proposed или not_required")
    source = proposal_source(text)
    if not meaningful(source):
        errors.append(f"{rel(path, root)}: source_bug не заполнен")
    else:
        source_path = Path(source)
        if not source_path.is_absolute():
            source_path = root / source_path
        if not source_path.exists():
            errors.append(f"{rel(path, root)}: source_bug не найден: {source}")
    target = field(text, "target_surface")
    verification = field(text, "verification")
    justification = field(text, "justification")
    if status == "proposed":
        if not meaningful(target):
            errors.append(f"{rel(path, root)}: target_surface не заполнен")
        if not meaningful(field(text, "proposed_change")):
            errors.append(f"{rel(path, root)}: proposed_change не заполнен")
        if not meaningful(verification):
            errors.append(f"{rel(path, root)}: verification не заполнен")
    if status == "not_required" and not meaningful(justification):
        errors.append(f"{rel(path, root)}: not_required требует justification")
    if len(meaningful_lines(text)) < 6:
        errors.append(f"{rel(path, root)}: proposal выглядит пустым или шаблонным")


def learning_reports(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for base in [root / "reports" / "learnings", root / "template-repo" / "template" / "reports" / "learnings"]:
        if not base.exists():
            continue
        for path in sorted(base.glob("*.md")):
            if path.name.endswith(".template") or path.name.endswith(".md.template"):
                continue
            candidates.append(path)
    return candidates


def bug_reports(root: Path) -> list[Path]:
    base = root / "reports" / "bugs"
    return sorted(base.glob("*.md")) if base.exists() else []


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет learning patch loop для reusable bug reports.")
    parser.add_argument("root", nargs="?", default=".", help="Корень repo")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []

    reports = learning_reports(root)
    source_to_reports: dict[str, list[Path]] = {}
    for report in reports:
        text = read_text(report)
        validate_proposal(report, root, errors)
        source = proposal_source(text)
        if source:
            source_to_reports.setdefault(source, []).append(report)

    for bug in bug_reports(root):
        text = read_text(bug)
        if not bug_is_reusable(text):
            continue
        bug_rel = rel(bug, root)
        if inline_learning_satisfied(text):
            continue
        if bug_rel not in source_to_reports and str(bug) not in source_to_reports:
            errors.append(f"{bug_rel}: reusable bug требует learning proposal или learning_patch_status: not_required с reason")

    if errors:
        print("LEARNING PATCH LOOP НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1
    print("LEARNING PATCH LOOP ВАЛИДЕН")
    if not reports:
        print("proposal_audit=skipped (no learning reports found)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
