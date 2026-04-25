#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    title: str
    status: str  # ok | warn | fail
    details: str
    fix: str | None = None


STATUS_LABEL = {
    "ok": "OK",
    "warn": "ВНИМАНИЕ",
    "fail": "НУЖНО ИСПРАВИТЬ",
}


def _check_runtime() -> CheckResult:
    if sys.version_info >= (3, 9):
        return CheckResult(
            title="Версия Python",
            status="ok",
            details=f"Найдена Python {sys.version.split()[0]}.",
        )
    return CheckResult(
        title="Версия Python",
        status="fail",
        details=(
            f"Найдена Python {sys.version.split()[0]}, а для скриптов шаблона нужен Python 3.9+."
        ),
        fix="Установите Python 3.9+ и повторите проверку.",
    )


def _check_os() -> CheckResult:
    system = platform.system()
    if system == "Linux":
        return CheckResult(
            title="Операционная система",
            status="ok",
            details="Linux окружение подтверждено. VPS-путь поддерживается штатно.",
        )
    return CheckResult(
        title="Операционная система",
        status="warn",
        details=(
            f"Сейчас система {system}. Скрипты обычно запускаются на Linux VPS, поэтому часть шагов может отличаться."
        ),
        fix="Если это не Linux VPS, проверьте команды вручную перед запуском launcher.",
    )


def _check_projects_root(project_root: Path) -> CheckResult:
    if not project_root.exists():
        return CheckResult(
            title="Корневой каталог проектов",
            status="fail",
            details=f"Каталог {project_root} не найден.",
            fix=f"Создайте каталог: mkdir -p {project_root}",
        )
    if not project_root.is_dir():
        return CheckResult(
            title="Корневой каталог проектов",
            status="fail",
            details=f"Путь {project_root} существует, но это не директория.",
            fix=f"Используйте отдельную директорию для project roots, например {project_root}.",
        )
    if os.access(project_root, os.W_OK):
        return CheckResult(
            title="Права записи в корень проектов",
            status="ok",
            details=f"Есть доступ на запись в {project_root}.",
        )
    return CheckResult(
        title="Права записи в корень проектов",
        status="fail",
        details=f"Нет прав записи в {project_root}.",
        fix=f"Выдайте права на запись для текущего пользователя в {project_root}.",
    )


def _check_projects_layout(project_root: Path) -> CheckResult:
    if not project_root.is_dir():
        return CheckResult(
            title="Структура /projects",
            status="warn",
            details="Пропущено: корень проектов ещё не готов.",
        )

    forbidden = []
    for entry in sorted(project_root.iterdir()):
        name = entry.name
        if name.startswith("_"):
            forbidden.append(name)

    if not forbidden:
        return CheckResult(
            title="Структура /projects",
            status="ok",
            details=(
                "В верхнем уровне нет служебных каталогов с '_' префиксом. Это соответствует правилу 'только project roots'."
            ),
        )

    listed = ", ".join(forbidden)
    return CheckResult(
        title="Структура /projects",
        status="fail",
        details=(
            f"Найдены служебные папки в верхнем уровне {project_root}: {listed}. Это ломает canonical layout."
        ),
        fix=(
            "Переместите такие папки внутрь конкретного проекта, например "
            f"{project_root}/<project-root>/_incoming/."
        ),
    )


def _check_slug(project_root: Path, project_slug: str | None, project_base: Path | None = None) -> list[CheckResult]:
    if not project_slug:
        return [
            CheckResult(
                title="Slug проекта",
                status="warn",
                details="Slug не передан, поэтому проверка целевой папки пропущена.",
                fix="Передайте --project-slug, чтобы проверить готовность конкретного проекта.",
            )
        ]

    results: list[CheckResult] = []
    if re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}", project_slug):
        results.append(
            CheckResult(
                title="Формат slug",
                status="ok",
                details=f"Slug '{project_slug}' выглядит безопасно для путей и URL.",
            )
        )
    else:
        results.append(
            CheckResult(
                title="Формат slug",
                status="warn",
                details=(
                    f"Slug '{project_slug}' нестандартный. Это может затруднить работу с путями, CI и доменами."
                ),
                fix="Используйте lowercase slug в формате: letters/numbers/hyphen.",
            )
        )

    base_for_target = project_base or project_root
    target_root = base_for_target / project_slug
    incoming_dir = target_root / "_incoming"

    if target_root.exists():
        if target_root.is_dir():
            results.append(
                CheckResult(
                    title="Целевая папка проекта",
                    status="warn",
                    details=f"Папка {target_root} уже существует.",
                    fix="Проверьте, что вы не перезапишете существующий проект с тем же slug.",
                )
            )
        else:
            results.append(
                CheckResult(
                    title="Целевая папка проекта",
                    status="fail",
                    details=f"Путь {target_root} существует, но это не директория.",
                    fix="Выберите другой slug или очистите конфликтующий путь.",
                )
            )

    if incoming_dir.exists() and incoming_dir.is_dir() and os.access(incoming_dir, os.W_OK):
        results.append(
            CheckResult(
                title="Каталог _incoming",
                status="ok",
                details=f"Каталог {incoming_dir} уже есть и доступен для записи.",
            )
        )
    elif incoming_dir.exists() and not incoming_dir.is_dir():
        results.append(
            CheckResult(
                title="Каталог _incoming",
                status="fail",
                details=f"Путь {incoming_dir} существует, но это не директория.",
                fix="Удалите конфликт и создайте директорию _incoming внутри project root.",
            )
        )
    else:
        results.append(
            CheckResult(
                title="Каталог _incoming",
                status="warn",
                details=(
                    f"Каталог {incoming_dir} пока не создан. Это нормально до первого входящего архива."
                ),
                fix=f"Создайте заранее: mkdir -p {incoming_dir}",
            )
        )

    return results


def _check_disk_space(project_root: Path) -> CheckResult:
    base = project_root if project_root.exists() else Path("/")
    try:
        usage = shutil.disk_usage(base)
    except OSError:
        return CheckResult(
            title="Свободное место",
            status="warn",
            details="Не удалось оценить свободное место автоматически.",
        )

    free_gb = usage.free / (1024 ** 3)
    if free_gb >= 5:
        return CheckResult(
            title="Свободное место",
            status="ok",
            details=f"Свободно примерно {free_gb:.1f} GiB. Этого обычно достаточно для первого запуска.",
        )
    return CheckResult(
        title="Свободное место",
        status="warn",
        details=f"Свободно только {free_gb:.1f} GiB. Для комфортной работы лучше иметь минимум 5 GiB.",
        fix="Освободите место перед распаковкой архивов и запуском тестов.",
    )


def _check_current_location(project_root: Path) -> CheckResult:
    cwd = Path.cwd().resolve()
    if cwd == project_root or project_root in cwd.parents:
        return CheckResult(
            title="Текущая рабочая папка",
            status="ok",
            details=f"Вы уже внутри {project_root}.",
        )
    return CheckResult(
        title="Текущая рабочая папка",
        status="warn",
        details=f"Сейчас рабочая папка: {cwd}. Обычно удобнее запускать из дерева {project_root}.",
        fix=f"Перейдите в каталог проекта под {project_root} перед bootstrap-скриптами.",
    )


def run_preflight(project_root: Path, project_slug: str | None, project_base: Path | None = None) -> list[CheckResult]:
    checks: list[CheckResult] = [
        _check_runtime(),
        _check_os(),
        _check_projects_root(project_root),
        _check_projects_layout(project_root),
        _check_current_location(project_root),
        _check_disk_space(project_root),
    ]
    checks.extend(_check_slug(project_root, project_slug, project_base=project_base))
    return checks


def _print_report(checks: list[CheckResult], project_root: Path, project_slug: str | None) -> None:
    project_info = f" / проект: {project_slug}" if project_slug else ""
    print(f"VPS preflight: {project_root}{project_info}")
    print("-" * 72)

    for check in checks:
        label = STATUS_LABEL.get(check.status, check.status.upper())
        print(f"[{label}] {check.title}")
        print(f"  {check.details}")
        if check.fix:
            print(f"  Что сделать: {check.fix}")
        print()

    ok_count = sum(1 for c in checks if c.status == "ok")
    warn_count = sum(1 for c in checks if c.status == "warn")
    fail_count = sum(1 for c in checks if c.status == "fail")

    print("Итог:")
    print(f"- OK: {ok_count}")
    print(f"- Предупреждения: {warn_count}")
    print(f"- Критичные блокеры: {fail_count}")

    if fail_count:
        print("\nЕсть блокирующие проблемы. Сначала исправьте их, затем запускайте wizard/launcher.")
    else:
        print("\nКритичных блокеров нет. Можно продолжать запуск первого проекта.")
        script_root = Path(__file__).resolve().parent.parent
        launcher_hint = (
            "template-repo/scripts/factory-launcher.py"
            if script_root.name == "template-repo"
            else "scripts/factory-launcher.py"
        )
        print(f"Guided next: python3 {launcher_hint} --mode greenfield")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Проверяет, готов ли VPS к первому запуску factory-template в понятном человеку виде.",
    )
    parser.add_argument(
        "--project-root",
        default="/projects",
        help="Корневая папка, где лежат project roots (по умолчанию: /projects).",
    )
    parser.add_argument(
        "--project-slug",
        help="Slug проекта для проверки целевой папки и _incoming.",
    )
    parser.add_argument(
        "--project-base",
        help=(
            "Базовая папка, где будет создан проект (по умолчанию используется --project-root). "
            "Нужно, если launch создает проект не прямо в /projects, а в подкаталоге."
        ),
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    project_base = Path(args.project_base).expanduser().resolve() if args.project_base else None
    checks = run_preflight(project_root, args.project_slug, project_base=project_base)
    _print_report(checks, project_root, args.project_slug)

    return 1 if any(c.status == "fail" for c in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
