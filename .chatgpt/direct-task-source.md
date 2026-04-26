task_class: deep
selected_profile: deep
project_profile: brownfield-without-repo
selected_scenario: brownfield/06-reverse-engineering-plan.md
pipeline_stage: source-candidate-map-and-closeout-defect-remediation
handoff_allowed: no
artifacts_to_update:
  - .chatgpt/task-launch.yaml
  - .chatgpt/direct-task-source.md
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/normalized-codex-handoff.md
  - .chatgpt/direct-task-response.md
  - template-repo/scripts/codex_task_router.py
  - template-repo/scripts/validate-codex-routing.py
  - template-repo/scripts/create-codex-task-pack.py
  - template-repo/scripts/validate-codex-task-pack.py
  - reports/bugs/bug-035-closeout-stopped-before-internal-followup-and-user-instruction.md
  - reports/factory-feedback/feedback-035-closeout-stopped-before-internal-followup-and-user-instruction.md
  - brownfield/source-candidate-map.md
  - brownfield/reconstruction-allowlist.md
  - brownfield/reconstruction-denylist.md
  - brownfield/change-map.md
  - brownfield/reverse-engineering-plan.md
  - brownfield/gap-register.md
  - .chatgpt/evidence-register.md
  - .chatgpt/reality-check.md
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

Продолжить полевой тест OpenClaw+ после intake и исправить reusable defect: предыдущий closeout остановился перед внутренним source-candidate-map и не дал обязательный пользовательский completion package. Построить source-candidate map и reconstruction boundary для /root/.openclaw и /root/openclaw-plus. Исправить генератор/валидаторы direct-task closeout так, чтобы self-handoff не требовал ручного продолжения, а финальная инструкция пользователю не пропадала. Не выполнять remediation OpenClaw runtime, не создавать repo в /root, не раскрывать секреты.
