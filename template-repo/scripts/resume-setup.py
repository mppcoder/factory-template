#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
from datetime import datetime
from pathlib import Path

import yaml


DEFAULT_STATE = {
    "schema_version": 1,
    "feature": {
        "id": "",
        "title": "",
        "rough_idea": "",
        "workspace": "",
    },
    "progress": {
        "current_stage": "interview",
        "last_completed_stage": "intake",
        "next_step_hint": "Ответьте на первый незаполненный вопрос интервью",
    },
    "interview": {
        "question_order": [
            "problem",
            "users",
            "value",
            "in_scope",
            "out_of_scope",
            "constraints",
            "acceptance",
        ],
        "questions": {
            "problem": {"prompt": "Какую проблему вы хотите решить?", "required": True},
            "users": {"prompt": "Кто основной пользователь результата?", "required": True},
            "value": {"prompt": "Почему это ценно для пользователя/команды?", "required": True},
            "in_scope": {"prompt": "Что точно входит в первый релиз?", "required": True},
            "out_of_scope": {"prompt": "Что точно не входит в первый релиз?", "required": True},
            "constraints": {
                "prompt": "Какие ограничения уже известны (время, доступы, legacy)?",
                "required": False,
            },
            "acceptance": {"prompt": "Как понять, что результат принят?", "required": True},
        },
        "answers": {
            "problem": "",
            "users": "",
            "value": "",
            "in_scope": "",
            "out_of_scope": "",
            "constraints": "",
            "acceptance": "",
        },
    },
    "timeline": {
        "created_at": "",
        "updated_at": "",
    },
    "session": {
        "last_actor": "",
        "resume_note": "Можно остановиться и продолжить позже: состояние сохраняется в interview-state.yaml",
    },
}


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def deep_merge(base: dict, override: dict) -> dict:
    merged = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


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


def template_candidates(workspace: Path, explicit: str | None) -> list[Path]:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())

    project_root = detect_project_root(workspace)
    script_path = Path(__file__).resolve()

    candidates.extend(
        [
            workspace / ".chatgpt" / "interview-state.yaml.template",
            project_root / ".chatgpt" / "interview-state.yaml.template",
            project_root / "template" / ".chatgpt" / "interview-state.yaml.template",
            script_path.parents[1] / "template" / ".chatgpt" / "interview-state.yaml.template",
            script_path.parents[2] / ".chatgpt" / "interview-state.yaml.template",
            script_path.parents[2] / "template-repo" / "template" / ".chatgpt" / "interview-state.yaml.template",
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


def load_initial_state(workspace: Path, template_path: str | None) -> tuple[dict, str]:
    source = "default"
    for candidate in template_candidates(workspace, template_path):
        if candidate.exists():
            loaded = yaml_load(candidate)
            return deep_merge(DEFAULT_STATE, loaded), str(candidate)
    return copy.deepcopy(DEFAULT_STATE), source


def parse_answers(pairs: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise SystemExit(f"Неверный формат --answer: {pair}. Используйте key=value")
        key, value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise SystemExit(f"Пустой ключ в --answer: {pair}")
        parsed[key] = value.strip()
    return parsed


def pending_question(state: dict) -> tuple[str | None, dict | None]:
    interview = state.get("interview", {})
    questions = interview.get("questions", {}) if isinstance(interview, dict) else {}
    answers = interview.get("answers", {}) if isinstance(interview, dict) else {}
    order = interview.get("question_order", []) if isinstance(interview, dict) else []

    for qid in order:
        question = questions.get(qid, {}) if isinstance(questions, dict) else {}
        if not bool(question.get("required", False)):
            continue
        answer = str(answers.get(qid, "")).strip() if isinstance(answers, dict) else ""
        if not answer:
            return qid, question

    return None, None


def answered_stats(state: dict) -> tuple[int, int]:
    interview = state.get("interview", {})
    questions = interview.get("questions", {}) if isinstance(interview, dict) else {}
    answers = interview.get("answers", {}) if isinstance(interview, dict) else {}

    required = [qid for qid, meta in (questions.items() if isinstance(questions, dict) else []) if bool(meta.get("required", False))]
    done = [qid for qid in required if str(answers.get(qid, "")).strip()]
    return len(done), len(required)


def main() -> int:
    parser = argparse.ArgumentParser(description="Создать или продолжить planning interview state.")
    parser.add_argument("--workspace", default=".", help="Папка feature-workspace.")
    parser.add_argument("--state-file", help="Явный путь к interview-state.yaml")
    parser.add_argument("--template", help="Явный путь к interview-state.yaml.template")
    parser.add_argument("--feature-id", help="Идентификатор фичи")
    parser.add_argument("--feature-title", help="Человекочитаемое название фичи")
    parser.add_argument("--idea", help="Черновая идея одной строкой")
    parser.add_argument("--set-stage", choices=["interview", "user-spec", "tech-spec", "decomposition", "done"])
    parser.add_argument("--answer", action="append", default=[], help="Ответ в формате key=value")
    parser.add_argument("--actor", default="human", help="Кто внёс последнее изменение состояния")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    project_root = detect_project_root(workspace)
    state_file = Path(args.state_file).expanduser().resolve() if args.state_file else workspace / "interview-state.yaml"

    if state_file.exists():
        loaded = yaml_load(state_file)
        state = deep_merge(DEFAULT_STATE, loaded)
        source = str(state_file)
    else:
        state, source = load_initial_state(workspace, args.template)

    feature = state.setdefault("feature", {})
    progress = state.setdefault("progress", {})
    timeline = state.setdefault("timeline", {})
    session = state.setdefault("session", {})
    interview = state.setdefault("interview", {})
    answers = interview.setdefault("answers", {})
    questions = interview.setdefault("questions", {})

    if args.feature_id:
        feature["id"] = args.feature_id
    if args.feature_title:
        feature["title"] = args.feature_title
    if args.idea:
        feature["rough_idea"] = args.idea

    feature["workspace"] = str(workspace)

    parsed_answers = parse_answers(args.answer)
    for key, value in parsed_answers.items():
        if key not in questions:
            questions[key] = {"prompt": f"Дополнительный вопрос: {key}", "required": False}
        answers[key] = value

    if args.set_stage:
        progress["current_stage"] = args.set_stage

    created = str(timeline.get("created_at", "")).strip()
    if not created:
        timeline["created_at"] = now_iso()
    timeline["updated_at"] = now_iso()
    session["last_actor"] = args.actor

    next_qid, next_question = pending_question(state)
    if next_qid:
        progress["current_stage"] = "interview"
        progress["next_step_hint"] = f"Заполните вопрос `{next_qid}`"
    else:
        if progress.get("current_stage") == "interview":
            progress["current_stage"] = "user-spec"
        progress["last_completed_stage"] = "interview"
        progress["next_step_hint"] = "Запустите generate-user-spec.py"

    yaml_dump(state_file, state)

    done, total = answered_stats(state)
    print(f"state_file={state_file}")
    print(f"source={source}")
    print(f"stage={progress.get('current_stage', 'interview')}")
    print(f"required_answers={done}/{total}")

    if next_qid and next_question:
        if (project_root / "scripts" / "resume-setup.py").exists():
            resume_command = "scripts/resume-setup.py"
        elif (project_root / "template-repo" / "scripts" / "resume-setup.py").exists():
            resume_command = "template-repo/scripts/resume-setup.py"
        else:
            resume_command = str(Path(__file__).resolve())
        print("next_question_id=" + next_qid)
        print("next_question_prompt=" + str(next_question.get("prompt", "")).strip())
        print("next_command=" + f"python3 {resume_command} --workspace {workspace} --answer {next_qid}='...'")
    else:
        if (project_root / "scripts" / "generate-user-spec.py").exists():
            next_command = "scripts/generate-user-spec.py"
        elif (project_root / "template-repo" / "scripts" / "generate-user-spec.py").exists():
            next_command = "template-repo/scripts/generate-user-spec.py"
        else:
            next_command = str(Path(__file__).resolve().parent / "generate-user-spec.py")
        print("next_command=" + f"python3 {next_command} --workspace {workspace}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
