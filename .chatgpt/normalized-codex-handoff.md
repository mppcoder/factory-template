# Normalized Codex Handoff

## Launch source
chatgpt-handoff

## Task class
review

## Task class evidence
- keyword hit: test
- keyword hit: провер
- explicit reasoning/model override matched default profile: review

## Selected profile
review

## Selected model
gpt-5.4

## Selected reasoning effort
high

## Selected plan mode reasoning
high

## Project profile
unknown-project-profile

## Selected scenario
00-master-router.md

## Pipeline stage
done

## Artifacts to update
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md

## Handoff allowed
yes (forbidden)

## Defect capture path
not-required-by-text-signal

## Launch boundary rule
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Executable switch rule
Надежно исполняемый switch в live Codex для этого repo: явный новый task launch через launcher и selected_profile.

## Model expectation rule
selected_model и selected_reasoning_effort фиксируют ожидаемую конфигурацию выбранного executable profile; advisory handoff text сам по себе ничего не переключает.

## Launch artifact path
`.chatgpt/codex-input.md`

## Executable launch command
`./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute`

## Direct Codex command behind launcher
`codex --profile review`

## Troubleshooting
- Если handoff вставлен в уже открытую или случайную Codex chat-сессию, это non-canonical path: завершите сессию и выполните новый task launch.
- Если после launch виден sticky last-used profile/model/reasoning, снова выполните launch_command и проверьте named profile в local Codex config.
- Если selected_model отсутствует в live catalog, обновите codex-routing.yaml или local profile mapping, прежде чем обещать этот model ID пользователю.

## Task payload
# Входной пакет для Codex

## Контекст
- Это smoke-test ядра фабрики проектов.
- Базовые проверки уже закрыты и подтверждены evidence-артефактами.
- При исполнении этого handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.

## Что должен сделать исполнитель
- Считать smoke-test завершенным без дополнительных изменений.

## Ограничения
- Не менять core-структуру проекта.
- Общие рабочие инструкции применять только там, где они не противоречат repo rules и старшим системным ограничениям среды.
