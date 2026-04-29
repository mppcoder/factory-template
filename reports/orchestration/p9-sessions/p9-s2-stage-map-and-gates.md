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
- template-repo/standards/lifecycle-stage-map.yaml
- template-repo/template/.chatgpt/standards-gates.yaml

## Задача
Добавить lifecycle-stage-map.yaml, связывающий phases idea, discovery/intake, feasibility/reality-check, product requirements, quality requirements, architecture/design, implementation, security review, accessibility/UX review, testing/verification, release readiness, deployment, operate/monitor, maintenance/updates, growth/monetization readiness if applicable, incident response, deprecation/retirement. Для каждой phase указать purpose, required artifacts, gates, applied standards, solo profile checks, commercial profile checks, evidence required, dashboard mapping, owner_boundary. Добавить standards-gates.yaml template for generated projects: gate status, standard_refs, required_for_profile, evidence, accepted_reason, owner_boundary, false_green_policy.

## Completion contract / правило завершения
Вернуть краткий result summary, changed files, verification commands, blockers and owner boundary.
