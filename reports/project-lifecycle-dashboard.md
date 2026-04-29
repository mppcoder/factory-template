# Панель жизненного цикла проекта / `project-lifecycle-dashboard`

Generated UTC: `2026-04-29T09:25:35+00:00`
Source: `/projects/factory-template/template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`

## Сейчас

- Проект: `{{PROJECT_NAME}}` (`{{PROJECT_SLUG}}`)
- Профиль: `greenfield-product`
- Lifecycle state: `{{LIFECYCLE_STATE}}`
- Текущий mode: `{{PROJECT_MODE}}`
- Factory producer layer: `False`
- Фаза: `intake` -> next `spec`
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

## Передача и оркестрация

- parent handoff: `p9-lifecycle-standards-navigator` `not_started`
- selected profile/model/reasoning: `deep` / `gpt-5.5` / `high`
- route boundary: Advisory layer показывает маршрут и handoff-текст, но не переключает model/profile/reasoning внутри уже открытой Codex-сессии; надежная executable boundary — новый task launch или ручной picker в новом чате.

## Пакеты операторских сценариев

| Package | Phase | Gates | Blockers | Next action |
|---|---|---|---|---|
| `01-factory-template` | `execution` | `route-receipt`, `implementation`, `verification`, `verified-sync` | none | Для задач самого шаблона пройти beginner user-only setup до Codex takeover point, затем передать automation Codex-runbook. |
| `02-greenfield-product` | `intake` | `scaffold`, `greenfield-docs`, `verification`, `closeout` | none | Для нового боевого проекта стартовать в ChatGPT Project шаблона фабрики: новый чат -> `новый проект` -> опрос -> generated Codex handoff. |
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
- dry-run report present: `True`
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
