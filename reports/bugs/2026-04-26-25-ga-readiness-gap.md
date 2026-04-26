# G25-GA readiness gap

## Summary / суть

- Date: `2026-04-26`
- Gate: `G25-GA`
- Type: GA blocker / evidence gap
- Status: closed
- Decision: remediated; `G25-GA` can pass after KPI evidence update

`G25-GA` initially could not be closed from the repository evidence. The gap was remediated by adding measured KPI evidence and validators for the full-threshold checks.

## Evidence reviewed / проверенные источники

- `docs/releases/release-scorecard.yaml`
- `docs/releases/2.5-success-metrics.md`
- `RELEASE_CHECKLIST.md`
- `TEST_REPORT.md`
- `VERIFY_SUMMARY.md`
- `tests/onboarding-smoke/ACCEPTANCE_REPORT.md`
- `UPGRADE_SUMMARY.md`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/verification-report.md`

## Metric confirmation / проверка метрик

| Metric | Full 2.5 threshold | Current evidence | GA result |
|---|---:|---|---|
| `M25-01` time-to-first-success | `<= 25` minutes | `tests/onboarding-smoke/ACCEPTANCE_REPORT.md` now records duration per scenario. | Pass |
| `M25-02` first-run completion rate | `>= 92%` | `reports/release/2.5-controlled-pilot-checklist.md` records `9/9`, `100%`. | Pass |
| `M25-03` manual intervention count | `<= 1` | `tests/onboarding-smoke/ACCEPTANCE_REPORT.md` records `0` interventions. | Pass |
| `M25-04` downstream safe-sync success rate | `>= 99%` | `reports/release/2.5-downstream-safe-sync-report.md` records `6/6`, `100%`. | Pass |
| `M25-05` critical defects | `0` open critical | Current verification docs do not identify open critical defects. | Pass |
| `M25-06` handoff rework loops | `<= 1` | `.chatgpt/handoff-rework-register.yaml` records max `1` loop. | Pass |
| `M25-07` release-facing doc consistency | `100% + no drift` | Release-facing docs aligned to GA state. | Pass |
| `M25-08` repo-first routing compliance | `100%` | The current remediation read `template-repo/scenario-pack/00-master-router.md` before implementation. | Pass |

## Release decision / решение

`G25-GA` is no longer blocked. `ga_ready: true` is allowed after `validate-25-ga-kpi-evidence.py`, full verify and release audit pass.

## Required remediation before GA retry / что нужно для следующей попытки

- Added timed beginner first-success runs in `tests/onboarding-smoke/ACCEPTANCE_REPORT.md`.
- Added controlled pilot checklist with sample size and completion percentage.
- Added manual intervention counts.
- Added downstream safe-sync success-rate report.
- Added handoff rework-loop register.
- Added `validate-25-ga-kpi-evidence.py` to keep `ga_ready: true` evidence-backed.
