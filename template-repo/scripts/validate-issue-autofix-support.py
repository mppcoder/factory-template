#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT_FILES = [
    ".github/workflows/issue-autofix.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/support-question.yml",
    ".github/ISSUE_TEMPLATE/factory-feedback.yml",
    ".github/ISSUE_TEMPLATE/change-request.yml",
    ".github/ISSUE_TEMPLATE/release-sync.yml",
    ".github/labels.yml",
    "docs/support-automation.md",
    "template-repo/scripts/issue-autofix-gate.py",
    "template-repo/scripts/create-issue-codex-handoff.py",
    "template-repo/scripts/run-issue-autofix.sh",
]
TEMPLATE_FILES = [
    "template-repo/template/.github/workflows/issue-autofix.yml",
    "template-repo/template/.github/ISSUE_TEMPLATE/config.yml",
    "template-repo/template/.github/ISSUE_TEMPLATE/bug.yml",
    "template-repo/template/.github/ISSUE_TEMPLATE/support-question.yml",
    "template-repo/template/.github/ISSUE_TEMPLATE/factory-feedback.yml",
    "template-repo/template/.github/ISSUE_TEMPLATE/change-request.yml",
    "template-repo/template/.github/ISSUE_TEMPLATE/release-sync.yml",
    "template-repo/template/docs/support-automation.md",
    "template-repo/template/SECURITY.md",
]


def fail(msg: str) -> None:
    raise SystemExit(f"validate-issue-autofix-support: {msg}")


def read(root: Path, path: str) -> str:
    full = root / path
    if not full.exists():
        fail(f"missing required file: {path}")
    return full.read_text(encoding="utf-8")


def validate_workflow(text: str, path: str) -> None:
    required = [
        "issues:",
        "issue_comment:",
        "workflow_dispatch:",
        "permissions:",
        "contents: write",
        "pull-requests: write",
        "concurrency:",
        "issue-autofix-gate.py",
        "create-issue-codex-handoff.py",
        "run-issue-autofix.sh",
    ]
    for marker in required:
        if marker not in text:
            fail(f"{path} missing workflow marker: {marker}")
    forbidden = ["pull_request_target", "auto-merge", "automerge"]
    for marker in forbidden:
        if marker in text:
            fail(f"{path} contains forbidden marker: {marker}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    for path in ROOT_FILES + TEMPLATE_FILES:
        read(root, path)
    validate_workflow(read(root, ".github/workflows/issue-autofix.yml"), ".github/workflows/issue-autofix.yml")
    validate_workflow(read(root, "template-repo/template/.github/workflows/issue-autofix.yml"), "template workflow")
    for form in [
        ".github/ISSUE_TEMPLATE/bug.yml",
        ".github/ISSUE_TEMPLATE/support-question.yml",
        ".github/ISSUE_TEMPLATE/factory-feedback.yml",
        ".github/ISSUE_TEMPLATE/change-request.yml",
        ".github/ISSUE_TEMPLATE/release-sync.yml",
    ]:
        text = read(root, form)
        for marker in ["expected", "validations:", "required: true"]:
            if marker not in text:
                fail(f"{form} missing required issue-form section marker: {marker}")
    docs = read(root, "docs/support-automation.md") + "\n" + read(root, "template-repo/template/docs/support-automation.md")
    for marker in ["agent:ready", "/factory fix", "no secrets", "no auto-merge", "reusable factory feedback"]:
        if marker not in docs:
            fail(f"support docs missing marker: {marker}")
    if "TODO" in docs or "PLACEHOLDER" in docs:
        fail("support docs contain placeholder-only marker")
    print("validate-issue-autofix-support=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
