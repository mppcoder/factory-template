# Factory Feedback: человекочитаемый слой factory-template должен оставаться русскоязычным

## Исходный bug report
`reports/bugs/bug-030-human-readable-language-layer-leaked-english.md`

## Почему это проблема фабрики
`factory-template` является русскоязычной фабрикой. Если generated guidance, closeout, handoff-пояснения и отчеты смешивают русский и английский без технической необходимости, operator UX деградирует, а правила проекта становятся менее явными.

## Где проявилось
`factory-template`, ответы Codex и closeout artifacts после исправления GitHub workflow.

## Повторяемый паттерн
- task выполняется в русскоязычном repo;
- technical identifiers остаются на английском;
- модель переносит английские шаблонные заголовки в человекочитаемый слой;
- пользователь получает смешанный язык в пояснениях.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- global rules
- handoff guidance
- closeout guidance
- generated boundary actions
- completion artifacts
- user-facing validator output

## Как проверить исправление
1. Человекочитаемые заголовки и инструкции в scenario-pack и generated boundary guidance написаны на русском.
2. Технические идентификаторы остаются допустимыми как literal values.
3. Новые `.chatgpt` reports и completed work records не используют английские описательные заголовки там, где есть русская замена.

## Статус
fixed
