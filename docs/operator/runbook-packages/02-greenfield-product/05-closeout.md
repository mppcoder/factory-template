# Закрытие: greenfield-product

## Критерии завершения

- Active profile: `greenfield-product`.
- Active mode: `greenfield`.
- Старт проекта прошел через ChatGPT Project шаблона фабрики: новый чат -> `новый проект` -> выбор default-decision mode -> recommendation-first опрос -> generated Codex handoff.
- Handoff содержит `default_decision_mode`, accepted defaults, overrides, unresolved decisions/blockers и no hidden forced defaults for risky actions.
- Codex создал и synced боевой repo или documented blocker.
- Codex подготовил готовую repo-first instruction для ChatGPT Project боевого проекта.
- Codex подготовил пошаговую инструкцию пользователю, куда вставить этот текст.
- Если пользователь должен копировать generated repo-first instruction, Codex выдал готовый fenced code block в финальном ответе; ссылка на файл не заменяет copy block.
- Внешние UI-шаги оформлены как диалоговый сценарий: цель, окно, подробные шаги, варианты с рекомендацией, ожидаемый результат и что прислать обратно.
- Пользователь создал ChatGPT Project боевого проекта в UI.
- Пользователь открыл Project settings/instructions.
- Пользователь вставил готовую repo-first instruction.
- Пользователь сохранил настройки.
- Дальнейшие задачи по боевому проекту идут через его собственный ChatGPT Project.
- Factory-template ChatGPT Project остается каналом создания/обновления проектов, а не постоянным каналом работы внутри каждого боевого проекта.
- External actions ledger содержит только реальные external/manual/runtime/downstream действия.
- Boundary wording: Codex готовит repo-first instruction для боевого ChatGPT Project. Пользователь создает ChatGPT Project в UI и вставляет готовый текст.

## Внешние действия

Пользователь нужен только для:

- команды `новый проект`, выбора default-decision mode и ответов на recommendation-first опрос в ChatGPT Project шаблона фабрики;
- вставки generated handoff в Codex;
- создания ChatGPT Project боевого проекта в UI;
- открытия Project settings/instructions, вставки готовой repo-first instruction и сохранения настроек;
- внешних approvals, secrets, GitHub UI blockers или real deploy/release decisions.

Если таких действий нет, closeout пишет: `Внешних действий не требуется.`
Если такие действия есть, closeout завершает ответ разделом `## Инструкция пользователю` и выдает весь текст для копирования прямо в fenced code blocks.
