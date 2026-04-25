# Factory feedback

## Источник
bug-031-closeout-language-and-chatgpt-handoff-drift

## Краткое описание
Closeout layer все еще может выдавать англоязычные описательные разделы и неудачно формулировать `ChatGPT Project` contour так, будто пользователю нужен новый handoff или обновление внешней инструкции.

## Reusable issue
Да.

## Предлагаемое правило
- Финальный closeout для `factory-template` должен быть русскоязычным в человекочитаемом слое.
- Технические literal values можно оставлять как есть.
- Completion package должен писать `не требуется` для незатронутых external contours и не называть это handoff.
- Proposal/report generators должны использовать русские заголовки и описания, если artifact предназначен для чтения оператором.

## Проверка
- Обновить closeout/scenario guidance.
- Обновить генератор model-routing proposal.
- Обновить текущие done/verification/proposal artifacts.
- Прогнать routing/task-pack validators и quick verify.
