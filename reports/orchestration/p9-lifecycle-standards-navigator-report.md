# Отчет parent Codex orchestration

Generated UTC: 2026-04-29T09:13:43+00:00
Status: dry-run
Plan: /projects/factory-template/reports/orchestration/p9-lifecycle-standards-navigator-parent-plan.yaml
Report: /projects/factory-template/reports/orchestration/p9-lifecycle-standards-navigator-report.md
Default path: VPS Remote SSH-first
Cloud default: false

## Parent задача

- id: `p9-lifecycle-standards-navigator`
- title: Standards-based lifecycle navigator/control layer for factory-template
- launch_source: `chatgpt-handoff`
- selected_scenario: `template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md`
- apply_mode: `manual-ui`
- strict_launch_mode: `optional`
- user_actions_policy: `defer-to-final-closeout`

## Subtasks / подзадачи

| Subtask | Profile | Model | Reasoning | Status | Boundary | Session file | Command |
|---|---|---|---|---|---|---|---|
| `p9-s0-gap-source-map` | `deep` | `gpt-5.5` | `high` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/p9-sessions/p9-s0-gap-source-map.md` | `codex --profile deep < /projects/factory-template/reports/orchestration/p9-sessions/p9-s0-gap-source-map.md` |
| `p9-s1-standards-registry` | `build` | `gpt-5.5` | `medium` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/p9-sessions/p9-s1-standards-registry.md` | `codex --profile build < /projects/factory-template/reports/orchestration/p9-sessions/p9-s1-standards-registry.md` |
| `p9-s2-stage-map-and-gates` | `build` | `gpt-5.5` | `medium` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/p9-sessions/p9-s2-stage-map-and-gates.md` | `codex --profile build < /projects/factory-template/reports/orchestration/p9-sessions/p9-s2-stage-map-and-gates.md` |
| `p9-s3-dashboard-integration` | `build` | `gpt-5.5` | `medium` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/p9-sessions/p9-s3-dashboard-integration.md` | `codex --profile build < /projects/factory-template/reports/orchestration/p9-sessions/p9-s3-dashboard-integration.md` |
| `p9-s4-standards-monitoring` | `build` | `gpt-5.5` | `medium` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/p9-sessions/p9-s4-standards-monitoring.md` | `codex --profile build < /projects/factory-template/reports/orchestration/p9-sessions/p9-s4-standards-monitoring.md` |
| `p9-s5-docs-beginner-ux` | `quick` | `gpt-5.4-mini` | `low` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/p9-sessions/p9-s5-docs-beginner-ux.md` | `codex --profile quick < /projects/factory-template/reports/orchestration/p9-sessions/p9-s5-docs-beginner-ux.md` |
| `p9-s6-validators-fixtures` | `review` | `gpt-5.5` | `high` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/p9-sessions/p9-s6-validators-fixtures.md` | `codex --profile review < /projects/factory-template/reports/orchestration/p9-sessions/p9-s6-validators-fixtures.md` |
| `p9-s7-final-review-sync-closeout` | `review` | `gpt-5.5` | `high` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/p9-sessions/p9-s7-final-review-sync-closeout.md` | `codex --profile review < /projects/factory-template/reports/orchestration/p9-sessions/p9-s7-final-review-sync-closeout.md` |

## Warnings / предупреждения

- none

## Errors / ошибки

- none

## Финальные действия пользователя

- `approve-future-standards-version-change`: В будущем подтвердить или отклонить standards-update-proposal, если мониторинг обнаружит новую версию стандарта или изменение применимости gates. (timing: `future-boundary`)
- `select-commercial-production-profile`: Для конкретного боевого проекта подтвердить переход с solo_lightweight на commercial_production profile, если проект становится коммерческим/production-critical. (timing: `future-boundary`)

## Напоминания о замене placeholder values

- `__OFFICIAL_STANDARDS_SOURCE_URLS__` -> Точные официальные ссылки/версии стандартов для manual/live standards research proposal, если repo не содержит актуального source map. (owner: `operator`, timing: `future-user-action`)
- `__BATTLE_PROJECT_STANDARDS_PROFILE__` -> Выбранный профиль конкретного боевого проекта: solo_lightweight, commercial_production или custom. (owner: `operator`, timing: `final-user-action`)

## Финальный parent closeout contract

- Collect child result summaries.
- Separate internal repo follow-up, external user action, runtime action and downstream/battle action.
- Move all user-required actions to the final closeout block.
- Use safe temporary placeholders where possible and remind the operator to replace them with real data at the end.
- Do not claim Cloud/App default.
- Do not claim already-open session auto-switch.
- If external action remains, final answer must include compact `## Инструкция пользователю`.
