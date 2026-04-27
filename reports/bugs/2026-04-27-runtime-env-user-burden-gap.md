# Bug: runtime proof env guidance pushed non-secret setup to the user

Date: 2026-04-27

## Summary

During 2.6 runtime proof preparation, the operator was asked to fill all `deploy/.env` production fields manually, even though most values were non-secret and could be safely derived by Codex on the VPS.

## Evidence

The production env validator initially failed on many fields:

- `DB_NAME`
- `DB_USER`
- `BACKUP_ENABLED`
- `BACKUP_PATH`
- `DOMAIN`
- `ACME_AGREE`
- `DB_PASSWORD`
- `TLS_EMAIL`

Only `DB_PASSWORD` and `TLS_EMAIL` were genuinely user-owned secrets/manual inputs for this run. Codex could safely set the repo-local/defaultable values:

- `OPERATOR_PRESET=production`
- `APP_BIND_ADDRESS=127.0.0.1`
- `DB_NAME=factory_template`
- `DB_USER=factory_template`
- `BACKUP_ENABLED=true`
- `BACKUP_PATH=/var/backups/factory-template-postgres`
- `DOMAIN=72-56-26-209.sslip.io`
- `ACME_AGREE=true`

## Layer Classification

- Layer: production VPS runtime proof operator UX.
- Defect class: excessive user burden / boundary classification error.
- Owner boundary: mixed.
  - Codex/repo can derive non-secret defaults.
  - User must still provide real secrets and approval.

## Remediation

Current run remediation: Codex filled all non-secret values and left only `DB_PASSWORD` and `TLS_EMAIL` for the operator.

Template remediation candidate: add a small helper or documented command for "prepare production env non-secret defaults" so future runtime proof requests do not ask the operator to fill values Codex can derive safely.

## Status

Captured during 2.6 runtime proof. Follow-up remediation should be committed with the runtime proof closeout if no higher-priority deploy blocker appears.
