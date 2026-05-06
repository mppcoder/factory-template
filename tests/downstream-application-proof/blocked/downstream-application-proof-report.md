# Отчет downstream application proof

Дата: 2026-05-06

proof_status: blocked_external_inputs
downstream_repo: external_input_required
app_image: external_real_app_image_required
runtime_target: external_target_required
healthcheck_url: external_healthcheck_required
healthcheck_result: not_run
migrations: not_run
backup_result: not_run
restore_result: not_run
rollback_result: not_run
sanitized_transcript: missing
secrets_boundary: unconfirmed
blocker_reason: external inputs missing for downstream repo, real APP_IMAGE, target, secrets, approvals and transcript
readiness_status: ready_for_external_pilot

## Runtime evidence данные

app_image_evidence: external real image digest required
healthcheck_evidence: external healthcheck evidence required
migrations_evidence: external migration policy required
backup_evidence: external backup evidence required
restore_evidence: external restore evidence required
rollback_evidence: external rollback evidence required
transcript_evidence: external sanitized transcript required
secrets_boundary_evidence: external secrets boundary confirmation required

## Novice-to-deploy scorecard данные

time_to_first_handoff_minutes: not_run
handoff_rework_loops: not_run
manual_interventions: not_run
external_blockers: 5
deploy_result: not_run
scorecard_evidence: blocked until real downstream pilot runs

## Санитизированный transcript

```text
not_run: no real downstream pilot has been executed.
```
