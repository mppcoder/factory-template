# Отчет о дефекте

## Идентификатор
bug-004-verified-sync-and-release-automation-gap

## Краткий заголовок
Factory-template не имел нормализованного production-grade verified sync и separate release automation path.

## Где найдено
Repo: `factory-template`, reusable process / automation layer:

- git sync workflow
- release decision workflow
- release publication workflow

## Ожидаемое поведение
- После successful verify repo должен уметь детерминированно выполнить commit/push проверенного состояния.
- Release/no-release decision должен оставаться отдельным явным контуром.
- После `decision=release` tag/release path должен выполняться автоматически или завершаться explicit fallback report.

## Фактическое поведение
- В repo был только documented manual/semi-manual protocol.
- Verified sync и release publication не были оформлены как нормализованные reusable scripts с validators и reports.
- Release path зависел от ручных внешних шагов без явного runtime fallback artifact.

## Evidence
- [PROJECT] В repo отсутствовали dedicated verified sync и release executor scripts.
- [PROJECT] `docs/operator/factory-template/*` и `VERIFY_SUMMARY.md` фиксировали только manual последовательность git-команд и fallback push workaround.
- [PROJECT] `RELEASE_NOTE_TEMPLATE.md` и release-facing docs описывали operator steps, но не reusable automation contour.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Нет, потому что gap найден и исправляется прямо в source-of-truth repo фабрики.

## Статус
исправляется
