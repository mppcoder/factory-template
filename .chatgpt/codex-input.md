# Codex handoff input

## Контекст
- Repo: `factory-template`
- Нужно зафиксировать новый reusable process gap: completion package был обязателен по смыслу, но реально появился только после дополнительного напоминания пользователя.
- При исполнении этого handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.

## Что должен сделать исполнитель
- Усилить process rules для immediate same-response completion.
- Обновить DoD, runbook/AGENTS и codex-task-pack checklist/validator.
- Зафиксировать defect отдельным bug report и closeout artifacts.

## Ограничения
- Не менять формат completion package заново.
- Не размывать release semantics.
- Общие рабочие инструкции применять только там, где они не противоречат repo rules и старшим системным ограничениям среды.
- Handoff для пользователя допустим только как один цельный copy-paste блок, а не как ссылка на файл или несколько фрагментов.
