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
class RoutePlan:
    route: str
    title: str
    preset: str | None
    mode: str
    next_step: str
    fallback_commands: list[str]


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
            print("  Формат не подходит. Используйте lowercase letters/numbers/hyphen.")
            continue
        return value


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


def _slugify(name: str) -> str:
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9а-яё]+", "-", slug)
    slug = slug.replace("ё", "e")
    slug = re.sub(r"-+", "-", slug).strip("-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug or "new-project"


def _run(command: list[str], cwd: Path, input_text: str | None = None) -> int:
    print(f"\n$ {' '.join(command)}")
    sys.stdout.flush()
    return subprocess.run(command, cwd=cwd, input=input_text, text=True, check=False).returncode


def _project_plan(template_root: Path, route: str, preset: str, project_slug: str) -> RoutePlan:
    preflight = _factory_hint(template_root, "preflight-vps-check.py")
    wizard = _factory_hint(template_root, "first-project-wizard.py")
    feature = _factory_hint(template_root, "init-feature-workspace.sh")
    if route == "greenfield":
        return RoutePlan(
            route=route,
            title="Greenfield start",
            preset=preset,
            mode="create-project",
            next_step=(
                "После создания проекта откройте его и начните planning workspace: "
                f"`bash scripts/init-feature-workspace.sh --feature-id first-feature`."
            ),
            fallback_commands=[
                f"python3 {preflight} --project-slug {project_slug}",
                f"python3 {wizard}",
                f"bash {feature} --feature-id first-feature",
            ],
        )
    return RoutePlan(
        route=route,
        title="Brownfield start",
        preset=preset,
        mode="create-project",
        next_step=(
            "После создания проекта начните с reality/evidence артефактов выбранного brownfield preset, "
            "затем запускайте planning workspace только для безопасной первой задачи."
        ),
        fallback_commands=[
            f"python3 {preflight} --project-slug {project_slug}",
            f"python3 {wizard}",
            f"python3 {_factory_hint(template_root, 'operator-dashboard.py')}",
        ],
    )


def _continue_plan(template_root: Path, feature_id: str | None) -> RoutePlan:
    feature = _factory_hint(template_root, "init-feature-workspace.sh")
    operator = _factory_hint(template_root, "operator-dashboard.py")
    fallback = [f"python3 {operator}"]
    if feature_id:
        fallback.insert(0, f"bash {feature} --feature-id {feature_id}")
    return RoutePlan(
        route="continue",
        title="Continue existing flow",
        preset=None,
        mode="continue",
        next_step=(
            f"Init feature workspace `{feature_id}` and then read operator recommendation."
            if feature_id
            else "Read the operator recommendation and run only the next command it prints."
        ),
        fallback_commands=fallback,
    )


def _print_plan(plan: RoutePlan, presets: dict) -> None:
    print("\nFactory Guided Launcher")
    print("-" * 72)
    print(f"Route: {plan.title}")
    if plan.preset:
        preset = presets.get(plan.preset, {})
        print(f"Preset: {plan.preset}")
        print(f"Project mode: {preset.get('default_mode', 'unknown')}")
        print(f"First change class: {preset.get('recommended_change_class', 'unknown')}")
        print(f"Execution mode: {preset.get('recommended_execution_mode', 'unknown')}")
    print(f"Next-step recommendation: {plan.next_step}")
    print("\nFallback commands stay available:")
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
    project_slug = args.project_slug or _ask_text(
        "Slug проекта",
        default=_slugify(project_name),
        pattern=r"[a-z0-9][a-z0-9-]{1,62}",
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
    code = _run(
        command,
        cwd=Path.cwd().resolve(),
        input_text=_wizard_answers(project_name, project_slug, asset_choice, goal_choice, args.yes),
    )
    if code != 0:
        return code

    project_root = Path.cwd().resolve() / project_slug
    if args.init_feature_workspace or args.feature_id:
        feature_id = args.feature_id or "first-feature"
        feature_script = project_root / "scripts" / "init-feature-workspace.sh"
        if feature_script.exists():
            return _run(["bash", str(feature_script), "--feature-id", feature_id], cwd=project_root)
        print(f"Feature workspace script не найден в созданном проекте: {feature_script}")
        return 2

    print("\nGuided launcher complete.")
    print(f"Project root: {project_root}")
    print(f"Recommended next: cd {project_slug} && bash scripts/init-feature-workspace.sh --feature-id first-feature")
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
            ("brownfield", "Начать с существующего проекта или системы"),
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
        help="Маршрут запуска. Без параметра launcher задаст conversational вопросы.",
    )
    parser.add_argument("--project-name", help="Название проекта для greenfield/brownfield route.")
    parser.add_argument("--project-slug", help="Slug проекта для greenfield/brownfield route.")
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
    mode = args.mode or _interactive_mode()

    if mode == "greenfield":
        return _run_project_route(args, template_root, scripts_dir, "greenfield", "greenfield-product", "1", "1")
    if mode == "brownfield":
        preset, asset_choice, goal_choice = BROWNFIELD_PRESETS[args.brownfield_kind]
        return _run_project_route(args, template_root, scripts_dir, "brownfield", preset, asset_choice, goal_choice)
    return _run_continue(args, template_root, scripts_dir)


if __name__ == "__main__":
    raise SystemExit(main())
