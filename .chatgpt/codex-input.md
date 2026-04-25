task_class: deep
selected_profile: deep
project_profile: factory-template
selected_scenario: 15-handoff-to-codex.md -> implementation/remediation
pipeline_stage: implementation
handoff_allowed: yes
defect_capture_path: not-required-by-text-signal; use reports/bugs/YYYY-MM-DD-production-operator-preset.md only for incidental/regression evidence
artifacts_to_update:
  - deploy/compose.yaml
  - deploy/compose.production.yaml
  - deploy/.env.example
  - deploy/presets/app-db.yaml
  - deploy/presets/reverse-proxy.yaml
  - template-repo/scripts/deploy-dry-run.sh
  - template-repo/scripts/deploy-local-vps.sh
  - template-repo/scripts/operator-dashboard.py
  - template-repo/scripts/validate-operator-env.py
  - docs/deploy-on-vps.md
  - docs/operator-next-step.md
  - template-repo/scripts/verify-all.sh

HANDOFF: FT-2.5.4-production-operator-presets

Objective:
Усилить operator surface до production-ready baseline для типовых single-VPS проектов, не ломая минимальный starter profile.

Scope:
- Добавить optional presets: app+db, reverse proxy/TLS, backup hooks, health checks.
- Улучшить env validation и operator diagnostics.
- Добавить безопасный remote-VPS readiness checklist.
- Обновить dashboard так, чтобы он понимал preset profile и показывал targeted recommendations.

Acceptance criteria:
- baseline starter profile остаётся рабочим
- optional profiles документированы и валидируются dry-run path
- dashboard различает starter profile и production preset
- operator docs покрывают secrets, backups, health checks, rollback path
- verify-all / matrix test включают минимум один preset-oriented сценарий

Required roles / skills:
- DevOps / Docker Compose
- Bash/Python scripting
- security review
- documentation
