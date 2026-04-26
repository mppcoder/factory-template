task_class: deep
selected_profile: deep
project_profile: brownfield-without-repo
selected_scenario: brownfield/11-codex-assisted-stabilization.md
pipeline_stage: fp-02-create-reconstructed-repo
handoff_allowed: no
artifacts_to_update:
  - .chatgpt/task-launch.yaml
  - .chatgpt/direct-task-source.md
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/normalized-codex-handoff.md
  - .chatgpt/direct-task-response.md
  - reports/bugs/bug-036-fp02-marked-passed-before-repo-creation.md
  - reports/factory-feedback/feedback-036-fp02-marked-passed-before-repo-creation.md
  - reports/release/field-pilot-scenarios/02-brownfield-without-repo.md
  - reports/release/2.5-field-pilot-evidence.md
  - brownfield/reconstruction-repo-report.md
  - brownfield/gap-register.md
  - .chatgpt/evidence-register.md
  - .chatgpt/reality-check.md
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

Исправить FP-02 defect: brownfield without repo подразумевает аудит и создание безопасного project repo boundary, а предыдущий closeout ошибочно пометил FP-02 passed только по audit/allowlist. Создан sanitized project repo /projects/openclaw-brownfield, source layer лежит в src/openclaw-plus, raw /root/.openclaw и значения /etc/openclaw-plus.env не перенесены. Зафиксировать отчет, bug/feedback и обновить field evidence.
