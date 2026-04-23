# Factory Feedback: make fill_smoke_artifacts target-aware and side-effect safe

## Исходный bug report
`reports/bugs/bug-023-fill-smoke-artifacts-ignores-target-path.md`

## Почему это проблема фабрики
Matrix/smoke tooling должен быть side-effect safe относительно root repo. Игнорирование target path в утилите генерации smoke artifacts приводит к ложным изменениям source-of-truth файлов и ломает reproducible verify pipeline.

## Где проявилось
- `tools/fill_smoke_artifacts.py`
- `MATRIX_TEST.sh`
- full verify path (`template-repo/scripts/verify-all.sh ci`)

## Повторяемый паттерн
- скрипт вызывается с аргументом target project;
- утилита игнорирует аргумент;
- запись идёт в cwd (часто repo root);
- появляются нецелевые изменения `.chatgpt/*` и красные проверки в конце пайплайна.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- smoke/matrix test tooling
- verify pipeline stability
- release hardening contract

## Как проверить исправление
1. `python3 tools/fill_smoke_artifacts.py <target>` пишет артефакты только в `<target>`.
2. `bash MATRIX_TEST.sh` не мутирует root `.chatgpt/*`.
3. `bash template-repo/scripts/verify-all.sh ci` стабильно проходит от clean state.

## Статус
зафиксировано
