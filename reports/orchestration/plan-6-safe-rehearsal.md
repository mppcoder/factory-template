# Plan №6 safe full orchestration rehearsal / безопасная репетиция

Date: 2026-04-28

## Scope / область

Synthetic rehearsal for beginner-first full handoff UX productization.

This report is repo-local evidence only:

- no secrets;
- no real VPS mutation;
- no real downstream app proof;
- dry-run or execute-safe only;
- placeholders remain placeholders.

## Inputs / входные данные

- Parent plan fixture: `tests/codex-orchestration/fixtures/future-placeholder/parent-plan.yaml`.
- Cockpit template: `template-repo/template/.chatgpt/orchestration-cockpit.yaml`.
- Parent plan validator wrapper: `template-repo/scripts/validate-parent-orchestration-plan.py`.
- Cockpit renderer/validator: `template-repo/scripts/render-orchestration-cockpit.py`, `validate-orchestration-cockpit.py`.
- Beginner UX scorecard: `template-repo/scripts/validate-beginner-handoff-ux.py`.

## Rehearsal steps / шаги репетиции

| Step | Mode | Expected result |
|---|---|---|
| Validate future-placeholder parent plan | dry-run | valid `codex-orchestration/v1`; future placeholders accepted |
| Render cockpit | dry-run | markdown cockpit written from YAML |
| Validate cockpit | dry-run | parent/route/children/blockers/next action valid |
| Route explain smoke | dry-run | deterministic keyword/rule evidence visible |
| Beginner UX scorecard | dry-run | one copy-paste block, no fake auto-switch, user actions last |

## Manual intervention count / ручные вмешательства

`0` for repo-local synthetic rehearsal.

## Blockers / блокеры

- none for Plan №6 repo-local synthetic rehearsal.
- future boundary: P4-S5/P4-S6 real downstream/battle app proof requires real downstream repo, real `APP_IMAGE`, approved VPS/staging target, secrets outside repo and sanitized transcript.

## Outcome / итог

Plan №6 rehearsal proves the repo-local productization layer can explain, validate and display a safe full handoff flow. It does not prove any real downstream/battle application.
