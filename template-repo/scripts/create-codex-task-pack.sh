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
"""

    handoff_policy = policy.get('handoff_policy', 'forbidden')
    active_scenarios = active.get('active', []) if isinstance(active.get('active'), list) else []
    scenario_status = active.get('status', 'неизвестно')
    if handoff_policy == 'required':
        handoff_line = 'Handoff в Codex обязателен: завершите handoff только после проверки codex-input.md, evidence-register.md и gate codex_handoff_allowed.'
    elif handoff_policy == 'optional':
        handoff_line = 'Handoff в Codex опционален: сначала проверьте, действительно ли проект дошел до момента передачи в Codex.'
    else:
        handoff_line = 'Handoff в Codex сейчас не является обязательным для выбранного профиля.'

    if scenario_status == 'нужно_загрузить_в_sources':
        sources_line = f'Загрузите единый scenario-pack в ChatGPT Project Sources через ./scripts/export-sources-pack.sh . и начните с {active.get("scenario_pack", {}).get("entrypoint", "00-master-router.md")}.'
    else:
        sources_line = 'Sources уже должны быть загружены; если есть сомнения, повторно экспортируйте единый scenario-pack через ./scripts/export-sources-pack.sh .'

    route_line = 'Активные стартовые сценарии: ' + (', '.join(active_scenarios) if active_scenarios else 'еще не определены.')
    boundary_actions = f"""# Boundary Actions

## Для пользователя

- Создать или открыть ChatGPT Project для этого рабочего проекта.
- {sources_line}
- {route_line}
- Проверить, что Codex получает актуальные `codex-input.md`, `codex-task-pack.md` и `boundary-actions.md`.

## Для handoff

- {handoff_line}
- Если выбран `hybrid` или `codex-led`, передать Codex актуальный `codex-task-pack.md`.
- После возврата из Codex обновить verification-report.md, done-report.md и CURRENT_FUNCTIONAL_STATE.md.

## Для внешних границ

- GitHub / внешние UI / секреты не выполнять автоматически из Codex.
- Все внешние действия фиксировать отдельной пошаговой инструкцией для пользователя.
"""

    (chat / 'codex-context.md').write_text(context, encoding='utf-8')
    (chat / 'codex-task-pack.md').write_text(pack, encoding='utf-8')
    (chat / 'boundary-actions.md').write_text(boundary_actions, encoding='utf-8')
    (chat / 'done-checklist.md').write_text(checklist, encoding='utf-8')
    print('Codex task pack собран.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
