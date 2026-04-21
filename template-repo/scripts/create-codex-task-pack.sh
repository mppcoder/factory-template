#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.exists() else ''


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    chat = root / '.chatgpt'
    task = yaml.safe_load((chat / 'task-index.yaml').read_text(encoding='utf-8')) if (chat / 'task-index.yaml').exists() else {}
    stage = yaml.safe_load((chat / 'stage-state.yaml').read_text(encoding='utf-8')) if (chat / 'stage-state.yaml').exists() else {}
    bugflow = yaml.safe_load((chat / 'bugflow-status.yaml').read_text(encoding='utf-8')) if (chat / 'bugflow-status.yaml').exists() else {}
    policy = yaml.safe_load((chat / 'policy-status.yaml').read_text(encoding='utf-8')) if (chat / 'policy-status.yaml').exists() else {}
    active = yaml.safe_load((chat / 'active-scenarios.yaml').read_text(encoding='utf-8')) if (chat / 'active-scenarios.yaml').exists() else {}
    task = task or {}
    stage = stage or {}
    bugflow = bugflow or {}
    policy = policy or {}
    active = active or {}
    change = task.get('change', {})
    classification = read_text(chat / 'classification.md').strip() or 'Классификация еще не заполнена.'
    codex_input = read_text(chat / 'codex-input.md').strip() or 'codex-input.md еще не заполнен.'

    defect_active = bool(bugflow.get('defect_detected')) or ('## Есть ли обнаруженный дефект\nда' in classification) or bool(re.search(r'\bbug\b|дефект|регрес|ошибк|gap', codex_input, re.I))

    bug_block_path = root / 'tasks' / 'codex' / 'codex-task-mandatory-bug-capture.block.md'
    if not bug_block_path.exists():
        bug_block_path = Path(__file__).resolve().parents[1] / 'tasks' / 'codex' / 'codex-task-mandatory-bug-capture.block.md'
    bug_block = "\n\n" + bug_block_path.read_text(encoding='utf-8').strip() + "\n" if defect_active and bug_block_path.exists() else ''

    context = f"""# Контекст для Codex

## Проект
{root.name}

## Классификация
{classification}

## Текущий этап
{stage.get('stage', {}).get('current', 'не определен')}

## Change ID
{change.get('id', 'не указан')}

## Краткое резюме
{change.get('summary', 'не заполнено')}
"""

    pack = f"""# Task pack для Codex

## Change ID
{change.get('id', 'не указан')}

## Заголовок
{change.get('title', 'не заполнен')}

## Класс изменения
{change.get('class', 'не заполнен')}

## Режим выполнения
{change.get('execution_mode', 'не заполнен')}

## Handoff input
{codex_input}{bug_block}
"""

    checklist = """# Чек-лист завершения

- [ ] Проверить, что задача выполнена
- [ ] Обновить verification-report.md
- [ ] Обновить done-report.md
- [ ] Обновить CURRENT_FUNCTIONAL_STATE.md
- [ ] Проверить, нужен ли feedback в фабрику
- [ ] Если был найден defect, создать или обновить bug report

## Impact classification

- [ ] impact.factory_sources
- [ ] impact.downstream_template_sync
- [ ] impact.downstream_project_sources
- [ ] impact.manual_archive_required
- [ ] impact.delete_before_replace

## Completion Package For Source Update Changes

- [ ] Что изменено
- [ ] Какие файлы обновлены в repo
- [ ] Нужно ли обновлять Sources factory-template ChatGPT Project
- [ ] Нужно ли обновлять downstream template in battle repos
- [ ] Нужно ли обновлять Sources battle ChatGPT Projects
- [ ] Готовые артефакты для скачивания
- [ ] Команды/скрипты для repo-level sync
- [ ] Удалить перед заменой
- [ ] Пошаговая инструкция по окнам
- [ ] Что прислать обратно после внешнего шага
- [ ] Completion package выдан в том же финальном ответе, без дополнительного напоминания пользователя
"""

    handoff_policy = policy.get('handoff_policy', 'forbidden')
    raw_active_scenarios = active.get('active_scenarios', active.get('active', []))
    active_scenarios = raw_active_scenarios if isinstance(raw_active_scenarios, list) else []
    scenario_pack = active.get('scenario_pack', {}) if isinstance(active.get('scenario_pack'), dict) else {}
    entrypoint = scenario_pack.get('entrypoint', '00-master-router.md')
    if handoff_policy == 'required':
        handoff_line = 'Handoff в Codex обязателен: завершите handoff только после проверки codex-input.md, evidence-register.md и gate codex_handoff_allowed.'
    elif handoff_policy == 'optional':
        handoff_line = 'Handoff в Codex опционален: сначала проверьте, действительно ли проект дошел до момента передачи в Codex.'
    else:
        handoff_line = 'Handoff в Codex сейчас не является обязательным для выбранного профиля.'

    if active.get('status') == 'нужно_загрузить_в_sources':
        sources_line = f'Загрузите единый scenario-pack в ChatGPT Project Sources через ./scripts/export-sources-pack.sh . и начните с {entrypoint}.'
    else:
        sources_line = f'Sources уже должны быть загружены; если есть сомнения, повторно экспортируйте единый scenario-pack через ./scripts/export-sources-pack.sh . Базовая точка входа: {entrypoint}.'

    route_line = 'Активные стартовые сценарии: ' + (', '.join(active_scenarios) if active_scenarios else 'еще не определены.')
    impact_model = policy.get('boundary_actions', {}).get('completion_impacts', {}) if isinstance(policy.get('boundary_actions', {}), dict) else {}
    impact_defaults = {
        "factory_sources": "Обновление Sources проекта шаблона в ChatGPT",
        "downstream_template_sync": "Обновление шаблона в боевых repo",
        "downstream_project_sources": "Обновление Sources боевых ChatGPT Projects",
        "manual_archive_required": "Нужен готовый архив или каталог для ручной загрузки",
        "delete_before_replace": "Перед заменой нужно удалить старые Sources",
    }
    impact_lines = []
    for key in [
        "factory_sources",
        "downstream_template_sync",
        "downstream_project_sources",
        "manual_archive_required",
        "delete_before_replace",
    ]:
        impact_lines.append(f"- `impact.{key}` — {impact_model.get(key, impact_defaults[key])}")
    impact_block = "\n".join(impact_lines)

    boundary_actions = f"""# Boundary Actions

## Для пользователя

Каноническая финальная секция ответа пользователю называется `Инструкция пользователю` и должна использовать структуру:
1. Цель
2. Где сделать
3. Точные шаги
4. Ожидаемый результат
5. Что прислать обратно

- Создать или открыть ChatGPT Project для этого рабочего проекта.
- {sources_line}
- {route_line}
- Проверить, что Codex получает актуальные `codex-input.md`, `codex-context.md`, `codex-task-pack.md` и `boundary-actions.md`.

## Impact Model

{impact_block}

## Completion Package For Source Update Changes

Если change затрагивает source-pack, scenario-pack, launcher, validators, runbooks, codex-task-pack, `.chatgpt` artifacts или другой downstream-consumed template content, пользовательский boundary output должен включать:

1. Что изменено
2. Какие файлы обновлены в repo
3. Нужно ли обновлять Sources factory-template ChatGPT Project
4. Нужно ли обновлять downstream template in battle repos
5. Нужно ли обновлять Sources battle ChatGPT Projects
6. Готовые артефакты для скачивания
7. Команды/скрипты для repo-level sync
8. Удалить перед заменой
9. Пошаговая инструкция по окнам
10. Что прислать обратно после внешнего шага

Обязательно различайте три контура:
- Обновление Sources проекта шаблона в ChatGPT
- Обновление шаблона в боевых repo
- Обновление Sources боевых ChatGPT Projects

Если contour не затронут, это нужно явно написать.

## Для handoff

- {handoff_line}
- Если выбран `hybrid` или `codex-led`, передать Codex актуальный `codex-task-pack.md`.
- После возврата из Codex обновить verification-report.md, done-report.md и CURRENT_FUNCTIONAL_STATE.md.
- Если handoff уже разрешен и задача достаточно определена, его нужно выдать inline в том же ответе, а не ограничиваться аналитикой.
- Если remaining work еще остается внутренним repo follow-up, handoff не должен исчезать из-за будущего user footer.
- Release-followup, source-pack refresh, export refresh, closeout-sync и release-facing consistency pass внутри repo считаются внутренней работой Codex.

## Для внешних границ

- GitHub / внешние UI / секреты не выполнять автоматически из Codex.
- Все внешние действия фиксировать отдельной пошаговой инструкцией для пользователя с финальным блоком `Инструкция пользователю`.
- `Инструкция пользователю` не должна подменять внутренний handoff, если internal repo follow-up еще не завершен.
- Для factory Sources refresh сначала сам выполните `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh`; этот шаг выполняет Codex внутри repo, после чего пользователю передаются уже готовые generated артефакты в `_sources-export/factory-template/`.
- Для downstream repo sync сначала используйте `workspace-packs/factory-ops/export-template-patch.sh` и `workspace-packs/factory-ops/apply-template-patch.sh`.
- Не перекладывайте на пользователя запуск внутренних repo-команд вроде `EXPORT_FACTORY_TEMPLATE_SOURCES.sh` или `GENERATE_BOUNDARY_ACTIONS.sh`, если эти шаги может выполнить Codex.
- Если replacement может создать stale duplicates, добавляйте точный раздел `Удалить перед заменой`.
"""

    (chat / 'codex-context.md').write_text(context, encoding='utf-8')
    (chat / 'codex-task-pack.md').write_text(pack, encoding='utf-8')
    (chat / 'boundary-actions.md').write_text(boundary_actions, encoding='utf-8')
    (chat / 'done-checklist.md').write_text(checklist, encoding='utf-8')
    print('Codex task pack собран.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
