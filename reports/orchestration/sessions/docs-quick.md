Язык ответа Codex: русский
Отвечай пользователю по-русски. Английский допускается только для технических идентификаторов, имен файлов, команд, YAML/TOML ключей и literal values.

# Child Codex session handoff / дочерний handoff

## Parent задача
- parent_id: p5-fixture-parent
- parent_title: VPS Remote SSH-first orchestration fixture
- default_context: VPS Remote SSH repo context

## Routing / маршрут
- task_class: quick
- selected_profile: quick
- selected_model: gpt-5.4-mini
- selected_reasoning_effort: low
- selected_plan_mode_reasoning_effort: medium
- selected_scenario: template-repo/scenario-pack/14-docs-normalization.md
- model_availability: repo-configured; last catalog validation passed

## Boundary / граница
- owner_boundary: internal-repo-follow-up
- child session не наследует parent route by default.
- Уже открытая live session не считается reliable auto-switch.
- Не хранить secrets, `.env` content или private transcripts в repo artifacts.

## Артефакты для обновления
- docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md

## Задача
Проверить русскоязычный operator wording и default VPS Remote SSH-first boundary.

## Completion contract / правило завершения
Вернуть краткий result summary, changed files, verification commands, blockers and owner boundary.
