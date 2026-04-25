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
15-handoff-to-codex.md -> 14-docs-normalization.md -> implementation/remediation

## Pipeline stage
implementation

## Artifacts to update
- template-repo/skills/skill-master-lite/SKILL.md
- template-repo/skills/skill-tester-lite/SKILL.md
- template-repo/skills/skill-tester-lite/references/test-design-guide.md
- template-repo/skills/skill-tester-lite/references/report-template.md
- docs/skills-quality-loop.md
- README.md

## Handoff allowed
yes

## Defect capture path
not-required-by-text-signal; use reports/bugs/YYYY-MM-DD-skill-meta-qa-loop.md only for incidental/regression evidence

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
selected_profile: build
project_profile: factory-template
selected_scenario: 15-handoff-to-codex.md -> 14-docs-normalization.md -> implementation/remediation
pipeline_stage: implementation
handoff_allowed: yes
defect_capture_path: not-required-by-text-signal; use reports/bugs/YYYY-MM-DD-skill-meta-qa-loop.md only for incidental/regression evidence
artifacts_to_update:
  - template-repo/skills/skill-master-lite/SKILL.md
  - template-repo/skills/skill-tester-lite/SKILL.md
  - template-repo/skills/skill-tester-lite/references/test-design-guide.md
  - template-repo/skills/skill-tester-lite/references/report-template.md
  - docs/skills-quality-loop.md
  - README.md

HANDOFF: FT-2.5.6-skill-meta-qa

Objective:
Добавить в factory-template облегчённый meta-QA цикл для skills и prompt-like artifacts:
создал -> протестировал -> улучшил trigger/usefulness.

Scope:
- Адаптировать идеи skill-master/skill-tester под нужды factory-template.
- Не переносить весь comparison repo; собрать только минимально полезный контур.
- Сделать это опциональным advanced mode, не обязательным слоем для новичка.

Acceptance criteria:
- существует documented optional workflow для тестирования skills/prompt artifacts
- workflow отделён от beginner default path
- есть минимум один пример использования на артефакте factory-template
- docs объясняют value простым языком: "это для улучшения шаблона, а не обязательный шаг новичка"

Model / reasoning effort suggestion:
GPT-5.2 Thinking
Reasoning effort: medium-high

Required roles / skills:
- prompt / skill design
- documentation
- evaluation design
- unspecified: если нужен отдельный evaluator/benchmark owner
