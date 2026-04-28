# Orchestration cockpit lite / лёгкая панель оркестрации

Generated UTC: `2026-04-28T12:06:09+00:00`

Status: `planned`
Parent: `plan-6-orchestration-productization`
Title: Plan №6 beginner-first full handoff UX

## Route receipt / подтверждение маршрута

- task_class: `deep`
- selected_profile: `deep`
- selected_model: `gpt-5.5`
- selected_reasoning_effort: `high`
- selected_plan_mode_reasoning_effort: `high`
- explanation: deterministic keywords: deep, audit, orchestration, verification; repo-configured mapping requires live catalog validation when catalog is stale or unavailable

## Child tasks / дочерние задачи

| Child | Class | Profile | Model | Reasoning | Status | Boundary |
|---|---|---|---|---|---|---|
| `p6-s0-audit-roadmap` | `deep` | `deep` | `gpt-5.5` | `high` | `planned` | `internal-repo-follow-up` |
| `p6-s1-cockpit-lite` | `build` | `build` | `gpt-5.5` | `medium` | `planned` | `internal-repo-follow-up` |

## Blockers / блокеры

- none

## Deferred user actions / отложенные действия пользователя

- `real-downstream-app-proof`: P4-S5/P4-S6 real downstream/battle app proof запускать только при real downstream repo, real APP_IMAGE, approved VPS/staging target, secrets outside repo and sanitized transcript. (`downstream-battle-action`)

## Placeholder replacements / замены placeholder

- `__REAL_DOWNSTREAM_REPO__`: Настоящий downstream/battle repo path для будущего P4-S5/P4-S6.
- `__REAL_APP_IMAGE__`: Настоящий application image для future real downstream app proof.

## Next action / следующее действие

- `internal-repo-follow-up`: Validate parent plan, run orchestration runner, render cockpit, run targeted validators.

## Continuation outcome / итог продолжения

Текущий internal scope продолжается в parent Codex; внешних действий до финального closeout нет.
