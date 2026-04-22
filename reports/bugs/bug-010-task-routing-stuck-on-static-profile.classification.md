# Классификация дефекта

## Идентификатор дефекта
bug-010-task-routing-stuck-on-static-profile

## Тип дефекта
factory-template

## Почему выбран этот тип
Дефект находится в source-of-truth логике самой фабрики: routing promises, template config, scenario-pack, codex-facing artifacts и launcher layer расходятся между собой и создают неверное ожидание downstream-проектам.

## Требуется ли factory feedback
да

## Требуется ли ChatGPT handoff
нет

## Требуется ли Codex исправление
да

## Можно ли закрыть задачу без этих шагов
нет
