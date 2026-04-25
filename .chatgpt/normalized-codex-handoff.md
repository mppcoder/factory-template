# Normalized Codex Handoff

## Launch source
chatgpt-handoff

## Task class
build

## Task class evidence
- explicit task class override: build
- explicit reasoning/model override matched default profile: build

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
unknown-project-profile

## Selected scenario
12-bug-analysis.md + 14-docs-normalization.md + 15-handoff-to-codex.md

## Pipeline stage
remediation

## Artifacts to update
- docs/releases/2.5-roadmap.md
- docs/releases/2.5-success-metrics.md
- CURRENT_FUNCTIONAL_STATE.md
- README.md
- RELEASE_CHECKLIST.md
- PRE_RELEASE_AUDIT.sh
- template-repo/scripts/verify-all.sh
- docs/releases/release-scorecard.yaml
- template-repo/scripts/validate-release-scorecard.py
- TEST_REPORT.md
- reports/bugs/2026-04-25-release-truth-drift.md

## Handoff allowed
yes

## Defect capture path
reproduce -> evidence -> bug report -> layer classification -> remediation -> verification

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
task_class: build
selected_scenario: 12-bug-analysis.md + 14-docs-normalization.md + 15-handoff-to-codex.md
pipeline_stage: remediation
artifacts_to_update:
  - docs/releases/2.5-roadmap.md
  - docs/releases/2.5-success-metrics.md
  - CURRENT_FUNCTIONAL_STATE.md
  - README.md
  - RELEASE_CHECKLIST.md
  - PRE_RELEASE_AUDIT.sh
  - template-repo/scripts/verify-all.sh
  - docs/releases/release-scorecard.yaml
  - template-repo/scripts/validate-release-scorecard.py
  - TEST_REPORT.md
  - reports/bugs/2026-04-25-release-truth-drift.md
handoff_allowed: yes
defect_capture_path: reproduce -> evidence -> bug report -> layer classification -> remediation -> verification

HANDOFF: FT-2.5.1-release-truth

Objective:
Свести в единый источник истины состояние релиза 2.5+, устранить drift между roadmap/current-state/README, добавить machine-readable release scorecard и включить его в pre-release/CI gates.

Scope:
- Синхронизировать docs/releases/2.5-roadmap.md, CURRENT_FUNCTIONAL_STATE.md, README.md, RELEASE_CHECKLIST.md.
- Создать единый файл release-scorecard.yaml или release-scorecard.json.
- Добавить в PRE_RELEASE_AUDIT.sh и verify-all.sh проверку согласованности release state.
- Обновить TEST_REPORT.md template/source-of-truth strategy так, чтобы статус релиза не зависел только от вручную обновляемого markdown.

Acceptance criteria:
- roadmap/current-state/README описывают одну и ту же стадию релиза без противоречий
- release-scorecard существует и заполняется однозначно
- PRE_RELEASE_AUDIT.sh падает при несогласованности release документов
- verify-all.sh ci включает проверку release-scorecard
- добавлен короткий human-readable раздел “How to read release truth”

Defect capture path:
reports/bugs/YYYY-MM-DD-release-truth-drift.md
