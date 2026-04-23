# Normalized Codex Handoff

## Launch source
chatgpt-handoff

## Task class
build

## Task class evidence
- explicit task class override: build
- explicit selected_profile override: build

## Selected profile
build

## Selected model
gpt-5.4

## Selected reasoning effort
medium

## Selected plan mode reasoning
medium

## Apply mode
manual-ui

## Manual UI apply
- Откройте новый чат/окно Codex в VS Code extension.
- Вручную выберите model `gpt-5.4` и reasoning `medium` в picker.
- Только после этого вставьте handoff.
- Уже открытая live session не считается надежным auto-switch boundary.

## Strict launch mode
optional

## Project profile
factory-template

## Selected scenario
00-master-router.md

## Pipeline stage
defect-capture -> classification -> remediation -> verify

## Artifacts to update
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

## Handoff allowed
yes

## Defect capture path
reproduce -> evidence -> bug report -> layer classification -> remediation

## Launch boundary rule
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Interactive default rule
Для интерактивной работы в VS Code Codex extension основной user-facing path: открыть новое окно/чат Codex, вручную выбрать model/reasoning в picker и затем вставить handoff.

## Executable switch rule
Строго воспроизводимый executable switch в live Codex для этого repo: явный новый task launch через launcher и selected_profile.

## Strict launch rule
Launcher-first path остается optional strict mode для automation, reproducibility, shell-first и scripted launch.

## Live session fallback rule
Уже открытая live session не является надежным механизмом автопереключения profile/model/reasoning и допустима только как non-canonical fallback.

## Model expectation rule
selected_model и selected_reasoning_effort фиксируют ожидаемую конфигурацию выбранного executable profile; advisory handoff text сам по себе ничего не переключает.

## Launch artifact path
`.chatgpt/codex-input.md`

## Optional strict launch command
`./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute`

## Strict launch use cases
- automation
- reproducibility
- shell-first
- scripted launch

## Direct Codex command behind launcher
`codex --profile build`

## Troubleshooting
- Если вы работаете через VS Code Codex extension интерактивно, используйте новый чат/окно, вручную выставьте selected_model и selected_reasoning_effort в picker, а затем вставьте handoff.
- Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же; не выдавайте manual UI apply за auto-switch.
- Если handoff вставлен в уже открытую или случайную Codex chat-сессию без ручной проверки picker, это non-canonical path: route может остаться stale.
- Если нужна строгая воспроизводимость, automation или shell-first запуск, используйте optional strict launch_command.
- Если после launch или manual UI apply виден sticky last-used profile/model/reasoning, закройте текущую сессию, откройте новую и при необходимости выполните launch_command, затем проверьте named profile в local Codex config.
- Если selected_model отсутствует в live catalog, обновите codex-routing.yaml или local profile mapping, прежде чем обещать этот model ID пользователю.

## Task payload
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