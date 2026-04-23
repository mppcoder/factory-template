# Normalized Codex Handoff

## Launch source
chatgpt-handoff

## Task class
deep

## Task class evidence
- explicit task class override: deep
- explicit selected_profile override: deep

## Selected profile
deep

## Selected model
gpt-5.4

## Selected reasoning effort
high

## Selected plan mode reasoning
high

## Apply mode
manual-ui

## Manual UI apply
- Откройте новый чат/окно Codex в VS Code extension.
- Вручную выберите model `gpt-5.4` и reasoning `high` в picker.
- Только после этого вставьте handoff.
- Уже открытая live session не считается надежным auto-switch boundary.

## Strict launch mode
optional

## Project profile
factory-template

## Selected scenario
00-master-router.md

## Pipeline stage
defect-capture -> classification -> remediation

## Artifacts to update
- template-repo/scenario-pack/00-master-router.md
- template-repo/codex-routing.yaml
- template-repo/scripts/bootstrap-codex-task.py
- template-repo/scripts/launch-codex-task.sh
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md
- source-facing runbooks/guides/templates for Codex / VS Code Codex extension handoff
- completion package / downstream update instructions if source files change

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
`codex --profile deep`

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
task_class: deep
selected_profile: deep
selected_model: gpt-5.4
selected_reasoning_effort: high
apply_mode: manual-ui
strict_launch_mode: optional
project_profile: factory-template
selected_scenario: 00-master-router.md
pipeline_stage: defect-capture -> classification -> remediation
artifacts_to_update:
  - template-repo/scenario-pack/00-master-router.md
  - template-repo/codex-routing.yaml
  - template-repo/scripts/bootstrap-codex-task.py
  - template-repo/scripts/launch-codex-task.sh
  - .chatgpt/codex-input.md
  - .chatgpt/codex-context.md
  - .chatgpt/codex-task-pack.md
  - .chatgpt/verification-report.md
  - .chatgpt/done-report.md
  - source-facing runbooks/guides/templates for Codex / VS Code Codex extension handoff
  - completion package / downstream update instructions if source files change
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> remediation

## Контекст
- Шаблон корректно различает advisory/policy layer и executable routing layer, но user-facing default UX для VS Code Codex extension перегружен launcher-first flow.
- Пользователь для interactive extension workflow не должен быть вынужден идти в terminal, если достаточно manual picker selection в новом окне/чате Codex.
- При этом нельзя обещать auto-switch profile/model/reasoning внутри уже открытой live session.

## Что именно нужно сделать
- Зафиксировать defect-capture по UX mismatch: проблема в default template behavior, а не в пользователе.
- Явно различить `manual-ui (default)`, `launcher-first strict mode (optional)` и `already-open session = non-canonical fallback`.
- Пересобрать handoff/completion слой так, чтобы для VS Code Codex extension по умолчанию выдавался UI-first handoff с `selected_profile`, `selected_model`, `selected_reasoning_effort`, `selected_scenario`, `pipeline_stage` и короткой manual UI apply-инструкцией.
- Сохранить launcher path только как optional strict mode для automation / reproducibility / shell-first / scripted launch.
- Обновить source-facing docs, templates, validators и generated `.chatgpt` artifacts под dual-path contract.
- Подготовить completion package для factory/downstream/ChatGPT Project source sync, если затронут downstream-consumed sources.

## Какие артефакты являются источником правды
- `AGENTS.md`
- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/12-bug-analysis.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/codex-routing.yaml`
- `template-repo/scripts/*codex*`
- `template-repo/template/docs/*`

## Что запрещено делать
- Нельзя подавать launcher-first path как обязательный default для интерактивной работы в VS Code Codex extension.
- Нельзя утверждать, что handoff text, static profile или уже открытая live session сами автоматически переключают model/profile/reasoning.
- Нельзя смешивать `новый чат + вставка handoff` с `new task launch через executable launcher`.