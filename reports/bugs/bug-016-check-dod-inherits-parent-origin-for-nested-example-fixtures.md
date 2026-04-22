# Отчет о дефекте

## Идентификатор
bug-016-check-dod-inherits-parent-origin-for-nested-example-fixtures

## Краткий заголовок
`check-dod.py` считает nested example fixture проектом с настроенным `origin`, если он лежит внутри внешнего git repo, и из-за этого ложно требует `verified-sync-report`.

## Где найдено
Repo: `factory-template`, validator layer:

- `template-repo/scripts/check-dod.py`
- `working-project-examples/example-change-small-fix`
- `working-project-examples/example-change-brownfield-audit`
- `working-project-examples/example-change-end-to-end`

## Шаги воспроизведения
1. Запустить `python3 template-repo/scripts/check-dod.py working-project-examples/example-change-small-fix`.
2. Убедиться, что fixture находится внутри корневого git repo `factory-template`, но сам не является отдельным git root.
3. Наблюдать, что validator всё равно считает `origin` настроенным и требует `.factory-runtime/reports/verified-sync-report.yaml`.

## Ожидаемое поведение
- `check-dod.py` должен требовать verified sync только если проверяемый `ROOT` сам является git repo root или отдельным рабочим repo с собственным `origin`.
- Nested example fixtures внутри внешнего monorepo не должны наследовать remote родительского repo как свой собственный.

## Фактическое поведение
- `git remote get-url origin` выполняется из cwd nested fixture.
- Git возвращает remote родительского repo.
- `check-dod.py` считает, что у fixture есть `origin`, и валится на отсутствии локального verified-sync report.

## Evidence
- [PROJECT] `python3 template-repo/scripts/check-dod.py working-project-examples/example-change-small-fix` -> `DOD НЕ ПРОЙДЕН` и сообщение `при настроенном origin требуется .factory-runtime/reports/verified-sync-report.yaml`.
- [PROJECT] `git -C working-project-examples/example-change-small-fix rev-parse --show-toplevel` возвращает `/projects/factory-template`, а не путь самого fixture.
- [PROJECT] `EXAMPLES_TEST.sh` из-за этого показывает `FAIL` на `check-dod.py` для всех трех example-change fixtures.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Да, потому что это reusable validator defect в source-of-truth repo: nested fixture validation accidentally depends on parent repo remote state.

## Статус
зафиксировано
