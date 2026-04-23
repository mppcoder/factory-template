# Factory Feedback: completion package must default factory-template ChatGPT Project to "no" unless instruction contract changed

## Исходный bug report
`reports/bugs/bug-021-repo-first-completion-package-overstates-factory-chatgpt-update.md`

## Почему это проблема фабрики
Repo-first contract хорош тем, что короткая Project instruction меняется редко. Если completion package по умолчанию продолжает подталкивать к обновлению `factory-template ChatGPT Project` даже без изменения repo/path/entrypoint/instruction text, он размывает границу между real instruction drift и обычным template change.

## Где проявилось
`factory-template`, source-facing closeout/completion package generator и related scenario docs.

## Повторяемый паттерн
- template change затрагивает repo files, но не instruction contract;
- closeout открывает standard completion package;
- contour `factory-template ChatGPT Project` перечисляется без explicit default=`нет`;
- оператор читает это как нормальный default step;
- появляется лишний manual step, хотя Project instruction обновлять не нужно.

## Нужна ли обратная синхронизация
да

## Какие зоны фабрики затронуты
- completion package rules
- handoff/closeout scenarios
- task-pack generator
- boundary-actions and done-checklist templates

## Как проверить исправление
1. Сгенерировать completion package после template change, не меняющего repo/path/entrypoint/instruction text.
2. Проверить, что contour `factory-template ChatGPT Project` явно помечен как `нет` по умолчанию.
3. Проверить, что `да` допускается только когда реально изменился instruction contract.
4. Убедиться, что финальный closeout больше не предлагает обновлять factory-template ChatGPT Project без фактической необходимости.

## Статус
зафиксировано
