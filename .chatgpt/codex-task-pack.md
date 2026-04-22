# Task pack для Codex

## Change ID
chg-20260422-004

## Заголовок
Require explicit no-user-action closeout wording

## Класс изменения
small-fix

## Режим выполнения
single-pass

## Launch source
chatgpt-handoff

## Task class
build

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

## Handoff allowed
yes (forbidden)

## Defect capture path
not-required-by-text-signal

## Repo Rules Priority
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Handoff input
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
