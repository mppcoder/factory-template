# Codex handoff input

## Контекст
- Repo: `factory-template`
- Нужно устранить defect в verified-sync metadata layer.
- После `stage.current = done` новый non-lightweight diff мог пройти prereqs с commit message из stale `.chatgpt/task-index.yaml`.
- Это создавало риск commit/push с неверным `change_id` и `title`.

## Что должен сделать исполнитель
- Зафиксировать bug report и factory feedback для reusable verified-sync defect.
- Добавить guard в automation, который блокирует post-done non-lightweight verified sync без обновленного `.chatgpt/task-index.yaml`.
- Обновить текущие `.chatgpt` metadata под этот новый change.
- Подтвердить проверкой, что stale path теперь падает с явным blocker.

## Ограничения
- Не делать вид, что stale metadata можно безопасно использовать для нового commit intent.
- Не ослаблять существующий lightweight follow-up path.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.
