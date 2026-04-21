# Отчет о дефекте

## Идентификатор
bug-007-missing-source-update-completion-package

## Краткий заголовок
Factory-template не требовал канонический source-update completion package после изменений, затрагивающих Sources и downstream template consumers.

## Где найдено
Repo: `factory-template`, reusable completion / handoff / boundary-actions layer:

- scenario-pack
- done/closeout semantics
- codex-task-pack generation and validation
- boundary-actions guidance

## Ожидаемое поведение
- Если completed change затрагивает content, который потом обновляется через ChatGPT Project Sources или downstream template sync, completion output должен явно различать affected contours.
- Для manual replacement должны быть указаны delete-before-replace semantics.
- Для downstream repo sync и Sources refresh должны быть указаны готовые артефакты, команды и пошаговая маршрутизация по окнам.

## Фактическое поведение
- Существовал общий footer `Инструкция пользователю`, но без обязательного completion package для factory Sources, downstream repo sync и battle ChatGPT Project Sources.
- Manual replacement и delete-before-replace semantics могли оставаться неявными.

## Evidence
- [PROJECT] Router, done-closeout и runbook требовали footer для внешних шагов, но не требовали трёхконтурный source-update completion package.
- [PROJECT] codex-task-pack generation/validation не требовал impact model и source-update specific sections.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Нет, потому что gap найден и закрывается в source-of-truth repo самой фабрики.

## Статус
исправлен
