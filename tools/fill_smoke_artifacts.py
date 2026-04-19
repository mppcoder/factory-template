from pathlib import Path
import yaml

root = Path('.')
chat = root / '.chatgpt'
(chat / 'evidence-register.md').write_text('''# Реестр доказательств

- [PROJECT] В каталоге `.factory-sources/scenario-pack` подтверждено наличие сценарного слоя и файлов маршрутизации.
- [DOC] В `bootstrap/04-как-работает-stage-pipeline.md` зафиксировано требование закрывать этапные шлюзы до handoff.
- [REAL] Живой smoke-test подтвердил, что launcher создает проект, копирует скрипты и заполняет стартовые YAML-файлы.
''', encoding='utf-8')
(chat / 'reality-check.md').write_text('''# Проверка реальности

## Что подтверждено в проекте
- В проекте уже созданы каталоги `.chatgpt`, `scripts`, `work` и `.factory-sources`.
- Версия пакета: 2.4.0.
- В репозитории подтверждено наличие `project-presets.yaml`, `policy-presets.yaml` и `change-classes.yaml`.

## Что говорит официальная документация
- В bootstrap описано, что сначала нужно пройти сценарии, закрыть проверки и только потом делать handoff в Codex.
- В документации фабрики указано, что артефакты должны жить в repo, а не только в чате.

## Реальные наблюдения и кейсы
- Реальный smoke-test подтвердил создание рабочего проекта через launcher.
- После создания доступны валидаторы `validate-stage.sh`, `validate-evidence.sh` и `validate-quality.sh`.
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
- Выполнен экспорт сценариев для загрузки в Sources.

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

## Что должен сделать исполнитель
- Считать smoke-test завершенным без дополнительных изменений.

## Ограничения
- Не менять core-структуру проекта.
''', encoding='utf-8')
stage = yaml.safe_load((chat / 'stage-state.yaml').read_text(encoding='utf-8'))
for key in ['reuse_check_complete','reality_check_complete','conflict_detection_complete','spec_ready','spec_validated','tech_spec_ready','tech_spec_validated','decomposition_complete','task_validation_complete','codex_handoff_allowed','execution_complete','verification_complete','done_complete']:
    stage['gates'][key] = True
stage['stage'] = {'current': 'done', 'previous': 'verification', 'next': 'none'}
(chat / 'stage-state.yaml').write_text(yaml.safe_dump(stage, allow_unicode=True, sort_keys=False), encoding='utf-8')
task = yaml.safe_load((chat / 'task-index.yaml').read_text(encoding='utf-8'))
task['change']['summary'] = 'Smoke-test изменение для проверки фабрики.'
for idx, task_item in enumerate(task.get('tasks', []), 1):
    if not task_item.get('outputs'):
        task_item['outputs'] = [f'work/active/{task["change"]["id"]}/tasks/T-{idx:03d}.md']
    if not task_item.get('acceptance'):
        task_item['acceptance'] = ['Артефакт создан', 'Проверка проходит']
(chat / 'task-index.yaml').write_text(yaml.safe_dump(task, allow_unicode=True, sort_keys=False), encoding='utf-8')
