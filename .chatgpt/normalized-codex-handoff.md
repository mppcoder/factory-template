# Нормализованный handoff для Codex

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

## Ручное применение через UI
- Откройте новый чат/окно Codex в VS Code extension.
- Вручную выберите model `gpt-5.5` и reasoning `medium` в picker.
- Только после этого вставьте handoff.
- Codex должен отвечать пользователю на русском языке; английский допустим только для technical literal values.
- Уже открытая live session не считается надежным auto-switch boundary.

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

## Язык ответа Codex
Русский. Английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Правило launch boundary
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Опциональная команда строгого запуска
`./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute`

## Прямая команда Codex за launcher
`codex --profile build`

## Диагностика проблем
- Если вы работаете через VS Code Codex extension интерактивно, используйте новый чат/окно, вручную выставьте selected_model и selected_reasoning_effort в picker, а затем вставьте handoff.
- Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же; не выдавайте manual UI apply за auto-switch.
- Если нужна строгая воспроизводимость, автоматизация или запуск из shell, используйте optional strict launch_command.

## Текст задачи
Закрепить правило: все temporary/intermediate/reconstructed/helper repos для intake/adoption/reconstruction должны находиться внутри repo целевого `greenfield-product`, а не как sibling project roots в `/projects`.
