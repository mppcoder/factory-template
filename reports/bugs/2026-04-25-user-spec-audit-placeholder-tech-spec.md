# Дефект: user-spec audit валидирует placeholder tech-spec как готовый документ

Дата: 2026-04-25
Слой: `factory-template`
Статус: fixed in current scope

## Контекст

`init-feature-workspace.sh` создаёт `specs/tech-spec.md` из template до того, как пользователь прошёл этап decompose.
После генерации user-spec скрипт `generate-user-spec.py` запускает `validate-spec-traceability.py --workspace`.

## Reproduce

1. Создать feature workspace через `init-feature-workspace.sh`.
2. Заполнить минимальные ответы интервью.
3. Запустить `generate-user-spec.py`.

## Фактический результат

Validator проверяет placeholder `specs/tech-spec.md` и падает:

```text
missing trace: .../specs/tech-spec.md не содержит US-anchor в `User Intent Binding`
```

## Ожидаемый результат

На этапе user-spec audit должен проверять готовый `user-spec.md` и пропускать ещё не заполненные placeholder docs с `{{...}}`.
После decompose validator должен проверять уже сгенерированные `tech-spec.md` и `tasks/T-*.md`.

## Классификация

- `project-only`: нет
- `factory-template`: да
- `shared/unknown`: нет

## Исправление

`validate-spec-traceability.py` пропускает placeholder markdown docs, содержащие незаполненные `{{...}}`, но продолжает проверять реальные документы без template placeholders.

