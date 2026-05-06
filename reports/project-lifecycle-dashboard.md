# Панель жизненного цикла проекта / `project-lifecycle-dashboard`

Generated UTC: `2026-05-06T11:14:33+00:00`
Source: `/projects/factory-template/template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`

## Сейчас

- Проект: `factory-template` (`factory-template`)
- Профиль: `greenfield-product`
- Lifecycle state: `{{LIFECYCLE_STATE}}`
- Текущий mode: ``
- Factory producer layer: `False`
- Фаза: `verification` -> next `release`
- Stage file говорит: current `intake`, next `classification`

## Активное изменение

- id: `FT-CH-0011-unified-roadmap`
- title: Single big VPS, downstream proof and beginner-first roadmap baseline
- class/priority/status: `feature` / `high` / `done`
- boundary: `internal-repo-follow-up`
- task-state next action: Заполнить task-index, stage-state и следующий конкретный шаг.

## Гейты этапов

| Gate | Status | Evidence / reason |
|---|---|---|
| `intake` Intake принят | `completed` | `.chatgpt/chat-handoff-index.yaml` |
| `classification` Маршрут и класс задачи выбраны | `completed` | `template-repo/scenario-pack/00-master-router.md` |
| `reuse_reality_check` Reuse/reality-check выполнен | `completed` | `docs/architecture/vps-project-hosting-topologies.md`, `docs/downstream-application-proof.md`, `docs/operator/runbook-packages/01-factory-template/01-user-runbook.md` |
| `spec` User spec готов | `completed` | `docs/releases/unified-single-vps-downstream-beginner-roadmap.md` |
| `tech_spec` Tech spec готов | `completed` | `docs/architecture/vps-project-hosting-topologies.md`, `docs/operator/single-big-vps-dev-runtime-architecture.md` |
| `handoff_allowed` Handoff разрешен | `completed` | `template-repo/scenario-pack/00-master-router.md` |
| `execution` Execution завершен | `completed` | `.chatgpt/chat-handoff-index.yaml`, `docs/releases/single-vps-downstream-proof-roadmap.md`, `docs/operator/beginner-first-windows-to-first-project.md` |
| `verification` Verification завершена | `completed` | `bash template-repo/scripts/verify-all.sh quick`, `bash template-repo/scripts/verify-all.sh` |
| `done` Done/архивирование завершено | `completed` | `git status --short --branch` |

## Многошаговое выполнение

- current wave: `1`
- completed tasks: `T-001, T-002, T-003, T-004`
- blocked tasks: `none`
- next task: `T-VERIFY` - Запустить validators, render dashboard, quick/full verify и verified sync.
- final verification: `passed` `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`, `python3 template-repo/scripts/validate-runbook-packages.py .`, `python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`, `python3 template-repo/scripts/validate-standards-gates.py .`, `bash template-repo/scripts/verify-all.sh quick`, `bash template-repo/scripts/verify-all.sh`
- archive allowed: `True`; Final verification passed; closeout remains repo sync only.

| Wave | Status | Tasks |
|---|---|---|
| `wave-1` State sync, module gates and roadmap materialization | `completed` | `T-001` `completed`, `T-002` `completed`, `T-003` `completed`, `T-004` `completed` |

## Визуальные поверхности для новичка

- default surfaces: `chatgpt-mini-card, codex-execution-card, markdown-dashboard`
- source of truth: `.chatgpt/project-lifecycle-dashboard.yaml`
- ChatGPT mini card template: `.chatgpt/visual-status-card.md.template`
- Codex execution card template: `.chatgpt/codex-execution-card.md.template`
- Markdown dashboard output: `reports/project-lifecycle-dashboard.md`
- heavy UI boundary: Default is ChatGPT mini card, Codex execution card and Markdown dashboard only; web app, daemon, SQLite, Telegram notifications, websocket/live-refresh and background worker are not default promises.
- compact lifecycle chain: ✅ Идея → ✅ Intake → ✅ Спека → ✅ Архитектура → ✅ Handoff → ✅ Исполнение
→ ✅ Проверка → 🕒 Release → 🕒 Deploy → 🕒 Сопровождение
- compact module readiness chain: ✅ Lifecycle → ✅ Core → ✅ Security → ✅ UI/A11y → ✅ Quality → ✅ WebSec
→ ✅ Ops → ⏸ AI

### Активные ChatGPT handoff-задачи

✅ FT-CX-0011 factory-template: ✅ Codex-WORK → ✅ Codex OK → ✅ Done

### История ChatGPT handoff-задач

✅ FT-CH-0001 dashboard-card-ui: ✅ GPT-HO → ✅ Codex OK → ✅ Done
⏸ FT-CH-0002 completion-report: ✅ GPT-HO → 🕒 Codex OK → ⏸ Done
⏸ FT-CH-0003 updates-monitor: ✅ GPT-HO → 🕒 Codex OK → ⏸ Superseded
⏸ FT-CH-0004 model-routing: ✅ GPT-HO → 🕒 Codex OK → ⏸ Done
✅ FT-CH-0010 release-package-updated-bootstrap: ✅ GPT-HO → ✅ Codex OK → ✅
  Done
✅ FT-CH-0011 single-vps-dev-runtime-host: ✅ GPT-HO → ✅ Codex OK → ✅ Done
✅ FT-CH-0012 chatgpt-first-answer-allocation-not-attempted: ✅ GPT-HO → ✅
  Codex OK → ✅ Done
✅ FT-CH-0013 universal-task-control-automation-roadmap: ✅ GPT-HO → ✅ Codex
  OK → ✅ Done
✅ FT-CH-0014 product-support-architecture: ✅ GPT-HO → ✅ Codex OK → ✅ Done
✅ FT-CH-0015 windows-bootstrapper-release-publication: ✅ GPT-HO → ✅ Codex
  OK → ✅ Done
🟡 FT-CH-0016 chat-title-allocator-blocker-regression: ✅ GPT-HO → 🕒 Codex
  OK → 🕒 Done

### История Codex-доработок

✅ FT-CX-0001 chat-counter-closeout-drift: ✅ Codex-WORK → ✅ Codex OK → ✅
  Done
✅ FT-CX-0002 handoff-execution-mode-ownership: ✅ Codex-WORK → ✅ Codex OK →
  ✅ Done
✅ FT-CX-0003 closeout-project-card: ✅ Codex-WORK → ✅ Codex OK → ✅ Done
✅ FT-CX-0004 compact-card-active-only: ✅ Codex-WORK → ✅ Codex OK → ✅ Done
✅ FT-CX-0005 stale-compact-card-tasks: ✅ Codex-WORK → ✅ Codex OK → ✅ Done
✅ FT-CX-0006 card-wrap-codex-numbering: ✅ Codex-WORK → ✅ Codex OK → ✅ Done
✅ FT-CX-0007 chatgpt-first-answer-card-title: ✅ Codex-WORK → ✅ Codex OK →
  ✅ Done
✅ FT-CX-0008 chatgpt-title-reservation-gap: ✅ Codex-WORK → ✅ Codex OK → ✅
  Done
⏸ FT-CX-0009 chatgpt: ✅ Codex-WORK → 🕒 Codex OK → ⏸ Superseded
✅ FT-CX-0010 chatgpt-first-answer-title-one-click-copy-chatgpt: ✅
  Codex-WORK → ✅ Codex OK → ✅ Done
✅ FT-CX-0011 factory-template: ✅ Codex-WORK → ✅ Codex OK → ✅ Done

## Передача и оркестрация

- parent handoff: `FT-CH-0011-unified-roadmap` `completed`
- selected profile/model/reasoning: `deep` / `gpt-5.5` / `high`
- route boundary: Advisory layer показывает маршрут и handoff-текст, но не переключает model/profile/reasoning внутри уже открытой Codex-сессии; надежная executable boundary — новый task launch или ручной picker в новом чате.

## Универсальный контроль задач

- status: `pending`
- registry: `template-repo/template/.chatgpt/task-registry.yaml`
- compact line: Tasks: 🕒 0 ready-for-handoff -> 0 ready-for-codex -> 0 running -> 0
  human-review
- next action: Generate or update Codex handoff for the next ready task.
- fallback: Keep task in triage until route, evidence and human boundary are clear.

| Counter | Value |
|---|---|
| `open` | `0` |
| `ready_for_handoff` | `0` |
| `ready_for_codex` | `0` |
| `codex_running` | `0` |
| `human_review` | `0` |
| `blocked` | `0` |
| `verified` | `0` |

### Подтверждения

- template-repo/template/.chatgpt/task-registry.yaml
- template-repo/scripts/validate-task-registry.py
- template-repo/scripts/allocate-task-id.py
- template-repo/scripts/issue-to-task-registry.py
- template-repo/scripts/preview-task-handoff.py
- template-repo/scripts/update-task-status.py
- template-repo/scripts/prepare-task-pack.py
- template-repo/scripts/render-task-queue.py
- reports/task-queue.md

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
| `01-factory-template` | `execution` | `route-receipt`, `implementation`, `verification`, `verified-sync` | none | Для задач самого шаблона пользователь останавливается на FT-170; clone/setup/verify/dashboard/sync выполняет Codex в remote context. |
| `02-greenfield-product` | `intake` | `scaffold`, `greenfield-docs`, `verification`, `closeout` | none | Новый боевой проект идет непрерывно: factory ChatGPT intake -> one-block Codex handoff -> repo/root/scaffold/verify/sync -> готовая repo-first instruction -> пользователь создает battle ChatGPT Project UI. |
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
- gate summary: `8/9` passed; missing `0`; blocking `0`
- current phase standards: `verification` -> iso_12207, iso_25010, nist_ssdf, owasp_asvs, wcag_22, dora_metrics, scrum_guide_2020
- missing evidence: `none`
- next standards action: Продолжить single big VPS + downstream proof line; не заявлять downstream pass без real pilot evidence.
- monitoring: `current`; proposal_required `False`
- allowed to advance phase: `True`
- boundary: Standards navigator is a lifecycle/evidence control layer, not ISO/NIST/OWASP/WCAG/DORA/OpenAI certification.

### Готовность модулей / standards-inspired readiness

| Module | Status | Standards | Gates | Sources | Evidence / reason |
|---|---|---|---|---|---|
| `lifecycle` Lifecycle | `completed` | `iso_12207` | `lifecycle_intent_recorded`, `product_requirements_recorded` | none | `.chatgpt/project-lifecycle-dashboard.yaml`, `.chatgpt/stage-state.yaml` |
| `core` Core | `completed` | none | none | `active_change`, `stage_gates`, `multi_step_execution`, `final_verification` | `.chatgpt/chat-handoff-index.yaml`, `docs/releases/unified-single-vps-downstream-beginner-roadmap.md`, `.chatgpt/task-index.yaml` |
| `security` Security | `completed` | `nist_ssdf` | `security_minimum_checked` | none | `docs/architecture/vps-project-hosting-topologies.md`, `docs/downstream-application-proof.md`, `docs/operator/runbook-packages/00-package-contract.md` |
| `ui_a11y` UI/A11y | `completed` | `wcag_22` | `accessibility_minimum_checked` | none | `docs/operator/runbook-packages/01-factory-template/01-user-runbook.md`, `docs/operator/runbook-packages/02-greenfield-product/01-user-runbook.md`, `docs/operator/beginner-first-windows-to-first-project.md` |
| `quality` Quality | `completed` | `iso_25010` | `quality_minimum_checked` | none | `template-repo/scripts/validate-runbook-packages.py`, `template-repo/scripts/validate-downstream-application-proof.py`, `bash template-repo/scripts/verify-all.sh quick` |
| `websec` WebSec | `completed` | `owasp_asvs` | `web_security_checked` | none | `docs/architecture/vps-project-hosting-topologies.md`, `docs/operator/single-big-vps-dev-runtime-architecture.md`, `docs/downstream-application-proof.md` |
| `ops` Ops | `completed` | `dora_metrics` | `operations_health_baseline` | `deploy_runtime`, `software_update_governance` | `docs/architecture/vps-project-hosting-topologies.md`, `docs/releases/single-vps-downstream-proof-roadmap.md`, `reports/release/downstream-application-proof-report.md` |
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

- Recommended (`internal-repo-follow-up`): Recommended next execution branch: single big VPS + downstream proof real-pilot-ready contour; do not reverse before beginner-first hardening.
- Fallback (`internal-repo-follow-up`): Если real downstream app отсутствует, удерживать proof в blocked_external_inputs и продолжать beginner-first Windows-to-first-project hardening.
