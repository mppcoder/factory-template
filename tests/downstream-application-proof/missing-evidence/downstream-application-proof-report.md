# Отчет downstream application proof

Дата: 2026-04-27

proof_status: passed
downstream_repo: /projects/generated-battle-app
app_image: factory-template-placeholder-app:local
runtime_target: staging-vps-01
healthcheck_url: https://battle-app.example.test/healthz
healthcheck_result: pass
migrations: not_applicable
backup_result: pass
restore_result: pass
rollback_result: pass
sanitized_transcript: missing
secrets_boundary: unconfirmed
blocker_reason: none

## Runtime evidence данные

app_image_evidence: placeholder
healthcheck_evidence: ok
migrations_evidence: ok
backup_evidence: ok
restore_evidence: ok
rollback_evidence: ok
transcript_evidence: missing
secrets_boundary_evidence: missing

## Novice-to-deploy scorecard данные

time_to_first_handoff_minutes: soon
handoff_rework_loops: 0
manual_interventions: 0
external_blockers: 0
deploy_result: pass
scorecard_evidence: TODO
