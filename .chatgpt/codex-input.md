# Codex handoff input

## Контекст
- Repo: `factory-template`
- Нужно внедрить каноническое правило обработки incidental / side bugs, найденных во время исполнения основного handoff.
- Нельзя silently drop такой баг в конце основной задачи.
- Нельзя делать вид, что текущая уже открытая Codex-сессия надежно auto-switches profile/model/reasoning для нового побочного бага.

## Что должен сделать исполнитель
- Обновить scenario-pack, process/policy слой, `.chatgpt` guidance и шаблоны bug/handoff/closeout.
- Добавить decision tree:
  - bug fixed in current scope;
  - bug unresolved but same route;
  - bug unresolved and different route;
  - bug requires deep research.
- Зафиксировать обязательные outputs:
  - structured bug report;
  - self-handoff for the new bug;
  - explicit wording for recommended new Codex task when route changes;
  - explicit fallback wording for continuing in current chat;
  - ChatGPT-ready deep research bug report/prompt when investigation is needed.
- Встроить это в closeout/completion package, чтобы incidental defects не терялись в финальном ответе.

## Ограничения
- Не утверждать, что advisory scenario text сам переключает уже открытую live-сессию.
- Надежная единица rerouting — только новый task launch.
- Fallback `continue in this chat anyway` допустим только как явно помеченный non-canonical path.
- Приоритет у правил repo: `AGENTS`, runbook, scenario-pack и policy files репозитория.
