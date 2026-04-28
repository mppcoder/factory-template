# Evidence для verified sync fallback

Date: 2026-04-28

## Область

This report records fallback coverage for `verified-sync.py` without changing stable sync logic.

No secrets are stored in this report. Use `FACTORY_SYNC_FALLBACK_PUSH_URL` only in the operator shell environment when an alternate push URL is required.

## Матрица coverage

| Case | Expected behavior | Evidence path |
|---|---|---|
| blocked push | `push_branch` first tries `origin`; if blocked, it tries fallback URL and records failed origin/fallback stderr if both fail. | `factory_automation_common.py` |
| remote drift | verified sync must fail through git push conflict instead of rewriting remote state. Operator resolves drift outside repo automation, then reruns verify/sync. | `verified-sync.py` + git push semantics |
| protected branch | protected branch rejection remains a push blocker; fallback URL does not bypass branch protection. | `push_branch` error report |
| branch ahead | branch ahead with local verified diff is allowed only after verification gates; report records commit SHA and push status. | `.factory-runtime/reports/verified-sync-report.yaml` |
| dirty state | dirty state is converted into an explicit staged commit only through `changed_paths`, denylist and sync plan validation. | `changed_paths` + `resolve_sync_plan` |
| fallback instructions | operator may set `FACTORY_SYNC_FALLBACK_PUSH_URL` for an alternate remote URL; repo must not store tokens, passwords or private keys. | this report |

## Граница

- Runtime auth failure is not remediated by editing repo files.
- Protected branch policy is an external repository rule.
- Remote drift requires fetch/rebase/merge decision by the operator or an approved repo policy task.
- Fallback URL must not include embedded credentials in committed docs, reports or fixtures.
