## Номер запроса Codex

```text
FT-CX-0039 continue-health-sync-bridge-next-stage
```

## Карточка проекта

🏭 factory-template
✅ Идея → ✅ Intake → ✅ Спека → ✅ Архитектура → ✅ Handoff → ✅ Исполнение
→ ✅ Проверка → 🕒 Release → 🕒 Deploy → 🕒 Сопровождение
Модули:
✅ Lifecycle → ✅ Core → ✅ Security → ✅ UI/A11y → ✅ Quality → ✅ WebSec
→ ✅ Ops → ⏸ AI
Tasks: 🕒 0 ready-for-handoff -> 0 ready-for-codex -> 0 running -> 0
  human-review
В работе:
🟡 FT-CX-0037 fix-stale-closeout-reports: ✅ Codex-WORK → ✅ Codex OK → 🕒
  Done
🟡 FT-CX-0038 continue-health-sync-bridge-project: ✅ Codex-WORK → ✅ Codex
  OK → 🕒 Done
🟡 FT-CX-0039 continue-health-sync-bridge-next-stage: ✅ Codex-WORK → ✅
  Codex OK → 🕒 Done

## Применение в Codex UI

`apply_mode: manual-ui (default)`.

Для интерактивной работы открой новый чат/окно Codex в VS Code extension, вручную выбери model `gpt-5.4-mini` и reasoning `low` в picker, затем вставь один цельный handoff block ниже.

Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же. Advisory layer сам по себе не переключает model/profile/reasoning; надежная единица маршрутизации — новый task launch. Уже открытая live session допустима только как non-canonical fallback без обещаний auto-switch.

## Строгий launch mode (опционально)

Используй launcher-first strict mode только для automation / reproducibility / shell-first запуска:

```bash
./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute
```

Прямая команда profile за launcher:

```bash
codex --profile quick
```

## Handoff в Codex

```text
Язык ответа Codex: русский
Отвечай пользователю по-русски. Английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

Цель:
Выполнить direct-task self-handoff и продолжить работу в этом же task, если текущий live route совпадает с routing ниже. Не завершай ответ только self-handoff block и не требуй ручного продолжения пользователя для внутренней Codex-eligible работы.

Visible answer contract:
Первый substantive ответ Codex для direct-task должен показывать `Номер запроса Codex` и `Карточка проекта` до route receipt, self-handoff или remediation. `Номер запроса Codex` берется из `.chatgpt/codex-work-index.yaml` как `codex_work_title` и не расходует ChatGPT `FT-CH` counter. Если номер не выделен, нужно показать exact blocker: `Нужно выделить номер через repo codex-work-index / allocator.`.

Repo rules:
В рамках repo приоритет у repo rules, AGENTS, runbook и policy files репозитория. Общие рабочие инструкции применяются только там, где не противоречат правилам repo и старшим системным ограничениям среды.

Routing:
- launch_source: direct-task
- handoff_shape: codex-task-handoff
- execution_mode_decision_owner: Codex runtime after task graph analysis
- execution_mode_closeout_required: actual execution mode plus child/subagent count
- goal_contract.normalized_goal: codex_work_id: FT-CX-0039
codex_work_title: FT-CX-0039 continue-health-sync-bridge-next-stage
task_slug: continue-health-sync-bridge-next-stage
codex_work_state: in_progress

user_request: продолжай проект HSB
normalized_goal: Continue the Health Sync Bridge project from the latest repo-local state by finding the next internal Codex-eligible step, executing it if safely possible, and closing with evidence or a concrete blocker.
- goal_contract.definition_of_done: evidence satisfies requested outcome and repo validators/blockers are documented
- goal_contract.proxy_signal_denylist: tests passed alone; file exists alone; commit exists alone; green dashboard alone; validator passed alone
- goal_runtime_recommendation: codex_goal_candidate
- codex_goal_live_validation_required: true
- codex_goal_runtime_rule: optional/live-gated; experimental goals require explicit user/operator choice and no already-open auto-switch
- task_class: quick
- selected_profile: quick
- selected_model: gpt-5.4-mini
- selected_reasoning_effort: low
- selected_plan_mode_reasoning_effort: medium
- apply_mode: manual-ui
- strict_launch_mode: optional
- project_profile: unknown-project-profile
- selected_scenario: 00-master-router.md
- pipeline_stage: done
- handoff_allowed: yes (forbidden)
- defect_capture_path: not-required-by-text-signal
- chat_id: not_applicable
- chat_title: not_applicable
- task_slug: continue-health-sync-bridge-next-stage
- chat_kind: not_applicable
- chat_state: not_applicable
- chat_index_path: not_applicable
- codex_work_id: FT-CX-0039
- codex_work_title: FT-CX-0039 continue-health-sync-bridge-next-stage
- codex_work_kind: self_handoff
- codex_work_state: in_progress
- codex_work_index_path: .chatgpt/codex-work-index.yaml

Артефакты для обновления:
- .chatgpt/goal-contract.yaml
- .chatgpt/goal-state.yaml
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md

Текст задачи:
codex_work_id: FT-CX-0039
codex_work_title: FT-CX-0039 continue-health-sync-bridge-next-stage
task_slug: continue-health-sync-bridge-next-stage
codex_work_state: in_progress

user_request: продолжай проект HSB
normalized_goal: Continue the Health Sync Bridge project from the latest repo-local state by finding the next internal Codex-eligible step, executing it if safely possible, and closing with evidence or a concrete blocker.

Continuation rule:
Если задача пришла в уже открытую Codex-сессию и этот route совместим с текущей сессией, после видимого self-handoff продолжай remediation / implementation / verification без отдельного запроса пользователя. Остановка допустима только при реальном blocker, внешнем действии, несовместимом route или необходимости нового task launch.

Completion rule:
Перед финальным ответом сгенерируй compact project card для фактического repo, которое закрывает текущий scope. Для `factory-template` используй `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout`; для downstream/greenfield проекта используй repo-local equivalent `python3 scripts/render-project-lifecycle-dashboard.py --input .chatgpt/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout`. Если closeout относится к созданному downstream-проекту, карточка должна быть downstream-проекта, а не template repo. Карточка должна содержать строки `Модули:` и `В работе:`. Если в конце остается следующий пользовательский или внешний шаг, финальный ответ обязан завершаться разделом `## Инструкция пользователю`. Если внешних действий нет, финальный ответ обязан явно сказать: `Внешних действий не требуется.` и добавить continuation outcome: `Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.`
```

## Совместимость validator

Этот раздел фиксирует legacy-маркеры direct-task response без создания второго handoff-блока:

- `## Номер запроса Codex`
- `## Карточка проекта`
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
