# Self-handoff для прямой задачи

## Источник запуска
direct-task

## Класс задачи
build

## Выбранный профиль
build

## Выбранная модель
gpt-5.5

## Выбранное reasoning effort
medium

## Выбранное reasoning effort для plan mode
medium

## Режим применения
manual-ui

## Строгий режим запуска
optional

## Профиль проекта
factory-template self-improvement / tree-boundary policy

## Выбранный сценарий
template-repo/scenario-pack/00-master-router.md

## Этап pipeline
defect-capture -> remediation -> verification -> closeout

## Артефакты для обновления
- `.chatgpt/codex-input.md`
- `.chatgpt/codex-context.md`
- `.chatgpt/codex-task-pack.md`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `template-repo/tree-contract.yaml`
- `template-repo/scripts/validate-tree-contract.py`
- active docs/scenario-pack/bootstrap guidance
- `tests/artifact-eval/specs/project-root-boundary.yaml`
- `tests/artifact-eval/reports/project-root-boundary.md`

## Разрешение handoff
true

## Маршрут defect-capture
reports/bugs/2026-04-28-flat-project-tree-intermediate-repo-gap.md

## Текст задачи
Закрепить правило: все temporary/intermediate/reconstructed/helper repos для intake/adoption/reconstruction должны находиться внутри repo целевого `greenfield-product`, а не как sibling project roots в `/projects`.
