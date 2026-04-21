# Отчет о дефекте

## Идентификатор
bug-008-deferred-completion-package-after-reminder

## Краткий заголовок
Factory-template всё ещё допускал отложенный completion package: обязательная инструкция появлялась только после напоминания пользователя.

## Где найдено
Repo: `factory-template`, completion / closeout / handoff behavior layer:

- done-closeout rules
- runbook / AGENTS
- codex-task-pack checklist

## Ожидаемое поведение
- Если change требует `## Инструкция пользователю` или source-update completion package, этот блок должен быть выдан в том же финальном ответе, где сообщается о завершении change.

## Фактическое поведение
- Даже после усиления completion package model мог появляться только после дополнительного вопроса пользователя.
- Значит правило immediate same-response completion оставалось недостаточно жёстким.

## Evidence
- [PROJECT] Реальный completion output для change `d17f33dc4e9211a6419a715207f93f6f4b68d3b4` не включил обязательный completion package в основном финальном ответе.
- [PROJECT] Инструкция была добавлена только после прямого напоминания пользователя.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Нет, потому что gap найден и закрывается в source-of-truth repo самой фабрики.

## Статус
исправлен
