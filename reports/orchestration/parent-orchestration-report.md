# Отчет parent Codex orchestration

Generated UTC: 2026-04-28T05:00:17+00:00
Status: dry-run
Plan: /projects/factory-template/tests/codex-orchestration/fixtures/valid/parent-plan.yaml
Report: /projects/factory-template/reports/orchestration/parent-orchestration-report.md
Default path: VPS Remote SSH-first
Cloud default: false

## Parent задача

- id: `p5-fixture-parent`
- title: VPS Remote SSH-first orchestration fixture
- launch_source: `chatgpt-handoff`
- selected_scenario: `template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md`
- apply_mode: `manual-ui`
- strict_launch_mode: `optional`
- user_actions_policy: `defer-to-final-closeout`

## Subtasks / подзадачи

| Subtask | Profile | Model | Reasoning | Status | Boundary | Session file | Command |
|---|---|---|---|---|---|---|---|
| `docs-quick` | `quick` | `gpt-5.4-mini` | `low` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/sessions/docs-quick.md` | `codex --profile quick < /projects/factory-template/reports/orchestration/sessions/docs-quick.md` |
| `runner-build` | `build` | `gpt-5.5` | `medium` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/sessions/runner-build.md` | `codex --profile build < /projects/factory-template/reports/orchestration/sessions/runner-build.md` |
| `audit-deep` | `deep` | `gpt-5.5` | `high` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/sessions/audit-deep.md` | `codex --profile deep < /projects/factory-template/reports/orchestration/sessions/audit-deep.md` |
| `verify-review` | `review` | `gpt-5.5` | `high` | session-file-written | `internal-repo-follow-up` | `/projects/factory-template/reports/orchestration/sessions/verify-review.md` | `codex --profile review < /projects/factory-template/reports/orchestration/sessions/verify-review.md` |

## Warnings / предупреждения

- none

## Errors / ошибки

- none

## Финальные действия пользователя

- `replace-real-app-image`: Заменить `__REAL_APP_IMAGE__` на настоящий application image перед real downstream proof. (timing: `final-closeout`)

## Напоминания о замене placeholder values

- `__REAL_APP_IMAGE__` -> Настоящий application image для downstream/battle runtime proof. (owner: `operator`, timing: `final-user-action`)

## Финальный parent closeout contract

- Collect child result summaries.
- Separate internal repo follow-up, external user action, runtime action and downstream/battle action.
- Move all user-required actions to the final closeout block.
- Use safe temporary placeholders where possible and remind the operator to replace them with real data at the end.
- Do not claim Cloud/App default.
- Do not claim already-open session auto-switch.
- If external action remains, final answer must include compact `## Инструкция пользователю`.
