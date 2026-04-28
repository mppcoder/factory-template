#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from project_naming import project_slug_from_name, validate_project_slug


@dataclass(frozen=True)
class RoutePlan:
    route: str
    title: str
    preset: str | None
    mode: str
    next_step: str
    fallback_commands: list[str]
    guided_steps: list[str]


BROWNFIELD_PRESETS = {
    "modernize": ("brownfield-with-repo-modernization", "2", "1"),
    "integrate": ("brownfield-with-repo-integration", "2", "2"),
    "audit": ("brownfield-with-repo-audit", "2", "3"),
    "no-repo": ("brownfield-without-repo", "3", "1"),
}


def _script_paths(explicit_root: str | None) -> tuple[Path, Path]:
    script_path = Path(__file__).resolve()
    template_root = Path(explicit_root).expanduser().resolve() if explicit_root else script_path.parent.parent
    return template_root, template_root / "scripts"


def _factory_hint(template_root: Path, script_name: str) -> str:
    if template_root.name == "template-repo":
        return f"template-repo/scripts/{script_name}"
    return f"scripts/{script_name}"


def _load_presets(template_root: Path) -> dict:
    presets_file = template_root / "project-presets.yaml"
    if not presets_file.exists():
        raise SystemExit(f"Не найден файл пресетов: {presets_file}")
    data = yaml.safe_load(presets_file.read_text(encoding="utf-8")) or {}
    return data.get("project_presets", {})


def _ask_text(prompt: str, default: str | None = None, pattern: str | None = None) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if not value and default:
            value = default
        if not value:
            print("  Нужен ответ, чтобы продолжить.")
            continue
        if pattern and not re.fullmatch(pattern, value):
            print("  Формат не подходит. Используйте маленькие латинские буквы, цифры и дефис.")
            continue
        return value


def _ask_slug(prompt: str, default: str | None = None, allow_reserved: bool = False) -> tuple[str, bool]:
    while True:
        slug = _ask_text(prompt, default=default)
        result = validate_project_slug(slug, allow_reserved=allow_reserved)
        if result.ok:
            return slug, allow_reserved and bool(result.warnings)
        print("  Slug не подходит:")
        for error in result.errors:
            print(f"  - {error}")
        if any("reserved/generic" in error for error in result.errors):
            if _ask_choice("Это намеренный reserved/generic slug?", [("yes", "Да"), ("no", "Нет")]) == "yes":
                override_result = validate_project_slug(slug, allow_reserved=True)
                if override_result.ok:
                    return slug, True
        if slug == default:
            default = None


def _ask_choice(question: str, options: list[tuple[str, str]]) -> str:
    print(f"\n{question}")
    for index, (_key, label) in enumerate(options, start=1):
        print(f"  {index}. {label}")
    while True:
        raw = input("Выберите номер варианта: ").strip()
        if raw.isdigit():
            index = int(raw)
            if 1 <= index <= len(options):
                return options[index - 1][0]
        print(f"  Введите число от 1 до {len(options)}.")


def _run(command: list[str], cwd: Path, input_text: str | None = None) -> int:
    print(f"\n$ {' '.join(command)}")
    sys.stdout.flush()
    return subprocess.run(command, cwd=cwd, input=input_text, text=True, check=False).returncode


def _dashboard_command(project_root: Path, args: argparse.Namespace) -> list[str]:
    dashboard = project_root / "scripts" / "operator-dashboard.py"
    command = [sys.executable, str(dashboard)]
    if args.run_dry_run:
        command.append("--run-dry-run")
    if args.verify_summary:
        command.append("--verify-summary")
    return command


def _show_project_knowledge(project_root: Path) -> None:
    knowledge_dir = project_root / "project-knowledge"
    print("\nШаг: знания проекта")
    if knowledge_dir.is_dir():
        print(f"- Готово: создана папка {knowledge_dir}.")
        print("- Это место для устойчивых решений: что за проект, архитектура, деплой и правила команды.")
        return
    print(f"- Внимание: папка {knowledge_dir} не найдена.")
    print("- Продолжить можно, но позже стоит восстановить project-knowledge из шаблона.")


def _project_plan(template_root: Path, route: str, preset: str, project_slug: str) -> RoutePlan:
    preflight = _factory_hint(template_root, "preflight-vps-check.py")
    wizard = _factory_hint(template_root, "first-project-wizard.py")
    feature = _factory_hint(template_root, "init-feature-workspace.sh")
    if route == "greenfield":
        return RoutePlan(
            route=route,
            title="Greenfield: steady-state product development",
            preset=preset,
            mode="create-project",
            next_step=(
                "Launcher может сразу создать проект, подготовить знания проекта, открыть workspace первой задачи "
                "и показать следующий операторский шаг."
            ),
            fallback_commands=[
                f"python3 {preflight} --project-slug {project_slug}",
                f"python3 {wizard}",
                f"bash {feature} --feature-id first-feature",
            ],
            guided_steps=[
                "выбрать режим: новый проект с нуля",
                "проверить окружение перед созданием проекта",
                "создать проект через прежний launcher",
                "проверить слой project-knowledge",
                "создать workspace первой задачи",
                "показать понятный следующий шаг оператора",
            ],
        )
    if preset == "brownfield-without-repo":
        brownfield_next = (
            "Launcher подготовит intake/reconstruction path: входящие материалы кладутся внутри project root, "
            "затем создается или определяется canonical repo и проект converted в greenfield-product."
        )
        brownfield_steps = [
            "выбрать brownfield без repo: intake/reconstruction path",
            "проверить окружение перед созданием проекта",
            "создать transitional brownfield preset",
            "зафиксировать evidence и reconstruction plan",
            "показать следующий шаг toward canonical repo and greenfield conversion",
        ]
    else:
        brownfield_next = (
            "Launcher подготовит with-repo adoption/modernization path: сначала audit/safe zones, "
            "затем conversion в greenfield-product."
        )
        brownfield_steps = [
            "выбрать brownfield с repo: adoption/modernization path",
            "проверить окружение перед созданием проекта",
            "создать transitional brownfield preset",
            "зафиксировать audit, risks и safe zones",
            "показать следующий шаг toward greenfield conversion",
        ]
    return RoutePlan(
        route=route,
        title="Brownfield transition: adoption path to greenfield",
        preset=preset,
        mode="create-project",
        next_step=brownfield_next,
        fallback_commands=[
            f"python3 {preflight} --project-slug {project_slug}",
            f"python3 {wizard}",
            f"python3 {_factory_hint(template_root, 'operator-dashboard.py')}",
        ],
        guided_steps=brownfield_steps,
    )


def _continue_plan(template_root: Path, feature_id: str | None) -> RoutePlan:
    feature = _factory_hint(template_root, "init-feature-workspace.sh")
    operator = _factory_hint(template_root, "operator-dashboard.py")
    fallback = [f"python3 {operator}"]
    if feature_id:
        fallback.insert(0, f"bash {feature} --feature-id {feature_id}")
    return RoutePlan(
        route="continue",
        title="Продолжить текущий проект",
        preset=None,
        mode="continue",
        next_step=(
            f"Создать workspace `{feature_id}`, затем показать рекомендацию оператора."
            if feature_id
            else "Показать состояние проекта и одну следующую команду."
        ),
        fallback_commands=fallback,
        guided_steps=[
            "прочитать состояние проекта",
            "при необходимости создать workspace задачи",
            "показать одну следующую команду",
            "по желанию запустить безопасный deploy dry-run",
        ],
    )


def _print_plan(plan: RoutePlan, presets: dict) -> None:
    print("\nУправляемый launcher фабрики")
    print("-" * 72)
    print(f"Маршрут: {plan.title}")
    if plan.preset:
        preset = presets.get(plan.preset, {})
        print(f"Профиль проекта: {plan.preset}")
        print(f"Режим проекта: {preset.get('default_mode', 'unknown')}")
        print(f"Первая задача: {preset.get('recommended_change_class', 'unknown')}")
        print(f"Как выполнять: {preset.get('recommended_execution_mode', 'unknown')}")
    print(f"Что будет дальше: {plan.next_step}")
    print("\nПолный путь:")
    for index, step in enumerate(plan.guided_steps, start=1):
        print(f"{index}. {step}")
    print("\nПрямые команды остаются запасным путем:")
    for command in plan.fallback_commands:
        print(f"- {command}")


def _wizard_answers(project_name: str, project_slug: str, asset_choice: str, goal_choice: str, yes: bool) -> str:
    tail = ["y", "y"] if yes else []
    return "\n".join([project_name, project_slug, asset_choice, goal_choice, *tail]) + "\n"


def _run_project_route(
    args: argparse.Namespace,
    template_root: Path,
    scripts_dir: Path,
    route: str,
    preset: str,
    asset_choice: str,
    goal_choice: str,
) -> int:
    project_name = args.project_name or _ask_text("\nКак назвать проект")
    default_slug = project_slug_from_name(project_name)
    if args.project_slug:
        project_slug = args.project_slug
        validation = validate_project_slug(project_slug, allow_reserved=args.allow_reserved_slug)
        if not validation.ok:
            for error in validation.errors:
                print(f"Slug error: {error}", file=sys.stderr)
            return 2
        reserved_slug_override = args.allow_reserved_slug and bool(validation.warnings)
    else:
        if not default_slug:
            print("  Не удалось получить slug из названия. Введите понятный lowercase Latin slug вручную.")
            if args.project_name and not sys.stdin.isatty():
                print("Slug error: empty generated project_slug; pass --project-slug explicitly.", file=sys.stderr)
                return 2
        default_validation = validate_project_slug(default_slug, allow_reserved=args.allow_reserved_slug)
        if args.project_name and default_slug and default_validation.ok:
            project_slug = default_slug
            reserved_slug_override = args.allow_reserved_slug and bool(default_validation.warnings)
        elif args.project_name and default_slug and not sys.stdin.isatty():
            for error in default_validation.errors:
                print(f"Slug error: {error}", file=sys.stderr)
            return 2
        else:
            project_slug, reserved_slug_override = _ask_slug(
                "Slug проекта",
                default=default_slug or None,
                allow_reserved=args.allow_reserved_slug,
            )
    presets = _load_presets(template_root)
    plan = _project_plan(template_root, route, preset, project_slug)
    _print_plan(plan, presets)

    if args.route_only:
        print("\nRoute-only режим: ничего не создавалось.")
        return 0

    wizard = scripts_dir / "first-project-wizard.py"
    if not wizard.exists():
        raise SystemExit(f"Не найден fallback wizard: {wizard}")

    command = [sys.executable, str(wizard), "--template-repo-root", str(template_root)]
    if args.skip_preflight:
        command.append("--skip-preflight")
    if args.allow_reserved_slug or reserved_slug_override:
        command.append("--allow-reserved-slug")
    if args.create_github_repo:
        command.append("--create-github-repo")
    if args.github_owner:
        command.extend(["--github-owner", args.github_owner])
    command.extend(["--github-visibility", args.github_visibility])
    if args.reuse_existing_github_repo:
        command.append("--reuse-existing-github-repo")
    code = _run(
        command,
        cwd=Path.cwd().resolve(),
        input_text=_wizard_answers(project_name, project_slug, asset_choice, goal_choice, args.yes),
    )
    if code != 0:
        return code

    project_root = Path.cwd().resolve() / project_slug
    _show_project_knowledge(project_root)

    should_init_feature = args.guided or args.init_feature_workspace or bool(args.feature_id)
    if should_init_feature:
        feature_id = args.feature_id or "first-feature"
        feature_script = project_root / "scripts" / "init-feature-workspace.sh"
        if feature_script.exists():
            code = _run(["bash", str(feature_script), "--feature-id", feature_id], cwd=project_root)
            if code != 0:
                return code
        else:
            print(f"Feature workspace script не найден в созданном проекте: {feature_script}")
            return 2

    if args.guided or args.status or args.run_dry_run or args.verify_summary:
        dashboard = project_root / "scripts" / "operator-dashboard.py"
        if not dashboard.exists():
            print(f"\nOperator dashboard не найден: {dashboard}")
            return 2
        print("\nШаг: следующий шаг оператора")
        return _run(_dashboard_command(project_root, args), cwd=project_root)

    print("\nГотово: проект создан.")
    print(f"Папка проекта: {project_root}")
    print(f"Следующий шаг: cd {project_slug} && python3 scripts/factory-launcher.py --continue")
    return 0


def _run_continue(args: argparse.Namespace, template_root: Path, scripts_dir: Path) -> int:
    presets = _load_presets(template_root)
    feature_id = args.feature_id
    plan = _continue_plan(template_root, feature_id)
    _print_plan(plan, presets)
    if args.route_only:
        print("\nRoute-only режим: ничего не запускалось.")
        return 0

    if feature_id:
        feature_script = scripts_dir / "init-feature-workspace.sh"
        workspace_base = Path.cwd().resolve() / "work" / "features"
        code = _run(
            ["bash", str(feature_script), "--feature-id", feature_id, "--base-dir", str(workspace_base)],
            cwd=Path.cwd().resolve(),
        )
        if code != 0:
            return code

    dashboard = scripts_dir / "operator-dashboard.py"
    command = [sys.executable, str(dashboard)]
    if args.run_dry_run:
        command.append("--run-dry-run")
    if args.verify_summary:
        command.append("--verify-summary")
    return _run(command, cwd=Path.cwd().resolve())


def _interactive_mode() -> str:
    return _ask_choice(
        "Что вы хотите сделать?",
        [
            ("greenfield", "Начать новый проект с нуля"),
            ("brownfield", "Начать transition существующей системы к greenfield"),
            ("continue", "Продолжить уже созданный flow"),
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Единый beginner-first launcher: greenfield, brownfield и продолжение текущего flow.",
    )
    parser.add_argument("--template-repo-root", help="Явный путь к template-repo.")
    parser.add_argument(
        "--mode",
        choices=["greenfield", "brownfield", "continue"],
        help="Маршрут запуска. Без параметра launcher задаст простые вопросы.",
    )
    parser.add_argument(
        "--guided",
        action="store_true",
        help="Пройти полный путь новичка: preflight, создание проекта, project-knowledge, workspace первой задачи и operator next step.",
    )
    parser.add_argument(
        "--continue",
        dest="continue_mode",
        action="store_true",
        help="Короткий alias для --mode continue.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Показать статус и следующий шаг. Для созданного проекта это alias continue-flow.",
    )
    parser.add_argument("--project-name", help="Название проекта для greenfield/brownfield route.")
    parser.add_argument("--project-slug", help="Slug проекта для greenfield/brownfield route.")
    parser.add_argument(
        "--allow-reserved-slug",
        action="store_true",
        help="Разрешить reserved/generic slug после явного подтверждения.",
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
    parser.add_argument(
        "--brownfield-kind",
        choices=sorted(BROWNFIELD_PRESETS),
        default="modernize",
        help="Тип brownfield старта: modernize, integrate, audit или no-repo.",
    )
    parser.add_argument("--feature-id", help="Feature id для init-feature-workspace на continue route.")
    parser.add_argument(
        "--init-feature-workspace",
        action="store_true",
        help="После создания проекта сразу создать workspace для первой feature.",
    )
    parser.add_argument("--skip-preflight", action="store_true", help="Передать --skip-preflight в wizard.")
    parser.add_argument("--route-only", action="store_true", help="Показать маршрут и next step без запуска действий.")
    parser.add_argument("--yes", action="store_true", help="Автоматически отвечать yes на подтверждения wizard.")
    parser.add_argument("--run-dry-run", action="store_true", help="На continue route запустить deploy dry-run.")
    parser.add_argument("--verify-summary", action="store_true", help="На continue route показать verify summary.")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)

    template_root, scripts_dir = _script_paths(args.template_repo_root)
    if args.continue_mode:
        if args.mode and args.mode != "continue":
            parser.error("--continue нельзя совмещать с --mode greenfield/brownfield")
        args.mode = "continue"
    if args.status and not args.mode:
        args.mode = "continue"

    mode = args.mode or _interactive_mode()

    if mode == "greenfield":
        return _run_project_route(args, template_root, scripts_dir, "greenfield", "greenfield-product", "1", "1")
    if mode == "brownfield":
        preset, asset_choice, goal_choice = BROWNFIELD_PRESETS[args.brownfield_kind]
        return _run_project_route(args, template_root, scripts_dir, "brownfield", preset, asset_choice, goal_choice)
    return _run_continue(args, template_root, scripts_dir)


if __name__ == "__main__":
    raise SystemExit(main())
