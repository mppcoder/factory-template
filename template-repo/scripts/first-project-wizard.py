#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Option:
    key: str
    title: str
    description: str


ASSET_OPTIONS = [
    Option(
        key="idea",
        title="Есть только идея (или ТЗ), кода пока нет",
        description="Создадим новый проект с нуля.",
    ),
    Option(
        key="has-repo",
        title="Есть действующий проект и репозиторий",
        description="Подберем brownfield-путь для проекта с repo.",
    ),
    Option(
        key="no-repo",
        title="Есть система/файлы, но нормального репозитория нет",
        description="Запустим evidence-first путь без требования сразу иметь repo.",
    ),
]

GOAL_OPTIONS_BY_ASSET = {
    "idea": [
        Option(
            key="new-product",
            title="Запустить новый продукт (MVP) с нуля",
            description="Рекомендуемый зеленый старт для первого проекта.",
        )
    ],
    "has-repo": [
        Option(
            key="modernize",
            title="Упростить и модернизировать существующую систему",
            description="Когда есть legacy-проект и нужно безопасное улучшение.",
        ),
        Option(
            key="integrate",
            title="Сделать интеграционный контур между системами",
            description="Когда основной риск в зависимостях и стыках.",
        ),
        Option(
            key="audit",
            title="Сначала провести аудит без обязательной реализации",
            description="Когда нужен диагностический шаг и карта рисков.",
        ),
    ],
    "no-repo": [
        Option(
            key="stabilize",
            title="Собрать факты и стабилизировать систему по шагам",
            description="Рекомендуемый путь, если нужно начать без готового repo.",
        )
    ],
}

PRESET_BY_ROUTE = {
    ("idea", "new-product"): "greenfield-product",
    ("has-repo", "modernize"): "brownfield-with-repo-modernization",
    ("has-repo", "integrate"): "brownfield-with-repo-integration",
    ("has-repo", "audit"): "brownfield-with-repo-audit",
    ("no-repo", "stabilize"): "brownfield-without-repo",
}

WHY_BY_PRESET = {
    "greenfield-product": "Вы начинаете с нуля, поэтому выбран greenfield-путь для нового продукта.",
    "brownfield-with-repo-modernization": "У вас уже есть repo, а цель - модернизация действующей системы.",
    "brownfield-with-repo-integration": "У вас есть repo, а фокус - интеграции и внешние связи.",
    "brownfield-with-repo-audit": "Сначала нужен аудит и карта рисков без обязательного внедрения.",
    "brownfield-without-repo": "Есть существующая система, но нет нормализованного repo, поэтому нужен evidence-first запуск.",
}


def _wizard_paths(explicit_root: str | None) -> tuple[Path, Path, Path, Path]:
    script_path = Path(__file__).resolve()
    repo_root = Path(explicit_root).expanduser().resolve() if explicit_root else script_path.parent.parent
    presets_file = repo_root / "project-presets.yaml"
    launcher_file = repo_root / "launcher.sh"
    preflight_file = repo_root / "scripts" / "preflight-vps-check.py"
    return repo_root, presets_file, launcher_file, preflight_file


def _load_presets(presets_file: Path) -> dict:
    if not presets_file.exists():
        raise SystemExit(f"Не найден файл пресетов: {presets_file}")
    data = yaml.safe_load(presets_file.read_text(encoding="utf-8")) or {}
    presets = data.get("project_presets", {})
    if not presets:
        raise SystemExit(f"В файле {presets_file} нет раздела project_presets.")
    return presets


def _ask_text(prompt: str, default: str | None = None, pattern: str | None = None, help_text: str | None = None) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if not value and default:
            value = default
        if not value:
            print("  Нужен ответ, чтобы продолжить.")
            continue
        if pattern and not re.fullmatch(pattern, value):
            print("  Формат не подходит.")
            if help_text:
                print(f"  Подсказка: {help_text}")
            continue
        return value


def _ask_yes_no(prompt: str, default_yes: bool = True) -> bool:
    suffix = "[Y/n]" if default_yes else "[y/N]"
    default_value = "y" if default_yes else "n"
    while True:
        raw = input(f"{prompt} {suffix}: ").strip().lower()
        if not raw:
            raw = default_value
        if raw in {"y", "yes", "д", "да"}:
            return True
        if raw in {"n", "no", "н", "нет"}:
            return False
        print("  Введите y или n.")


def _ask_option(question: str, options: list[Option]) -> Option:
    print(f"\n{question}")
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option.title}")
        print(f"     {option.description}")

    while True:
        raw = input("Выберите номер варианта: ").strip()
        if raw.isdigit():
            index = int(raw)
            if 1 <= index <= len(options):
                return options[index - 1]
        print(f"  Введите число от 1 до {len(options)}.")


def _slugify(name: str) -> str:
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9а-яё]+", "-", slug)
    slug = slug.replace("ё", "e")
    slug = re.sub(r"-+", "-", slug).strip("-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug or "new-project"


def _resolve_selection(asset_key: str, goal_key: str) -> str:
    preset = PRESET_BY_ROUTE.get((asset_key, goal_key))
    if not preset:
        raise SystemExit("Не удалось сопоставить выбранные ответы с preset. Проверьте mapping в wizard.")
    return preset


def _render_plan(
    project_name: str,
    project_slug: str,
    preset_name: str,
    preset: dict,
    asset: Option,
    goal: Option,
    destination: Path,
) -> None:
    mode = preset.get("default_mode", "greenfield")
    change_class = preset.get("recommended_change_class", "feature")
    exec_mode = preset.get("recommended_execution_mode", "codex-led")
    why = WHY_BY_PRESET.get(preset_name, "Маршрут выбран по вашим ответам.")

    print("\nПлан запуска")
    print("-" * 72)
    print(f"Проект: {project_name}")
    print(f"Slug: {project_slug}")
    print(f"Что у вас сейчас: {asset.title}")
    print(f"Что вы запускаете: {goal.title}")
    print(f"Рекомендованный маршрут: {preset_name}")
    print(f"Режим проекта: {mode}")
    print(f"Тип первой задачи: {change_class}")
    print(f"Режим выполнения: {exec_mode}")
    print(f"Куда будет создан проект: {destination}")
    print(f"Почему так: {why}")

    print("\nЧто система сделает дальше")
    print("1. Создаст папку проекта и скопирует туда рабочий шаблон.")
    print("2. Подставит безопасные стартовые настройки под выбранный маршрут.")
    print("3. Включит сценарный контур и .chatgpt-артефакты для первого цикла.")
    print("4. Сгенерирует долгоживущий слой project-knowledge для накопления знаний.")


def _run_preflight(preflight_file: Path, project_slug: str, launch_cwd: Path) -> int:
    if not preflight_file.exists():
        print(f"\nPreflight-скрипт не найден: {preflight_file}")
        return 2

    print("\nЗапускаю проверку VPS до создания проекта...")
    sys.stdout.flush()
    result = subprocess.run(
        [
            sys.executable,
            str(preflight_file),
            "--project-slug",
            project_slug,
            "--project-base",
            str(launch_cwd),
        ],
        check=False,
    )
    return result.returncode


def _run_launcher(
    launcher_file: Path,
    launch_cwd: Path,
    project_name: str,
    project_slug: str,
    preset_name: str,
    preset: dict,
) -> int:
    if not launcher_file.exists():
        print(f"\nНе найден launcher: {launcher_file}")
        print("Запустите wizard из template-repo или передайте --template-repo-root.")
        return 2

    mode = str(preset.get("default_mode", "greenfield"))
    change_class = str(preset.get("recommended_change_class", "feature"))
    exec_mode = str(preset.get("recommended_execution_mode", "codex-led"))

    answers = "\n".join(
        [
            project_name,
            project_slug,
            preset_name,
            mode,
            change_class,
            exec_mode,
        ]
    ) + "\n"

    print("\nСоздаю проект через существующий launcher (guided wrapper)...")
    process = subprocess.run(
        [str(launcher_file)],
        input=answers,
        text=True,
        cwd=launch_cwd,
        check=False,
    )
    return process.returncode


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)

    parser = argparse.ArgumentParser(
        description=(
            "Beginner-friendly wizard: подбирает правильный вход и запускает проект без знания preset-терминов. "
            "Для единого greenfield/brownfield/continue входа используйте factory-launcher.py."
        ),
    )
    parser.add_argument(
        "--template-repo-root",
        help="Явный путь к template-repo (если wizard запущен не из стандартной структуры).",
    )
    parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Пропустить VPS preflight перед созданием проекта.",
    )
    parser.add_argument(
        "--route-only",
        action="store_true",
        help="Только показать маршрут без запуска launcher.",
    )
    args = parser.parse_args()

    repo_root, presets_file, launcher_file, preflight_file = _wizard_paths(args.template_repo_root)
    presets = _load_presets(presets_file)
    launch_cwd = Path.cwd().resolve()

    print("Первый проект: мастер запуска")
    print("Отвечайте простыми словами: wizard сам сопоставит ответы с нужным маршрутом.")

    project_name = _ask_text("\nКак назвать проект")
    default_slug = _slugify(project_name)
    project_slug = _ask_text(
        "Slug проекта (папка и технический идентификатор)",
        default=default_slug,
        pattern=r"[a-z0-9][a-z0-9-]{1,62}",
        help_text="Например: my-first-service",
    )

    asset = _ask_option("1) Что у вас уже есть?", ASSET_OPTIONS)
    goal = _ask_option("2) Что вы хотите запустить сейчас?", GOAL_OPTIONS_BY_ASSET[asset.key])

    preset_name = _resolve_selection(asset.key, goal.key)
    if preset_name not in presets:
        raise SystemExit(f"Preset '{preset_name}' не найден в {presets_file}")

    preset = presets[preset_name]
    destination = launch_cwd / project_slug

    print("\n3) Что система сделает для вас дальше?")
    _render_plan(project_name, project_slug, preset_name, preset, asset, goal, destination)

    if args.route_only:
        print("\nRoute-only режим: проект не создавался.")
        return 0

    if not args.skip_preflight:
        preflight_code = _run_preflight(preflight_file, project_slug, launch_cwd)
        if preflight_code == 1:
            proceed = _ask_yes_no(
                "Preflight нашел блокеры. Продолжить создание проекта несмотря на это",
                default_yes=False,
            )
            if not proceed:
                print("Остановлено до исправления preflight-блокеров.")
                return 1
        elif preflight_code > 1:
            proceed = _ask_yes_no(
                "Preflight не выполнился корректно. Продолжить без preflight",
                default_yes=False,
            )
            if not proceed:
                print("Остановлено: сначала восстановите preflight-проверку.")
                return 2

    if not _ask_yes_no("Создать проект с этими настройками", default_yes=True):
        print("Запуск отменен пользователем.")
        return 0

    code = _run_launcher(launcher_file, launch_cwd, project_name, project_slug, preset_name, preset)
    if code != 0:
        print("\nLauncher завершился с ошибкой.")
        return code

    print("\nГотово: проект создан через beginner-friendly wizard.")
    print(f"Папка проекта: {destination}")
    print("Что делать дальше:")
    print("1. Откройте созданную папку проекта.")
    print("2. Для planning workspace запустите: bash scripts/init-feature-workspace.sh --feature-id first-feature")
    print("3. Для operator next step запустите: python3 scripts/factory-launcher.py --mode continue")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
