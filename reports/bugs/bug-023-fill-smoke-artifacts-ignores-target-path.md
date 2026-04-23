# Отчет о дефекте

## Идентификатор
bug-023-fill-smoke-artifacts-ignores-target-path

## Краткий заголовок
`tools/fill_smoke_artifacts.py` игнорирует аргумент target path и перезаписывает `.chatgpt/*` в текущем repo root.

## Тип дефекта
reusable-process-defect

## Где найдено
- `tools/fill_smoke_artifacts.py`
- `MATRIX_TEST.sh`
- `template-repo/scripts/verify-all.sh` (full/ci path)

## Шаги воспроизведения
1. Запустить `bash MATRIX_TEST.sh` в repo root.
2. Обратить внимание на вызов `python3 tools/fill_smoke_artifacts.py "$P"`.
3. Проверить root `.chatgpt/handoff-response.md` после прогона.
4. Увидеть, что root handoff-response перезаписан smoke-template контентом.

## Ожидаемое поведение
- Скрипт должен применять заполнение только к явно переданному project path.
- Root repo не должен мутироваться побочным эффектом matrix/scaffold сценариев.

## Фактическое поведение
- Скрипт всегда использует `Path('.')` и игнорирует CLI-аргументы.
- При запуске из root в `MATRIX_TEST.sh` изменяются root `.chatgpt/*` файлы.
- Это ломает стабильность full verify path и вносит нерелевантный diff.

## Evidence
- [PROJECT] Поиск показал отсутствие чтения `sys.argv` в `tools/fill_smoke_artifacts.py`.
- [PROJECT] После `MATRIX_TEST.sh` root `.chatgpt/handoff-response.md` заменяется smoke-контентом.

## Слой дефекта
factory-template

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Route impact
Route не меняется; это test tooling defect в текущем remediation scope.

## Временный обход
Запускать скрипт только из целевой рабочей директории и не передавать path-аргумент.

## Решение / статус
fixed
