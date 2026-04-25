#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ANCHOR_RE = re.compile(r"\bUS-\d{3}\b")
DEV_RE = re.compile(r"\bDEV-\d{3}\b")
DEVIATION_SIGNAL_RE = re.compile(
    r"\b\[DEVIATION\]\b|deviation required|отклонение от user-spec|расхождение с user-spec|не по user-spec",
    re.IGNORECASE,
)


@dataclass
class MarkdownDoc:
    path: Path
    text: str
    sections: dict[str, str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def parse_markdown(path: Path) -> MarkdownDoc:
    text = read_text(path)
    sections: dict[str, list[str]] = {"__intro__": []}
    current = "__intro__"
    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            current = normalize_heading(match.group(1))
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return MarkdownDoc(path=path, text=text, sections={key: "\n".join(value).strip() for key, value in sections.items()})


def normalize_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def has_heading(doc: MarkdownDoc, heading: str) -> bool:
    return normalize_heading(heading) in doc.sections


def section_text(doc: MarkdownDoc, heading: str) -> str:
    return doc.sections.get(normalize_heading(heading), "")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def template_root(root: Path) -> Path:
    if (root / "template-repo" / "template" / "work-templates").exists():
        return root / "template-repo" / "template" / "work-templates"
    if (root / "template" / "work-templates").exists():
        return root / "template" / "work-templates"
    return root / "template-repo" / "template" / "work-templates"


def validate_template(path: Path, required_fragments: list[str], errors: list[str], root: Path) -> None:
    text = read_text(path)
    if not path.exists():
        errors.append(f"structural drift: не найден template {rel(path, root)}")
        return
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"structural drift: {rel(path, root)} не содержит `{fragment}`")


def validate_templates(root: Path, errors: list[str]) -> None:
    base = template_root(root)
    validate_template(
        base / "user-spec.md.template",
        ["## User Intent Anchors", "{{USER_INTENT_ANCHORS}}", "## User-Spec Deviations", "{{USER_SPEC_DEVIATIONS}}"],
        errors,
        root,
    )
    validate_template(
        base / "tech-spec.md.template",
        ["## User Intent Binding", "{{USER_INTENT_BINDING}}", "## User-Spec Deviations", "{{USER_SPEC_DEVIATIONS}}"],
        errors,
        root,
    )
    validate_template(
        base / "tasks" / "task.md.template",
        ["## User Intent Binding", "{{USER_INTENT_BINDING}}", "## User-Spec Deviations", "{{USER_SPEC_DEVIATIONS}}"],
        errors,
        root,
    )


def extract_user_anchors(user_spec: MarkdownDoc, errors: list[str], root: Path) -> set[str]:
    if not has_heading(user_spec, "User Intent Anchors"):
        errors.append(f"structural drift: {rel(user_spec.path, root)} не содержит `## User Intent Anchors`")
        return set()
    anchors = set(ANCHOR_RE.findall(section_text(user_spec, "User Intent Anchors")))
    if not anchors:
        errors.append(f"missing trace: {rel(user_spec.path, root)} не содержит anchors вида `US-001`")
    return anchors


def validate_deviation_records(doc: MarkdownDoc, known_anchors: set[str], errors: list[str], root: Path) -> None:
    if not has_heading(doc, "User-Spec Deviations"):
        errors.append(f"structural drift: {rel(doc.path, root)} не содержит `## User-Spec Deviations`")
        return

    deviations = section_text(doc, "User-Spec Deviations")
    records = [
        line.strip()
        for line in deviations.splitlines()
        if DEV_RE.search(line) and "US-xxx" not in line and "decision=..." not in line
    ]
    for line in records:
        missing_fields = [field for field in ["anchor=", "decision=", "reason=", "validation="] if field not in line]
        if missing_fields:
            errors.append(
                f"undocumented deviation: {rel(doc.path, root)} запись `{DEV_RE.search(line).group(0)}` "
                f"не содержит {', '.join(missing_fields)}"
            )
        anchors = set(ANCHOR_RE.findall(line))
        if not anchors:
            errors.append(f"undocumented deviation: {rel(doc.path, root)} запись `{DEV_RE.search(line).group(0)}` не ссылается на US-anchor")
        unknown = sorted(anchors - known_anchors)
        if unknown:
            errors.append(f"undocumented deviation: {rel(doc.path, root)} ссылается на неизвестные anchors: {', '.join(unknown)}")

    outside_deviation_section = doc.text.replace(deviations, "")
    if DEVIATION_SIGNAL_RE.search(outside_deviation_section) and not records:
        errors.append(
            f"undocumented deviation: {rel(doc.path, root)} содержит сигнал отклонения, но не содержит DEV-xxx record "
            "в `User-Spec Deviations`"
        )


def validate_binding(doc: MarkdownDoc, known_anchors: set[str], errors: list[str], root: Path) -> None:
    if not has_heading(doc, "User Intent Binding"):
        errors.append(f"structural drift: {rel(doc.path, root)} не содержит `## User Intent Binding`")
        return
    binding = section_text(doc, "User Intent Binding")
    anchors = set(ANCHOR_RE.findall(binding))
    if not anchors:
        errors.append(f"missing trace: {rel(doc.path, root)} не содержит US-anchor в `User Intent Binding`")
        return
    unknown = sorted(anchors - known_anchors)
    if unknown:
        errors.append(f"missing trace: {rel(doc.path, root)} ссылается на неизвестные anchors: {', '.join(unknown)}")


def validate_workspace(workspace: Path, root: Path, errors: list[str]) -> None:
    user_spec_path = workspace / "specs" / "user-spec.md"
    tech_spec_path = workspace / "specs" / "tech-spec.md"
    tasks_dir = workspace / "tasks"

    if not user_spec_path.exists():
        errors.append(f"structural drift: workspace {rel(workspace, root)} не содержит specs/user-spec.md")
        return

    user_spec = parse_markdown(user_spec_path)
    known_anchors = extract_user_anchors(user_spec, errors, root)
    validate_deviation_records(user_spec, known_anchors, errors, root)

    if tech_spec_path.exists():
        tech_spec = parse_markdown(tech_spec_path)
        validate_binding(tech_spec, known_anchors, errors, root)
        validate_deviation_records(tech_spec, known_anchors, errors, root)

    if tasks_dir.exists():
        task_files = sorted(path for path in tasks_dir.glob("T-*.md") if path.is_file())
        for task_path in task_files:
            task_doc = parse_markdown(task_path)
            validate_binding(task_doc, known_anchors, errors, root)
            validate_deviation_records(task_doc, known_anchors, errors, root)


def discover_workspaces(root: Path) -> list[Path]:
    candidates = [
        root / "template-repo" / "work" / "features",
        root / "work" / "features",
    ]
    workspaces: list[Path] = []
    for base in candidates:
        if not base.exists():
            continue
        for child in sorted(base.iterdir()):
            if (child / "specs" / "user-spec.md").exists():
                workspaces.append(child)
    return workspaces


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate lightweight user-spec traceability.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root. Defaults to current directory.")
    parser.add_argument("--workspace", action="append", help="Feature workspace to audit. May be passed multiple times.")
    parser.add_argument("--skip-template-check", action="store_true", help="Skip factory template structural checks.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []

    if not args.skip_template_check:
        validate_templates(root, errors)

    workspaces = [Path(item).expanduser().resolve() for item in args.workspace or []]
    if not workspaces and not args.workspace:
        workspaces = discover_workspaces(root)
    for workspace in workspaces:
        validate_workspace(workspace, root, errors)

    if errors:
        print("SPEC TRACEABILITY НЕВАЛИДНА")
        for error in errors:
            print("-", error)
        return 1

    print("SPEC TRACEABILITY ВАЛИДНА")
    if not workspaces:
        print("workspace_audit=skipped (no generated feature workspaces found)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
