# Отчет production VPS field pilot

Дата: 2026-04-27

## Результат

Status: `infrastructure-runtime-proof-passed-real-app-proof-pending`.

Production VPS field pilot path подготовлен и частично автоматизирован:

- starter: preserved as beginner default.
- app-db: opt-in preset.
- reverse-proxy-tls: opt-in preset.
- backup: opt-in preset requiring `app-db`.
- healthcheck: opt-in preset.
- rollback drill: documented as required field pilot stage.

The original remediation was report-first and did not mutate a VPS. Later on 2026-04-27, explicit operator approval was provided and the real VPS runtime proof executed on `72.56.26.209`.

P3-S5 status: runtime QA boundary prepared and executed for infrastructure proof. On 2026-04-27 an approved 2.6 runtime proof was executed for production preset infrastructure path on VPS `72.56.26.209`; see `reports/release/2.6-runtime-proof-report.md`. P3-S6 then aligned release-facing roadmap/status docs.

## Обновленные артефакты

- `docs/deploy-on-vps.md`
- `docs/production-vps-field-pilot.md`
- `template-repo/scripts/deploy-dry-run.sh`
- `template-repo/scripts/deploy-local-vps.sh`
- `template-repo/scripts/operator-dashboard.py`
- `template-repo/scripts/validate-operator-env.py`
- `template-repo/scripts/verify-all.sh`
- `reports/bugs/2026-04-27-production-vps-field-pilot-gap.md`
- `TEST_REPORT.md`
- `CURRENT_FUNCTIONAL_STATE.md`

## Режим field pilot report

New safe report modes:

```bash
python3 template-repo/scripts/validate-operator-env.py \
  --preset production \
  --field-pilot-report .factory-runtime/reports/operator-env-field-pilot-latest.md

bash template-repo/scripts/deploy-dry-run.sh \
  --preset production \
  --strict-env \
  --field-pilot-report .factory-runtime/reports/production-vps-field-pilot-latest.md

python3 template-repo/scripts/operator-dashboard.py \
  --preset production \
  --field-pilot-report .factory-runtime/reports/production-vps-field-pilot-latest.md
```

`deploy-local-vps.sh --field-pilot-report` exists for post-deploy evidence, but deploy itself remains operator-approved through prompt or explicit `--yes`.

## Покрытие checklist

- DNS: covered in runbook and field pilot reports.
- Firewall: covered for `80/443` TLS path.
- Docker Compose: covered by dashboard status and dry-run.
- Env secrets: covered by `validate-operator-env.py`.
- Backup restore test: documented as required runtime proof; dry-run checks only backup inputs.
- Pre-deploy QA: documented as env + dry-run + DNS/firewall/backup/rollback readiness gate.
- Post-deploy QA: documented as healthcheck + backup restore + rollback evidence gate.
- Sanitized runtime transcript: required for any production proof claim beyond report-ready/dry-run evidence.

## Выводы по rollback и backup

- Minimum rollback drill is image/tag rollback: record old `APP_IMAGE`, deploy candidate, revert `APP_IMAGE`, dry-run, deploy previous tag, verify healthcheck.
- DB rollback is application-specific and must start with a fresh `db-backup`.
- Backup proof is not complete until a readable dump is restored into a disposable/staging target.
- Without restore proof, production field pilot remains `pending-backup-restore-proof`.

## Цикл Project Knowledge Done

Decisions recorded:

- Keep `starter` as default to protect beginner VPS path.
- Keep production aliases/presets opt-in to avoid forcing DNS, DB, TLS and backup secrets on first deploy.
- Treat report-mode and dry-run as evidence, not production proof.
- Require external approval for real deploy/rollback/restore because those mutate runtime infrastructure.
- Require sanitized runtime transcript before declaring deploy, restore or rollback passed.

Downstream impact:

- Downstream/generated projects should receive the updated deploy docs and scripts on next template sync.
- Existing downstream ChatGPT Project instructions do not need changes if they already read repo-first from the materialized repo.

Done evidence:

- Dedicated runbook added.
- Dedicated release report added.
- Defect-capture report added.
- Script report modes added.
- Quick verify smoke extended to production field pilot report mode.

## Внешняя граница pending

- Real business application Docker image.
- Application-specific healthcheck/migration expectations.
- Application-level backup/restore interpretation if the real app changes data semantics.
- Approved repeat runtime proof if release claims depend on the real app workload.
- Sanitized runtime transcript for that application-level proof.

## 2026-04-27 runtime execution summary

- Production preset deploy: passed.
- HTTPS healthcheck: passed.
- Backup run: passed.
- Restore test: passed.
- Rollback drill: passed.
- Placeholder app deploy: passed with `APP_IMAGE=factory-template-placeholder-app:local`.
- Boundary: application-level production proof remains pending until a real app image is deployed.
