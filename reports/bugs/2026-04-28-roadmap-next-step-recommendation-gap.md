# Roadmap next-step recommendation gap

Дата: 2026-04-28

## Summary контекст

Пользователь спросил, что дальше по roadmap, но получил развилку без достаточно явной рекомендации следующего шага.

## Evidence данные

- `docs/releases/plan-4-battle-app-proof-roadmap.md` фиксировал P4-S5/P4-S6 как future/external boundary.
- `CURRENT_FUNCTIONAL_STATE.md` фиксировал, что P4-S5/P4-S6 blocked until a real downstream/battle project is selected.
- Ответ должен был явно рекомендовать: если есть real downstream/battle app, идти в P4-S5/P4-S6; если такого app нет, открывать внутренний Plan №5 / hardening contour.

## Classification слой

- Layer: roadmap closeout / user-facing continuation outcome.
- Severity: guidance defect, not runtime regression.
- Owner boundary: repo docs, scenario router and closeout checklist.

## Remediation план

- Add explicit recommended next step to Plan №4 roadmap.
- Update current state and test report with the recommendation.
- Strengthen router/checklist so roadmap readouts with multiple branches must name the recommended branch and fallback branch.
- Add Artifact Eval regression coverage for roadmap branch recommendation in done closeout.
