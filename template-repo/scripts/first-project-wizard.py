#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from project_naming import project_code_from_slug, project_slug_from_name, validate_project_code, validate_project_slug


@dataclass(frozen=True)
class Option:
    key: str
    title: str
    description: str


ASSET_OPTIONS = [
    Option(
        key="idea",
        title="Есть только идея (или ТЗ), кода пока нет",
        description="Создадим greenfield steady-state project с нуля.",
    ),
    Option(
        key="has-repo",
        title="Есть действующий проект и репозиторий",
        description="Подберем transitional brownfield с repo: audit/adoption, затем conversion в greenfield.",
    ),
    Option(
        key="no-repo",
        title="Есть система/файлы, но нормального репозитория нет",
        description="Запустим intake/reconstruction path, затем conversion в greenfield.",
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
            description="Когда есть repo: audit/adoption path с обязательным выходом в greenfield.",
        ),
        Option(
            key="integrate",
            title="Сделать интеграционный контур между системами",
            description="Когда основной риск в зависимостях; после adoption проект становится greenfield-product.",
        ),
        Option(
            key="audit",
            title="Сначала провести аудит без обязательной реализации",
            description="Когда нужен diagnostic step; audit не является финальным типом проекта.",
        ),
    ],
    "no-repo": [
        Option(
            key="stabilize",
            title="Собрать факты и стабилизировать систему по шагам",
            description="Рекомендуемый intake/reconstruction path, если нужно начать без готового repo.",
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
    "brownfield-with-repo-modernization": "У вас уже есть repo, поэтому выбран adoption/modernization transition с выходом в greenfield-product.",
    "brownfield-with-repo-integration": "У вас есть repo, а фокус - интеграции; после adoption активный профиль должен стать greenfield-product.",
    "brownfield-with-repo-audit": "Сначала нужен аудит и карта рисков; audit должен перейти к adoption/conversion или blocker.",
    "brownfield-without-repo": "Есть существующая система, но нет нормализованного repo, поэтому нужен intake/reconstruction path с выходом в greenfield-product.",
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


def _ask_slug(prompt: str, default: str | None = None, allow_reserved: bool = False) -> tuple[str, bool]:
    while True:
        slug = _ask_text(
            prompt,
            default=default,
            help_text="Например: moy-pervyy-proekt или ai-factory.",
        )
        result = validate_project_slug(slug, allow_reserved=allow_reserved)
        if result.ok:
            return slug, allow_reserved and bool(result.warnings)
        print("  Slug не подходит:")
        for error in result.errors:
            print(f"  - {error}")
        if any("reserved/generic" in error for error in result.errors):
            if _ask_yes_no("  Это намеренный reserved/generic slug", default_yes=False):
                override_result = validate_project_slug(slug, allow_reserved=True)
                if override_result.ok:
                    return slug, True
        if default == slug:
            default = None


def _resolve_project_code(project_slug: str, explicit: str | None = None) -> str:
    if explicit:
        code = explicit.strip().upper()
    else:
        default = project_code_from_slug(project_slug)
        if sys.stdin.isatty():
            code = _ask_text(
                "PROJECT_CODE проекта (для CH/CX/TASK id, выбирается один раз)",
                default=default,
                pattern=r"[A-Z][A-Z0-9]{1,11}",
                help_text="Например: MP, CRM2 или NGIS. FT зарезервирован за factory-template.",
            ).upper()
        else:
            code = default
    errors = validate_project_code(code)
    if errors:
        raise SystemExit("PROJECT_CODE не подходит:\n- " + "\n- ".join(errors))
    return code


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


def _resolve_selection(asset_key: str, goal_key: str) -> str:
    preset = PRESET_BY_ROUTE.get((asset_key, goal_key))
    if not preset:
        raise SystemExit("Не удалось сопоставить выбранные ответы с preset. Проверьте mapping в wizard.")
    return preset


def _render_plan(
    project_name: str,
    project_slug: str,
    project_code: str,
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
    print(f"PROJECT_CODE: {project_code}")
    print(f"Что у вас сейчас: {asset.title}")
    print(f"Что вы запускаете: {goal.title}")
    print(f"Рекомендованный маршрут: {preset_name}")
    print(f"Режим проекта: {mode}")
    lifecycle_target = preset.get("target_lifecycle_state") if preset.get("conversion_required") else preset.get("lifecycle_state", "greenfield-active")
    print(f"Целевое lifecycle-состояние: {lifecycle_target}")
    print(f"Тип первой задачи: {change_class}")
    print(f"Режим выполнения: {exec_mode}")
    print(f"Куда будет создан проект: {destination}")
    print(f"Почему так: {why}")

    print("\nЧто система сделает дальше")
    print("1. Создаст папку проекта и скопирует туда рабочий шаблон.")
    print("2. Подставит безопасные стартовые настройки под выбранный маршрут.")
    print("3. Сгенерирует repo-local ChatGPT/Codex индексы с выбранным PROJECT_CODE.")
    print("4. Включит сценарный контур и .chatgpt-артефакты для первого цикла.")
    print("5. Подготовит project-knowledge: папку для устойчивых знаний о проекте.")
    if preset.get("conversion_required"):
        print("6. Зафиксирует, что brownfield является transition и должен завершиться greenfield-product.")


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
    project_code: str,
    reserved_slug_override: bool,
    preset_name: str,
    preset: dict,
    args: argparse.Namespace,
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
    env = {
        **dict(os.environ),
        "FACTORY_RESERVED_SLUG_OVERRIDE": "true" if reserved_slug_override else "false",
        "FACTORY_PROJECT_CODE": project_code,
        "FACTORY_ALLOW_RESERVED_SLUG": "true" if args.allow_reserved_slug or reserved_slug_override else "false",
        "FACTORY_CREATE_GITHUB_REPO": "true" if args.create_github_repo else "false",
        "FACTORY_GITHUB_OWNER": args.github_owner or "",
        "FACTORY_GITHUB_VISIBILITY": args.github_visibility,
        "FACTORY_GITHUB_REUSE_EXISTING": "true" if args.reuse_existing_github_repo else "false",
    }
    process = subprocess.run(
        [str(launcher_file)],
        input=answers,
        text=True,
        cwd=launch_cwd,
        env=env,
        check=False,
    )
    return process.returncode


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)

    parser = argparse.ArgumentParser(
        description=(
            "Мастер первого проекта: подбирает правильный вход и запускает проект без знания внутренних preset-имен. "
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
    parser.add_argument(
        "--allow-reserved-slug",
        action="store_true",
        help="Разрешить reserved/generic slug после явного подтверждения маршрута.",
    )
    parser.add_argument(
        "--project-code",
        help="PROJECT_CODE для repo-local CH/CX/TASK id. По умолчанию генерируется из project_slug.",
    )
    parser.add_argument(
        "--create-github-repo",
        action="store_true",
        help="После локального создания проекта создать/подключить GitHub repo <owner>/<project_slug> и push.",
    )
    parser.add_argument("--github-owner", help="GitHub owner для создаваемого repo.")
    parser.add_argument(
        "--github-visibility",
        choices=["private", "public"],
        default="private",
        help="Visibility создаваемого GitHub repo. По умолчанию private.",
    )
    parser.add_argument(
        "--reuse-existing-github-repo",
        action="store_true",
        help="Разрешить использовать уже существующий GitHub repo, если он подтвержден как тот же проект.",
    )
    args = parser.parse_args()

    repo_root, presets_file, launcher_file, preflight_file = _wizard_paths(args.template_repo_root)
    presets = _load_presets(presets_file)
    launch_cwd = Path.cwd().resolve()

    print("Первый проект: мастер запуска")
    print("Отвечайте простыми словами: мастер сам выберет подходящий маршрут.")

    project_name = _ask_text("\nКак назвать проект")
    default_slug = project_slug_from_name(project_name)
    if not default_slug:
        print("  Не удалось получить slug из названия. Введите понятный lowercase Latin slug вручную.")
    project_slug, reserved_slug_override = _ask_slug(
        "Slug проекта (папка и технический идентификатор)",
        default=default_slug or None,
        allow_reserved=args.allow_reserved_slug,
    )
    project_code = _resolve_project_code(project_slug, args.project_code)

    asset = _ask_option("1) Что у вас уже есть?", ASSET_OPTIONS)
    goal = _ask_option("2) Что вы хотите запустить сейчас?", GOAL_OPTIONS_BY_ASSET[asset.key])

    preset_name = _resolve_selection(asset.key, goal.key)
    if preset_name not in presets:
        raise SystemExit(f"Preset '{preset_name}' не найден в {presets_file}")

    preset = presets[preset_name]
    destination = launch_cwd / project_slug

    print("\n3) Что система сделает для вас дальше?")
    _render_plan(project_name, project_slug, project_code, preset_name, preset, asset, goal, destination)

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

    code = _run_launcher(
        launcher_file,
        launch_cwd,
        project_name,
        project_slug,
        project_code,
        reserved_slug_override,
        preset_name,
        preset,
        args,
    )
    if code != 0:
        print("\nLauncher завершился с ошибкой.")
        return code

    print("\nГотово: проект создан через мастер первого проекта.")
    print(f"Папка проекта: {destination}")
    print("Что делать дальше:")
    print("1. Откройте созданную папку проекта.")
    print("2. Для planning workspace запустите: bash scripts/init-feature-workspace.sh --feature-id first-feature")
    print("3. Для следующего шага оператора запустите: python3 scripts/factory-launcher.py --continue")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
