# Отчет о дефекте

## Идентификатор
bug-021-repo-first-completion-package-overstates-factory-chatgpt-update

## Краткий заголовок
Completion package слишком широко трактовал contour `factory-template ChatGPT Project` и по умолчанию подталкивал к обновлению Project instructions даже там, где canonical repo, entrypoint и короткая repo-first инструкция не менялись.

## Тип дефекта
reusable-process-defect

## Где найдено
Repo: `factory-template`, completion/handoff closeout layer:

- `template-repo/scenario-pack/00-master-router.md`
- `template-repo/scenario-pack/15-handoff-to-codex.md`
- `template-repo/scenario-pack/16-done-closeout.md`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- generated `.chatgpt/boundary-actions.md`
- generated `.chatgpt/done-checklist.md`

## Шаги воспроизведения
1. Выполнить template change, не меняющий canonical repo, scenario entrypoint и саму короткую repo-first instruction для `factory-template` ChatGPT Project.
2. Сформировать completion package.
3. Прочитать contour `Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project`.
4. Увидеть, что completion layer слишком легко подразумевает `да`, хотя реальный impact на Project instructions отсутствует.

## Ожидаемое поведение
- Для `factory-template ChatGPT Project` canonical default должен быть `нет`, если не менялись:
  - canonical repo;
  - repo/path setting;
  - entrypoint `00-master-router.md`;
  - короткая repo-first instruction text.
- `Да` допустимо только если один из этих элементов реально изменился.

## Фактическое поведение
- Completion package оставлял contour `factory-template ChatGPT Project` слишком generic.
- Это создавало ложное ожидание, что почти любой template change требует ручного обновления Project instructions.
- В результате closeout мог рекомендовать лишний внешний шаг без фактического изменения instruction contract.

## Evidence
- [PROJECT] Root `README.md` уже фиксирует конкретную repo-first instruction для `factory-template`: `mppcoder/factory-template` + `template-repo/scenario-pack/00-master-router.md`.
- [PROJECT] В текущем small-fix change эти поля не менялись.
- [PROJECT] При этом completion-layer templates и generator по-прежнему перечисляли contour `factory-template ChatGPT Project` без explicit default=`нет`, если instruction contract не тронут.

## Слой дефекта
factory-template

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Route impact
Route не меняется; это completion/docs defect внутри того же template scope.

## Временный обход
До исправления оператор мог вручную интерпретировать contour как `нет`, если instruction contract не менялся, но шаблон не подсказывал это явно.

## Решение / статус
fixed
