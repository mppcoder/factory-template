# Закрытие: greenfield-product

## Критерии завершения

- Active profile: `greenfield-product`.
- Active mode: `greenfield`.
- Старт проекта прошел через ChatGPT Project шаблона фабрики: новый чат -> `новый проект` -> scenario-pack опрос -> generated Codex handoff.
- Codex создал и synced боевой repo или documented blocker.
- Codex подготовил готовую repo-first instruction для ChatGPT Project боевого проекта.
- Пользователь создал ChatGPT Project боевого проекта в UI.
- Пользователь вставил готовую repo-first instruction.
- Дальнейшие задачи по боевому проекту идут через его собственный ChatGPT Project.
- Factory-template ChatGPT Project остается каналом создания/обновления проектов, а не постоянным каналом работы внутри каждого боевого проекта.
- External actions ledger содержит только реальные external/manual/runtime/downstream действия.

## Внешние действия

Пользователь нужен только для:

- команды `новый проект` и ответов на опрос в ChatGPT Project шаблона фабрики;
- вставки generated handoff в Codex;
- создания/изменения ChatGPT Project боевого проекта в UI;
- вставки готовой repo-first instruction;
- внешних approvals, secrets, GitHub UI blockers или real deploy/release decisions.

Если таких действий нет, closeout пишет: `Внешних действий не требуется.`
