#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from datetime import datetime
from pathlib import Path
import re
import subprocess
import sys

import yaml


FALLBACK_TEMPLATE = """# User Spec: {{FEATURE_TITLE}}

> generated_at: {{GENERATED_AT}}
> feature_id: {{FEATURE_ID}}
> Этот документ отвечает на вопрос "что хочет пользователь" и должен быть понятен человеку без технического бэкграунда.

## Короткое описание
{{SHORT_DESCRIPTION}}

## Какую проблему решаем
{{PROBLEM}}

## Для кого делаем
{{USERS}}

## Пользовательская ценность
{{VALUE}}

## Что входит в первую версию
{{IN_SCOPE}}

## Что не входит в первую версию
{{OUT_OF_SCOPE}}

## Ограничения
{{CONSTRAINTS}}

## Критерии приемки
{{ACCEPTANCE}}

## User Intent Anchors
Короткие метки исходного пользовательского намерения. На них ссылаются tech-spec и задачи.

{{USER_INTENT_ANCHORS}}

## User-Spec Deviations
Обычно здесь `Нет`. Если позже агент предлагает отойти от исходного intent, deviation нужно перенести в tech-spec и утвердить отдельно.

{{USER_SPEC_DEVIATIONS}}

## Открытые вопросы
{{OPEN_QUESTIONS}}
"""


DEFAULT_INTERVIEW = {
    "question_order": [
        "problem",
        "users",
        "value",
        "in_scope",
        "out_of_scope",
        "constraints",
        "acceptance",
    ],
    "answers": {
        "problem": "",
        "users": "",
        "value": "",
        "in_scope": "",
        "out_of_scope": "",
        "constraints": "",
        "acceptance": "",
    },
}


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def yaml_load(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def yaml_dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def detect_project_root(start: Path) -> Path:
    start = start.resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".chatgpt").exists():
            return candidate
    return start


def template_candidates(project_root: Path, explicit: str | None) -> list[Path]:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())

    script_path = Path(__file__).resolve()
    candidates.extend(
        [
            project_root / "work-templates" / "user-spec.md.template",
            project_root / "template" / "work-templates" / "user-spec.md.template",
            script_path.parents[1] / "template" / "work-templates" / "user-spec.md.template",
            script_path.parents[2] / "template-repo" / "template" / "work-templates" / "user-spec.md.template",
        ]
    )

    unique: list[Path] = []
    seen: set[Path] = set()
    for item in candidates:
        resolved = item.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(resolved)
    return unique


def load_template(project_root: Path, explicit: str | None) -> tuple[str, str]:
    for path in template_candidates(project_root, explicit):
        if path.exists():
            return path.read_text(encoding="utf-8"), str(path)
    return FALLBACK_TEMPLATE, "builtin"


def normalize_answer(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def to_bullets(value: str, fallback: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return f"- {fallback}"

    lines: list[str] = []
    for item in re.split(r"[\n;]+", raw):
        chunk = item.strip(" -*\t")
        if chunk:
            lines.append(f"- {chunk}")
    if not lines:
        lines.append(f"- {fallback}")
    return "\n".join(lines)


def intent_line(anchor_id: str, label: str, value: str, fallback: str) -> str:
    normalized = normalize_answer(value) or fallback
    return f"- {anchor_id}: {label} — {normalized}"


def build_user_intent_anchors(answers: dict, idea: str) -> str:
    rows = [
        intent_line("US-001", "problem", str(answers.get("problem", "")), "Проблема пока не заполнена"),
        intent_line("US-002", "users", str(answers.get("users", "")), "Пользователь пока не указан"),
        intent_line("US-003", "value", str(answers.get("value", "")), "Ценность пока не описана"),
        intent_line("US-004", "scope", str(answers.get("in_scope", "") or idea), "Границы первого релиза пока не указаны"),
        intent_line("US-005", "acceptance", str(answers.get("acceptance", "")), "Критерии приемки пока не заполнены"),
    ]
    return "\n".join(rows)


def default_deviations() -> str:
    return "\n".join(
        [
            "- Нет.",
            "- Формат при необходимости: DEV-001 | anchor=US-xxx | decision=... | reason=... | validation=... | approval=pending",
        ]
    )


def merge_defaults(state: dict) -> dict:
    merged = copy.deepcopy(state if isinstance(state, dict) else {})
    merged.setdefault("feature", {})
    merged.setdefault("progress", {})
    merged.setdefault("timeline", {})
    interview = merged.setdefault("interview", {})
    interview.setdefault("question_order", DEFAULT_INTERVIEW["question_order"])
    answers = interview.setdefault("answers", {})
    for key, value in DEFAULT_INTERVIEW["answers"].items():
        answers.setdefault(key, value)
    return merged


def load_idea(args: argparse.Namespace) -> str:
    if args.idea:
        return normalize_answer(args.idea)
    if args.idea_file:
        content = Path(args.idea_file).expanduser().read_text(encoding="utf-8")
        return normalize_answer(content)
    return ""


def render(template: str, mapping: dict[str, str]) -> str:
    result = template
    for key, value in mapping.items():
        result = result.replace("{{" + key + "}}", value)
    return result


def run_traceability_audit(workspace: Path) -> None:
    validator = Path(__file__).resolve().parent / "validate-spec-traceability.py"
    if not validator.exists():
        print("traceability_audit=skipped (validator not found)")
        return
    subprocess.run(
        [sys.executable, str(validator), "--workspace", str(workspace), "--skip-template-check"],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Сгенерировать user-spec.md из interview-state.")
    parser.add_argument("--workspace", required=True, help="Папка feature workspace")
    parser.add_argument("--state-file", help="Явный путь к interview-state.yaml")
    parser.add_argument("--template", help="Явный путь к user-spec template")
    parser.add_argument("--output", help="Куда записать user-spec")
    parser.add_argument("--idea", help="Черновая идея одной строкой")
    parser.add_argument("--idea-file", help="Файл с rough idea")
    parser.add_argument("--force", action="store_true", help="Перезаписать output, если файл уже существует")
    parser.add_argument("--skip-traceability-audit", action="store_true", help="Не запускать post-generation traceability audit")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    project_root = detect_project_root(workspace)
    state_file = Path(args.state_file).expanduser().resolve() if args.state_file else workspace / "interview-state.yaml"
    output = Path(args.output).expanduser().resolve() if args.output else workspace / "specs" / "user-spec.md"

    if output.exists() and not args.force:
        existing = output.read_text(encoding="utf-8")
        if "{{" not in existing:
            raise SystemExit(f"Файл уже существует: {output}. Добавьте --force для перезаписи.")

    state = merge_defaults(yaml_load(state_file))
    feature = state.get("feature", {}) if isinstance(state, dict) else {}
    progress = state.get("progress", {}) if isinstance(state, dict) else {}
    timeline = state.get("timeline", {}) if isinstance(state, dict) else {}

    answers = state.get("interview", {}).get("answers", {}) if isinstance(state.get("interview"), dict) else {}
    idea = load_idea(args) or normalize_answer(str(feature.get("rough_idea", "")))

    feature_title = str(feature.get("title") or feature.get("id") or workspace.name).strip() or workspace.name
    feature_id = str(feature.get("id") or workspace.name).strip()

    template_text, template_source = load_template(project_root, args.template)

    mapping = {
        "FEATURE_TITLE": feature_title,
        "FEATURE_ID": feature_id,
        "SHORT_DESCRIPTION": to_bullets(idea, "Краткое описание пока не заполнено"),
        "PROBLEM": to_bullets(str(answers.get("problem", "")), "Проблема пока не заполнена"),
        "USERS": to_bullets(str(answers.get("users", "")), "Пользователь пока не указан"),
        "VALUE": to_bullets(str(answers.get("value", "")), "Ценность пока не описана"),
        "IN_SCOPE": to_bullets(str(answers.get("in_scope", "")), "Границы in-scope пока не указаны"),
        "OUT_OF_SCOPE": to_bullets(str(answers.get("out_of_scope", "")), "Границы out-of-scope пока не указаны"),
        "CONSTRAINTS": to_bullets(str(answers.get("constraints", "")), "Явные ограничения пока не зафиксированы"),
        "ACCEPTANCE": to_bullets(str(answers.get("acceptance", "")), "Критерии приемки пока не заполнены"),
        "USER_INTENT_ANCHORS": build_user_intent_anchors(answers, idea),
        "USER_SPEC_DEVIATIONS": default_deviations(),
        "OPEN_QUESTIONS": "- Нужна ли дополнительная детализация до перехода к tech-spec?",
        "GENERATED_AT": now_iso(),
    }

    rendered = render(template_text, mapping).rstrip() + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")

    feature["workspace"] = str(workspace)
    if idea and not str(feature.get("rough_idea", "")).strip():
        feature["rough_idea"] = idea

    progress["last_completed_stage"] = "user-spec"
    progress["current_stage"] = "tech-spec"
    progress["next_step_hint"] = "Запустите decompose-feature.py для tech-spec и задач"
    timeline.setdefault("created_at", now_iso())
    timeline["updated_at"] = now_iso()

    state["feature"] = feature
    state["progress"] = progress
    state["timeline"] = timeline
    yaml_dump(state_file, state)

    print(f"user_spec={output}")
    print(f"template_source={template_source}")
    print(f"state_file={state_file}")
    if not args.skip_traceability_audit:
        sys.stdout.flush()
        run_traceability_audit(workspace)
    if (project_root / "scripts" / "decompose-feature.py").exists():
        decompose_command = "scripts/decompose-feature.py"
    elif (project_root / "template-repo" / "scripts" / "decompose-feature.py").exists():
        decompose_command = "template-repo/scripts/decompose-feature.py"
    else:
        decompose_command = str(Path(__file__).resolve().parent / "decompose-feature.py")
    print(f"next_command=python3 {decompose_command} --workspace {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
