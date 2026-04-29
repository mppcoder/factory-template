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
- template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml
- template-repo/scripts/render-project-lifecycle-dashboard.py
- template-repo/scripts/validate-project-lifecycle-dashboard.py

## Задача
Расширить lifecycle dashboard: показывать selected standards profile, lifecycle backbone version/status, standards gate summary, current phase required standards, missing standards evidence, next safe standards action, standards monitoring status, allowed_to_advance_phase. Validator должен падать на: phase advanced without gates, production/commercial claim without production profile gates, security/accessibility/quality passed without evidence or accepted_reason, AI app ready without AI safety gate, stale standard_version but dashboard says current, compliance/certification claim without evidence.

## Completion contract / правило завершения
Вернуть краткий result summary, changed files, verification commands, blockers and owner boundary.
