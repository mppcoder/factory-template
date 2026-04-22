# Task pack для Codex

## Change ID
chg-20260422-006

## Заголовок
Prepare release-facing package and ship patch release 2.4.3

## Класс изменения
feature

## Режим выполнения
codex-led

## Launch source
chatgpt-handoff

## Task class
deep

## Selected profile
deep

## Selected model
gpt-5.4

## Selected reasoning effort
high

## Selected plan mode reasoning
high

## Project profile
factory-template

## Selected scenario
00-master-router.md -> change/release-docs-and-release-followup

## Pipeline stage
definition-and-release-planning -> done

## Handoff allowed
yes

## Defect capture path
not-required-by-text-signal; incidental defects still require capture if discovered

## Repo Rules Priority
При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Handoff input
# Codex handoff input

## Контекст
- Repo: `factory-template`
- Требуется подготовить полный release-facing пакет по пункту 12 и выпустить новый patch-релиз.
- В repo уже есть сильный канон по scenario-pack, runbooks, launcher и release automation, но root-level `RELEASE_NOTES.md` отсутствовал, а release-facing описания были распределены между несколькими документами.

## Что должен сделать исполнитель
- Провести discovery и gap-analysis по release-facing документации.
- Нормализовать канонический пакет вокруг `README.md`, `docs/template-architecture-and-event-workflows.md`, `RELEASE_NOTES.md`, versioning layer и `.chatgpt` closeout artifacts.
- Синхронизировать `VERSION.md`, `CHANGELOG.md`, manifests, template/meta release docs и source/export profiles под новый релиз.
- Подтвердить изменения полным suite:
  - `EXAMPLES_TEST.sh`
  - `MATRIX_TEST.sh`
  - `SMOKE_TEST.sh`
  - `VALIDATE_FACTORY_TEMPLATE_OPS.sh`
  - `PRE_RELEASE_AUDIT.sh`
  - `VALIDATE_VERIFIED_SYNC_PREREQS.sh`
  - `VALIDATE_RELEASE_DECISION.sh`
  - `VALIDATE_RELEASE_NOTES_SOURCE.sh`

## Ограничения
- Не плодить параллельные источники истины по release notes и workflow.
- Не заменять repo-first канон ad hoc release-файлами.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.
