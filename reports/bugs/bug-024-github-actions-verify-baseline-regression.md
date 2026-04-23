# Отчет о дефекте

## Идентификатор
bug-024-github-actions-verify-baseline-regression

## Краткий заголовок
`CI / verify-baseline` падал в GitHub Actions на шаге `EXAMPLES_TEST` из-за недетерминированной зависимости versioning-валидатора от внешнего `rg`.

## Тип дефекта
reusable-process-defect

## Где найдено
- `.github/workflows/ci.yml` (`verify-baseline` -> `bash template-repo/scripts/verify-all.sh ci`)
- `EXAMPLES_TEST.sh`
- `template-repo/scripts/validate-versioning-layer.py`

## Шаги воспроизведения
1. Открыть failed run `24839250094` (commit `6322b8e0e6605572a6f01a1ee8370b1f92746d77`).
2. В job `verify-baseline` (`72708173547`) посмотреть шаг `Run consolidated verification`.
3. Увидеть, что внутри `verify-all.sh ci` падает `EXAMPLES_TEST`:
   - `example-change-small-fix | validate-versioning-layer.py | FAIL`
   - `example-change-brownfield-audit | validate-versioning-layer.py | FAIL`
   - `example-change-end-to-end | validate-versioning-layer.py | FAIL`
4. Локально воспроизвести тот же паттерн, если `rg` недоступен/ломается в окружении validator-а:
   - подменить `rg` shim-скриптом с non-zero exit;
   - запустить `bash EXAMPLES_TEST.sh`;
   - получить те же 3 FAIL на `validate-versioning-layer.py`.

## Ожидаемое поведение
- Versioning-валидатор должен быть детерминированным и независимым от наличия/версии внешнего `rg`.
- При падении проверок CI должен показывать диагностику конкретного failing чекера, а не только агрегированный `FAIL`.

## Фактическое поведение
- Валидатор использовал shell + `rg` для проверки кириллицы.
- В `EXAMPLES_TEST.sh` stdout/stderr конкретного чекера были подавлены (`>/dev/null 2>&1`), поэтому root cause из CI-лога не читался.
- В итоге `verify-baseline` падал с `exit code 1`, а `release-bundle-dry-run` пропускался по `needs: verify-baseline`.

## Evidence
- [REAL] GitHub Actions run `24839250094`, job `72708173547`: `EXAMPLES TEST НЕ ПРОЙДЕН`, `неуспешных=3`, `Process completed with exit code 1`.
- [PROJECT] В `EXAMPLES_TEST.sh` проверка запускалась как `timeout 40s "$SCRIPTS/$chk" "$ROOT/$ex" >/dev/null 2>&1`.
- [PROJECT] Локальная симуляция недоступного `rg` воспроизводит идентичный профиль отказа (ровно 3 FAIL на `validate-versioning-layer.py`).

## Слой дефекта
factory-template

## Классификация failing layer
verify pipeline -> examples regression gate -> versioning validator runtime dependency

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Route impact
Route не меняется: `release-hardening` / `defect-capture/ci-regression-triage` / `verify-regression`.

## Временный обход
Установить/чинить `rg` в runner-среде и отдельно прогонять `validate-versioning-layer.py` с ручной диагностикой.

## Решение / статус
fixed
