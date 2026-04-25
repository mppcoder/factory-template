## Direct Task Self-Handoff

## Classification
direct-task

## Selected project profile
factory-template

## Selected scenario
17-direct-task-self-handoff.md -> 15-handoff-to-codex.md -> implementation/remediation

## Current pipeline stage
implementation

## Task class
build

## Selected profile
build

## Selected model
gpt-5.5

## Selected reasoning effort
medium

## Apply mode
manual-ui

## Manual UI apply
- Откройте новый чат/окно Codex.
- Вручную выберите model `gpt-5.5` и reasoning `medium` в picker.
- Только после этого продолжайте работу по self-handoff.
- Уже открытая live session не является надежным auto-switch boundary.

## Strict launch mode
optional

## Artifacts to update
- template-repo/codex-routing.yaml
- template-repo/scripts/codex_task_router.py
- template-repo/template/.codex/config.toml
- workspace-packs/vscode-codex-bootstrap/codex/global-codex-config.example.toml
- factory_template_only_pack/03-mode-routing-factory-template.md
- factory_template_only_pack/06-codex-config-factory-template.toml
- .chatgpt/direct-task-self-handoff.md
- .chatgpt/direct-task-response.md
- .chatgpt/task-launch.yaml

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
`codex --profile build`

## Troubleshooting
- Если вы работаете через VS Code Codex extension интерактивно, используйте новый чат/окно, вручную выставьте selected_model и selected_reasoning_effort в picker, а затем вставьте handoff.
- Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же; не выдавайте manual UI apply за auto-switch.
- Если handoff вставлен в уже открытую или случайную Codex chat-сессию без ручной проверки picker, это non-canonical path: route может остаться stale.
- Если нужна строгая воспроизводимость, automation или shell-first запуск, используйте optional strict launch_command.
- Если после launch или manual UI apply виден sticky last-used profile/model/reasoning, закройте текущую сессию, откройте новую и при необходимости выполните launch_command, затем проверьте named profile в local Codex config.
- Если selected_model отсутствует в live catalog, обновите codex-routing.yaml или local profile mapping, прежде чем обещать этот model ID пользователю.

## Task payload
task_class: build
selected_profile: build
project_profile: factory-template
selected_scenario: 17-direct-task-self-handoff.md -> 15-handoff-to-codex.md -> implementation/remediation
pipeline_stage: implementation
handoff_allowed: yes
defect_capture_path: not-required-by-text-signal
artifacts_to_update:
  - template-repo/codex-routing.yaml
  - template-repo/scripts/codex_task_router.py
  - template-repo/template/.codex/config.toml
  - workspace-packs/vscode-codex-bootstrap/codex/global-codex-config.example.toml
  - factory_template_only_pack/03-mode-routing-factory-template.md
  - factory_template_only_pack/06-codex-config-factory-template.toml
  - .chatgpt/direct-task-self-handoff.md
  - .chatgpt/direct-task-response.md
  - .chatgpt/task-launch.yaml

task: обновить список рекомендуемых моделей для выполнения handoff с учетом выхода GPT-5.5

## Next step
Только после этого блока допустимы remediation / implementation / verification.
