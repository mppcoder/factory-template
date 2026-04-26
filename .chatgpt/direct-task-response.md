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
Провести evidence-first intake/reconstruction для полевого теста шаблона фабрики проектов на brownfield without repo.

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
- selected_scenario: brownfield/00-brownfield-entry.md
- pipeline_stage: brownfield-without-repo-intake
- handoff_allowed: no
- defect_capture_path: brownfield gap -> structured defect/gap report before remediation planning

Входные корни:
- /root/.openclaw — настроенный live runtime / дистрибутив.
- /root/openclaw-plus — package / overlay / тонкий слой кастомных доработок.

Границы scope:
- Делать только inventory, repo-audit, as-is architecture, gap capture и reverse-engineering planning.
- Не выполнять remediation runtime.
- Не создавать git repo внутри /root/.openclaw или /root/openclaw-plus.
- Не создавать temporary/intermediate repo прямо в /projects.
- Не переносить значения секретов в repo-артефакты.

Обязательные артефакты:
- .chatgpt/task-launch.yaml
- .chatgpt/direct-task-source.md
- .chatgpt/direct-task-self-handoff.md
- .chatgpt/normalized-codex-handoff.md
- brownfield/system-inventory.md
- brownfield/repo-audit.md
- brownfield/as-is-architecture.md
- brownfield/gap-register.md
- brownfield/reverse-engineering-plan.md
- brownfield/reverse-engineering-summary.md
- brownfield/decision-log.md
- .chatgpt/evidence-register.md
- .chatgpt/reality-check.md

Verify expectations:
- Подтвердить существование обоих корней.
- Подтвердить git/repo-state обоих корней.
- Зафиксировать сервисы и валидаторы без изменения runtime.
- Проверить, что /root/.openclaw не подменен старым ошибочным путем /root/openclaw.
- Запустить repo validators для evidence, handoff language, brownfield transition и handoff response format.

Риски и ограничения:
- Package root содержит тяжелые generated/dependency зоны.
- Runtime и env содержат secret-bearing state.
- Backup-файлы требуют отдельного triage.
- Validator green может содержать warning, который нужно оформить как gap до remediation.

Factory feedback:
Если обнаружен template-level defect или generated handoff format defect, зафиксируй его в gap register. Если defect исправлен в рамках текущего scope, отметь fixed-in-current-scope.
```

## Совместимость validator

Этот раздел фиксирует обязательные legacy-маркеры direct-task response без создания второго handoff-блока:

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
