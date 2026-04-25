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
15-handoff-to-codex.md -> implementation/remediation

## Pipeline stage
implementation

## Artifacts to update
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

## Handoff allowed
yes

## Defect capture path
not-required-by-text-signal; use reports/bugs/YYYY-MM-DD-production-operator-preset.md only for incidental/regression evidence

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
