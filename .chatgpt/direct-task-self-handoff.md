# Self-handoff для прямой задачи

## Источник запуска
direct-task

## Вид handoff
codex-task-handoff

## Контракт цели
- normalized_goal: `codex_work_id: FT-CX-0035
codex_work_title: FT-CX-0035 continue-internal-followup-bug
task_slug: continue-internal-followup-bug
codex_work_state: codex_accepted

user_request: почему остановка? продолжай все шаги без остановки и пофиксь этот баг
normalized_goal: Fix premature user-step closeout and guided launcher nested project root bugs, then continue Health Sync Bridge internal implementation scaffolding until real external blockers.`
- definition_of_done: evidence satisfies requested outcome and relevant repo validators or blockers are documented.
- evidence_required: verification-report.md, done-report.md, targeted validation evidence.
- scope: repo-local artifacts selected by route.
- non_goals: production/destructive/secrets actions unless explicitly approved.
- proxy_signal_denylist: tests passed alone; file exists alone; commit exists alone; green dashboard alone; validator passed alone.
- goal_achievement_rule: mark achieved only when evidence satisfies DoD, not when proxy signals pass.

## Среда выполнения цели
- goal_runtime_recommendation: `codex_goal_candidate`
- codex_goal_live_validation_required: `true`
- rule: Codex /goal runtime optional/live-gated; experimental goals require explicit user/operator choice and do not auto-enable in already-open sessions.

## Решение о фактическом execution mode
- owner: Codex после route receipt и анализа task graph.
- allowed modes: `single-session execution` или `orchestrated-child-sessions`.
- closeout обязателен: назвать actual execution mode и `child/subagent count`.
- rule: handoff остается одним `codex-task-handoff`; orchestration candidate signals не равны фактическому запуску child/subagent sessions.

## Стабильная identity чата и handoff
- chat_id: ``
- chat_title: ``
- task_slug: `continue-internal-followup-bug`
- kind: ``
- state: ``
- source_of_truth: `.chatgpt/chat-handoff-index.yaml`
- rule: номер выделяется из общего repo counter до первого substantive ответа; status/kind не добавляются в title.

## Evidence для вида handoff
- default neutral handoff: Codex decides actual execution_mode after analysis

## Класс задачи
build

## Evidence для класса задачи
- keyword-hit: fix
- keyword-hit: implement
- keyword-hit: implementation
- явный reasoning/model override совпал с default profile: build

## Выбранный профиль
build

## Выбранная модель
gpt-5.5

## Выбранное reasoning effort
medium

## Выбранное reasoning effort для plan mode
medium

## Режим применения
manual-ui

## Ручное применение через UI
- Откройте новый чат/окно Codex в VS Code extension.
- Вручную выберите model `gpt-5.5` и reasoning `medium` в picker.
- Только после этого вставьте handoff.
- Codex должен отвечать пользователю на русском языке; английский допустим только для technical literal values.
- Уже открытая live session не считается надежным auto-switch boundary.

## Язык ответа Codex
Русский. Английский допустим только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

## Строгий режим запуска
optional

## Профиль проекта
unknown-project-profile

## Выбранный сценарий
00-master-router.md

## Этап pipeline
done

## Артефакты для обновления
- .chatgpt/goal-contract.yaml
- .chatgpt/goal-state.yaml
- .chatgpt/codex-input.md
- .chatgpt/codex-context.md
- .chatgpt/codex-task-pack.md
- .chatgpt/verification-report.md
- .chatgpt/done-report.md
- reports/bugs/
- reports/factory-feedback/

## Разрешение handoff
yes (forbidden)

## Маршрут defect-capture
reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation

## Правило launch boundary
Выбор модели и reasoning mode считается надежным только на новом запуске Codex для новой задачи.

## Правило интерактивного режима по умолчанию
Для интерактивной работы в VS Code Codex extension основной пользовательский путь: открыть новое окно/чат Codex, вручную выбрать model/reasoning в picker и затем вставить handoff.

## Правило executable switch
Строго воспроизводимое executable-переключение в live Codex для этого repo: явный новый task launch через launcher и selected_profile.

## Правило строгого запуска
Launcher-first path остается опциональным строгим режимом для автоматизации, воспроизводимости, запуска из shell и scripted launch.

## Правило fallback для live session
Уже открытая live session не является надежным механизмом автопереключения profile/model/reasoning и допустима только как неканонический fallback.

## Правило ожиданий по модели
selected_model и selected_reasoning_effort фиксируют repo-configured mapping выбранного executable profile; live availability подтверждается отдельной проверкой `codex debug models`, а advisory handoff text сам по себе ничего не переключает.

## Статус catalog check
available

## Последняя catalog check UTC
2026-04-25T18:26:17Z

## Примечание по live availability
selected_model совпадает с последним сохраненным snapshot repo catalog; перед внешними обещаниями повторите live catalog check

## Базовый prompt contract для GPT-5.5
- GPT-5.5 не считать drop-in replacement для старого prompt stack.
- Начинать с fresh baseline: роль/область ответственности, ожидаемый outcome, success criteria, constraints, output shape и stop rules.
- Сохранять обязательные repo invariants: чтение router, defect-capture, handoff/routing/closeout rules.
- Убирать лишнюю пошаговую процессность, если путь не является обязательным repo invariant.
- Для tool-heavy задач явно задавать evidence requirements, validation commands и fallback/blocker behavior.
- Держать stable rules выше task-specific dynamic content, чтобы prompt caching и повторное использование оставались устойчивыми.
- Не вставлять current date как постоянную model instruction; даты reports/filenames фиксировать как metadata.

## Путь launch artifact
`.chatgpt/direct-task-source.md`

## Опциональная команда строгого запуска
`./scripts/launch-codex-task.sh --launch-source direct-task --task-file .chatgpt/direct-task-source.md --execute`

## Сценарии для строгого запуска
- автоматизация
- воспроизводимость
- запуск из shell
- scripted launch

## Прямая команда Codex за launcher
`codex --profile build`

## Диагностика проблем
- Если вы работаете через VS Code Codex extension интерактивно, используйте новый чат/окно, вручную выставьте selected_model и selected_reasoning_effort в picker, а затем вставьте handoff.
- Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же; не выдавайте manual UI apply за auto-switch.
- Если handoff вставлен в уже открытую или случайную Codex chat-сессию без ручной проверки picker, это неканонический путь: route может остаться устаревшим.
- Если нужна строгая воспроизводимость, автоматизация или запуск из shell, используйте optional strict launch_command.
- Если после launch или manual UI apply виден sticky last-used profile/model/reasoning, закройте текущую сессию, откройте новую и при необходимости выполните launch_command, затем проверьте именованный profile в local Codex config.
- Если selected_model отсутствует в live catalog, обновите codex-routing.yaml или local profile mapping, прежде чем обещать этот model ID пользователю.
- Если новый model ID появился в live catalog, сначала создайте proposal через `scripts/check-codex-model-catalog.py --write-proposal`; promotion profile mapping требует ручного review.
- Если используется experimental `goals`, сначала проверьте `codex features list`; включение goal runtime является runtime/operator choice и не следует из advisory текста.

## Текст задачи
codex_work_id: FT-CX-0035
codex_work_title: FT-CX-0035 continue-internal-followup-bug
task_slug: continue-internal-followup-bug
codex_work_state: codex_accepted

user_request: почему остановка? продолжай все шаги без остановки и пофиксь этот баг
normalized_goal: Fix premature user-step closeout and guided launcher nested project root bugs, then continue Health Sync Bridge internal implementation scaffolding until real external blockers.
