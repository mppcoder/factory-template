# Factory Feedback: completion package must default downstream ChatGPT Projects to "no" in clean repo-first mode

## Исходный bug report
`reports/bugs/bug-020-repo-first-completion-package-overstates-downstream-chatgpt-updates.md`

## Почему это проблема фабрики
Фабрика уже давно закрепила repo-first contract, где source-of-truth живет в репо, а не в Project instructions/Sources. Если completion package по умолчанию продолжает подсказывать обновление downstream ChatGPT Projects как равноправный contour, он размывает этот contract и подталкивает к лишним manual steps.

## Где проявилось
`factory-template`, source-facing closeout/completion package generator и related scenario docs.

## Повторяемый паттерн
- template change затрагивает downstream-consumed source files;
- closeout открывает standard completion package;
- contour `battle ChatGPT Projects` перечисляется без explicit default=`нет`;
- оператор читает это как нормальный default step;
- repo-first contract размывается и появляются лишние внешние действия.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- completion package rules
- handoff/closeout scenarios
- task-pack generator
- boundary-actions and done-checklist templates

## Как проверить исправление
1. Сгенерировать completion package после template change.
2. Проверить, что contour `battle ChatGPT Projects` явно помечен как `нет по умолчанию` для чистого repo-first режима.
3. Проверить, что `да` допускается только как legacy/hybrid fallback.
4. Убедиться, что финальный closeout больше не подталкивает к обновлению downstream ChatGPT Projects, если repo-first contract уже соблюдается.

## Статус
зафиксировано
