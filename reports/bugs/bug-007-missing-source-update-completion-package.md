# Отчет о дефекте

## Идентификатор
bug-007-missing-source-update-completion-package

## Краткий заголовок
Factory-template не требовал канонический completion package после изменений, затрагивающих repo-first instruction updates и downstream template consumers.

## Где найдено
Repo: `factory-template`, reusable completion / handoff / boundary-actions layer:

- scenario-pack
- done/closeout semantics
- codex-task-pack generation and validation
- boundary-actions guidance

## Ожидаемое поведение
- Если completed change затрагивает content, который потом обновляется через repo-first ChatGPT Project instruction или downstream template sync, completion output должен явно различать affected contours.
- Для manual replacement должны быть указаны delete-before-replace semantics.
- Для downstream repo sync и repo-first instruction refresh должны быть указаны готовые артефакты, команды и пошаговая маршрутизация по окнам.

## Фактическое поведение
- Существовал общий footer `Инструкция пользователю`, но без обязательного completion package для factory ChatGPT Project instruction, downstream repo sync и battle ChatGPT Project instructions.
- Manual replacement и delete-before-replace semantics могли оставаться неявными.

## Evidence
- [PROJECT] Router, done-closeout и runbook требовали footer для внешних шагов, но не требовали трёхконтурный completion package для repo-first instruction update contours.
- [PROJECT] codex-task-pack generation/validation не требовал impact model и repo-first instruction specific sections.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Нет, потому что gap найден и закрывается в source-of-truth repo самой фабрики.

## Статус
исправлен
