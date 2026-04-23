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
  - reports/bugs/bug-020-repo-first-completion-package-overstates-downstream-chatgpt-updates.md
  - reports/factory-feedback/feedback-020-repo-first-completion-package-overstates-downstream-chatgpt-updates.md
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> remediation

## Контекст
- Шаблонный completion package слишком широко трактует contour `downstream/battle ChatGPT Projects`.
- Для чистого repo-first режима это должен быть `нет` по умолчанию, а не generic contour, который легко превращается в `да`.

## Что именно нужно сделать
- Зафиксировать reusable process defect completion-layer.
- Переписать source-of-truth rules и generator так, чтобы `Нужно ли обновлять repo-first инструкции battle ChatGPT Projects` по умолчанию означало `нет` для чистого repo-first режима.
- Сохранить `да` только как legacy/hybrid fallback.
- Пересобрать `.chatgpt` artifacts, проверить validators и довести change до verified sync.

## Какие артефакты являются источником правды
- `AGENTS.md`
- `template-repo/AGENTS.md`
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scenario-pack/16-done-closeout.md`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- `README.md`

## Что запрещено делать
- Нельзя трактовать downstream ChatGPT Project instructions как default contour в чистом repo-first режиме.
- Нельзя советовать refresh `Sources` или переписывание Project instructions там, где source-of-truth уже давно читается из репо.
