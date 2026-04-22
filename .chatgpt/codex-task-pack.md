# Task pack для Codex

## Change ID
chg-20260422-002

## Заголовок
Guard verified sync against stale task-index metadata

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
reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

## Repo Rules Priority
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Handoff input
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

## Обязательное правило фиксации дефектов
Если в ходе анализа, реализации, тестирования, reverse engineering или verification обнаружен дефект, регрессия, расхождение, пропущенный шаг, шаблонный сбой или reusable process failure, его нельзя silently patch.

Нужно:
1. создать или обновить bug report в `reports/bugs/`;
2. собрать evidence и шаги воспроизведения;
3. указать слой дефекта: `project-only`, `factory-template` или `shared/unknown`;
4. определить, исправляется ли дефект в текущем scope или требует отдельного task boundary;
5. выполнить self-handoff для нового defect;
6. при необходимости подготовить ChatGPT handoff bug note или deep-research prompt;
7. если проблема reusable — создать или обновить factory feedback в `reports/factory-feedback/` или `meta-feedback/`;
8. только после этого или одновременно с этим делать fix.
