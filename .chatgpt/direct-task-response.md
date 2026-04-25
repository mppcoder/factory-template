## Direct Task Self-Handoff

## Classification
direct-task

## Selected project profile
factory-template

## Selected scenario
16-done-closeout.md + 17-direct-task-self-handoff.md

## Current pipeline stage
closeout sync

## Task class
review

## Selected profile
review

## Selected model
gpt-5.4

## Selected reasoning effort
high

## Apply mode
manual-ui

## Manual UI apply
- Откройте новый чат/окно Codex.
- Вручную выберите model `gpt-5.4` и reasoning `high` в picker.
- Только после этого продолжайте работу по self-handoff.
- Уже открытая live session не является надежным auto-switch boundary.

## Strict launch mode
optional

## Artifacts to update
- .chatgpt/task-launch.yaml
- .chatgpt/direct-task-self-handoff.md
- .chatgpt/direct-task-response.md
- git commit
- origin/main

## Handoff allowed
yes

## Defect capture path
not-required-by-text-signal

## Launch source
direct-task

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

## Optional strict launch command
`./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute`

## Strict launch use cases
- automation
- reproducibility
- shell-first
- scripted launch

## Direct Codex command behind launcher
`codex --profile review`

## Troubleshooting
- Если вы работаете через VS Code Codex extension интерактивно, используйте новый чат/окно, вручную выставьте selected_model и selected_reasoning_effort в picker, а затем вставьте handoff.
- Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же; не выдавайте manual UI apply за auto-switch.
- Если handoff вставлен в уже открытую или случайную Codex chat-сессию без ручной проверки picker, это non-canonical path: route может остаться stale.
- Если нужна строгая воспроизводимость, automation или shell-first запуск, используйте optional strict launch_command.
- Если после launch или manual UI apply виден sticky last-used profile/model/reasoning, закройте текущую сессию, откройте новую и при необходимости выполните launch_command, затем проверьте named profile в local Codex config.
- Если selected_model отсутствует в live catalog, обновите codex-routing.yaml или local profile mapping, прежде чем обещать этот model ID пользователю.

## Task payload
classification: direct-task
project_profile: factory-template
selected_scenario: 16-done-closeout.md + 17-direct-task-self-handoff.md
pipeline_stage: closeout sync
artifacts_to_update:
  - .chatgpt/task-launch.yaml
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/direct-task-response.md
  - git commit
  - origin/main
handoff_allowed: yes
defect_capture_path: not-required-by-text-signal
task: закрывай, комить и пуш

## Next step
Только после этого блока допустимы remediation / implementation / verification.
