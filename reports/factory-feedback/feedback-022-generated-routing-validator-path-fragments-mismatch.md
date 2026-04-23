# Factory Feedback: normalize routing validator for template and generated repos

## Исходный bug report
`reports/bugs/bug-022-generated-routing-validator-path-fragments-mismatch.md`

## Почему это проблема фабрики
Routing validator обязан быть reusable для canonical template repo и для generated working project. Жёсткая привязка к `template/docs/*` и узкие README literals делают validator хрупким и создают ложные падения в smoke/matrix контуре.

## Где проявилось
- `template-repo/scripts/validate-codex-routing.py`
- `SMOKE_TEST.sh`
- `MATRIX_TEST.sh`

## Повторяемый паттерн
- generated проект содержит корректные routing docs в `docs/*`;
- validator ищет только `template/docs/*`;
- эквивалентные README формулировки не распознаются;
- routing check краснеет без реальной маршрутной деградации.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- routing validators
- smoke/matrix verification baseline
- release hardening verification contract

## Как проверить исправление
1. `bash SMOKE_TEST.sh` проходит без false-negative на routing validator.
2. `bash MATRIX_TEST.sh` зелёный на шагах `validate-codex-routing.py`.
3. `python3 template-repo/scripts/validate-codex-routing.py .` остаётся зелёным для текущего repo.
4. Валидатор всё ещё ловит реальные пропуски required routing docs/fragments.

## Статус
зафиксировано
