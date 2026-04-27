# Отчет downstream application proof

Дата: 2026-04-27

proof_status: passed
downstream_repo: /projects/generated-battle-app
app_image: registry.example.test/generated-battle-app:2026-04-27
runtime_target: staging-vps-01
healthcheck_url: https://battle-app.example.test/healthz
healthcheck_result: pass
migrations: not_applicable
backup_result: pass
restore_result: pass
rollback_result: pass
sanitized_transcript: included
secrets_boundary: confirmed
blocker_reason: none

## Runtime evidence данные

app_image_evidence: digest sha256:1111222233334444555566667777888899990000aaaabbbbccccdddd
healthcheck_evidence: HTTP 200 from /healthz after deploy
migrations_evidence: application has no migrations for this build
backup_evidence: backup artifact battle-app-20260427.sql created without secrets
restore_evidence: restored into disposable database battle_app_restore_probe
rollback_evidence: rollback restored previous image registry.example.test/generated-battle-app:previous and healthcheck passed
transcript_evidence: sanitized transcript included below
secrets_boundary_evidence: operator confirmed secrets entered in deploy/.env outside repo

## Novice-to-deploy scorecard данные

time_to_first_handoff_minutes: 12
handoff_rework_loops: 1
manual_interventions: 2
external_blockers: 0
deploy_result: pass
scorecard_evidence: operator completed handoff, deploy and rollback with two approved manual secret/target steps

## Санитизированный transcript

```text
deploy=pass healthcheck=pass backup=pass restore=pass rollback=pass secrets=redacted
```
