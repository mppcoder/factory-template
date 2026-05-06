# Отчет downstream application proof

Дата: 2026-05-06

proof_status: blocked_external_inputs
downstream_repo: external_input_required
app_image: external_real_app_image_required
runtime_target: external_approved_target_required
healthcheck_url: external_healthcheck_required
healthcheck_result: not_run
migrations: not_run
backup_result: not_run
restore_result: not_run
rollback_result: not_run
sanitized_transcript: missing
secrets_boundary: unconfirmed
blocker_reason: external inputs missing: downstream repo path, real APP_IMAGE, approved VPS/staging target, secrets outside repo, deploy/restore/rollback approval and sanitized transcript are required before pass claim
readiness_status: ready_for_external_pilot

## Runtime evidence данные

app_image_evidence: external real image digest required before pass
healthcheck_evidence: app-specific healthcheck required before pass
migrations_evidence: migration policy or not-applicable reason required before pass
backup_evidence: project backup artifact required before pass
restore_evidence: disposable or staging restore evidence required before pass
rollback_evidence: rollback drill evidence required before pass
transcript_evidence: sanitized transcript required before pass
secrets_boundary_evidence: secrets must be entered outside repo and transcript before pass

## Novice-to-deploy scorecard данные

time_to_first_handoff_minutes: not_run
handoff_rework_loops: not_run
manual_interventions: not_run
external_blockers: 5
deploy_result: not_run
scorecard_evidence: scorecard is blocked until a real downstream pilot runs

## Санитизированный transcript

```text
not_run: no downstream/battle pilot has been executed for this report.
```

## Boundary правило

This report does not claim downstream/battle application proof pass. It records that the proof contour is ready for an external pilot and blocked on real downstream inputs.
