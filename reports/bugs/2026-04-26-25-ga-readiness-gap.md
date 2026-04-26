# G25-GA readiness gap

## Summary / суть

- Date: `2026-04-26`
- Gate: `G25-GA`
- Type: GA blocker / evidence gap
- Status: open until full KPI evidence exists
- Decision: no-go for `2.5` GA

`G25-GA` cannot be closed from the current repository evidence. The RC baseline is green, but several full-threshold KPI measurements from `docs/releases/2.5-success-metrics.md` are not present as measurable artifacts.

## Evidence reviewed / проверенные источники

- `docs/releases/release-scorecard.yaml`
- `docs/releases/2.5-success-metrics.md`
- `RELEASE_CHECKLIST.md`
- `TEST_REPORT.md`
- `VERIFY_SUMMARY.md`
- `onboarding-smoke/ACCEPTANCE_REPORT.md`
- `UPGRADE_SUMMARY.md`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/verification-report.md`

## Metric confirmation / проверка метрик

| Metric | Full 2.5 threshold | Current evidence | GA result |
|---|---:|---|---|
| `M25-01` time-to-first-success | `<= 25` minutes | Scripted novice smoke is green, but no timed first-success measurement is recorded. | Missing evidence |
| `M25-02` first-run completion rate | `>= 92%` | No controlled pilot checklist or sample size is recorded. Script pass count is not a human first-run completion rate. | Missing evidence |
| `M25-03` manual intervention count | `<= 1` | No run notes or support prompts register records intervention counts. | Missing evidence |
| `M25-04` downstream safe-sync success rate | `>= 99%` | `UPGRADE_SUMMARY.md` covers a representative downstream fixture, not a measured success-rate population. | Missing evidence |
| `M25-05` critical defects | `0` open critical | Current verification docs do not identify open critical defects; this file is an evidence blocker, not a product-critical defect. | Provisionally OK |
| `M25-06` handoff rework loops | `<= 1` | No aggregate handoff history or per-task loop counter is recorded for the GA population. | Missing evidence |
| `M25-07` release-facing doc consistency | `100% + no drift` | Release-facing docs are being aligned to no-go state in this closeout. | OK after verification |
| `M25-08` repo-first routing compliance | `100%` | This closeout read `template-repo/scenario-pack/00-master-router.md` before implementation; no contrary evidence found for the current task. | OK for current closeout |

## Release decision / решение

`G25-GA` is blocked. Do not mark `ga_ready: true`, do not publish a `2.5` GA release, and do not write release-facing markdown that claims GA.

## Required remediation before GA retry / что нужно для следующей попытки

- Record timed beginner first-success runs and compare them to the `<= 25` minute threshold.
- Produce a controlled pilot checklist with sample size and completion percentage for `M25-02`.
- Record manual intervention counts and support-prompt notes for first-run tasks.
- Run downstream safe-sync verification across enough downstream samples to claim `>= 99%`.
- Add an aggregate handoff rework-loop register for the GA evidence population.
- Re-run full verify and update `docs/releases/release-scorecard.yaml` only after the evidence exists.
