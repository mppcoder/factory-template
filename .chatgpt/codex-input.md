# Codex handoff input

## Контекст
- Repo: `factory-template`
- Нужно устранить bug в executable routing layer.
- Structured handoff мог явно просить `selected_reasoning_effort: high`, но generated `.chatgpt` artifacts фиксировали `medium`.
- Причина: router уважал keyword fallback сильнее, чем explicit handoff routing fields.

## Что должен сделать исполнитель
- Зафиксировать bug report и factory feedback для reusable routing defect.
- Обновить `template-repo/scripts/codex_task_router.py`, чтобы он читал structured handoff поля и подбирал совместимый executable profile по model/reasoning.
- Сохранить keyword fallback только как запасной путь, а не как override поверх explicit handoff.
- Подтвердить reproduce path до и после исправления.

## Ограничения
- Не делать вид, что уже открытая сессия auto-switches reasoning без нового launch boundary.
- Если requested profile из handoff не существует в routing spec, нужно подобрать совместимый executable profile и явно зафиксировать это в reasons.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.
