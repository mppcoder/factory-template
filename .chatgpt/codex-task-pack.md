# Task pack для Codex

## Идентификатор изменения
chg-20260428-model-prompt-policy

## Заголовок
Связать model updates с prompt policy migration

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
reports/bugs/2026-04-28-model-update-missing-prompt-policy-gap.md

## Приоритет правил repo
При исполнении задачи приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.

## Целевой результат
Model availability auto-check и proposal flow должны обновлять не только model routing, но и prompt policy под новую model по official OpenAI guidance.

## Критерии успеха
- `codex-model-routing.yaml` содержит `prompt_migration_policy`.
- `check-codex-model-catalog.py --write-proposal` генерирует prompt migration section.
- Validator/eval ловят отсутствие связки model promotion и prompt policy.
- Docs объясняют, что новая model не является drop-in replacement.

## Артефакты
- `template-repo/codex-model-routing.yaml`
- `template-repo/scripts/check-codex-model-catalog.py`
- `template-repo/scripts/validate-model-prompt-policy.py`
- `tests/artifact-eval/specs/model-prompt-policy.yaml`
- `tests/artifact-eval/reports/model-prompt-policy.md`
- `reports/model-routing/model-routing-proposal.md`
- `reports/bugs/2026-04-28-model-update-missing-prompt-policy-gap.md`
- `reports/factory-feedback/feedback-2026-04-28-model-update-missing-prompt-policy-gap.md`

## Проверка
- `python3 template-repo/scripts/validate-model-prompt-policy.py .`
- `python3 template-repo/scripts/check-codex-model-catalog.py . --write-proposal`
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/model-prompt-policy.yaml --output tests/artifact-eval/reports/model-prompt-policy.md`
- `bash template-repo/scripts/verify-all.sh quick`

## Входные данные handoff
Direct task от пользователя: в проекте уже предусмотрено автообновление выбора моделей и режимов при выходе новой модели; дополнительно предусмотреть обновление политики промптов под новую модель в соответствии с рекомендациями OpenAI.
