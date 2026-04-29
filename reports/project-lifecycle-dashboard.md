# Панель жизненного цикла проекта / `project-lifecycle-dashboard`

Generated UTC: `2026-04-29T15:18:14+00:00`
Source: `/projects/factory-template/template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`

## Сейчас

- Проект: `factory-template` (`factory-template`)
- Профиль: `greenfield-product`
- Lifecycle state: `{{LIFECYCLE_STATE}}`
- Текущий mode: ``
- Factory producer layer: `False`
- Фаза: `execution` -> next `verification`
- Stage file говорит: current `intake`, next `classification`

## Активное изменение

- id: ``
- title: Первое изменение проекта
- class/priority/status: `feature` / `medium` / `draft`
- boundary: `internal-repo-follow-up`
- task-state next action: Заполнить task-index, stage-state и следующий конкретный шаг.

## Гейты этапов

| Gate | Status | Evidence / reason |
|---|---|---|
| `intake` Intake принят | `pending` |  |
| `classification` Маршрут и класс задачи выбраны | `pending` |  |
| `reuse_reality_check` Reuse/reality-check выполнен | `pending` |  |
| `spec` User spec готов | `pending` |  |
| `tech_spec` Tech spec готов | `pending` |  |
| `handoff_allowed` Handoff разрешен | `pending` |  |
| `execution` Execution завершен | `pending` |  |
| `verification` Verification завершена | `pending` |  |
| `done` Done/архивирование завершено | `pending` |  |

## Многошаговое выполнение

- current wave: `0`
- completed tasks: `none`
- blocked tasks: `none`
- next task: `T-001` - Заполнить `.chatgpt/task-index.yaml`, `.chatgpt/stage-state.yaml` и уточнить первый рабочий шаг.
- final verification: `pending` 
- archive allowed: `False`; Feature нельзя архивировать до `final_verification.status: passed` и evidence.

| Wave | Status | Tasks |
|---|---|---|
| `wave-0` Подготовка | `pending` | `T-001` `pending` |

## Визуальные поверхности для новичка

- default surfaces: `chatgpt-mini-card, codex-execution-card, markdown-dashboard`
- source of truth: `.chatgpt/project-lifecycle-dashboard.yaml`
- ChatGPT mini card template: `.chatgpt/visual-status-card.md.template`
- Codex execution card template: `.chatgpt/codex-execution-card.md.template`
- Markdown dashboard output: `reports/project-lifecycle-dashboard.md`
- heavy UI boundary: Default is ChatGPT mini card, Codex execution card and Markdown dashboard only; web app, daemon, SQLite, Telegram notifications, websocket/live-refresh and background worker are not default promises.
- compact lifecycle chain: ✅ Идея → ✅ Intake → ✅ Спека → ✅ Архитектура → ✅ Handoff → 🟡 Исполнение → 🕒 Проверка → 🕒 Release → 🕒 Deploy → 🕒 Сопровождение
- compact module readiness chain: ✅ Lifecycle → 🟡 Core → 🟡 Security → 🕒 UI/A11y → 🕒 Quality → 🕒 WebSec → 🕒 Ops → ⏸ AI

### Активные ChatGPT handoff-задачи

🟡 FT-CH-0002 completion-report: ✅ GPT-HO → 🕒 Codex OK → 🕒 Done
🔴 FT-CH-0004 model-routing: ✅ GPT-HO → ✅ Codex OK → 🔴 Blocked
✅ FT-CH-0008 compact-card-active-only: ✅ Codex-SHO → ✅ Codex OK → ✅ Done

### История ChatGPT handoff-задач

✅ FT-CH-0001 dashboard-card-ui: ✅ GPT-HO → ✅ Codex OK → ✅ Done
🟡 FT-CH-0002 completion-report: ✅ GPT-HO → 🕒 Codex OK → 🕒 Done
⏸ FT-CH-0003 updates-monitor: ✅ GPT-HO → 🕒 Codex OK → ⏸ Superseded
🔴 FT-CH-0004 model-routing: ✅ GPT-HO → ✅ Codex OK → 🔴 Blocked
✅ FT-CH-0005 chat-counter-closeout-drift: ✅ Codex-SHO → ✅ Codex OK → ✅ Done
✅ FT-CH-0006 handoff-execution-mode-ownership: ✅ Codex-SHO → ✅ Codex OK → ✅ Done
✅ FT-CH-0007 closeout-project-card: ✅ Codex-SHO → ✅ Codex OK → ✅ Done
✅ FT-CH-0008 compact-card-active-only: ✅ Codex-SHO → ✅ Codex OK → ✅ Done

## Передача и оркестрация

- parent handoff: `p9-lifecycle-standards-navigator` `not_started`
- selected profile/model/reasoning: `deep` / `gpt-5.5` / `high`
- route boundary: Advisory layer показывает маршрут и handoff-текст, но не переключает model/profile/reasoning внутри уже открытой Codex-сессии; надежная executable boundary — новый task launch или ручной picker в новом чате.

## Контроль реализации handoff / Handoff implementation control

- source artifact: `.chatgpt/handoff-implementation-register.yaml`
- schema: `handoff-implementation-register/v1`
- queue policy: `deterministic_dependency_priority_calculation`
- open/blocked/implemented-not-verified/stale: `0` / `0` / `0` / `0`
- route boundary: Dashboard показывает handoff route/model/reasoning как readout; handoff/register не переключают model/profile/reasoning внутри уже открытой Codex-сессии.

### Очередь queued / ready

- нет queued/ready задач

### Заблокировано dependencies

- нет blocked задач

### Блокеры и prerequisite tasks

- нет prerequisite/blocker задач

### В работе

- нет in-progress задач

### Реализовано, но не verified

- нет implemented-but-not-verified задач

### Снято, superseded или archived

- нет снятых, superseded или archived задач

### Stale items без свежего evidence

- stale задач без свежего evidence нет

## Пакеты операторских сценариев

| Package | Phase | Gates | Blockers | Next action |
|---|---|---|---|---|
| `01-factory-template` | `execution` | `route-receipt`, `implementation`, `verification`, `verified-sync` | none | Для задач самого шаблона пройти beginner user-only setup до Codex takeover point, затем передать automation Codex-runbook. |
| `02-greenfield-product` | `intake` | `scaffold`, `greenfield-docs`, `verification`, `closeout` | none | Для нового боевого проекта стартовать в ChatGPT Project шаблона фабрики: новый чат -> `новый проект` -> выбор default-decision mode -> recommendation-first опрос -> generated Codex handoff. |
| `03-brownfield-with-repo-to-greenfield` | `adoption` | `audit`, `adoption`, `conversion`, `verification` | none | Для существующего repo дать Codex remote access к canonical root; audit/adoption/conversion выполняет Codex-runbook. |
| `04-brownfield-without-repo-to-greenfield` | `reconstruction` | `intake`, `reconstruction`, `with-repo-adoption`, `conversion` | none | Для материалов без repo загрузить их в target root/_incoming; reconstruction/adoption/conversion выполняет Codex-runbook. |

## Готовность релиза

- version: ``
- status: `pending`
- verification: `pending`
- changelog/release notes/scorecard: `` / `` / ``
- VERIFY_SUMMARY present: `True`

## Развертывание и выполнение

- status: `pending`
- preset: `starter`
- operator source: `template-repo/scripts/operator-dashboard.py`
- dry-run report present: `False`
- deploy report present: `False`
- boundary: Runtime evidence может подтягиваться из operator-dashboard reports; dry-run/report evidence не является real deploy proof.

## Навигатор стандартов

- profile: `solo_lightweight`
- lifecycle backbone: `iso_12207` `2017` (`current_with_revision_pending`)
- gate summary: `0/9` passed; missing `9`; blocking `0`
- current phase standards: `intake` -> iso_12207, scrum_guide_2020
- missing evidence: `lifecycle_intent_recorded, product_requirements_recorded, quality_minimum_checked, security_minimum_checked, web_security_checked, accessibility_minimum_checked, operations_health_baseline, false_compliance_checked`
- next standards action: Заполнить `.chatgpt/standards-gates.yaml` для текущей фазы и приложить evidence или accepted_reason.
- monitoring: `current`; proposal_required `False`
- allowed to advance phase: `False`
- boundary: Standards navigator is a lifecycle/evidence control layer, not ISO/NIST/OWASP/WCAG/DORA/OpenAI certification.

### Готовность модулей / standards-inspired readiness

| Module | Status | Standards | Gates | Sources | Evidence / reason |
|---|---|---|---|---|---|
| `lifecycle` Lifecycle | `completed` | `iso_12207` | `lifecycle_intent_recorded`, `product_requirements_recorded` | none | `.chatgpt/project-lifecycle-dashboard.yaml`, `.chatgpt/stage-state.yaml` |
| `core` Core | `in_progress` | none | none | `active_change`, `stage_gates`, `multi_step_execution`, `final_verification` |  |
| `security` Security | `in_progress` | `nist_ssdf` | `security_minimum_checked` | none |  |
| `ui_a11y` UI/A11y | `pending` | `wcag_22` | `accessibility_minimum_checked` | none |  |
| `quality` Quality | `pending` | `iso_25010` | `quality_minimum_checked` | none |  |
| `websec` WebSec | `pending` | `owasp_asvs` | `web_security_checked` | none |  |
| `ops` Ops | `pending` | `dora_metrics` | `operations_health_baseline` | `deploy_runtime`, `software_update_governance` |  |
| `ai` AI | `not_applicable` | `openai_ai_safety_overlay` | `ai_safety_gate` | none | Project has not declared AI model, agent or AI-output behavior. |

## Управление обновлениями

- baseline status: `pending`
- auto-update policy: `manual-approved-upgrade`
- last intelligence check: `not recorded`
- relevant findings: `0`
- upgrade proposal: `not_started`
- blockers: `none`
- next safe action: Заполнить `.chatgpt/software-inventory.yaml`, проверить unattended upgrades и обновить watchlist без установки обновлений.
- fallback action: Если baseline неполный, заблокировать upgrade proposal до записи OS/runtime/package evidence.

## Улучшения после релиза

- incidents: `0`
- feedback: `0`
- learning proposals: `0`
- backlog candidates: `0`

## Реестр внешних действий

- внешних/manual действий сейчас нет

## Следующий шаг

- Recommended (`internal-repo-follow-up`): Продолжить repo-first intake: обновить stage/task state и подготовить spec.
- Fallback (`internal-repo-follow-up`): Если scope пока неясен, открыть guided launcher continue path и зафиксировать один следующий шаг.
