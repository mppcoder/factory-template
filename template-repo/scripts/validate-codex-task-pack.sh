#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def ensure_contains(text: str, needle: str, errors: list[str], label: str) -> None:
    if needle not in text:
        errors.append(f"{label}: отсутствует обязательный фрагмент `{needle}`")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    chat = root / ".chatgpt"
    errors: list[str] = []

    context_path = chat / "codex-context.md"
    pack_path = chat / "codex-task-pack.md"
    boundary_path = chat / "boundary-actions.md"
    checklist_path = chat / "done-checklist.md"

    for path in [context_path, pack_path, boundary_path, checklist_path]:
        if not path.exists():
            errors.append(f"Не найден {path.name}")

    if errors:
        print("CODEX TASK PACK НЕВАЛИДЕН")
        for err in errors:
            print("-", err)
        return 1

    context = read_text(context_path)
    pack = read_text(pack_path)
    boundary = read_text(boundary_path)
    checklist = read_text(checklist_path)

    ensure_contains(context, "# Контекст для Codex", errors, "codex-context.md")
    ensure_contains(context, "## Проект", errors, "codex-context.md")
    ensure_contains(context, "## Текущий этап", errors, "codex-context.md")
    ensure_contains(context, "## Change ID", errors, "codex-context.md")
    ensure_contains(context, "## Краткое резюме", errors, "codex-context.md")
    if "не указан" in context or "не заполнено" in context:
        errors.append("codex-context.md содержит незаполненные fallback-значения")

    ensure_contains(pack, "# Task pack для Codex", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Change ID", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Заголовок", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Класс изменения", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Режим выполнения", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Handoff input", errors, "codex-task-pack.md")
    if "codex-input.md еще не заполнен." in pack:
        errors.append("codex-task-pack.md ссылается на пустой codex-input.md")

    ensure_contains(boundary, "# Boundary Actions", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для пользователя", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Impact Model", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Completion Package For Source Update Changes", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для handoff", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для внешних границ", errors, "boundary-actions.md")
    ensure_contains(boundary, "Инструкция пользователю", errors, "boundary-actions.md")
    ensure_contains(boundary, "internal repo follow-up", errors, "boundary-actions.md")
    ensure_contains(boundary, "Release-followup, source-pack refresh, export refresh, closeout-sync и release-facing consistency pass внутри repo считаются внутренней работой Codex.", errors, "boundary-actions.md")
    ensure_contains(boundary, "`Инструкция пользователю` не должна подменять внутренний handoff", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление Sources проекта шаблона в ChatGPT", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление шаблона в боевых repo", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление Sources боевых ChatGPT Projects", errors, "boundary-actions.md")
    ensure_contains(boundary, "Удалить перед заменой", errors, "boundary-actions.md")
    ensure_contains(boundary, "workspace-packs/factory-ops/export-template-patch.sh", errors, "boundary-actions.md")
    ensure_contains(boundary, "workspace-packs/factory-ops/apply-template-patch.sh", errors, "boundary-actions.md")
    ensure_contains(boundary, "bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh", errors, "boundary-actions.md")
    if "описание не задано" in boundary:
        errors.append("boundary-actions.md содержит незаполненные impact descriptions")
    for required_file in ["`codex-input.md`", "`codex-context.md`", "`codex-task-pack.md`", "`boundary-actions.md`"]:
        ensure_contains(boundary, required_file, errors, "boundary-actions.md")

    active_yaml = yaml.safe_load(read_text(chat / "active-scenarios.yaml")) or {}
    active_scenarios = active_yaml.get("active_scenarios", active_yaml.get("active", []))
    if isinstance(active_scenarios, list) and active_scenarios:
        if "еще не определены" in boundary:
            errors.append("boundary-actions.md не отразил активные сценарии из active-scenarios.yaml")
        first_route = active_scenarios[0]
        if first_route not in boundary:
            errors.append(f"boundary-actions.md не содержит активный сценарий `{first_route}`")
    scenario_pack = active_yaml.get("scenario_pack", {})
    if isinstance(scenario_pack, dict):
        entrypoint = scenario_pack.get("entrypoint")
        if entrypoint and entrypoint not in boundary:
            errors.append(f"boundary-actions.md не содержит entrypoint `{entrypoint}`")

    ensure_contains(checklist, "# Чек-лист завершения", errors, "done-checklist.md")
    ensure_contains(checklist, "## Impact classification", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.factory_sources", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.downstream_template_sync", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.downstream_project_sources", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.manual_archive_required", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.delete_before_replace", errors, "done-checklist.md")
    ensure_contains(checklist, "## Completion Package For Source Update Changes", errors, "done-checklist.md")
    for item in [
        "verification-report.md",
        "done-report.md",
        "CURRENT_FUNCTIONAL_STATE.md",
        "bug report",
    ]:
        ensure_contains(checklist, item, errors, "done-checklist.md")

    if errors:
        print("CODEX TASK PACK НЕВАЛИДЕН")
        for err in errors:
            print("-", err)
        return 1

    print("CODEX TASK PACK ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
