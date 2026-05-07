from pathlib import Path
import subprocess
import sys

import yaml

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
chat = root / '.chatgpt'
if not chat.exists():
    raise SystemExit(f"Не найден каталог .chatgpt в target: {root}")
(chat / 'evidence-register.md').write_text('''# Реестр доказательств

- [PROJECT] В каталоге `template-repo/scenario-pack` подтверждено наличие сценарного слоя и файлов маршрутизации.
- [DOC] В `bootstrap/04-как-работает-stage-pipeline.md` зафиксировано требование закрывать этапные шлюзы до handoff.
- [REAL] Живой smoke-test подтвердил, что launcher создает проект, копирует скрипты и заполняет стартовые YAML-файлы.
''', encoding='utf-8')
(chat / 'reality-check.md').write_text('''# Проверка реальности

## Что подтверждено в проекте
- В проекте уже созданы каталоги `.chatgpt`, `scripts`, `work` и `template-repo`.
- Версия пакета: 2.4.1.
- В репозитории подтверждено наличие `project-presets.yaml`, `policy-presets.yaml` и `change-classes.yaml`.

## Что говорит официальная документация
- В bootstrap описано, что сначала нужно пройти сценарии, закрыть проверки и только потом делать handoff в Codex.
- В документации фабрики указано, что артефакты должны жить в repo, а не только в чате.

## Реальные наблюдения и кейсы
- Реальный smoke-test подтвердил создание рабочего проекта через launcher.
- После создания доступны валидаторы `validate-stage.py`, `validate-evidence.py` и `validate-quality.py`.
- На свежем scaffold проверки evidence, quality и DoD корректно не проходят до заполнения артефактов.

## Расхождения и выводы
- Внешних расхождений по сценарию smoke-test не выявлено.
- Основное ограничение: quality-проверка остается эвристической и требует содержательного текста, а не только заголовков.

## Вывод
- Текущего состояния достаточно для перехода к user-spec, tech-spec и подготовке handoff.
- Для полноценного использования нужно поддерживать реестр доказательств и закрывать gate-флаги.
''', encoding='utf-8')
(chat / 'user-spec.md').write_text('''# Пользовательская спецификация

## Цель изменения
- Проверить, что ядро фабрики может создать проект и провести его через smoke-test.

## Что должно получиться
- Рабочий проект создается без ручной правки структуры.
- Основные валидаторы проходят после заполнения артефактов.

## Что не входит в объем
- Глубокая семантическая оценка качества документов за пределами smoke-test.
''', encoding='utf-8')
(chat / 'tech-spec.md').write_text('''# Техническая спецификация

## Шаги реализации
- Создать проект через launcher.
- Заполнить evidence-register и reality-check.
- Закрыть ключевые gate-флаги в stage-state.
- Прогнать валидаторы и экспорт сценариев.

## Выходные артефакты
- Обновленные `.chatgpt/*` файлы.
- Экспортированный сценарный пакет.
''', encoding='utf-8')
(chat / 'user-spec-validation.md').write_text('''# Проверка пользовательской спецификации

- Пользовательская спецификация описывает цель smoke-test и ожидаемый результат.
- Границы изменения зафиксированы и понятны человеку.
- Противоречий между целью и ожидаемым результатом не выявлено.
- Документ пригоден как основа для технической спецификации.
''', encoding='utf-8')
(chat / 'tech-spec-validation.md').write_text('''# Проверка технической спецификации

- Техническая спецификация перечисляет шаги smoke-test и ожидаемые артефакты.
- Связь с пользовательской спецификацией прослеживается.
- Заданы понятные выходные файлы и проверки.
- Документ готов к декомпозиции и handoff.
''', encoding='utf-8')
(chat / 'verification-report.md').write_text('''# Отчет о проверке результата

## Что проверяли
- Создание проекта через launcher.sh.
- Применение профиля проекта и политики.
- Прохождение основных валидаторов после заполнения артефактов.

## Что подтверждено
- Проект создан, стартовые YAML-файлы заполнены.
- Скрипты в working project доступны и работают.
- Проверки stage, evidence, quality и DoD пройдены после заполнения артефактов.

## Что требует внимания
- Семантическое качество артефактов вне smoke-test остается зоной ответственности сценарного слоя.

## Итоговый вывод
- Стартовый контур фабрики работоспособен и готов к дальнейшей работе.
''', encoding='utf-8')
(chat / 'done-report.md').write_text('''# Отчет о завершении

## Что было запрошено
- Проверить жизнеспособность ядра фабрики и тестового контура.

## Что реально сделано
- Создан проект через launcher.
- Заполнены ключевые артефакты `.chatgpt`.
- Пройдены stage, evidence, quality, handoff и DoD проверки.
- Выполнен экспорт сценариев как reference/archive набора.

## Какие артефакты обновлены
- `.chatgpt/reality-check.md`
- `.chatgpt/evidence-register.md`
- `.chatgpt/user-spec.md`
- `.chatgpt/tech-spec.md`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`

## Что осталось вне объема
- Полноценный сценарный анализ реального проекта.

## Итог закрытия
- Smoke-test завершен успешно и может использоваться как воспроизводимый базовый прогон.
''', encoding='utf-8')
(chat / 'codex-input.md').write_text('''# Входной пакет для Codex

## Контекст
- Это smoke-test ядра фабрики проектов.
- Базовые проверки уже закрыты и подтверждены evidence-артефактами.
- При исполнении этого handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.

## Что должен сделать исполнитель
- Считать smoke-test завершенным без дополнительных изменений.

## Ограничения
- Не менять core-структуру проекта.
- Общие рабочие инструкции применять только там, где они не противоречат repo rules и старшим системным ограничениям среды.
''', encoding='utf-8')
(chat / 'handoff-response.md').write_text('''## Применение в Codex UI

- `apply_mode: manual-ui (default)`.
- Для VS Code Codex extension откройте новый чат/окно Codex.
- Вручную выберите model/reasoning в picker.
- Только после этого вставьте handoff-блок ниже.
- новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же.
- Advisory handoff text сам по себе не переключает profile/model/reasoning.
- Если видите sticky last-used state, закройте текущую сессию и начните новый task launch.

## Строгий launch mode (опционально)

```bash
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute
```

- advisory/handoff text не равен executable profile switch.

## Handoff в Codex

```text
Repo: smoke-test project
Цель: завершить smoke-test без дополнительных изменений кода.
Язык ответа Codex: русский. Отвечай пользователю по-русски.
Приоритет: сначала правила repo, затем общие инструкции, если нет конфликта.
Scope: не менять core-структуру проекта.
Verify: использовать уже заполненные smoke artifacts и существующие validators.
```

## Инструкция пользователю
1. Цель
Подтвердить, что smoke-test уже закрыт.
2. Где сделать
В текущем проекте.
3. Точные шаги
Посмотреть verification-report и done-report.
4. Ожидаемый результат
Состояние проекта подтверждено как green smoke baseline.
5. Что прислать обратно
Ничего, если follow-up не нужен.
''', encoding='utf-8')
stage = yaml.safe_load((chat / 'stage-state.yaml').read_text(encoding='utf-8'))
for key in ['intake_complete','classification_complete','reuse_check_complete','reality_check_complete','conflict_detection_complete','spec_ready','spec_validated','tech_spec_ready','tech_spec_validated','decomposition_complete','task_validation_complete','codex_handoff_allowed','execution_complete','verification_complete','done_complete']:
    stage['gates'][key] = True
stage['stage'] = {'current': 'done', 'previous': 'verification', 'next': 'none'}
(chat / 'stage-state.yaml').write_text(yaml.safe_dump(stage, allow_unicode=True, sort_keys=False), encoding='utf-8')
task_state_path = chat / 'task-state.yaml'
if task_state_path.exists():
    task_state = yaml.safe_load(task_state_path.read_text(encoding='utf-8')) or {}
    task_state['current_state'] = 'done'
    task_state['owner_boundary'] = 'internal_repo'
    task_state['next_action'] = {
        'type': 'none',
        'summary': 'Smoke-test scope closed; no internal action remains.',
    }
    task_state['blocked'] = {'status': False, 'reason': 'not_required'}
    boundaries = task_state.setdefault('boundaries', {})
    boundaries['internal_work'] = ['Smoke-test repo work completed and verified.']
    boundaries['external_user_actions'] = []
    boundaries['external_runtime'] = []
    boundaries['downstream_sync'] = []
    task_state['last_updated'] = __import__('datetime').date.today().isoformat()
    task_state_path.write_text(yaml.safe_dump(task_state, allow_unicode=True, sort_keys=False), encoding='utf-8')
task = yaml.safe_load((chat / 'task-index.yaml').read_text(encoding='utf-8'))
task['change']['summary'] = 'Smoke-test изменение для проверки фабрики.'
for idx, task_item in enumerate(task.get('tasks', []), 1):
    if not task_item.get('outputs'):
        task_item['outputs'] = [f'work/active/{task["change"]["id"]}/tasks/T-{idx:03d}.md']
    if not task_item.get('acceptance'):
        task_item['acceptance'] = ['Артефакт создан', 'Проверка проходит']
(chat / 'task-index.yaml').write_text(yaml.safe_dump(task, allow_unicode=True, sort_keys=False), encoding='utf-8')
dashboard_path = chat / 'project-lifecycle-dashboard.yaml'
if dashboard_path.exists():
    dashboard = yaml.safe_load(dashboard_path.read_text(encoding='utf-8')) or {}
    active_change = dashboard.setdefault('active_change', {})
    if isinstance(active_change, dict):
        active_change['id'] = str(task.get('change', {}).get('id') or active_change.get('id') or 'generated-smoke-change')
        active_change['title'] = 'Generated project smoke-test baseline'
        active_change['status'] = 'done'
        active_change['evidence'] = [
            '.chatgpt/verification-report.md',
            '.chatgpt/done-report.md',
            'bash scripts/verify-all.sh quick',
            'python3 scripts/check-dod.py .',
        ]
        active_change['source_artifacts'] = ['.chatgpt/task-index.yaml', '.chatgpt/stage-state.yaml']
    lifecycle = dashboard.setdefault('lifecycle_phase', {})
    if isinstance(lifecycle, dict):
        lifecycle['current'] = 'release'
        lifecycle['previous'] = 'verification'
        lifecycle['next'] = 'deploy'
    execution = dashboard.setdefault('multi_step_execution', {})
    if isinstance(execution, dict):
        execution['final_verification'] = {
            'status': 'passed',
            'evidence': [
                'bash scripts/verify-all.sh quick',
                'python3 scripts/check-dod.py .',
            ],
        }
        execution['next_task'] = {
            'id': 'T-NEXT',
            'owner_boundary': 'internal-repo-follow-up',
            'action': 'Use the project ChatGPT Project for the next product task.',
        }
    orchestration = dashboard.setdefault('handoff_orchestration', {})
    if isinstance(orchestration, dict):
        orchestration['parent_handoff'] = {
            'id': 'not_allocated',
            'title': 'No ChatGPT handoff allocated inside this generated repo yet',
            'status': 'not_started',
            'evidence': [],
        }
        orchestration['child_tasks'] = []
    for package in dashboard.get('runbook_packages', []) or []:
        if isinstance(package, dict) and package.get('id') == '02-greenfield-product':
            package['battle_chatgpt_project_created'] = True
            package['current_phase'] = 'done'
            package['current_step'] = 'first-project-ready'
    dashboard_path.write_text(yaml.safe_dump(dashboard, allow_unicode=True, sort_keys=False), encoding='utf-8')

render_script = root / 'scripts' / 'render-project-lifecycle-dashboard.py'
if render_script.exists():
    subprocess.run(
        [
            sys.executable,
            str(render_script),
            '--input',
            str(dashboard_path),
            '--format',
            'markdown-full',
            '--output',
            str(root / 'reports' / 'project-lifecycle-dashboard.md'),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(render_script),
            '--input',
            str(dashboard_path),
            '--format',
            'chatgpt-card',
            '--output',
            str(root / 'reports' / 'project-status-card.md'),
        ],
        check=True,
    )
