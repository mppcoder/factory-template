## Применение в Codex UI

`apply_mode: manual-ui (default)`.

Для интерактивной работы открой новый чат/окно Codex в VS Code extension, вручную выбери model `gpt-5.5` и reasoning `high` в picker, затем вставь один цельный handoff block ниже.

Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же. Advisory layer сам по себе не переключает model/profile/reasoning; надежная единица маршрутизации — новый task launch. Уже открытая live session допустима только как non-canonical fallback без обещаний auto-switch.

## Строгий launch mode (опционально)

Используй launcher-first strict mode только для automation / reproducibility / shell-first запуска:

```bash
./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute
```

Прямая команда profile за launcher:

```bash
codex --profile deep
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
- task_class: deep
- selected_profile: deep
- selected_model: gpt-5.5
- selected_reasoning_effort: high
- selected_plan_mode_reasoning_effort: high
- apply_mode: manual-ui
- strict_launch_mode: optional
- project_profile: brownfield-without-repo
- selected_scenario: brownfield/10-evidence-pack-completion.md
- pipeline_stage: field-pilot-fp-02-evidence-pack-completion
- handoff_allowed: no
- defect_capture_path: brownfield gap -> structured defect/gap report before remediation planning

Артефакты для обновления:
- .chatgpt/task-launch.yaml
- .chatgpt/direct-task-source.md
- .chatgpt/direct-task-self-handoff.md
- .chatgpt/normalized-codex-handoff.md
- .chatgpt/direct-task-response.md
- reports/release/2.5-field-pilot-evidence.md
- reports/release/field-pilot-scenarios/02-brownfield-without-repo.md
- docs/releases/2.5.1-field-pilot-roadmap.md
- brownfield/reverse-engineering-summary.md
- brownfield/gap-register.md
- .chatgpt/evidence-register.md
- .chatgpt/reality-check.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md

Текст задачи:
task_class: deep
selected_profile: deep
project_profile: brownfield-without-repo
selected_scenario: brownfield/10-evidence-pack-completion.md
pipeline_stage: field-pilot-fp-02-evidence-pack-completion
handoff_allowed: no
artifacts_to_update:
  - .chatgpt/task-launch.yaml
  - .chatgpt/direct-task-source.md
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/normalized-codex-handoff.md
  - .chatgpt/direct-task-response.md
  - reports/release/2.5-field-pilot-evidence.md
  - reports/release/field-pilot-scenarios/02-brownfield-without-repo.md
  - docs/releases/2.5.1-field-pilot-roadmap.md
  - brownfield/reverse-engineering-summary.md
  - brownfield/gap-register.md
  - .chatgpt/evidence-register.md
  - .chatgpt/reality-check.md
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
defect_capture_path: brownfield gap -> structured defect/gap report before remediation planning

Продолжить roadmap полевого теста шаблона: закрыть FP-02 Battle brownfield without repo как sanitized field evidence по фактическому OpenClaw+ кейсу (/root/.openclaw + /root/openclaw-plus), обновить release field-pilot evidence и scenario file. Не выдавать synthetic checks за недостающие FP-01/FP-03/FP-04/FP-05; если следующий roadmap шаг требует недоступный real project, зафиксировать blocker/next external boundary в инструкции пользователю.

Continuation rule:
Если задача пришла в уже открытую Codex-сессию и этот route совместим с текущей сессией, после видимого self-handoff продолжай remediation / implementation / verification без отдельного запроса пользователя. Остановка допустима только при реальном blocker, внешнем действии, несовместимом route или необходимости нового task launch.

Completion rule:
Если в конце остается следующий пользовательский или внешний шаг, финальный ответ обязан завершаться разделом `## Инструкция пользователю`. Если внешних действий нет, финальный ответ обязан явно сказать: `Внешних действий не требуется.`
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
