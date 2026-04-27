# External actions closeout gap

Дата: 2026-04-27
Статус: fixed-in-current-scope
Класс: closeout / completion package defect

## Симптом

Пользовательский follow-up: "опять потерял внешние действия".

Предыдущий closeout содержал общий `## Инструкция пользователю`, но не выделил внешний contour как отдельную actionable таблицу со статусом, причиной и точным действием. В результате пользователь не получил достаточно явный список внешних действий, хотя change затронул downstream-consumed template content.

## Evidence

- `template-repo/scenario-pack/00-master-router.md` и `16-done-closeout.md` уже требуют structured completion package.
- `.chatgpt/boundary-actions.md` содержит требования к `Рекомендация по внешним действиям`.
- `template-repo/template/.chatgpt/done-checklist.md` оставался коротким downstream template checklist и не требовал перечислять каждый external contour как actionable item.
- Финальный ответ Codex по Artifact Eval Harness указал downstream sync как recommended, но не дал отдельный "external actions ledger" с `статус / причина / действие пользователя`.

## Layer classification

- advisory/policy layer: scenario-pack, done checklist, boundary-actions guidance.
- executable validation layer: `validate-codex-task-pack.py` должен проверять наличие строгого wording в generated boundary/checklist artifacts.

## Impact

Closeout можно формально считать содержащим `Инструкция пользователю`, но practically потерять внешние действия. Это ломает user-facing boundary: пользователь не понимает, что именно делать с downstream sync, ChatGPT Project instructions и legacy Sources fallback.

## Remediation

- Усилить template done checklist: completion package должен содержать "Реестр внешних действий" или эквивалентную таблицу.
- Усилить generated boundary-actions: каждый contour должен иметь `Статус`, `Причина`, `Действие пользователя`, `Когда выполнять`.
- Усилить validator для codex task pack, чтобы новые checklist/boundary artifacts не регрессировали к общему footer.
- Зафиксировать в closeout, что внешний action ledger обязателен даже когда часть contours имеет статус `не требуется`.
