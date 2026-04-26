# Проверка реальности

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

## Полевой brownfield-тест OpenClaw+

Дата: 2026-04-26

### Что подтверждено

- Текущий запрос классифицирован как `brownfield-without-repo`.
- Входные корни `/root/.openclaw` и `/root/openclaw-plus` существуют.
- Оба корня не являются git repo.
- `/root/.openclaw` является live runtime/config/state root.
- `/root/openclaw-plus` является package/overlay/docs/validators/systemd/templates/scripts root.
- Сервисы `openclaw-gateway`, `openclaw-retrieval`, `openclaw-vectorizer`, `gpt2giga`, `postgresql`, `nginx` active и enabled.
- Live acceptance package validator проходит.

### Что не подтверждено

- Не подтверждена safe source-of-truth boundary для будущего repo.
- Не выполнена классификация всех файлов на source/generated/runtime-state/secret-bearing.
- Не выполнен backup triage.
- Не создан reconstruction repo.

### Расхождения и риски

- Оба рабочих корня находятся под `/root`, а не в выделенном `/projects/<project-root>`; для reconstruction нужно создать отдельный project root и не делать temporary repo прямо в `/projects`.
- Package root содержит `.venvs/` и dependency-heavy wrapper tree; naive import в repo будет шумным.
- `/etc/openclaw-plus.env` и runtime credential/state folders требуют redaction discipline.
- Validator green содержит warning о duplicated content/context bloat; это gap до remediation.

### Вывод по field test

Evidence-first intake завершен на минимально достаточном уровне для следующего шага: `source-candidate-map`.
Remediation пока не разрешена.

## Follow-up по source-candidate

Дата: 2026-04-26

### Что подтверждено

- `source-candidate-map` является внутренним Codex-eligible follow-up, а не пользовательским ручным шагом.
- `/root/openclaw-plus` является основным source candidate root.
- `/root/.openclaw` является limited candidate root только после redaction/review.
- `.venvs`, `node_modules`, `__pycache__`, `var`, logs, sqlite и jsonl/session files должны быть исключены из reconstruction.

### Проверка реальности дефекта

- Предыдущий closeout остановился перед внутренним follow-up и не дал `## Инструкция пользователю`.
- Это reusable process defect, а не ошибка пользователя.
- Исправление должно жить в generator/validator/scenario layer, а не только в текущем ответе.
