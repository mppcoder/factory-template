# Task pack для Codex

## Идентификатор изменения
chg-20260428-project-root-boundary

## Заголовок
Закрепить project-root boundary для intermediate repos

## Класс изменения
fix

## Режим выполнения
codex-led

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

## Ручной UI по умолчанию
Для интерактивной работы в VS Code Codex extension откройте новый чат/окно Codex, вручную выберите `selected_model=gpt-5.5` и `selected_reasoning_effort=medium` в picker, затем вставьте handoff.
Новый чат + вставка handoff и executable launcher path — не одно и то же.
Уже открытая live session не является надежным auto-switch механизмом.

## Язык ответа Codex
Русский. Codex должен отвечать пользователю по-русски; английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Опциональная команда строгого запуска
./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute

## Прямая команда Codex за launcher
codex --profile build

## Выбранный сценарий
template-repo/scenario-pack/00-master-router.md

## Этап pipeline
defect-capture -> remediation -> verification -> closeout

## Разрешение handoff
true

## Маршрут defect-capture
reports/bugs/2026-04-28-flat-project-tree-intermediate-repo-gap.md

## Приоритет правил repo
При исполнении задачи приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Целевой результат
Canonical VPS layout должен явно запрещать размещение промежуточных repo как siblings в `/projects`; все temporary/intermediate/reconstructed/helper repos должны жить внутри repo целевого `greenfield-product`.

## Критерии успеха
- Active docs и scenario-pack используют формулировку про целевой `greenfield-product`.
- `tree-contract.yaml` содержит machine-readable `workspace_layout_policy`.
- `validate-tree-contract.py` проверяет наличие правила в active source paths.
- Artifact Eval `project-root-boundary` проходит и включен в `verify-all.sh`.

## Артефакты
- `README.md`
- `ENTRY_MODES.md`
- `docs/tree-contract.md`
- `docs/brownfield-to-greenfield-transition.md`
- `docs/operator/factory-template/README.md`
- `docs/operator/factory-template/01-runbook-dlya-polzovatelya-factory-template.md`
- `template-repo/scenario-pack/01-global-rules.md`
- `template-repo/scenario-pack/brownfield/00-brownfield-entry.md`
- `template-repo/template/docs/codex-workflow.md`
- `factory/producer/extensions/workspace-packs/vscode-codex-bootstrap/README.md`
- `factory/producer/ops/templates/factory-template-boundary-actions.template.md`
- `template-repo/tree-contract.yaml`
- `template-repo/scripts/validate-tree-contract.py`
- `tests/artifact-eval/specs/project-root-boundary.yaml`
- `tests/artifact-eval/reports/project-root-boundary.md`

## Проверка
- `git diff --check`
- `python3 template-repo/scripts/validate-tree-contract.py .`
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/project-root-boundary.yaml --output tests/artifact-eval/reports/project-root-boundary.md`
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/project-root-boundary.md`
- `python3 template-repo/scripts/validate-codex-task-pack.py .`
- `python3 template-repo/scripts/validate-human-language-layer.py .`
- `bash template-repo/scripts/verify-all.sh quick`

## Входные данные handoff
Direct task от пользователя: добавить в запрет плоского дерева repo проектов в директории `projects` правило, что все промежуточные repo должны находиться внутри repo целевого greenfield проекта.
