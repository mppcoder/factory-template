Язык ответа Codex: русский
Отвечай пользователю по-русски. Английский допускается только для технических идентификаторов, имен файлов, команд, YAML/TOML ключей и literal values.

# Child Codex session handoff / дочерний handoff

## Parent задача
- parent_id: p9-lifecycle-standards-navigator
- parent_title: Standards-based lifecycle navigator/control layer for factory-template
- default_context: VPS Remote SSH repo context

## Routing / маршрут
- task_class: build
- selected_profile: build
- selected_model: gpt-5.5
- selected_reasoning_effort: medium
- selected_plan_mode_reasoning_effort: medium
- selected_scenario: template-repo/scenario-pack/15-handoff-to-codex.md
- model_availability: repo-configured; last catalog validation passed

## Boundary / граница
- owner_boundary: internal-repo-follow-up
- child session не наследует parent route by default.
- Уже открытая live session не считается reliable auto-switch.
- Не хранить secrets, `.env` content или private transcripts в repo artifacts.

## Артефакты для обновления
- template-repo/scripts/check-standards-watchlist.py
- reports/standards/README.md

## Задача
Добавить lightweight offline-first standards monitoring. check-standards-watchlist.py должен проверять registry/watchlist freshness без обязательного web/network access. Если last_checked stale, выдавать warning/proposal-needed, но не менять gates. Предусмотреть future manual/live research path через standards-update-proposal. Любое изменение версии стандарта: proposal -> impact classification -> user approval -> template update.

## Completion contract / правило завершения
Вернуть краткий result summary, changed files, verification commands, blockers and owner boundary.
