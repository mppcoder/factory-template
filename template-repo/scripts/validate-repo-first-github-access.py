#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_MARKERS = {
    "AGENTS.md": [
        "## Правило доступа к GitHub repo",
        "GitHub connector, repo tool или authenticated `gh`",
        "Public URL fallback допустим только при явном blocker",
    ],
    "template-repo/AGENTS.md": [
        "## Правило доступа к GitHub repo",
        "GitHub connector, repo tool или authenticated `gh`",
        "Public URL fallback допустим только при явном blocker",
    ],
    "template-repo/scenario-pack/00-master-router.md": [
        "## Контракт доступа к GitHub repo",
        "repo-first означает authenticated repo-first",
        "authenticated `gh` access",
        "raw.githubusercontent.com",
        "При таком fallback ответ обязан явно назвать blocker",
    ],
    "template-repo/scenario-pack/01-global-rules.md": [
        "reusable process defect repo-first/GitHub access layer",
    ],
    "template-repo/template/.chatgpt/boundary-actions.md": [
        "сначала GitHub repo через GitHub connector / repo tool / authenticated `gh`",
        "Public `github.com` / raw URL fallback допустим только при named blocker",
    ],
    ".chatgpt/boundary-actions.md": [
        "сначала GitHub repo через GitHub connector / repo tool / authenticated `gh`",
        "Public `github.com` / raw URL fallback допустим только при named blocker",
    ],
    "docs/operator/runbook-packages/01-factory-template/02-codex-runbook.md": [
        "Primary path для repo `mppcoder/factory-template`",
        "gh repo clone mppcoder/factory-template factory-template",
        "Public HTTPS clone не используется как default для Codex",
    ],
    "template-repo/scripts/create-codex-task-pack.py": [
        "сначала GitHub repo через GitHub connector / repo tool / authenticated `gh`",
        "public URL fallback допустим только при named blocker",
    ],
}

FORBIDDEN_PUBLIC_DEFAULTS = {
    "docs/operator/runbook-packages/01-factory-template/02-codex-runbook.md": [
        "git clone https://github.com/mppcoder/factory-template.git factory-template",
    ],
}


def read(path: Path) -> str:
    if not path.exists():
        raise ValueError(f"missing required artifact: {path}")
    return path.read_text(encoding="utf-8")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for relative, markers in REQUIRED_MARKERS.items():
        path = root / relative
        try:
            text = read(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing marker `{marker}`")

    for relative, forbidden_values in FORBIDDEN_PUBLIC_DEFAULTS.items():
        text = read(root / relative)
        for forbidden in forbidden_values:
            if forbidden in text:
                errors.append(f"{relative}: public GitHub URL remains default Codex repo path")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate repo-first GitHub access uses connector/tool/authenticated gh before public URL fallback."
    )
    parser.add_argument("root", nargs="?", default=".", help="Project root")
    args = parser.parse_args()

    errors = validate(Path(args.root))
    if errors:
        print("REPO-FIRST GITHUB ACCESS НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("repo-first GitHub access contract OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
