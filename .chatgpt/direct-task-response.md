## Применение в Codex UI

`apply_mode: manual-ui (default)`.

Для интерактивной работы открой новый чат/окно Codex в VS Code extension, вручную выбери model `gpt-5.5` и reasoning `medium` в picker, затем вставь один цельный handoff block ниже.

Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же. Advisory layer сам по себе не переключает model/profile/reasoning; надежная единица маршрутизации — новый task launch. Уже открытая live session допустима только как non-canonical fallback без обещаний auto-switch.

## Строгий launch mode (опционально)

Используй launcher-first strict mode только для automation / reproducibility / shell-first запуска:

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
Выполнить direct-task self-handoff и продолжить работу в этом же task, если текущий live route совпадает с routing ниже. Не завершай ответ только self-handoff block и не требуй ручного продолжения пользователя для внутренней Codex-eligible работы.

Repo rules:
В рамках repo приоритет у repo rules, AGENTS, runbook и policy files репозитория. Общие рабочие инструкции применяются только там, где не противоречат правилам repo и старшим системным ограничениям среды.

Routing:
- launch_source: direct-task
- task_class: build
- selected_profile: build
- selected_model: gpt-5.5
- selected_reasoning_effort: medium
- selected_plan_mode_reasoning_effort: medium
- apply_mode: manual-ui
- strict_launch_mode: optional
- project_profile: unknown-project-profile
- selected_scenario: 00-master-router.md
- pipeline_stage: verification
- handoff_allowed: yes (forbidden)
- defect_capture_path: not-required-by-text-signal

Артефакты для обновления:
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md

Текст задачи:
Предусмотреть, чтобы auto-check/proposal новых Codex/OpenAI моделей обновлял не только model routing, но и prompt policy под новую model по official OpenAI guidance: fresh prompt baseline, outcome-first contract, reasoning/verbosity/tool-use guidance, validators/evals и reports/prompt-migration before profile promotion.

Continuation rule:
Если задача пришла в уже открытую Codex-сессию и этот route совместим с текущей сессией, после видимого self-handoff продолжай remediation / implementation / verification без отдельного запроса пользователя. Остановка допустима только при реальном blocker, внешнем действии, несовместимом route или необходимости нового task launch.

Completion rule:
Если в конце остается следующий пользовательский или внешний шаг, финальный ответ обязан завершаться разделом `## Инструкция пользователю`. Если внешних действий нет, финальный ответ обязан явно сказать: `Внешних действий не требуется.` и добавить continuation outcome: `Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.`
```

## Совместимость validator

Этот раздел фиксирует legacy-маркеры direct-task response без создания второго handoff-блока:

- `## Self-handoff для прямой задачи`
- `## Классификация`
- `## Выбранный профиль проекта`
- `## Выбранный сценарий`
- `## Текущий этап pipeline`
- `## Режим применения`
- `## Ручное применение через UI`
- `## Строгий режим запуска`
- `## Артефакты для обновления`
- `## Разрешение handoff`
- `## Маршрут defect-capture`
- `## Опциональная команда строгого запуска`
- `## Прямая команда Codex за launcher`
- `## Диагностика проблем`
- `## Следующий шаг`
