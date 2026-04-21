# Глобальные правила

1. Repo — источник правды. Чат не является источником правды.
2. Нельзя переходить к реализации без нормализованных артефактов.
3. Любое решение должно быть помечено источником:
   - `[PROJECT]` — основано на текущем проекте;
   - `[FIX]` — основано на ранее подтвержденном фиксе;
   - `[DOC]` — основано на официальной документации;
   - `[REAL]` — основано на реальном кейсе;
   - `[ASSUMPTION]` — предположение.
4. Если есть конфликт между реальностью проекта и документацией, зафиксируй его отдельно.

## Правило фиксации дефектов
Любой обнаруженный дефект, регрессия, расхождение, пропущенный шаг, шаблонный сбой или reusable process failure должен быть оформлен как структурированный bug report до исправления или одновременно с ним. Silent fixes запрещены.

## Alignment Rule
Фабрика, greenfield и brownfield могут различаться по предметным шагам, но не могут различаться по правилам фиксации дефектов, handoff и completion.

Отсутствие inline Codex handoff в ответе, где handoff уже допустим и задача достаточно определена, считается reusable process defect.

Отсутствие финального блока `Инструкция пользователю` в ответе, где есть pending external/user step, считается reusable process defect.

Подмена internal repo follow-up user-only closeout'ом считается reusable process defect.

Смешение internal repo work и external boundary action без явного разделения на handoff и user footer считается reusable process defect.

Если change влияет на Sources или downstream template consumers, но completion output не различает affected contours, delete-before-replace semantics и boundary steps по окнам/папкам, это считается reusable process defect.
