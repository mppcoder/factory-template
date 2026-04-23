# Отчет о дефекте

## Идентификатор
bug-022-generated-routing-validator-path-fragments-mismatch

## Краткий заголовок
`validate-codex-routing.py` ложно падает на generated projects из-за жёстких путей `template/docs/*` и overly-strict README fragment checks.

## Тип дефекта
reusable-process-defect

## Где найдено
Repo: `factory-template`, routing validation layer:

- `template-repo/scripts/validate-codex-routing.py`
- `SMOKE_TEST.sh`
- `MATRIX_TEST.sh`

## Шаги воспроизведения
1. Запустить `bash SMOKE_TEST.sh` в корне `factory-template`.
2. Дождаться шага `validate-codex-routing.py` для generated проекта.
3. Зафиксировать ошибку вида:
   - отсутствуют fragments в generated `README.md`;
   - не найден `template/docs/codex-workflow.md`;
   - не найден `template/docs/integrations.md`.
4. Повторить через `bash MATRIX_TEST.sh` и увидеть аналогичное падение в ветках `factory-bugflow` и `direct-task-routing`.

## Ожидаемое поведение
- Валидатор должен корректно проверять source-facing routing docs для обоих контуров:
  - canonical template repo;
  - generated working project.
- Проверка README должна учитывать валидные формулировки `manual-ui`/advisory/routing, а не только один жёсткий literal.

## Фактическое поведение
- Проверка ожидает `template/docs/*` там, где generated проект хранит документы в `docs/*`.
- README fragments проверяются слишком узко, что создаёт false-negative при эквивалентных формулировках.
- В результате `SMOKE_TEST.sh` и `MATRIX_TEST.sh` падают на корректном generated маршруте.

## Evidence
- [PROJECT] `bash SMOKE_TEST.sh` завершился ошибкой на `CODEX ROUTING НЕВАЛИДЕН`.
- [PROJECT] `bash MATRIX_TEST.sh` завершился `fail=2` по `validate-codex-routing.py`.
- [PROJECT] В generated проекте присутствуют `docs/codex-workflow.md` и `docs/integrations.md`, но отсутствует `template/docs/*`.

## Слой дефекта
factory-template

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Route impact
Route не меняется; это validator hardening в том же профиле и сценарии.

## Временный обход
Не включать `validate-codex-routing.py` в smoke/matrix или вручную игнорировать false-negative.

## Решение / статус
fixed
