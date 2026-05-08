#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


COMMON_REQUIRED_FRAGMENTS = [
    "один цельный",
    "Язык ответа Codex: русский",
    "manual-ui",
    "уже открытая live session не является надежным",
    "goal_contract",
    "goal_runtime_recommendation",
    "Codex /goal runtime optional",
    "proxy signals alone",
    "continuation outcome",
]
PARENT_REQUIRED_FRAGMENTS = [
    "parent plan expectations",
    "child subtask boundaries",
    "defer-to-final-closeout",
    "deferred_user_actions",
    "placeholder_replacements",
    "owner_boundary",
    "route explanation",
]
SINGLE_REQUIRED_FRAGMENTS = [
    "parent orchestration не требуется",
]
NEUTRAL_REQUIRED_FRAGMENTS = [
    "Codex решает фактический режим исполнения",
    "child/subagent count",
]
ALLOWED_HANDOFF_SHAPES = {"codex-task-handoff", "single-agent-handoff", "parent-orchestration-handoff"}
PARENT_TRIGGER_PATTERNS = [
    re.compile(r"(?i)(?:2\+|two or more|две или больше|2 или больше).{0,80}(?:child|subtask|подзадач)"),
    re.compile(r"(?i)(?:different|разные).{0,80}(?:selected_profile|selected_model|reasoning|profile|model)"),
    re.compile(r"(?i)(?:orchestration cockpit|parent status tracking|dashboard)"),
    re.compile(r"(?i)(?:deferred_user_actions|placeholder_replacements|external-user-action|runtime/downstream)"),
    re.compile(r"(?i)(?:audit/deep|implementation/build).{0,120}(?:validators/tests|final review|workstreams)"),
]
SINGLE_TRIGGER_PATTERNS = [
    re.compile(r"(?i)(?:маленькая|small|цельная).{0,80}(?:задача|task)"),
    re.compile(r"(?i)(?:одним|one).{0,80}(?:route|profile|агент)"),
    re.compile(r"(?i)parent orchestration не требуется"),
]
FORBIDDEN_PATTERNS = [
    re.compile(r"(?i)read .*codex-input\.md.*instead"),
    re.compile(r"(?i)file-based handoff"),
    re.compile(r"(?i)run this shell command first.*then paste"),
    re.compile(r"(?i)already-open .*auto-switch"),
    re.compile(r"(?i)Codex /goal runtime (?:is )?(?:guaranteed|mandatory|always enabled)"),
    re.compile(r"(?i)\b[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*[:=]\s*['\"]?[^'\"\s]+"),
]


def detect_handoff_shape(text: str) -> str | None:
    match = re.search(r"(?m)^\s*handoff_shape\s*:\s*([A-Za-z0-9_-]+)\s*$", text)
    return match.group(1) if match else None


def validate_text(text: str) -> list[str]:
    errors: list[str] = []
    for fragment in COMMON_REQUIRED_FRAGMENTS:
        if fragment not in text:
            errors.append(f"missing `{fragment}`")
    code_blocks = re.findall(r"```", text)
    if len(code_blocks) > 2:
        errors.append("expected one copy-paste block, found multiple fenced blocks")
    handoff_shape = detect_handoff_shape(text)
    if not handoff_shape:
        errors.append("missing `handoff_shape`")
    elif handoff_shape not in ALLOWED_HANDOFF_SHAPES:
        errors.append(f"unknown handoff_shape `{handoff_shape}`")
    elif handoff_shape == "parent-orchestration-handoff":
        for fragment in PARENT_REQUIRED_FRAGMENTS:
            if fragment not in text:
                errors.append(f"parent handoff missing `{fragment}`")
        if any(pattern.search(text) for pattern in SINGLE_TRIGGER_PATTERNS):
            errors.append("small cohesive task must not use parent-orchestration-handoff without parent triggers")
    elif handoff_shape == "single-agent-handoff":
        for fragment in SINGLE_REQUIRED_FRAGMENTS:
            if fragment not in text:
                errors.append(f"single-agent handoff missing `{fragment}`")
        for pattern in PARENT_TRIGGER_PATTERNS:
            if pattern.search(text):
                errors.append("large or multi-child task must not use single-agent-handoff")
                break
    elif handoff_shape == "codex-task-handoff":
        for fragment in NEUTRAL_REQUIRED_FRAGMENTS:
            if fragment not in text:
                errors.append(f"neutral handoff missing `{fragment}`")
    for pattern in FORBIDDEN_PATTERNS:
        match = pattern.search(text)
        if match:
            context = text[max(0, match.start() - 80): match.end() + 80].lower()
            if "не является" in context or "запрещ" in context or "not default" in context:
                continue
            errors.append(f"forbidden pattern `{match.group(0)}`")
    if "следующий пользовательский шаг отсутствует" not in text and "## Инструкция пользователю" not in text:
        errors.append("missing final continuation outcome or user instruction block")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет beginner full handoff UX scorecard.")
    parser.add_argument("path", nargs="?", default="tests/beginner-handoff-ux/positive/handoff.md")
    args = parser.parse_args()
    path = Path(args.path)
    errors = validate_text(path.read_text(encoding="utf-8"))
    if errors:
        print("BEGINNER HANDOFF UX НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print("BEGINNER HANDOFF UX ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
