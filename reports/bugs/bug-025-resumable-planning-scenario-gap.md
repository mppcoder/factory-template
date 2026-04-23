# Отчет о дефекте

## Идентификатор
bug-025-resumable-planning-scenario-gap

## Краткий заголовок
Handoff указывает сценарий `release-2.5/track-b/resumable-planning`, но такой маршрут не материализован в `template-repo/scenario-pack`.

## Тип дефекта
reusable-process-defect

## Где найдено
- входной handoff для задачи `feature-planning-system`
- `template-repo/scenario-pack/manifest.yaml`
- фактическое дерево `template-repo/scenario-pack/*`

## Шаги воспроизведения
1. Открыть `template-repo/scenario-pack/00-master-router.md`.
2. Проверить дерево сценариев: `find template-repo/scenario-pack -maxdepth 4 -type f`.
3. Убедиться, что пути `release-2.5/track-b/resumable-planning` нет.

## Ожидаемое поведение
Если handoff использует named scenario, он должен существовать в scenario-pack или иметь явный alias/bridge.

## Фактическое поведение
`selected_scenario` в handoff не совпадает с текущим materialized набором сценариев.

## Evidence
- [PROJECT] `template-repo/scenario-pack/manifest.yaml` содержит только entrypoint и bundle flags.
- [PROJECT] В `template-repo/scenario-pack` отсутствует файл/папка для `release-2.5/track-b/resumable-planning`.
- [REAL] Во время задачи требуемые новые planning-артефакты пришлось вводить как remediation без scenario alias.

## Слой дефекта
factory-template

## Классификация failing layer
scenario-pack routing / naming consistency

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Route impact
Маршрут выполнения задачи не меняется; gap закрыт defect-capture и docs/tooling remediation в текущем scope.

## Временный обход
Использовать `00-master-router.md` + фактические сценарии в repo как source-of-truth до materialized alias.

## Решение / статус
fixed
