#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
import subprocess

import yaml


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def ensure_contains(text: str, needle: str, errors: list[str], label: str) -> None:
    if needle not in text:
        errors.append(f"{label}: отсутствует обязательный фрагмент `{needle}`")


def run_handoff_language_validator(root: Path, path: Path, errors: list[str]) -> None:
    validator = root / "scripts" / "validate-handoff-language.py"
    if not validator.exists():
        fallback = root / "template-repo" / "scripts" / "validate-handoff-language.py"
        validator = fallback if fallback.exists() else validator
    if not validator.exists() or not path.exists():
        return
    result = subprocess.run(
        [sys.executable, str(validator), str(path)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        details = (result.stdout or result.stderr).strip()
        errors.append(f"{path.name}: нарушен language contract входящего handoff\n{details}")


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
    codex_input_path = chat / "codex-input.md"

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
    run_handoff_language_validator(root, codex_input_path, errors)
    run_handoff_language_validator(root, normalized_handoff_path, errors)

    ensure_contains(context, "# Контекст для Codex", errors, "codex-context.md")
    ensure_contains(context, "## Проект", errors, "codex-context.md")
    ensure_contains(context, "## Текущий этап", errors, "codex-context.md")
    ensure_contains(context, "## Идентификатор изменения", errors, "codex-context.md")
    ensure_contains(context, "## Краткое резюме", errors, "codex-context.md")
    if "не указан" in context or "не заполнено" in context:
        errors.append("codex-context.md содержит незаполненные fallback-значения")

    ensure_contains(pack, "# Task pack для Codex", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Идентификатор изменения", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Заголовок", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Класс изменения", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Режим выполнения", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Источник запуска", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Класс задачи", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Выбранный профиль", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Выбранная модель", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Выбранное reasoning effort", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Режим применения", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Строгий режим запуска", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Ручной UI по умолчанию", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Язык ответа Codex", errors, "codex-task-pack.md")
    ensure_contains(pack, "Codex должен отвечать пользователю по-русски", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Опциональная команда строгого запуска", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Прямая команда Codex за launcher", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Выбранный сценарий", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Этап pipeline", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Разрешение handoff", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Маршрут defect-capture", errors, "codex-task-pack.md")
    ensure_contains(pack, "## Входные данные handoff", errors, "codex-task-pack.md")
    ensure_contains(pack, "приоритет у правил repo", errors, "codex-task-pack.md")
    if "codex-input.md еще не заполнен." in pack:
        errors.append("codex-task-pack.md ссылается на пустой codex-input.md")

    ensure_contains(boundary, "# Действия на границе", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для пользователя", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Модель влияния", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Пакет завершения для изменений repo-first инструкций", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для handoff", errors, "boundary-actions.md")
    ensure_contains(boundary, "manual-ui (default)", errors, "boundary-actions.md")
    ensure_contains(boundary, "strict_launch_mode: optional", errors, "boundary-actions.md")
    ensure_contains(boundary, "новый чат + вставка handoff", errors, "boundary-actions.md")
    ensure_contains(boundary, "non-canonical fallback", errors, "boundary-actions.md")
    ensure_contains(boundary, "advisory layer", errors, "boundary-actions.md")
    ensure_contains(boundary, "`.chatgpt/task-launch.yaml`", errors, "boundary-actions.md")
    ensure_contains(boundary, "`selected_profile` — это исполнимая граница маршрутизации", errors, "boundary-actions.md")
    ensure_contains(boundary, "При исполнении handoff приоритет у правил repo", errors, "boundary-actions.md")
    ensure_contains(boundary, "только один цельный блок для вставки в Codex", errors, "boundary-actions.md")
    ensure_contains(boundary, "Нельзя заменять handoff ссылкой на файл", errors, "boundary-actions.md")
    ensure_contains(boundary, "## Для внешних границ", errors, "boundary-actions.md")
    ensure_contains(boundary, "Инструкция пользователю", errors, "boundary-actions.md")
    ensure_contains(boundary, "internal repo follow-up", errors, "boundary-actions.md")
    ensure_contains(boundary, "GitHub repo/remote creation не считать внешним шагом автоматически", errors, "boundary-actions.md")
    ensure_contains(boundary, "создать GitHub repo, добавить `origin` и выполнить первый push", errors, "boundary-actions.md")
    ensure_contains(boundary, 'Просьба пользователю "создай repo на GitHub и пришли URL" допустима только при конкретном blocker', errors, "boundary-actions.md")
    ensure_contains(boundary, "owner/repo, целевой visibility, точную команду или UI-шаг, ожидаемый remote URL", errors, "boundary-actions.md")
    ensure_contains(boundary, "Release-followup, source-pack refresh, export refresh, closeout-sync и release-facing consistency pass внутри repo считаются внутренней работой Codex.", errors, "boundary-actions.md")
    ensure_contains(boundary, "Brownfield source-candidate map, reconstruction allowlist/denylist, change-map и reverse-engineering summary внутри repo тоже считаются внутренней работой Codex.", errors, "boundary-actions.md")
    ensure_contains(boundary, "не завершает ответ просьбой пользователя вручную написать \"продолжай\"", errors, "boundary-actions.md")
    ensure_contains(boundary, "Перед финальным ответом Codex обязан выполнить `git status --short --branch`", errors, "boundary-actions.md")
    ensure_contains(boundary, "dirty worktree или branch ahead без конкретного blocker означает, что closeout еще не завершен", errors, "boundary-actions.md")
    ensure_contains(boundary, "Codex выполняет `VALIDATE_VERIFIED_SYNC_PREREQS.sh` и `VERIFIED_SYNC.sh` сам", errors, "boundary-actions.md")
    ensure_contains(boundary, "commit/push нельзя оставлять пользователю", errors, "boundary-actions.md")
    ensure_contains(boundary, "commit hash / sync status или `no-op`", errors, "boundary-actions.md")
    ensure_contains(boundary, "`Инструкция пользователю` не должна подменять внутренний handoff", errors, "boundary-actions.md")
    ensure_contains(boundary, "Если внешнего шага нет, финальный ответ все равно должен явно сказать, что внешних действий не требуется.", errors, "boundary-actions.md")
    ensure_contains(boundary, "Внешних действий не требуется.", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление repo-first инструкции проекта шаблона в ChatGPT", errors, "boundary-actions.md")
    ensure_contains(boundary, "canonical default — `нет`, если canonical repo/path/entrypoint/instruction text не менялись", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление шаблона в боевых repo", errors, "boundary-actions.md")
    ensure_contains(boundary, "Обновление repo-first инструкции боевых ChatGPT Projects", errors, "boundary-actions.md")
    ensure_contains(boundary, "canonical default — `нет`, если downstream уже живет в чистом repo-first режиме", errors, "boundary-actions.md")
    ensure_contains(boundary, "Рекомендация по внешним действиям", errors, "boundary-actions.md")
    ensure_contains(boundary, "`Рекомендация`: `требуется`, `рекомендуется`, `не требуется`, `опционально` или `только legacy/hybrid fallback`", errors, "boundary-actions.md")
    ensure_contains(boundary, "`Когда выполнять`: сейчас, при следующем downstream sync, только для legacy/hybrid fallback или не выполнять", errors, "boundary-actions.md")
    ensure_contains(boundary, "Реестр внешних действий", errors, "boundary-actions.md")
    ensure_contains(boundary, "Нельзя ограничиваться общей фразой", errors, "boundary-actions.md")
    ensure_contains(boundary, "`factory-template ChatGPT Project instructions`", errors, "boundary-actions.md")
    ensure_contains(boundary, "`downstream/battle repo sync`", errors, "boundary-actions.md")
    ensure_contains(boundary, "`downstream/battle ChatGPT Project instructions`", errors, "boundary-actions.md")
    ensure_contains(boundary, "`Sources fallback`", errors, "boundary-actions.md")
    ensure_contains(boundary, "Удалить перед заменой", errors, "boundary-actions.md")
    ensure_contains(boundary, "factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh", errors, "boundary-actions.md")
    ensure_contains(boundary, "factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh", errors, "boundary-actions.md")
    ensure_contains(boundary, "выполняет Codex внутри repo", errors, "boundary-actions.md")
    ensure_contains(boundary, "Troubleshooting sticky state", errors, "boundary-actions.md")
    ensure_contains(boundary, "Codex обязан отвечать пользователю на русском языке", errors, "boundary-actions.md")
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
    ensure_contains(checklist, "## Классификация влияния", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.factory_sources", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.downstream_template_sync", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.downstream_project_sources", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.manual_archive_required", errors, "done-checklist.md")
    ensure_contains(checklist, "impact.delete_before_replace", errors, "done-checklist.md")
    ensure_contains(checklist, "## Пакет завершения для изменений repo-first инструкций", errors, "done-checklist.md")
    ensure_contains(checklist, "По умолчанию: нет, если canonical repo/path/entrypoint/instruction text не менялись", errors, "done-checklist.md")
    ensure_contains(checklist, "По умолчанию: нет для чистого repo-first режима", errors, "done-checklist.md")
    ensure_contains(checklist, "Рекомендация по внешним действиям", errors, "done-checklist.md")
    ensure_contains(checklist, "Реестр внешних действий", errors, "done-checklist.md")
    ensure_contains(checklist, "Для каждого contour указан статус", errors, "done-checklist.md")
    ensure_contains(checklist, "Для каждого contour указана причина", errors, "done-checklist.md")
    ensure_contains(checklist, "Для каждого contour указано, когда выполнять действие", errors, "done-checklist.md")
    ensure_contains(checklist, "Внешние действия перечислены отдельными actionable строками", errors, "done-checklist.md")
    ensure_contains(checklist, "Пакет завершения выдан в том же финальном ответе", errors, "done-checklist.md")
    ensure_contains(checklist, "bash VALIDATE_VERIFIED_SYNC_PREREQS.sh", errors, "done-checklist.md")
    ensure_contains(checklist, "bash VERIFIED_SYNC.sh", errors, "done-checklist.md")
    ensure_contains(checklist, "Перед финальным ответом выполнить `git status --short --branch`", errors, "done-checklist.md")
    ensure_contains(checklist, "Если branch ahead или рабочее дерево dirty, выполнить sync/push или явно назвать blocker", errors, "done-checklist.md")
    ensure_contains(checklist, "В финальном ответе указать commit hash / sync status или `no-op`", errors, "done-checklist.md")
    ensure_contains(checklist, "не просить пользователя вручную написать \"продолжай\"", errors, "done-checklist.md")
    ensure_contains(checklist, "классифицировать его как internal / external / mixed / fully done", errors, "done-checklist.md")
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

    ensure_contains(normalized_handoff, "# Нормализованный handoff для Codex", errors, "normalized-codex-handoff.md")
    for section in [
        "## Источник запуска",
        "## Класс задачи",
        "## Выбранный профиль",
        "## Выбранная модель",
        "## Выбранное reasoning effort",
        "## Режим применения",
        "## Ручное применение через UI",
        "## Строгий режим запуска",
        "## Профиль проекта",
        "## Выбранный сценарий",
        "## Этап pipeline",
        "## Артефакты для обновления",
        "## Разрешение handoff",
        "## Маршрут defect-capture",
        "## Опциональная команда строгого запуска",
        "## Прямая команда Codex за launcher",
        "## Диагностика проблем",
    ]:
        ensure_contains(normalized_handoff, section, errors, "normalized-codex-handoff.md")

    ensure_contains(handoff_response, "## Применение в Codex UI", errors, "handoff-response.md")
    ensure_contains(handoff_response, "## Строгий launch mode (опционально)", errors, "handoff-response.md")
    ensure_contains(handoff_response, "## Handoff в Codex", errors, "handoff-response.md")
    ensure_contains(handoff_response, "Язык ответа Codex: русский", errors, "handoff-response.md")
    ensure_contains(handoff_response, "Отвечай пользователю по-русски", errors, "handoff-response.md")
    ensure_contains(handoff_response, "manual-ui", errors, "handoff-response.md")
    ensure_contains(handoff_response, "launch-codex-task.sh", errors, "handoff-response.md")
    ensure_contains(handoff_response, "новый чат + вставка handoff", errors, "handoff-response.md")
    ensure_contains(handoff_response, "новый task launch", errors, "handoff-response.md")
    ensure_contains(handoff_response, "advisory/handoff text не равен executable profile switch", errors, "handoff-response.md")
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
