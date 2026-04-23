# Factory Feedback: stabilize verify-baseline versioning gate and surface checker diagnostics

## Исходный bug report
`reports/bugs/bug-024-github-actions-verify-baseline-regression.md`

## Почему это проблема фабрики
Versioning validator входит в reusable baseline (`template-repo/scripts/*`) и используется в factory verify path для шаблона и downstream-примеров. Зависимость от внешнего `rg` делала gate environment-sensitive, а подавление stderr в `EXAMPLES_TEST` скрывало root cause в CI.

## Где проявилось
- GitHub Actions: `CI / verify-baseline` (run `24839250094`, job `72708173547`)
- `EXAMPLES_TEST.sh` (агрегированный table-only FAIL без деталей)
- `template-repo/scripts/validate-versioning-layer.py` (runtime-зависимость от `rg`)

## Повторяемый паттерн
- В CI падает ровно `validate-versioning-layer.py` на всех golden examples.
- Подробная причина не видна в pipeline output из-за `>/dev/null 2>&1`.
- Зависимость от утилиты среды вместо self-contained validator logic приводит к false-red verify-baseline.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- verify pipeline reliability
- examples gate observability
- release hardening baseline

## Как проверить исправление
1. `bash EXAMPLES_TEST.sh` проходит в стандартной среде.
2. `bash EXAMPLES_TEST.sh` сохраняет pass по `validate-versioning-layer.py` даже при подмене `rg` shim-скриптом с ошибкой.
3. При намеренном падении любого checker-а `EXAMPLES_TEST.sh` показывает diagnostic block `[DETAIL]`.
4. `bash template-repo/scripts/verify-all.sh ci` проходит.
5. GitHub Actions `CI / verify-baseline` и зависимый `CI / release-bundle-dry-run` становятся зелёными.

## Статус
зафиксировано
