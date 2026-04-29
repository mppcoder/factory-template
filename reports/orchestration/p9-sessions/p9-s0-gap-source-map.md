Язык ответа Codex: русский
Отвечай пользователю по-русски. Английский допускается только для технических идентификаторов, имен файлов, команд, YAML/TOML ключей и literal values.

# Child Codex session handoff / дочерний handoff

## Parent задача
- parent_id: p9-lifecycle-standards-navigator
- parent_title: Standards-based lifecycle navigator/control layer for factory-template
- default_context: VPS Remote SSH repo context

## Routing / маршрут
- task_class: deep
- selected_profile: deep
- selected_model: gpt-5.5
- selected_reasoning_effort: high
- selected_plan_mode_reasoning_effort: high
- selected_scenario: template-repo/scenario-pack/00-master-router.md
- model_availability: repo-configured; last catalog validation passed

## Boundary / граница
- owner_boundary: internal-repo-follow-up
- child session не наследует parent route by default.
- Уже открытая live session не считается reliable auto-switch.
- Не хранить secrets, `.env` content или private transcripts в repo artifacts.

## Артефакты для обновления
- reports/gaps/lifecycle-standards-navigator-gap.md
- docs/decisions/lifecycle-standards-stack.md

## Задача
Прочитать repo-router и lifecycle/dashboard/control artifacts. Зафиксировать gap: есть dashboard/task-state/cockpit/operator-dashboard, но нет standards-based lifecycle navigator. Создать gap report и ADR. В ADR обосновать lightweight standards stack для solo/small-company проекта: ISO/IEC/IEEE 12207 as lifecycle backbone, Scrum/Kanban-lite as rhythm, ISO 25010, NIST SSDF, OWASP ASVS, WCAG, DORA, AI-specific OpenAI safety overlay. Не заявлять certification. Если версия стандарта не подтверждена repo/current official source, зафиксировать verify-current gate.

## Completion contract / правило завершения
Вернуть краткий result summary, changed files, verification commands, blockers and owner boundary.
