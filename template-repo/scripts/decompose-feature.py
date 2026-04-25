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


FALLBACK_TECH_TEMPLATE = """# Tech Spec: {{FEATURE_TITLE}}

## Кратко о подходе
{{IMPLEMENTATION_OVERVIEW}}

## Что меняем
{{CHANGES}}

## User Intent Binding
{{USER_INTENT_BINDING}}

## User-Spec Deviations
{{USER_SPEC_DEVIATIONS}}

## Какие артефакты затрагиваем
{{TOUCHED_COMPONENTS}}

## Как проверяем
{{VERIFICATION}}

## Ограничения и риски
{{RISKS_AND_CONSTRAINTS}}
"""


FALLBACK_TASK_TEMPLATE = """# {{TASK_ID}} — {{TASK_TITLE}}

## Цель
{{TASK_GOAL}}

## Входной контекст
{{TASK_INPUT_CONTEXT}}

## User Intent Binding
{{USER_INTENT_BINDING}}

## User-Spec Deviations
{{USER_SPEC_DEVIATIONS}}

## Действия
{{TASK_ACTIONS}}

## Критерии приемки
{{TASK_ACCEPTANCE}}

## Зависимости
{{TASK_DEPENDENCIES}}

## Риски
{{TASK_RISKS}}
"""


DEFAULT_STATE = {
    "progress": {
        "current_stage": "tech-spec",
        "last_completed_stage": "user-spec",
        "next_step_hint": "Запустите decompose-feature.py",
    },
    "timeline": {
        "created_at": "",
        "updated_at": "",
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


def deep_merge(base: dict, override: dict) -> dict:
    merged = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def detect_project_root(start: Path) -> Path:
    start = start.resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".chatgpt").exists():
            return candidate
    return start


def unique_paths(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(resolved)
    return out


def locate_template(project_root: Path, explicit: str | None, rel: str) -> tuple[str, str]:
    script_path = Path(__file__).resolve()
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())

    candidates.extend(
        [
            project_root / "work-templates" / rel,
            project_root / "template" / "work-templates" / rel,
            script_path.parents[1] / "template" / "work-templates" / rel,
            script_path.parents[2] / "template-repo" / "template" / "work-templates" / rel,
        ]
    )

    for candidate in unique_paths(candidates):
        if candidate.exists():
            return candidate.read_text(encoding="utf-8"), str(candidate)

    fallback = FALLBACK_TECH_TEMPLATE if rel == "tech-spec.md.template" else FALLBACK_TASK_TEMPLATE
    return fallback, "builtin"


def parse_user_spec(path: Path) -> tuple[str, dict[str, list[str]]]:
    if not path.exists():
        raise SystemExit(f"Не найден user-spec: {path}")

    text = path.read_text(encoding="utf-8")
    feature_title = path.parent.parent.name
    for line in text.splitlines():
        if line.startswith("#"):
            raw_title = re.sub(r"^#+\s*", "", line).strip()
            raw_title = re.sub(r"^(user spec:|спецификация потребности пользователя:?)\s*", "", raw_title, flags=re.IGNORECASE)
            feature_title = raw_title.strip() or feature_title
            break

    sections: dict[str, list[str]] = {"__intro__": []}
    current = "__intro__"

    for line in text.splitlines():
        match = re.match(r"^##\s+(.+)$", line.strip())
        if match:
            current = match.group(1).strip().lower()
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line.rstrip())

    return feature_title, sections


def bullets(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        match = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value:
            out.append(value)
    return out


def first_nonempty(sections: dict[str, list[str]], keywords: list[str]) -> list[str]:
    for header, lines in sections.items():
        lowered = header.lower()
        if any(keyword in lowered for keyword in keywords):
            vals = bullets(lines)
            if vals:
                return vals
    return []


def markdown_list(values: list[str], fallback: str) -> str:
    if not values:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in values)


def extract_user_intents(sections: dict[str, list[str]]) -> list[tuple[str, str]]:
    for header, lines in sections.items():
        lowered = header.lower()
        if "user intent anchors" not in lowered and "user intent" not in lowered:
            continue
        anchors: list[tuple[str, str]] = []
        for line in lines:
            match = re.match(r"^\s*[-*]\s+(US-\d{3})\s*:\s*(.+?)\s*$", line)
            if match:
                anchors.append((match.group(1), match.group(2).strip()))
        if anchors:
            return anchors
    return []


def build_fallback_intents(goals: list[str], in_scope: list[str], acceptance: list[str]) -> list[tuple[str, str]]:
    values = [
        ("US-001", goals[0] if goals else "Пользовательская проблема не указана"),
        ("US-002", in_scope[0] if in_scope else "Граница первого релиза не указана"),
        ("US-003", acceptance[0] if acceptance else "Критерий приемки не указан"),
    ]
    return values


def format_user_intent_binding(intents: list[tuple[str, str]], source: str, limit: int | None = None) -> str:
    selected = intents[:limit] if limit else intents
    lines = [f"- source: {source}"]
    for anchor_id, text in selected:
        lines.append(f"- {anchor_id}: {text}")
    return "\n".join(lines)


def format_task_user_intent_binding(
    intents: list[tuple[str, str]],
    source: str,
    task_index: int,
    task_text: str,
) -> str:
    primary = intents[min(task_index - 1, len(intents) - 1)] if intents else ("US-001", task_text)
    lines = [
        f"- source: {source}",
        f"- primary: {primary[0]} — {primary[1]}",
    ]
    acceptance_anchor = next((item for item in intents if item[0] == "US-005"), None)
    if acceptance_anchor and acceptance_anchor[0] != primary[0]:
        lines.append(f"- acceptance: {acceptance_anchor[0]} — {acceptance_anchor[1]}")
    return "\n".join(lines)


def default_deviations() -> str:
    return "\n".join(
        [
            "- None.",
            "- Если решение расходится с user-spec, добавьте запись: DEV-001 | anchor=US-xxx | decision=... | reason=... | validation=...",
        ]
    )


def clean_title(value: str, fallback: str) -> str:
    title = re.sub(r"\s+", " ", value).strip(" .:-")
    return title[:90] if title else fallback


def render(template: str, mapping: dict[str, str]) -> str:
    output = template
    for key, value in mapping.items():
        output = output.replace("{{" + key + "}}", value)
    return output


def write_if_needed(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        existing = path.read_text(encoding="utf-8")
        if "{{" not in existing:
            return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def relpath_for_human(path: Path, workspace: Path) -> str:
    try:
        return str(path.resolve().relative_to(workspace.resolve()))
    except ValueError:
        return str(path)


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
    parser = argparse.ArgumentParser(description="Сгенерировать tech-spec и разбить фичу на задачи.")
    parser.add_argument("--workspace", required=True, help="Папка feature workspace")
    parser.add_argument("--user-spec", help="Явный путь к user-spec.md")
    parser.add_argument("--state-file", help="Явный путь к interview-state.yaml")
    parser.add_argument("--tech-template", help="Явный путь к tech-spec template")
    parser.add_argument("--task-template", help="Явный путь к task template")
    parser.add_argument("--tech-output", help="Куда записать tech-spec")
    parser.add_argument("--tasks-dir", help="Папка task-файлов")
    parser.add_argument("--max-tasks", type=int, default=6)
    parser.add_argument("--skip-tech-spec", action="store_true")
    parser.add_argument("--skip-tasks", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip-traceability-audit", action="store_true", help="Не запускать post-generation traceability audit")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    project_root = detect_project_root(workspace)
    user_spec_path = Path(args.user_spec).expanduser().resolve() if args.user_spec else workspace / "specs" / "user-spec.md"
    state_file = Path(args.state_file).expanduser().resolve() if args.state_file else workspace / "interview-state.yaml"

    tech_output = Path(args.tech_output).expanduser().resolve() if args.tech_output else workspace / "specs" / "tech-spec.md"
    tasks_dir = Path(args.tasks_dir).expanduser().resolve() if args.tasks_dir else workspace / "tasks"

    feature_title, sections = parse_user_spec(user_spec_path)

    goals = first_nonempty(sections, ["что нужно сделать", "короткое", "краткое описание"])
    in_scope = first_nonempty(sections, ["входит", "объём", "первая верс"])
    out_of_scope = first_nonempty(sections, ["не входит"])
    constraints = first_nonempty(sections, ["огранич", "constraint", "risk"])
    acceptance = first_nonempty(sections, ["критерии", "как понять", "приемк"])

    if not goals:
        goals = ["Сделать понятный и проверяемый первый релиз функции"]

    if not in_scope:
        in_scope = goals[:]

    if not acceptance:
        acceptance = ["Результат понятен непрограммисту и может быть проверен по шагам"]

    user_intents = extract_user_intents(sections) or build_fallback_intents(goals, in_scope, acceptance)
    user_spec_rel = relpath_for_human(user_spec_path, workspace)
    tech_template, tech_template_source = locate_template(project_root, args.tech_template, "tech-spec.md.template")
    task_template, task_template_source = locate_template(project_root, args.task_template, "tasks/task.md.template")

    tech_mapping = {
        "FEATURE_TITLE": feature_title,
        "IMPLEMENTATION_OVERVIEW": markdown_list(
            [
                "Используем пошаговый flow: interview -> user-spec -> tech-spec -> tasks.",
                "Сохраняем промежуточное состояние, чтобы можно было продолжить работу позже.",
                "Формируем артефакты простым языком для review без технического бэкграунда.",
            ],
            "Подход пока не заполнен",
        ),
        "CHANGES": markdown_list(in_scope, "Список изменений пока не определен"),
        "USER_INTENT_BINDING": format_user_intent_binding(user_intents, user_spec_rel),
        "USER_SPEC_DEVIATIONS": default_deviations(),
        "TOUCHED_COMPONENTS": markdown_list(
            [
                user_spec_rel,
                relpath_for_human(tech_output, workspace),
                relpath_for_human(tasks_dir, workspace),
                relpath_for_human(state_file, workspace),
            ],
            "Компоненты пока не определены",
        ),
        "VERIFICATION": markdown_list(
            acceptance
            + [
                "Пройти глазами по user-spec/tech-spec: текст должен быть понятен человеку без кода.",
                "Проверить, что каждая задача в tasks имеет цель, шаги и критерии приемки.",
            ],
            "План проверки пока не указан",
        ),
        "RISKS_AND_CONSTRAINTS": markdown_list(
            constraints + [f"Out-of-scope для первого релиза: {', '.join(out_of_scope) if out_of_scope else 'не задано'}"],
            "Риски и ограничения пока не зафиксированы",
        ),
        "GENERATED_AT": now_iso(),
    }

    if not args.skip_tech_spec:
        tech_content = render(tech_template, tech_mapping)
        write_if_needed(tech_output, tech_content, args.force)

    created_tasks: list[str] = []
    task_inputs = in_scope[: args.max_tasks]
    if not task_inputs:
        task_inputs = goals[: args.max_tasks]
    fallback_small_steps = [
        "Подготовить и согласовать tech-spec для первого релиза",
        "Разбить решение на минимальные задачи с ясными критериями",
        "Проверить, что план понятен непрограммисту",
    ]
    for step in fallback_small_steps:
        if len(task_inputs) >= max(3, min(args.max_tasks, 6)):
            break
        if step not in task_inputs:
            task_inputs.append(step)
    task_inputs = task_inputs[: args.max_tasks]

    if not args.skip_tasks:
        tasks_dir.mkdir(parents=True, exist_ok=True)
        for index, item in enumerate(task_inputs, start=1):
            task_id = f"T-{index:03d}"
            depends_on = "- []" if index == 1 else f"- [T-{index - 1:03d}]"
            task_mapping = {
                "TASK_ID": task_id,
                "TASK_TITLE": clean_title(item, f"Шаг {index}"),
                "TASK_GOAL": markdown_list([item], "Цель пока не указана"),
                "TASK_INPUT_CONTEXT": markdown_list(
                    [
                        f"user-spec: {user_spec_rel}",
                        f"tech-spec: {relpath_for_human(tech_output, workspace)}",
                    ],
                    "Контекст пока не указан",
                ),
                "USER_INTENT_BINDING": format_task_user_intent_binding(user_intents, user_spec_rel, index, item),
                "USER_SPEC_DEVIATIONS": default_deviations(),
                "TASK_ACTIONS": markdown_list(
                    [
                        "Прочитать связанный фрагмент user-spec.",
                        "Сделать минимальное изменение для этой задачи.",
                        "Обновить артефакты так, чтобы следующий шаг мог продолжиться без потери контекста.",
                    ],
                    "Действия пока не описаны",
                ),
                "TASK_ACCEPTANCE": markdown_list(
                    acceptance[:2] or ["Есть проверяемый критерий завершения"],
                    "Критерии приемки пока не указаны",
                ),
                "TASK_DEPENDENCIES": depends_on,
                "TASK_RISKS": markdown_list(
                    constraints[:2] or ["Риск: недостающая детализация требований"],
                    "Риски пока не определены",
                ),
                "GENERATED_AT": now_iso(),
            }

            task_file = tasks_dir / f"{task_id}.md"
            task_content = render(task_template, task_mapping)
            write_if_needed(task_file, task_content, args.force)
            created_tasks.append(relpath_for_human(task_file, workspace))

        index_md = [f"# Task list for {feature_title}", "", "## Сгенерированные задачи"]
        for task_file in created_tasks:
            index_md.append(f"- {task_file}")
        write_if_needed(tasks_dir / "index.md", "\n".join(index_md), args.force)

    state = deep_merge(DEFAULT_STATE, yaml_load(state_file))
    progress = state.setdefault("progress", {})
    timeline = state.setdefault("timeline", {})

    if not args.skip_tech_spec:
        progress["last_completed_stage"] = "tech-spec"
    if not args.skip_tasks:
        progress["last_completed_stage"] = "decomposition"
    progress["current_stage"] = "done"
    progress["next_step_hint"] = "Проверьте артефакты и подтвердите readiness к реализации"
    timeline.setdefault("created_at", now_iso())
    timeline["updated_at"] = now_iso()

    yaml_dump(state_file, state)

    print(f"user_spec={user_spec_path}")
    print(f"tech_spec={(tech_output if not args.skip_tech_spec else 'skipped')}")
    print(f"tasks_dir={(tasks_dir if not args.skip_tasks else 'skipped')}")
    print(f"tech_template_source={tech_template_source}")
    print(f"task_template_source={task_template_source}")
    print(f"state_file={state_file}")
    if not args.skip_traceability_audit:
        sys.stdout.flush()
        run_traceability_audit(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
