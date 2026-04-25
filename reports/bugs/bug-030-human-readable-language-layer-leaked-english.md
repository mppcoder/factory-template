# Отчет о дефекте

## Идентификатор
bug-030-human-readable-language-layer-leaked-english

## Краткий заголовок
В русскоязычном человекочитаемом слое появились английские описательные заголовки и фразы.

## Тип дефекта
reusable-process-defect

## Где найдено
- Ответы Codex пользователю после PR closeout.
- `.chatgpt/verification-report.md`.
- `.chatgpt/done-report.md`.
- `.chatgpt/boundary-actions.md`.
- `work/completed/chg-20260425-actions-workflow-backlog.md`.
- Generated boundary guidance в `template-repo/scripts/create-codex-task-pack.py`.
- User-facing output в `template-repo/scripts/validate-operator-env.py`.

## Шаги воспроизведения
1. Выполнить задачу в `factory-template`, где repo profile language is `ru`.
2. Сформировать self-handoff, closeout или report.
3. Использовать англоязычные шаблонные заголовки и описательные фразы там, где есть нормальная русская замена.
4. Пользователь получает смешанный язык в инструкциях и отчетах.

## Ожидаемое поведение
- Все человекочитаемые ответы, инструкции, отчеты, описания, closeout и handoff-пояснения для `factory-template` пишутся на русском языке.
- Английский остается только там, где он является техническим идентификатором: команда, имя файла, ключ YAML/JSON, GitHub field, branch, commit, action, model или literal value.

## Фактическое поведение
- В ответах и repo artifacts были использованы английские описательные заголовки и фразы без технической необходимости.
- Пользователь отдельно указал, что тексты и описания должны быть только на русском.

## Evidence
- [REAL] Пользовательский сигнал: "есть правило все тексты и описания тоолько на русском".
- [PROJECT] `.chatgpt/verification-report.md` содержал англоязычные описательные строки.
- [PROJECT] `.chatgpt/done-report.md` содержал англоязычные описательные строки.
- [PROJECT] `.chatgpt/boundary-actions.md` содержал англоязычные описательные заголовки.
- [PROJECT] `validate-operator-env.py` печатал англоязычные описательные сообщения в text output.

## Слой дефекта
factory-template

## Классификация failing layer
language / completion artifacts / generated guidance

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Решение / статус
fixed
