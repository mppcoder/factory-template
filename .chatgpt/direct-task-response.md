## Применение в Codex UI

`apply_mode: manual-ui`.

Для интерактивной работы открой новый чат/окно Codex в VS Code extension, вручную выбери model `gpt-5.5` и reasoning `medium` в picker, затем вставь один цельный handoff block ниже.

Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же. Advisory layer сам по себе не переключает model/profile/reasoning; надежная единица маршрутизации — новый task launch.

## Строгий launch mode (опционально)

Опционально для automation / reproducibility / shell-first запуска:

```bash
./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute
```

Прямая команда profile за launcher:

```bash
codex --profile build
```

## Handoff в Codex

```text
Язык ответа Codex: русский
Отвечай пользователю по-русски. Английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

Цель:
Закрепить правило canonical VPS layout: все temporary/intermediate/reconstructed/helper repos для intake/adoption/reconstruction находятся внутри repo целевого greenfield-product, а не как sibling project roots в /projects.

Repo rules:
Сначала прочитай template-repo/scenario-pack/00-master-router.md и действуй строго repo-first. Приоритет у repo rules, AGENTS, scenario-pack, runbooks и policy files.

Routing:
- launch_source: direct-task
- task_class: build
- selected_profile: build
- selected_model: gpt-5.5
- selected_reasoning_effort: medium
- selected_plan_mode_reasoning_effort: medium
- apply_mode: manual-ui
- strict_launch_mode: optional
- project_profile: factory-template self-improvement / tree-boundary policy
- selected_scenario: template-repo/scenario-pack/00-master-router.md
- pipeline_stage: defect-capture -> remediation -> verification -> closeout
- handoff_allowed: true
- defect_capture_path: reports/bugs/2026-04-28-flat-project-tree-intermediate-repo-gap.md

Артефакты для обновления:
- active docs/scenario-pack/bootstrap guidance
- template-repo/tree-contract.yaml
- template-repo/scripts/validate-tree-contract.py
- tests/artifact-eval/specs/project-root-boundary.yaml
- tests/artifact-eval/reports/project-root-boundary.md
- .chatgpt verification/done closeout

Completion rule:
Если внешних действий нет, финальный ответ обязан явно сказать: Внешних действий не требуется.
Если в конце остается следующий пользовательский или внешний шаг, финальный ответ обязан завершаться разделом ## Инструкция пользователю.
Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.
Не завершай ответ только self-handoff block; после видимого self-handoff продолжай remediation / implementation / verification без отдельного запроса пользователя.
```

## Self-handoff для прямой задачи

## Классификация
Direct task: reusable factory gap в canonical VPS layout / project-root boundary.

## Выбранный профиль проекта
factory-template self-improvement / tree-boundary policy

## Выбранный сценарий
template-repo/scenario-pack/00-master-router.md

## Текущий этап pipeline
defect-capture -> remediation -> verification -> closeout

## Режим применения
manual-ui

## Ручное применение через UI
Открыть новый чат/окно Codex, вручную выбрать `gpt-5.5` и reasoning `medium`, затем вставить handoff.

## Строгий режим запуска
optional

## Артефакты для обновления
- active docs/scenario-pack/bootstrap guidance
- `template-repo/tree-contract.yaml`
- `template-repo/scripts/validate-tree-contract.py`
- `tests/artifact-eval/specs/project-root-boundary.yaml`
- `tests/artifact-eval/reports/project-root-boundary.md`

## Разрешение handoff
true

## Маршрут defect-capture
reports/bugs/2026-04-28-flat-project-tree-intermediate-repo-gap.md

## Опциональная команда строгого запуска
`./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute`

## Прямая команда Codex за launcher
`codex --profile build`

## Диагностика проблем
- Advisory layer сам по себе не переключает model/profile/reasoning.
- Уже открытая live session не является надежным auto-switch boundary.
- Для строгой воспроизводимости используйте launcher-first path.

## Следующий шаг
Продолжить remediation, verification и closeout в текущем scope; внешних действий не требуется.
