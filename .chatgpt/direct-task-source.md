task_class: deep
selected_profile: deep
project_profile: brownfield-without-repo
selected_scenario: brownfield/11-codex-assisted-stabilization.md
pipeline_stage: fp-02-github-remote-and-roadmap-continuation
handoff_allowed: no
artifacts_to_update:
  - .chatgpt/task-launch.yaml
  - .chatgpt/direct-task-source.md
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/normalized-codex-handoff.md
  - .chatgpt/direct-task-response.md
  - .chatgpt/boundary-actions.md
  - .chatgpt/done-checklist.md
  - reports/bugs/bug-037-github-repo-creation-misclassified-as-user-step.md
  - reports/factory-feedback/feedback-037-github-repo-creation-misclassified-as-user-step.md
  - reports/bugs/bug-038-generated-project-root-script-verify-all-wrong-root.md
  - reports/factory-feedback/feedback-038-generated-project-root-script-verify-all-wrong-root.md
  - reports/release/field-pilot-scenarios/02-brownfield-without-repo.md
  - reports/release/2.5-field-pilot-evidence.md
  - brownfield/reconstruction-repo-report.md
  - brownfield/gap-register.md
  - .chatgpt/evidence-register.md
  - .chatgpt/reality-check.md
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

Исправить пойманные баги: не останавливаться просьбой пользователю создать GitHub repo и прислать URL, если gh/GitHub write path доступен; дать четкую инструкцию по внешним действиям только при реальном blocker; исправить generated root scripts/verify-all.sh, который в downstream repo вычислял ROOT как /projects. Создать/подключить GitHub remote для /projects/openclaw-brownfield и продолжить field pilot roadmap честно.
