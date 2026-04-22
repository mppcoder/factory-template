#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

from codex_task_router import build_launch_record, render_normalized_handoff, write_launch_record


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
    routing_record = build_launch_record(root, "chatgpt-handoff", codex_input)
    write_launch_record(root, routing_record)
    launch = routing_record["launch"]
    (chat / 'normalized-codex-handoff.md').write_text(
        render_normalized_handoff(routing_record, codex_input, "Normalized Codex Handoff"),
        encoding='utf-8',
    )

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

## Launch source
{launch.get('launch_source', 'не определен')}

## Task class
{launch.get('task_class', 'не определен')}

## Selected profile
{launch.get('selected_profile', 'не определен')}

## Selected model
{launch.get('selected_model', 'не определен')}

## Selected reasoning effort
{launch.get('selected_reasoning_effort', 'не определен')}

## Selected plan mode reasoning
{launch.get('selected_plan_mode_reasoning_effort', 'не определен')}

## Executable launch command
{launch.get('launch_command', 'не определен')}

## Direct Codex command behind launcher
{launch.get('codex_profile_command', 'не определен')}

## Project profile
{launch.get('project_profile', 'не определен')}

## Selected scenario
{launch.get('selected_scenario', 'не определен')}

## Pipeline stage
{launch.get('pipeline_stage', 'не определен')}

## Handoff allowed
{launch.get('handoff_allowed', 'не определен')}

## Defect capture path
{launch.get('defect_capture_path', 'не определен')}

## Repo Rules Priority
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

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
- [ ] Проверить `.chatgpt/task-launch.yaml`
- [ ] Проверить `.chatgpt/normalized-codex-handoff.md`
- [ ] Если `origin` настроен и verify green, прогнать `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- [ ] Если prereqs green и diff допустим, прогнать `bash VERIFIED_SYNC.sh` до финального closeout
- [ ] Если verified sync не выполнен, явно зафиксировать реальный blocker и не помечать change как `done`

## Impact classification

- [ ] impact.factory_sources
- [ ] impact.downstream_template_sync
- [ ] impact.downstream_project_sources
- [ ] impact.manual_archive_required
- [ ] impact.delete_before_replace

## Completion Package For Repo-First Instruction Changes

- [ ] Что изменено
- [ ] Какие файлы обновлены в repo
- [ ] Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project
- [ ] Нужно ли обновлять downstream template in battle repos
- [ ] Нужно ли обновлять repo-first инструкции battle ChatGPT Projects
- [ ] Готовые артефакты для скачивания
- [ ] Команды/скрипты для repo-level sync
- [ ] Удалить перед заменой
- [ ] Пошаговая инструкция по окнам
- [ ] Что прислать обратно после внешнего шага
- [ ] Completion package выдан в том же финальном ответе, без дополнительного напоминания пользователя
- [ ] Если есть pending external step, финальный ответ действительно заканчивается блоком `## Инструкция пользователю`
- [ ] Если pending external step нет, финальный ответ явно говорит, что внешних действий не требуется
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

    if active.get('status') == 'нужно_обновить_repo_first_инструкцию':
        sources_line = f'Обновите repo-first инструкцию в ChatGPT Project и начните с {entrypoint}. Сценарии нужно читать прямо из GitHub repo.'
    else:
        sources_line = f'В ChatGPT Project должен действовать repo-first режим: сначала GitHub repo, затем {entrypoint}. Сценарии не должны пересказываться из памяти.'

    route_line = 'Активные стартовые сценарии: ' + (', '.join(active_scenarios) if active_scenarios else 'еще не определены.')
    impact_model = policy.get('boundary_actions', {}).get('completion_impacts', {}) if isinstance(policy.get('boundary_actions', {}), dict) else {}
    impact_defaults = {
        "factory_sources": "Обновление repo-first инструкции проекта шаблона в ChatGPT",
        "downstream_template_sync": "Обновление шаблона в боевых repo",
        "downstream_project_sources": "Обновление repo-first инструкции боевых ChatGPT Projects",
        "manual_archive_required": "Нужен готовый архив или каталог для ручной загрузки",
        "delete_before_replace": "Перед заменой нужно удалить старую repo-first инструкцию, если она конфликтует с новой",
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

## Completion Package For Repo-First Instruction Changes

Если change затрагивает scenario-pack, launcher, validators, runbooks, codex-task-pack, `.chatgpt` artifacts или другой downstream-consumed template content, пользовательский boundary output должен включать:

1. Что изменено
2. Какие файлы обновлены в repo
3. Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project
4. Нужно ли обновлять downstream template in battle repos
5. Нужно ли обновлять repo-first инструкции battle ChatGPT Projects
6. Готовые артефакты для скачивания
7. Команды/скрипты для repo-level sync
8. Удалить перед заменой
9. Пошаговая инструкция по окнам
10. Что прислать обратно после внешнего шага

Обязательно различайте три контура:
- Обновление repo-first инструкции проекта шаблона в ChatGPT
- Обновление шаблона в боевых repo
- Обновление repo-first инструкции боевых ChatGPT Projects

Если contour не затронут, это нужно явно написать.

## Для handoff

- {handoff_line}
- Рабочая единица выбора модели и reasoning mode: только новый task launch, а не старая уже закрепленная сессия.
- `AGENTS`, ChatGPT Project instructions, scenario-pack и `.chatgpt` guidance являются advisory layer; profile/model выбирает executable launcher/router.
- `selected_profile` — это исполнимая граница маршрутизации; `selected_model` и `selected_reasoning_effort` описывают ожидаемую конфигурацию этого profile, а не auto-switch от текста handoff.
- Проверяемая фиксация реального выбора хранится в `.chatgpt/task-launch.yaml`.
- Перед передачей handoff сначала выполните явный launch command из `.chatgpt/task-launch.yaml`, а уже потом вставляйте handoff в свежий Codex task.
- При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
- Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.
- Если выбран `hybrid` или `codex-led`, передать Codex актуальный `codex-task-pack.md`.
- После возврата из Codex обновить verification-report.md, done-report.md и CURRENT_FUNCTIONAL_STATE.md.
- Если handoff уже разрешен и задача достаточно определена, его нужно выдать inline в том же ответе, а не ограничиваться аналитикой.
- Формат handoff для пользователя: только один цельный блок для copy-paste в Codex.
- Нельзя заменять handoff ссылкой на файл, несколькими разрозненными блоками или инструкцией собрать handoff из `codex-input.md`, `codex-context.md`, `codex-task-pack.md`.
- Если remaining work еще остается внутренним repo follow-up, handoff не должен исчезать из-за будущего user footer.
- Release-followup, source-pack refresh, export refresh, closeout-sync и release-facing consistency pass внутри repo считаются внутренней работой Codex.
- Troubleshooting sticky state:
  - если пользователь открыл случайную или уже существующую Codex chat-сессию и просто вставил handoff, profile/model/reasoning могли не переключиться;
  - канонический путь: закрыть такую сессию и выполнить новый task launch через `./scripts/launch-codex-task.sh`;
  - если после этого route все еще выглядит stale, проверить named profile в local Codex config и сверить `selected_model` с live `codex debug models`.

## Для внешних границ

- GitHub / внешние UI / секреты не выполнять автоматически из Codex.
- Все внешние действия фиксировать отдельной пошаговой инструкцией для пользователя с финальным блоком `Инструкция пользователю`.
- `Инструкция пользователю` не должна подменять внутренний handoff, если internal repo follow-up еще не завершен.
- Если внешнего шага нет, финальный ответ все равно должен явно сказать, что внешних действий не требуется.
- Для обновления factory ChatGPT Project сначала сам подготовьте точный repo-first instruction text; этот шаг выполняет Codex внутри repo до пользовательского блока.
- Для downstream repo sync сначала используйте `workspace-packs/factory-ops/export-template-patch.sh` и `workspace-packs/factory-ops/apply-template-patch.sh`.
- Для downstream repo instruction layer source-of-truth хранится в `template-repo/AGENTS.md`, а Codex в battle repo должен читать materialized root `AGENTS.md`.
- Не перекладывайте на пользователя запуск внутренних repo-команд вроде `GENERATE_BOUNDARY_ACTIONS.sh`, если эти шаги может выполнить Codex.
- Если replacement может создать stale duplicates, добавляйте точный раздел `Удалить перед заменой`.

Если closeout полностью внутренний и `Инструкция пользователю` не нужна, используйте явную формулировку вроде:
- `Внешних действий не требуется.`
- `Следующий пользовательский шаг отсутствует; change закрыт полностью внутри repo.`
"""

    handoff_response = f"""## Launch в Codex

```bash
{launch.get('launch_command', './scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute')}
```

- Выполняйте этот launch command из корня repo как новый task launch.
- Advisory handoff text сам по себе не переключает profile/model/reasoning в уже открытой или случайной Codex chat-сессии.
- `selected_profile` — исполнимая граница; `selected_model` и `selected_reasoning_effort` — ожидаемая конфигурация profile, а не promise auto-switch.
- Если видите sticky last-used state, закройте текущую сессию и снова выполните launch command, а затем проверьте local named profile.

## Handoff в Codex

```text
Repo: {root.name}
Цель: выполнить текущий handoff по проекту {root.name}.
Приоритет: сначала правила repo (`AGENTS`, runbook, scenario-pack, policy files), затем общие инструкции без конфликта с ними.
Entry point: {entrypoint}
Launch source: {launch.get('launch_source', 'chatgpt-handoff')}
Task class: {launch.get('task_class', 'build')}
Selected profile: {launch.get('selected_profile', 'build')}
Selected model: {launch.get('selected_model', 'gpt-5.4')}
Selected reasoning effort: {launch.get('selected_reasoning_effort', 'medium')}
Executable launch command: {launch.get('launch_command', './scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute')}
Direct Codex command behind launcher: {launch.get('codex_profile_command', 'codex --profile build')}
Routing rule: advisory/handoff text != executable profile switch; reliable routing unit = new task launch only.
Pipeline stage: {launch.get('pipeline_stage', 'unknown-stage')}
Handoff allowed: {launch.get('handoff_allowed', 'unknown')}
Scope: работать только в пределах этого repo и связанных project artifacts.
Verify: использовать актуальные validators, verification-report.md и done-report.md.
```

## Инструкция пользователю
1. Цель
Передать задачу в Codex уже по нормализованному handoff.
2. Где сделать
В текущем проекте.
3. Точные шаги
Сначала выполнить launch command из блока `Launch в Codex`, затем вставить handoff-блок без пересборки из файлов вручную.
4. Ожидаемый результат
Codex стартует на явной launch boundary и получает один цельный copy-paste handoff по правилам repo.
5. Что прислать обратно
Итог выполнения или уточнение, если появится внешний блокирующий шаг.
"""

    (chat / 'codex-context.md').write_text(context.rstrip() + '\n', encoding='utf-8')
    (chat / 'codex-task-pack.md').write_text(pack.rstrip() + '\n', encoding='utf-8')
    (chat / 'boundary-actions.md').write_text(boundary_actions.rstrip() + '\n', encoding='utf-8')
    (chat / 'done-checklist.md').write_text(checklist.rstrip() + '\n', encoding='utf-8')
    (chat / 'handoff-response.md').write_text(handoff_response.rstrip() + '\n', encoding='utf-8')
    print('Codex task pack собран.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
