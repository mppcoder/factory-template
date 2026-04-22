# Factory Feedback: check-dod leaks parent repo origin into nested example fixtures

## Исходный bug report
`reports/bugs/bug-016-check-dod-inherits-parent-origin-for-nested-example-fixtures.md`

## Почему это проблема фабрики
Фабрика использует nested working-project examples как reference fixtures, но validator `check-dod.py` всё ещё определяет наличие `origin` по текущему cwd без проверки git top-level boundary. В результате fixture validation начинает зависеть от remote родительского repo и даёт ложные DoD failures.

## Где проявилось
`factory-template`, example fixtures внутри `working-project-examples/`.

## Повторяемый паттерн
- example/project fixture лежит внутри внешнего git repo;
- сам fixture не является отдельным git root;
- validator запускается по пути fixture;
- git возвращает remote родительского repo;
- validator ошибочно требует verified-sync-report как будто fixture был полноценным рабочим repo с собственным `origin`.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- validator layer
- example fixtures
- DoD integrity checks
- automation trust boundary

## Как проверить исправление
1. Запустить `check-dod.py` на nested example fixture внутри `working-project-examples/`.
2. Убедиться, что validator больше не требует verified-sync report только из-за `origin` родительского repo.
3. Повторно прогнать `EXAMPLES_TEST.sh` и убедиться, что прежние fixture false positives исчезли.

## Статус
зафиксировано
