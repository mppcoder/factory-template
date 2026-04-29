Язык ответа Codex: русский
Отвечай пользователю по-русски. Английский допускается только для технических идентификаторов, имен файлов, команд, YAML/TOML ключей и literal values.

# Child Codex session handoff / дочерний handoff

## Parent задача
- parent_id: p9-lifecycle-standards-navigator
- parent_title: Standards-based lifecycle navigator/control layer for factory-template
- default_context: VPS Remote SSH repo context

## Routing / маршрут
- task_class: review
- selected_profile: review
- selected_model: gpt-5.5
- selected_reasoning_effort: high
- selected_plan_mode_reasoning_effort: high
- selected_scenario: template-repo/scenario-pack/16-done-closeout.md
- model_availability: repo-configured; last catalog validation passed

## Boundary / граница
- owner_boundary: internal-repo-follow-up
- child session не наследует parent route by default.
- Уже открытая live session не считается reliable auto-switch.
- Не хранить secrets, `.env` content или private transcripts в repo artifacts.

## Артефакты для обновления
- CURRENT_FUNCTIONAL_STATE.md
- TEST_REPORT.md
- VERIFY_SUMMARY.md
- reports/orchestration/
- reports/project-lifecycle-dashboard.md

## Задача
Провести финальный review: связность стандартов, dashboard, validators, docs, generated project safety, no heavy web default, no false compliance, no false auto-switch. Обновить reports/orchestration/cockpit и reports/project-lifecycle-dashboard.md если repo flow поддерживает. Запустить git status --short --branch. Если verify green и origin/write path доступен, выполнить canonical verified sync. Финальный closeout обязан назвать commit hash/sync status или explicit blocker. Если есть внешние действия — только actionable Инструкция пользователю. Если внешних действий нет — явно сказать, что внешних действий не требуется, и назвать next boundary.

## Completion contract / правило завершения
Вернуть краткий result summary, changed files, verification commands, blockers and owner boundary.
