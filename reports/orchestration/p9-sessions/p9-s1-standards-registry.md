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
- template-repo/standards/lifecycle-standards-registry.yaml
- template-repo/standards/standards-watchlist.yaml

## Задача
Добавить machine-readable standards registry. Включить profiles: solo_lightweight, commercial_production, custom. Для каждого standard указать role, selected_version, fallback_version where needed, update_monitoring, source verification status, applicability and false-compliance boundary. Добавить standards-watchlist для offline/manual monitoring. Не вводить network-dependent quick verify.

## Completion contract / правило завершения
Вернуть краткий result summary, changed files, verification commands, blockers and owner boundary.
