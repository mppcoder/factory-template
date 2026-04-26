# Потеря рекомендации по внешним действиям в closeout

## Кратко

- Дата: `2026-04-26`
- Тип: reusable process defect
- Слой: completion / boundary actions / final closeout
- Статус: fixed in this remediation

Финальный closeout после `G25-GA` содержал блок `Инструкция пользователю`, но снова потерял явную рекомендацию по внешним действиям: что именно требуется, что не требуется, что опционально и что относится только к legacy/hybrid fallback.

## Как воспроизвести

1. Завершить release-facing change, который затрагивает downstream-consumed template content.
2. Выполнить verify, sync и release executor.
3. Сформировать финальный completion package.
4. Проверить, содержит ли он только перечисление contours без явной строки `Рекомендация`.

## Ожидаемое поведение

Финальный блок `## Инструкция пользователю` должен явно давать recommendation по каждому внешнему контуру:

- factory-template ChatGPT Project instructions: `требуется` / `не требуется` + причина.
- downstream/battle repo sync: `рекомендуется` / `не требуется` / `по ситуации` + точный command path.
- downstream/battle ChatGPT Project instructions: `требуется` / `не требуется` / `только legacy/hybrid fallback` + причина.
- Sources fallback: `не требуется` / `только legacy/hybrid fallback`.

## Фактическое поведение

Closeout перечислил внешние контуры, но формулировка была слишком слабой: пользователь справедливо не получил явную recommendation matrix.

## Причина

`boundary-actions.md`, generator и validator требовали наличие completion package, но не требовали отдельного маркера `Рекомендация по внешним действиям` и не проверяли recommendation labels по ключевым внешним контурам.

## Исправление

- Усилен boundary-actions guidance.
- Усилен done checklist.
- Усилен `create-codex-task-pack.py`.
- Усилен `validate-codex-task-pack.py`, чтобы generated pack не проходил без recommendation guardrail.
