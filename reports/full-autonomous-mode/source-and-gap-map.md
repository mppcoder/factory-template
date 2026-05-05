# Карта source/gap gated full autonomous mode

Дата: 2026-05-05

## Карта текущих источников

| Layer | Current source | Status before this increment |
|---|---|---|
| Advanced automation gates | `docs/operator/factory-template/full-advanced-automation-gates.md` | Policy documented; dangerous capabilities prohibited by default. |
| Worktree isolation | `docs/operator/factory-template/worktree-isolation-policy.md` | Policy documented; real worktree manager missing. |
| Bounded runner | `template-repo/scripts/bounded-task-runner.py` | Safe one-task skeleton; parallel refused. |
| Permission model | `docs/operator/factory-template/issue-autofix-permission-model.md` | Policy documented; reusable enforcement layer missing. |
| Audit ledger | `template-repo/scripts/automation_run_ledger.py` | Append helper existed; hash-chain and schema validation needed hardening. |
| Rollback | `template-repo/scripts/automation-rollback-plan.py` | Basic dry-run plan existed; broader rollback proof needed. |
| Human review / approvals | operator docs | Separate approval layer missing. |
| Auto-merge / deploy / security / public submit | refusal docs | Gate scripts missing; actions must remain disabled by default. |

## Текущие запрещённые возможности

- `pull_request_target` in issue-derived automation.
- Live GitHub label/issue mutation outside gated workflows.
- Auto-merge by default.
- Production deploy by default.
- Security issue autofix through public issues.
- Public external report auto-submit.
- Unbounded parallel agents or shared dirty-state parallel execution.
- Secrets copied into worktrees, issue-derived runs or logs.

## Классификация gaps

| Gap | Classification | Required outcome |
|---|---|---|
| Real per-issue/per-task worktree manager | internal implementation | Dry-run plan plus write-capable isolated worktree creation with locks/run state. |
| Parallel runner proof | internal implementation | Parallel dry-run only after approval, worktree validator, ledger and rollback plan. |
| Permission enforcement | internal implementation | Actor/scope approval checks with offline fixtures and no live mutation. |
| Approval records | internal implementation | Separate approval artifacts, validate/consume CLI and ledger logging. |
| Tamper-evident ledger | internal implementation | Required fields, secret scrubbing and optional hash chain validation. |
| Rollback proof | internal implementation | Dry-run plans for branch/PR/label/task/deploy/public/security recovery, no main rewrite. |
| Required human review policy | internal implementation | Explicit policy plus validator and runner/gate references. |
| Auto-merge | external approval | Disabled by default; unlock only with matching approval, green checks and rollback proof. |
| Production deploy | external approval | Disabled by default; unlock only with target, environment approval, health/rollback plans and safe secrets boundary. |
| Security issue autofix | prohibited by policy for public issue path | Public security issues are refused; private safe placeholder only. |
| Public external report submit | external approval | Disabled by default; unlock only with redaction, consent, approval and rollback/update plan. |
| Full live autonomous mode | future only | Available only as gated substrate; no dangerous action enabled by default. |

## F0 safety-вывод

This increment may build the gated substrate, validators and dry-run proofs. It must not enable dangerous live actions by default.
