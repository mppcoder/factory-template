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
        render_normalized_handoff(routing_record, codex_input, "Нормализованный handoff для Codex"),
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

## Идентификатор изменения
{change.get('id', 'не указан')}

## Краткое резюме
{change.get('summary', 'не заполнено')}
"""

    pack = f"""# Task pack для Codex

## Идентификатор изменения
{change.get('id', 'не указан')}

## Заголовок
{change.get('title', 'не заполнен')}

## Класс изменения
{change.get('class', 'не заполнен')}

## Режим выполнения
{change.get('execution_mode', 'не заполнен')}

## Источник запуска
{launch.get('launch_source', 'не определен')}

## Класс задачи
{launch.get('task_class', 'не определен')}

## Выбранный профиль
{launch.get('selected_profile', 'не определен')}

## Выбранная модель
{launch.get('selected_model', 'не определен')}

## Выбранное reasoning effort
{launch.get('selected_reasoning_effort', 'не определен')}

## Выбранное reasoning effort для plan mode
{launch.get('selected_plan_mode_reasoning_effort', 'не определен')}

## Статус model catalog
{launch.get('model_catalog_status', 'не определен')}

## Примечание по live availability
{launch.get('model_catalog_validation_note', 'selected_model является repo-configured mapping и требует live validation через codex debug models')}

## Режим применения
{launch.get('apply_mode', 'не определен')}

## Строгий режим запуска
{launch.get('strict_launch_mode', 'не определен')}

## Ручной UI по умолчанию
Для интерактивной работы в VS Code Codex extension откройте новый чат/окно Codex, вручную выберите `selected_model={launch.get('selected_model', 'не определен')}` и `selected_reasoning_effort={launch.get('selected_reasoning_effort', 'не определен')}` в picker, затем вставьте handoff.
Новый чат + вставка handoff и executable launcher path — не одно и то же.
Уже открытая live session не является надежным auto-switch механизмом.

## Язык ответа Codex
Русский. Codex должен отвечать пользователю по-русски; английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Опциональная команда строгого запуска
{launch.get('launch_command', 'не определен')}

## Прямая команда Codex за launcher
{launch.get('codex_profile_command', 'не определен')}

## Профиль проекта
{launch.get('project_profile', 'не определен')}

## Выбранный сценарий
{launch.get('selected_scenario', 'не определен')}

## Этап pipeline
{launch.get('pipeline_stage', 'не определен')}

## Разрешение handoff
{launch.get('handoff_allowed', 'не определен')}

## Маршрут defect-capture
{launch.get('defect_capture_path', 'не определен')}

## Приоритет правил repo
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Входные данные handoff
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
- [ ] Перед финальным ответом выполнить `git status --short --branch`
- [ ] Если branch ahead или рабочее дерево dirty, выполнить sync/push или явно назвать blocker
- [ ] В финальном ответе указать commit hash / sync status или `no-op`
- [ ] Если остался внутренний Codex-eligible follow-up, выполнить его в текущем task или выдать inline handoff; не просить пользователя вручную написать "продолжай"
- [ ] Если в финале назван следующий этап pipeline, классифицировать его как internal / external / mixed / fully done до отправки ответа

## Классификация влияния

- [ ] impact.factory_sources
- [ ] impact.downstream_template_sync
- [ ] impact.downstream_project_sources
- [ ] impact.manual_archive_required
- [ ] impact.delete_before_replace

## Пакет завершения для изменений repo-first инструкций

- [ ] Что изменено
- [ ] Какие файлы обновлены в repo
- [ ] Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project
- [ ] По умолчанию: нет, если canonical repo/path/entrypoint/instruction text не менялись
- [ ] Нужно ли обновлять downstream template in battle repos
- [ ] Нужно ли обновлять repo-first инструкции battle ChatGPT Projects
  По умолчанию: нет для чистого repo-first режима; да только для legacy/hybrid fallback
- [ ] Готовые артефакты для скачивания
- [ ] Команды/скрипты для repo-level sync
- [ ] Удалить перед заменой
- [ ] Пошаговая инструкция по окнам
- [ ] Что прислать обратно после внешнего шага
- [ ] Рекомендация по внешним действиям
- [ ] Реестр внешних действий
- [ ] Для каждого contour указан статус: `требуется`, `рекомендуется`, `не требуется`, `опционально` или `только legacy/hybrid fallback`
- [ ] Для каждого contour указана причина и точное действие пользователя или `действие не требуется`
- [ ] Для каждого contour указано, когда выполнять действие: сейчас, при следующем downstream sync, только для legacy/hybrid fallback или не выполнять
- [ ] Внешние действия перечислены отдельными actionable строками, а не только общей фразой в summary
- [ ] Пакет завершения выдан в том же финальном ответе, без дополнительного напоминания пользователя
- [ ] Если есть ожидающий внешний шаг, финальный ответ действительно заканчивается блоком `## Инструкция пользователю`
- [ ] Если ожидающего внешнего шага нет, финальный ответ явно говорит, что внешних действий не требуется
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
        "factory_sources": "Обновление repo-first инструкции проекта шаблона в ChatGPT только если изменились canonical repo/path/entrypoint или короткая instruction text; иначе по умолчанию не требуется",
        "downstream_template_sync": "Обновление шаблона в боевых repo",
        "downstream_project_sources": "Обновление repo-first инструкции боевых ChatGPT Projects только для legacy/hybrid fallback; для чистого repo-first режима по умолчанию не требуется",
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

    boundary_actions = f"""# Действия на границе

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

## Модель влияния

{impact_block}

## Пакет завершения для изменений repo-first инструкций

Если change затрагивает scenario-pack, launcher, validators, runbooks, codex-task-pack, `.chatgpt` artifacts или другой downstream-consumed template content, пользовательский boundary output должен включать:

1. Что изменено
2. Какие файлы обновлены в repo
3. Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project
   По умолчанию: нет, если canonical repo/path/entrypoint/instruction text не менялись
4. Нужно ли обновлять downstream template in battle repos
5. Нужно ли обновлять repo-first инструкции battle ChatGPT Projects
   По умолчанию: нет для чистого repo-first режима; да только для legacy/hybrid fallback
6. Готовые артефакты для скачивания
7. Команды/скрипты для repo-level sync
8. Удалить перед заменой
9. Пошаговая инструкция по окнам
10. Что прислать обратно после внешнего шага

Отдельно обязателен подраздел `Рекомендация по внешним действиям`.
В нем для каждого внешнего contour нужно явно указать:
- `Рекомендация`: `требуется`, `рекомендуется`, `не требуется`, `опционально` или `только legacy/hybrid fallback`;
- `Причина`: почему именно такой статус;
- `Действие пользователя`: точная команда, UI-шаг или фраза `действие не требуется`.
- `Когда выполнять`: сейчас, при следующем downstream sync, только для legacy/hybrid fallback или не выполнять.

Сразу после рекомендации нужен `Реестр внешних действий`: отдельные actionable строки по каждому contour. Нельзя ограничиваться общей фразой "downstream sync рекомендуется" без точного действия и момента выполнения.

Минимальный набор contour'ов для recommendation:
- `factory-template ChatGPT Project instructions`;
- `downstream/battle repo sync`;
- `downstream/battle ChatGPT Project instructions`;
- `Sources fallback`.

Обязательно различайте три контура:
- Обновление repo-first инструкции проекта шаблона в ChatGPT
- Обновление шаблона в боевых repo
- Обновление repo-first инструкции боевых ChatGPT Projects

Если contour не затронут, это нужно явно написать.
Для contour `Обновление repo-first инструкции проекта шаблона в ChatGPT` canonical default — `нет`, если canonical repo/path/entrypoint/instruction text не менялись.
Для contour `Обновление repo-first инструкции боевых ChatGPT Projects` canonical default — `нет`, если downstream уже живет в чистом repo-first режиме.

## Для handoff

- {handoff_line}
- `apply_mode: manual-ui (default)` — основной user-facing путь для интерактивной работы через VS Code Codex extension.
- Для ручного применения через UI откройте новый чат/окно Codex, вручную выберите `selected_model={launch.get('selected_model', 'не определен')}` и `selected_reasoning_effort={launch.get('selected_reasoning_effort', 'не определен')}` в picker, затем вставьте handoff.
- `strict_launch_mode: optional` — используйте launch command из `.chatgpt/task-launch.yaml`, если нужна automation, reproducibility, shell-first или scripted launch.
- `новый чат + вставка handoff` и `новый task launch через executable launcher` — не одно и то же.
- Уже открытая live session является только non-canonical fallback и не должна подаваться как надежный auto-switch path.
- `AGENTS`, ChatGPT Project instructions, scenario-pack и `.chatgpt` guidance являются advisory layer; profile/model выбирает executable launcher/router.
- `selected_profile` — это исполнимая граница маршрутизации; `selected_model` и `selected_reasoning_effort` описывают repo-configured mapping этого profile, а не auto-switch от текста handoff.
- Model availability auto-check выполняется через `scripts/check-codex-model-catalog.py` / `codex debug models`; если catalog недоступен или stale, не утверждайте, что selected_model точно live-available.
- Если новый model появляется в live catalog, сначала создайте proposal через `--write-proposal`; promotion существующего profile требует ручного review.
- Проверяемая фиксация реального выбора хранится в `.chatgpt/task-launch.yaml`.
- При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
- Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.
- Если выбран `hybrid` или `codex-led`, передать Codex актуальный `codex-task-pack.md`.
- После возврата из Codex обновить verification-report.md, done-report.md и CURRENT_FUNCTIONAL_STATE.md.
- Если handoff уже разрешен и задача достаточно определена, его нужно выдать inline в том же ответе, а не ограничиваться аналитикой.
- Формат handoff для пользователя: только один цельный блок для вставки в Codex.
- Нельзя заменять handoff ссылкой на файл, несколькими разрозненными блоками или инструкцией собрать handoff из `codex-input.md`, `codex-context.md`, `codex-task-pack.md`.
- Если remaining work еще остается внутренним repo follow-up, handoff не должен исчезать из-за будущего user footer.
- Release-followup, source-pack refresh, export refresh, closeout-sync и release-facing consistency pass внутри repo считаются внутренней работой Codex.
- Brownfield source-candidate map, reconstruction allowlist/denylist, change-map и reverse-engineering summary внутри repo тоже считаются внутренней работой Codex.
- Если такой внутренний follow-up уже назван и route текущей live-сессии совместим, Codex продолжает выполнение в этом task и не завершает ответ просьбой пользователя вручную написать "продолжай".
- Перед финальным ответом Codex обязан выполнить `git status --short --branch`; dirty worktree или branch ahead без конкретного blocker означает, что closeout еще не завершен.
- Если `origin` настроен, verify green и sync технически доступен, Codex выполняет `VALIDATE_VERIFIED_SYNC_PREREQS.sh` и `VERIFIED_SYNC.sh` сам; commit/push нельзя оставлять пользователю.
- Финальный ответ по внутренне закрытому repo change должен назвать commit hash / sync status или `no-op`.
- Человекочитаемые заголовки, инструкции, отчеты и closeout-тексты должны быть на русском языке; английский допустим только для технических идентификаторов, команд, файлов, ключей конфигурации и literal values.
- Upstream ChatGPT-generated handoff в `.chatgpt/codex-input.md` тоже должен быть на русском в человекочитаемом слое; англоязычные разделы `Goal`, `Hard constraints`, `Required implementation`, `Verification commands`, `Completion requirements` считаются language-contract defect.
- Codex обязан отвечать пользователю на русском языке. Английский допустим только для technical literal values: команды, пути, ключи конфигурации, model IDs и route fields.
- Troubleshooting sticky state:
  - если пользователь открыл случайную или уже существующую Codex chat-сессию и просто вставил handoff, profile/model/reasoning могли не переключиться;
  - для интерактивного процесса сначала закройте устаревшую сессию, откройте новую и вручную проверьте picker;
  - если нужна строгая boundary-гарантия, выполните optional strict launch command через `./scripts/launch-codex-task.sh`;
  - если после этого route все еще выглядит устаревшим, проверить именованный profile в local Codex config и сверить `selected_model` с live `codex debug models`.

## Для внешних границ

- GitHub PR merge не считать внешним шагом автоматически. Если `gh` или GitHub connector доступен, PR относится к текущей задаче, checks green, PR mergeable и нет required human approval/conflict/неясной merge strategy, Codex должен сам выполнить ready/merge/delete-branch/local sync.
- GitHub repo/remote creation не считать внешним шагом автоматически. Если `gh` или GitHub connector доступен с write permissions, owner/name однозначны и repo можно безопасно создать или использовать, Codex должен сам создать GitHub repo, добавить `origin` и выполнить первый push.
- Просьба пользователю "создай repo на GitHub и пришли URL" допустима только при конкретном blocker: нет авторизации, нет прав, неоднозначный owner/name, repo name conflict без безопасного решения или требуется человеческое security/release approval.
- GitHub UI считать внешним шагом только при конкретном блокере: нет авторизации, нет прав, required human review/approval, red/pending checks, конфликт, release/security approval или другое действие, которое нельзя безопасно выполнить инструментами Codex.
- Внешние UI / секреты не выполнять автоматически из Codex.
- Все внешние действия фиксировать отдельной пошаговой инструкцией для пользователя с финальным блоком `Инструкция пользователю`.
- Финальный блок должен содержать `Рекомендация по внешним действиям` с явным статусом для каждого contour: `требуется`, `рекомендуется`, `не требуется`, `опционально` или `только legacy/hybrid fallback`.
- Если GitHub repo creation действительно заблокирован, `Инструкция пользователю` должна явно указать owner/repo, целевой visibility, точную команду или UI-шаг, ожидаемый remote URL, команду проверки и что прислать обратно.
- `Инструкция пользователю` не должна подменять внутренний handoff, если internal repo follow-up еще не завершен.
- Если внешнего шага нет, финальный ответ все равно должен явно сказать, что внешних действий не требуется.
- Для обновления factory ChatGPT Project сначала сам подготовьте точный repo-first instruction text; этот шаг выполняет Codex внутри repo до пользовательского блока.
- Для downstream repo sync сначала используйте `factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh` и `factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh`.
- Для downstream repo instruction layer source-of-truth хранится в `template-repo/AGENTS.md`, а Codex в battle repo должен читать materialized root `AGENTS.md`.
- Не перекладывайте на пользователя запуск внутренних repo-команд вроде `GENERATE_BOUNDARY_ACTIONS.sh`, если эти шаги может выполнить Codex.
- Если замена может создать устаревшие дубликаты, добавляйте точный раздел `Удалить перед заменой`.

Если closeout полностью внутренний и `Инструкция пользователю` не нужна, используйте явную формулировку вроде:
- `Внешних действий не требуется.`
- `Следующий пользовательский шаг отсутствует; change закрыт полностью внутри repo.`
"""

    handoff_response = f"""## Применение в Codex UI

- `apply_mode: {launch.get('apply_mode', 'manual-ui')} (default)`
- Для VS Code Codex extension откройте новый чат/окно Codex.
- Вручную выберите model `{launch.get('selected_model', 'gpt-5.4')}` и reasoning `{launch.get('selected_reasoning_effort', 'medium')}` в picker.
- Только после этого вставьте handoff-блок ниже.
- новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же.
- Advisory handoff text сам по себе не переключает profile/model/reasoning в уже открытой или случайной Codex chat-сессии.
- Уже открытая live session не является надежным механизмом автопереключения.
- `selected_profile` — исполнимая граница; `selected_model` и `selected_reasoning_effort` — repo-configured mapping profile, а не promise auto-switch или live availability guarantee.
- `model_catalog_status: {launch.get('model_catalog_status', 'unknown')}`; `selected_model` требует live validation, если catalog недоступен или stale.
- Если видите sticky last-used state, закройте текущую сессию, откройте новую и заново проверьте picker.

## Строгий launch mode (опционально)

- `strict_launch_mode: {launch.get('strict_launch_mode', 'optional')}`
- Используйте этот путь, если нужна automation, reproducibility, shell-first или scripted launch.

```bash
{launch.get('launch_command', './scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute')}
```

- Это строгая executable boundary для нового task launch.
- Если ручное применение через UI выглядит устаревшим или нужен строго воспроизводимый route, закройте текущую сессию и используйте эту команду.

## Handoff в Codex

```text
Репозиторий: {root.name}
Цель: выполнить текущий handoff по проекту {root.name}.
Язык ответа Codex: русский. Отвечай пользователю по-русски; английский оставляй только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.
Приоритет: сначала правила repo (`AGENTS`, runbook, scenario-pack, policy files), затем общие инструкции без конфликта с ними.
Точка входа: {entrypoint}
Источник запуска: {launch.get('launch_source', 'chatgpt-handoff')}
Класс задачи: {launch.get('task_class', 'build')}
Выбранный профиль: {launch.get('selected_profile', 'build')}
Выбранная модель: {launch.get('selected_model', 'gpt-5.4')}
Выбранное reasoning effort: {launch.get('selected_reasoning_effort', 'medium')}
Выбранное plan mode reasoning effort: {launch.get('selected_plan_mode_reasoning_effort', 'medium')}
Статус model catalog: {launch.get('model_catalog_status', 'unknown')}
Примечание по live availability: {launch.get('model_catalog_validation_note', 'selected_model repo-configured; требует live validation')}
Режим применения: {launch.get('apply_mode', 'manual-ui')} (default)
Строгий режим запуска: {launch.get('strict_launch_mode', 'optional')}
Опциональная команда строгого запуска: {launch.get('launch_command', './scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute')}
Прямая команда Codex за launcher: {launch.get('codex_profile_command', 'codex --profile build')}
Правило маршрутизации: advisory/handoff text не равен executable profile switch; надежная единица маршрутизации — только новый task launch.
Правило ручного UI: для VS Code Codex extension откройте новый чат/окно, вручную выберите model/reasoning в picker, затем вставьте этот handoff.
Правило live session: уже открытая live session = non-canonical fallback; не обещать auto-switch.
Этап pipeline: {launch.get('pipeline_stage', 'unknown-stage')}
Разрешение handoff: {launch.get('handoff_allowed', 'unknown')}
Область работы: работать только в пределах этого repo и связанных project artifacts.
Проверка: использовать актуальные validators, verification-report.md и done-report.md.
```

## Инструкция пользователю
1. Цель
Передать задачу в Codex уже по нормализованному handoff.
2. Где сделать
В VS Code Codex extension или, при необходимости strict routing, через терминал в текущем проекте.
3. Точные шаги
По умолчанию используйте блок `Применение в Codex UI`: новый чат/окно, ручной выбор model/reasoning в picker, затем вставка handoff-блока без пересборки из файлов вручную. Если нужна строгая воспроизводимость, используйте блок `Строгий launch mode (опционально)`.
4. Ожидаемый результат
Codex получает один цельный handoff для вставки по правилам repo, а пользователь выбирает между ручным применением через UI по умолчанию и опциональным строгим launch path.
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
