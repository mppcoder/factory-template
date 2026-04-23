# Отчет о дефекте

## Идентификатор
bug-020-repo-first-completion-package-overstates-downstream-chatgpt-updates

## Краткий заголовок
Completion package слишком широко трактовал contour `downstream/battle ChatGPT Projects` и по умолчанию подталкивал к обновлению Project instructions даже там, где downstream уже давно работает в чистом repo-first режиме.

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
1. Выполнить change, который затрагивает template source files и completion package.
2. Сформировать финальный closeout по текущим source rules.
3. Прочитать contour `Нужно ли обновлять repo-first инструкции battle ChatGPT Projects`.
4. Увидеть, что completion layer слишком легко тянет generic answer `да`, хотя repo уже работает в чистом repo-first режиме и instructions берутся из репо.

## Ожидаемое поведение
- Для чистого repo-first режима downstream ChatGPT Projects по умолчанию должны получать ответ `нет`.
- `Да` допустимо только для legacy/hybrid fallback, где Project instructions или Sources еще содержат дублированный source layer вне репо.
- Completion package должен явно разделять:
  - canonical repo-first path;
  - optional legacy/hybrid fallback.

## Фактическое поведение
- Source-facing completion package оставлял contour `battle ChatGPT Projects` слишком generic.
- Это создавало ложное ожидание, что обновление downstream ChatGPT Project instructions является нормальным default step даже в чистом repo-first режиме.
- В результате closeout мог выходить более широким, чем фактический impact change.

## Evidence
- [PROJECT] Root `AGENTS.md` и `template-repo/AGENTS.md` уже фиксируют repo-first contract и materialized clone model.
- [PROJECT] Root `README.md` прямо говорит, что refresh `Sources` не является default path и допустим только как compatibility fallback для legacy/hybrid проектов.
- [PROJECT] При этом completion-layer templates и generator по-прежнему перечисляли contour `battle ChatGPT Projects` без явного default=`нет` для чистого repo-first режима.

## Слой дефекта
factory-template

## Связь с текущим scope
fixed-in-current-scope

## Self-handoff решение
current-route-valid

## Route impact
Текущий route не меняется; это completion-layer/docs defect внутри того же template scope.

## Временный обход
До исправления оператор мог вручную интерпретировать contour как `нет`, если downstream уже живет в чистом repo-first режиме, но шаблон не подсказывал это достаточно явно.

## Решение / статус
fixed
