# Task pack для Codex

## Change ID
chg-20260422-005

## Заголовок
Fix DoD validator for nested example fixtures

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
- Проведен генеральный audit проекта на целостность, полноту и соответствие.
- Главный реальный defect найден в `template-repo/scripts/check-dod.py`: validator наследовал `origin` родительского git repo для nested example fixtures и выдавал false positive по `verified-sync-report`.

## Что должен сделать исполнитель
- Зафиксировать reusable defect и factory feedback.
- Исправить `check-dod.py`, чтобы remote-проверка срабатывала только когда проверяемый путь сам является git repo root.
- Подтвердить исправление полным suite:
  - `EXAMPLES_TEST.sh`
  - `MATRIX_TEST.sh`
  - `SMOKE_TEST.sh`
  - `VALIDATE_FACTORY_TEMPLATE_OPS.sh`
  - `PRE_RELEASE_AUDIT.sh`

## Ограничения
- Не маскировать проблему под правку example fixtures.
- Не ослаблять verified-sync guard для реальных рабочих repo.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.
