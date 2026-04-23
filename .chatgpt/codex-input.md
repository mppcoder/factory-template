# Входной пакет для Codex

launch_source: chatgpt-handoff
task_class: build
selected_profile: build
selected_model: gpt-5.4
selected_reasoning_effort: medium
apply_mode: manual-ui
strict_launch_mode: optional
project_profile: factory-template
selected_scenario: 00-master-router.md
pipeline_stage: defect-capture -> classification -> remediation -> verify
artifacts_to_update:
  - template-repo/scenario-pack/00-master-router.md
  - template-repo/scenario-pack/15-handoff-to-codex.md
  - template-repo/scenario-pack/16-done-closeout.md
  - template-repo/scripts/create-codex-task-pack.py
  - template-repo/scripts/validate-codex-task-pack.py
  - docs/template-architecture-and-event-workflows.md
  - .chatgpt/codex-input.md
  - .chatgpt/codex-context.md
  - .chatgpt/codex-task-pack.md
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
  - reports/bugs/bug-021-repo-first-completion-package-overstates-factory-chatgpt-update.md
  - reports/factory-feedback/feedback-021-repo-first-completion-package-overstates-factory-chatgpt-update.md
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> remediation

## Контекст
- Completion package все еще слишком широко трактует contour `factory-template ChatGPT Project`.
- Для чистого repo-first режима этот contour тоже должен быть `нет` по умолчанию, если canonical repo/path/entrypoint/instruction text не менялись.

## Что именно нужно сделать
- Зафиксировать reusable process defect completion-layer.
- Переписать source-of-truth rules и generator так, чтобы `Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project` по умолчанию означало `нет`, если instruction contract не менялся.
- Оставить `да` только для случаев реального изменения repo/path/entrypoint/instruction text.
- Пересобрать `.chatgpt` artifacts, проверить validators и довести change до verified sync.

## Какие артефакты являются источником правды
- `AGENTS.md`
- `README.md`
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scenario-pack/16-done-closeout.md`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-task-pack.py`

## Что запрещено делать
- Нельзя трактовать factory-template ChatGPT Project instruction как default contour, если canonical repo/path/entrypoint/instruction text не менялись.
- Нельзя советовать лишний manual update для Project instructions там, где contract уже остается прежним.
