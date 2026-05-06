# Дорожная карта single VPS downstream/battle proof

## Статус

Current status: `ready_for_external_pilot`.

`factory-template` has template/runtime proof and a supported `single-host` topology. It does not have a selected real downstream/battle app in this repo. Therefore downstream/battle application proof must remain blocked until external pilot inputs exist.

## Непрерывный proof path

| Stage | Gate | Required evidence | Status |
|---|---|---|---|
| A | Single big VPS topology proof | `/projects` vs `/srv`, per-project env/systemd/nginx/docker/backup boundaries | prepared |
| B | Select downstream/battle project | downstream repo path and owner-approved scope | blocked_external_inputs |
| C | Replace placeholder `APP_IMAGE` | real image reference/digest, not `factory-template-placeholder-app:local` | blocked_external_inputs |
| D | Healthcheck and migrations policy | app-specific healthcheck and migrations/not-applicable reason | blocked_external_inputs |
| E | Approved deploy | approval and deploy to `/srv/<project>-prod` or approved staging target | blocked_external_inputs |
| F | HTTPS/nginx/systemd/docker healthcheck | nginx/systemd/docker checks and runtime probe | blocked_external_inputs |
| G | Backup | backup artifact/snapshot without secrets | blocked_external_inputs |
| H | Disposable/staging restore | restore target and result | blocked_external_inputs |
| I | Rollback drill | previous image/version restored and probe passed | blocked_external_inputs |
| J | Sanitized transcript | transcript without secrets, tokens, private keys or raw env | blocked_external_inputs |
| K | Fill proof report | `reports/release/downstream-application-proof-report.md` | ready |
| L | Validate report | `validate-downstream-application-proof.py` | ready |
| M | Update dashboard/release continuity | no false green, no release-ready claim | ready |
| N | Claim proof pass | only after all real evidence exists | blocked_external_inputs |

## Внешние inputs для pass

- downstream repo path;
- real `APP_IMAGE`;
- approved VPS/staging target;
- secrets entered outside repo;
- deploy/restore/rollback approval;
- sanitized transcript.

Operator runbook for these actions:
`docs/operator/downstream-battle-external-pilot-runbook.md`.

## Защита от false pass

- Placeholder app proves only template/runtime path, not business workload.
- `proof_status: passed` fails if `APP_IMAGE` is placeholder, restore/rollback evidence is missing, transcript is missing or secrets boundary is unconfirmed.
- `proof_status: blocked_external_inputs`, `ready_for_external_pilot` or `not_run` is valid only with blocker reason and no pass claim.

## Следующее действие

Recommended next execution branch: single big VPS + downstream proof real pilot when the external inputs above exist.

Fallback branch: keep downstream proof blocked/ready and continue beginner-first Windows-to-first-project hardening.
