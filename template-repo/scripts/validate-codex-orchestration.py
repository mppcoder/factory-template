#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml

from orchestrate_codex_handoff_import import load_orchestrator


orchestrator = load_orchestrator()

DOC_PATHS = [
    "docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md",
    "template-repo/template/docs/codex-workflow.md",
    "docs/operator/factory-template/03-mode-routing-factory-template.md",
    "template-repo/scenario-pack/15-handoff-to-codex.md",
]

REQUIRED_DOC_FRAGMENTS = [
    "VPS Remote SSH-first",
    "one-paste autopilot",
    "Codex App / Cloud Director",
    "optional, not default",
    "Already-open live session",
    "selected_profile",
    "selected_model",
    "selected_reasoning_effort",
    "selected_scenario",
    "defer-to-final-closeout",
    "deferred_user_actions",
    "placeholder_replacements",
    "temporary placeholders",
    "orchestrate-codex-handoff.py --execute",
]

FORBIDDEN_PATTERNS = [
    re.compile(r"(?i)(codex app|cloud director|codex cloud)\s+(is|является|—|-)?\s*(the\s+)?default"),
    re.compile(r"(?i)already-open (?:live )?session (?:is|является)?\s*(?:a\s+)?(?:reliable\s+)?auto-switch"),
    re.compile(r"(?i)one pasted handoff.*switch(?:es)? model"),
    re.compile(r"(?i)ask the user first"),
    re.compile(r"(?i)wait for user data before internal subtasks"),
    re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def validate_docs(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in DOC_PATHS:
        path = root / rel
        if not path.exists():
            errors.append(f"Не найден orchestration doc: {rel}")
            continue
        text = read_text(path)
        for fragment in REQUIRED_DOC_FRAGMENTS:
            if fragment not in text:
                errors.append(f"{rel}: отсутствует fragment `{fragment}`")
        for pattern in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(text):
                snippet = match.group(0)
                context = text[max(0, match.start() - 80): match.end() + 80].lower()
                if (
                    "not default" in context
                    or "не является" in context
                    or "reject" in context
                    or "запрещ" in context
                    or "forbidden" in context
                ):
                    continue
                errors.append(f"{rel}: forbidden wording `{snippet}`")
    return errors


def count_handoff_blocks(text: str) -> int:
    return len(re.findall(r"```(?:text|markdown)?\s*\n(?:Язык ответа Codex: русский|CODEX HANDOFF|Codex handoff)", text))


def validate_handoff_blocks(path: Path) -> list[str]:
    text = read_text(path)
    errors: list[str] = []
    blocks = count_handoff_blocks(text)
    if blocks > 1:
        errors.append(f"{path}: найдено больше одного copy-paste handoff block")
    return errors


def load_plan(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(read_text(path))
    return data if isinstance(data, dict) else {}


def validate_plan_file(path: Path, root: Path) -> list[str]:
    data = load_plan(path)
    errors, warnings = orchestrator.validate_plan(data, root)
    return [f"{path}: {item}" for item in errors]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate VPS Remote SSH-first Codex orchestration layer.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root")
    parser.add_argument("--plan", help="Optional orchestration plan fixture")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    errors = validate_docs(root)
    docs_orchestration = root / "docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md"
    if docs_orchestration.exists():
        errors.extend(validate_handoff_blocks(docs_orchestration))

    plan = Path(args.plan).resolve() if args.plan else root / "tests/codex-orchestration/fixtures/valid/parent-plan.yaml"
    if plan.exists():
        errors.extend(validate_plan_file(plan, root))
    else:
        errors.append(f"Не найден orchestration plan fixture: {plan}")

    if errors:
        print("CODEX ORCHESTRATION НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1
    print("CODEX ORCHESTRATION ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
