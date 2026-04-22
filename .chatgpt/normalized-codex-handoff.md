# Normalized Codex Handoff

## Launch source
chatgpt-handoff

## Task class
build

## Task class evidence
- keyword hit: change

## Selected profile
build

## Selected model
gpt-5.4

## Selected reasoning effort
medium

## Selected plan mode reasoning
medium

## Project profile
unknown-project-profile

## Selected scenario
00-master-router.md

## Pipeline stage
done

## Artifacts to update
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md
- reports/bugs/
- reports/factory-feedback/

## Handoff allowed
yes (forbidden)

## Defect capture path
reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

## Launch boundary rule
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Executable launch command
`codex --profile build`

## Task payload
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