# Normalized Codex Handoff

## Launch source
chatgpt-handoff

## Task class
build

## Task class evidence
- keyword hit: change
- explicit reasoning/model override matched default profile: build

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

## Handoff allowed
yes (forbidden)

## Defect capture path
not-required-by-text-signal

## Launch boundary rule
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Executable launch command
`codex --profile build`

## Task payload
# Codex handoff input

## Контекст
- Repo: `factory-template`
- Нужно уточнить closeout behavior.
- Если финальный ответ не требует `## Инструкция пользователю`, он всё равно должен явно говорить, что внешних действий не требуется.
- Сейчас это правило в repo описано недостаточно жёстко и из-за этого закрытый internal change может выглядеть как неявно незавершённый.

## Что должен сделать исполнитель
- Обновить scenario closeout rule и DoD.
- Синхронизировать generated `.chatgpt` guidance и validator.
- Подтвердить, что task-pack generation и validation проходят.

## Ограничения
- Не требовать `## Инструкция пользователю`, если внешнего шага реально нет.
- Но и не оставлять отсутствие внешнего шага подразумеваемым.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.