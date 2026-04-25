# Отчет о дефекте

## Идентификатор
bug-031-closeout-language-and-chatgpt-handoff-drift

## Краткий заголовок
Финальный closeout снова смешал английский человекочитаемый слой и создал ощущение handoff обратно в ChatGPT.

## Тип дефекта
reusable-process-defect

## Где найдено
- Финальный ответ Codex пользователю после feature 16.
- `.chatgpt/done-report.md`.
- `.chatgpt/verification-report.md`.
- `reports/model-routing/model-routing-proposal.md`.
- Генератор `template-repo/scripts/check-codex-model-catalog.py`.

## Шаги воспроизведения
1. Завершить repo-first задачу в `factory-template`.
2. Сформировать completion package для изменения, затрагивающего downstream-consumed template слой.
3. Использовать англоязычные описательные заголовки вроде `What Changed`, `Model-Routing Policy`, `Completion Package`, `Known limitation`.
4. Упомянуть `ChatGPT Project` без явной формулировки, что новый handoff или обновление инструкции не требуется.

## Ожидаемое поведение
- Финальный человекочитаемый closeout пишется на русском языке.
- Английский остается только для технических идентификаторов, команд, файлов, YAML/JSON ключей, model IDs и literal values.
- Completion package явно говорит: требуется ли действие, не создавая впечатление handoff обратно в ChatGPT.
- Если repo/path/entrypoint/instruction contract не менялись, ответ должен прямо сказать: обновление `factory-template ChatGPT Project` не требуется.

## Фактическое поведение
- Финальный ответ содержал англоязычные описательные разделы.
- Формулировки про `ChatGPT Project` выглядели как внешний handoff/следующий шаг, хотя фактически action не требовался.
- Часть repo artifacts, созданных в рамках feature 16, также осталась с англоязычными описательными текстами.

## Evidence
- [REAL] Пользовательский сигнал: "почему опять хэндофф в чатгпт и здесь все на английском?"
- [PROJECT] `.chatgpt/done-report.md` содержал англоязычные описательные строки.
- [PROJECT] `.chatgpt/verification-report.md` содержал англоязычные описательные строки.
- [PROJECT] `reports/model-routing/model-routing-proposal.md` был с английскими заголовками.

## Слой дефекта
factory-template

## Классификация failing layer
completion package / language layer / generated proposal artifact

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Решение / статус
fixed
