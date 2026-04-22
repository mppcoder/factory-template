# Task pack для Codex

## Change ID
chg-20260422-007

## Заголовок
Normalize canonical factory hierarchy and ship 2.4.4

## Класс изменения
feature

## Режим выполнения
codex-led

## Launch source
chatgpt-handoff

## Task class
review

## Selected profile
review

## Selected model
gpt-5.4

## Selected reasoning effort
high

## Selected plan mode reasoning
high

## Executable launch command
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute

## Direct Codex command behind launcher
codex --profile review

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
# Входной пакет для Codex

## Контекст
- Это smoke-test ядра фабрики проектов.
- Базовые проверки уже закрыты и подтверждены evidence-артефактами.
- При исполнении этого handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.

## Что должен сделать исполнитель
- Считать smoke-test завершенным без дополнительных изменений.

## Ограничения
- Не менять core-структуру проекта.
- Общие рабочие инструкции применять только там, где они не противоречат repo rules и старшим системным ограничениям среды.
