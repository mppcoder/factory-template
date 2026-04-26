# FP-03: Battle brownfield with repo / реальный brownfield с repo

## Статус

- Current status: `pending`
- Evidence class: field pilot
- Result: `no-field-evidence`

## Входные условия

- Доступен real existing repo.
- В repo есть хотя бы одна meaningful project-owned area, которую нельзя overwrite.
- Operator может выполнить audit/verify commands или предоставить sanitized command results.

## Ожидаемый результат

- Repo audit summary.
- Change map and risk register.
- Protected project-owned zones identified.
- Conversion path to `greenfield-product` или documented blocker.

## Измеряемые KPI

| KPI | Pass threshold |
|---|---:|
| Project-owned protected zones identified | `100%` known live zones |
| Audit findings classified | `100%` |
| Template-owned sync candidates separated from manual/advisory changes | yes |
| Critical defects open at closeout | `0` |

## Команды / шаги

1. Прочитать `template-repo/scenario-pack/00-master-router.md`.
2. Запустить guided brownfield-with-repo path:
   `python3 template-repo/scripts/factory-launcher.py --mode brownfield --brownfield-kind modernize --guided --project-name "<real repo>" --project-slug "<slug>" --yes`
3. В pilot repo выполнить project tests и:
   `bash template-repo/scripts/verify-all.sh quick`
4. Создать или обновить audit artifacts: system inventory, repo audit, change map, risks/constraints.
5. Если conversion возможен, записать `greenfield-product` conversion evidence. Если нет, записать blocker.

## Pass criteria / критерии прохождения

- Existing repo можно audit без destructive template overwrite.
- Project-owned и template-owned zones разделены.
- Transition завершается conversion evidence или blocker, который можно review.

## Fail criteria / критерии провала

- Template sync overwrites project-owned files.
- Project не может выполнить meaningful audit/verify step и blocker не записан.
- Critical risk найден без defect capture.

## Repo artifacts to retain / сохраняемые артефакты

- Sanitized repo audit summary.
- Change map и risk register.
- Protected-zone inventory.
- Conversion или blocker summary.
