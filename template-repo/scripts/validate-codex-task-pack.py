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
    launch_path = chat / "task-launch.yaml"
    normalized_handoff_path = chat / "normalized-codex-handoff.md"
    handoff_response_path = chat / "handoff-response.md"

    for path in [context_path, pack_path, boundary_path, checklist_path, launch_path, normalized_handoff_path, handoff_response_path]:
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
    launch_yaml = yaml.safe_load(read_text(launch_path)) or {}
    normalized_handoff = read_text(normalized_handoff_path)
    handoff_response = read_text(handoff_response_path)

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
    ensure_contains(pack, "## Launch source", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Task class", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Selected profile", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Selected model", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Selected reasoning effort", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Apply mode", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Strict launch mode", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Manual UI default", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Optional strict launch command", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Direct Codex command behind launcher", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Selected scenario", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Pipeline stage", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Handoff allowed", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Defect capture path", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Handoff input", errors, "codex-task-pack.md")
    ensure_contains(pack, "приоритет у правил repo", errors, "codex-task-pack.md")
    if "codex-input.md еще не заполнен." in pack:
        errors.append("codex-task-pack.md ссылается на пустой codex-input.md")

    ensure_contains(boundary, "# Boundary Actions", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для пользователя", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Impact Model", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Completion Package For Repo-First Instruction Changes", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для handoff", errors, "boundary-actions.md")
    ensure_contains(boundary, "manual-ui (default)", errors, "boundary-actions.md")
    ensure_contains(boundary, "strict_launch_mode: optional", errors, "boundary-actions.md")
    ensure_contains(boundary, "новый чат + вставка handoff", errors, "boundary-actions.md")
    ensure_contains(boundary, "non-canonical fallback", errors, "boundary-actions.md")
    ensure_contains(boundary, "advisory layer", errors, "boundary-actions.md")
    ensure_contains(boundary, "`.chatgpt/task-launch.yaml`", errors, "boundary-actions.md")
    ensure_contains(boundary, "`selected_profile` — это исполнимая граница маршрутизации", errors, "boundary-actions.md")
    ensure_contains(boundary, "При исполнении handoff приоритет у правил repo", errors, "boundary-actions.md")
    ensure_contains(boundary, "только один цельный блок для copy-paste в Codex", errors, "boundary-actions.md")
    ensure_contains(boundary, "Нельзя заменять handoff ссылкой на файл", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для внешних границ", errors, "boundary-actions.md")
    ensure_contains(boundary, "Инструкция пользователю", errors, "boundary-actions.md")
    ensure_contains(boundary, "internal repo follow-up", errors, "boundary-actions.md")
    ensure_contains(boundary, "Release-followup, source-pack refresh, export refresh, closeout-sync и release-facing consistency pass внутри repo считаются внутренней работой Codex.", errors, "boundary-actions.md")
    ensure_contains(boundary, "`Инструкция пользователю` не должна подменять внутренний handoff", errors, "boundary-actions.md")
    ensure_contains(boundary, "Если внешнего шага нет, финальный ответ все равно должен явно сказать, что внешних действий не требуется.", errors, "boundary-actions.md")
    ensure_contains(boundary, "Внешних действий не требуется.", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление repo-first инструкции проекта шаблона в ChatGPT", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление шаблона в боевых repo", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление repo-first инструкции боевых ChatGPT Projects", errors, "boundary-actions.md")
    ensure_contains(boundary, "Удалить перед заменой", errors, "boundary-actions.md")
    ensure_contains(boundary, "workspace-packs/factory-ops/export-template-patch.sh", errors, "boundary-actions.md")
    ensure_contains(boundary, "workspace-packs/factory-ops/apply-template-patch.sh", errors, "boundary-actions.md")
    ensure_contains(boundary, "выполняет Codex внутри repo", errors, "boundary-actions.md")
    ensure_contains(boundary, "Troubleshooting sticky state", errors, "boundary-actions.md")
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
    ensure_contains(checklist, "## Completion Package For Repo-First Instruction Changes", errors, "done-checklist.md")
    ensure_contains(checklist, "Completion package выдан в том же финальном ответе", errors, "done-checklist.md")
    ensure_contains(checklist, "bash VALIDATE_VERIFIED_SYNC_PREREQS.sh", errors, "done-checklist.md")
    ensure_contains(checklist, "bash VERIFIED_SYNC.sh", errors, "done-checklist.md")
    ensure_contains(checklist, "финальный ответ действительно заканчивается блоком `## Инструкция пользователю`", errors, "done-checklist.md")
    ensure_contains(checklist, "финальный ответ явно говорит, что внешних действий не требуется", errors, "done-checklist.md")
    ensure_contains(checklist, ".chatgpt/task-launch.yaml", errors, "done-checklist.md")
    ensure_contains(checklist, ".chatgpt/normalized-codex-handoff.md", errors, "done-checklist.md")
    for item in [
        "verification-report.md",
        "done-report.md",
        "CURRENT_FUNCTIONAL_STATE.md",
        "bug report",
    ]:
        ensure_contains(checklist, item, errors, "done-checklist.md")

    launch = launch_yaml.get("launch", {})
    for key in [
        "launch_source",
        "task_class",
        "selected_profile",
        "selected_model",
        "selected_reasoning_effort",
        "apply_mode",
        "strict_launch_mode",
        "project_profile",
        "selected_scenario",
        "pipeline_stage",
        "artifacts_to_update",
        "handoff_allowed",
        "defect_capture_path",
        "launch_artifact_path",
        "launch_command",
        "codex_profile_command",
    ]:
        if not launch.get(key):
            errors.append(f"task-launch.yaml не содержит launch.{key}")
    if launch.get("launch_command") and "launch-codex-task.sh" not in str(launch.get("launch_command", "")):
        errors.append("task-launch.yaml не фиксирует repo launcher внутри launch_command")
    if launch.get("selected_profile") and f"--profile {launch.get('selected_profile')}" not in str(launch.get("codex_profile_command", "")):
        errors.append("task-launch.yaml не фиксирует selected_profile внутри codex_profile_command")
    if launch.get("launch_command") and str(launch.get("launch_artifact_path", "")) not in str(launch.get("launch_command", "")):
        errors.append("task-launch.yaml не фиксирует launch_artifact_path внутри launch_command")
    if launch.get("launch_artifact_path") and not (chat.parent / str(launch.get("launch_artifact_path"))).exists():
        errors.append("task-launch.yaml ссылается на отсутствующий launch_artifact_path")

    ensure_contains(normalized_handoff, "# Normalized Codex Handoff", errors, "normalized-codex-handoff.md")
    for section in [
        "## Launch source",
        "## Task class",
        "## Selected profile",
        "## Selected model",
        "## Selected reasoning effort",
        "## Apply mode",
        "## Manual UI apply",
        "## Strict launch mode",
        "## Project profile",
        "## Selected scenario",
        "## Pipeline stage",
        "## Artifacts to update",
        "## Handoff allowed",
        "## Defect capture path",
        "## Optional strict launch command",
        "## Direct Codex command behind launcher",
        "## Troubleshooting",
    ]:
        ensure_contains(normalized_handoff, section, errors, "normalized-codex-handoff.md")

    ensure_contains(handoff_response, "## Применение в Codex UI", errors, "handoff-response.md")
    ensure_contains(handoff_response, "## Строгий launch mode (опционально)", errors, "handoff-response.md")
    ensure_contains(handoff_response, "## Handoff в Codex", errors, "handoff-response.md")
    ensure_contains(handoff_response, "manual-ui", errors, "handoff-response.md")
    ensure_contains(handoff_response, "launch-codex-task.sh", errors, "handoff-response.md")
    ensure_contains(handoff_response, "новый чат + вставка handoff", errors, "handoff-response.md")
    ensure_contains(handoff_response, "new task launch", errors, "handoff-response.md")
    ensure_contains(handoff_response, "advisory/handoff text != executable profile switch", errors, "handoff-response.md")
    ensure_contains(handoff_response, "sticky last-used state", errors, "handoff-response.md")

    if errors:
        print("CODEX TASK PACK НЕВАЛИДЕН")
        for err in errors:
            print("-", err)
        return 1

    print("CODEX TASK PACK ВАЛИДЕН")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
