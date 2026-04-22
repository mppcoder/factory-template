# Отчет о дефекте

## Идентификатор
bug-014-verified-sync-stale-task-index-commit-message

## Краткий заголовок
`VALIDATE_VERIFIED_SYNC_PREREQS.sh` может пропустить post-done non-lightweight diff и предложить commit message из stale `task-index.yaml`.

## Где найдено
Repo: `factory-template`, verified-sync automation layer:

- `template-repo/scripts/factory_automation_common.py`
- `template-repo/scripts/validate-verified-sync-prereqs.py`
- `template-repo/scripts/verified-sync.py`

Сценарий: после завершения одной задачи внутри уже открытого repo выполняется новый internal follow-up change без обновления `.chatgpt/task-index.yaml`.

## Шаги воспроизведения
1. Иметь repo в состоянии `stage.current = done` и валидный green verify baseline от предыдущего change.
2. Оставить в `.chatgpt/task-index.yaml` metadata предыдущего change.
3. Внести новый non-lightweight diff в scenario-pack / process / `.chatgpt` artifacts, но не обновлять `.chatgpt/task-index.yaml`.
4. Запустить `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`.
5. Наблюдать, что prereqs проходят и печатают `commit_message`, собранный из старого `change.title`.

## Ожидаемое поведение
- Post-done non-lightweight verified sync не должен доверять stale metadata от предыдущего change.
- Если новый diff не обновил `.chatgpt/task-index.yaml`, automation должна остановиться с явным blocker.
- Commit/push не должны продолжаться с сообщением от другого change.

## Фактическое поведение
- `resolve_sync_plan()` переходил в full mode.
- `validate_verify_prereqs()` брал `change.title` из существующего `.chatgpt/task-index.yaml` без проверки его свежести относительно текущего diff.
- В результате prereqs печатали commit message от предыдущей задачи: `fix: Canonicalize VPS project-root layout under /projects`, хотя текущий diff относился к incidental defect handling.

## Evidence
- [PROJECT] Во время closeout после change `fix: require incidental defect self-handoff and closeout routing` `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh` вывел:
  - `mode: full`
  - `change_id: chg-20260422-001`
  - `commit_message: fix: Canonicalize VPS project-root layout under /projects`
- [PROJECT] Текущий diff в тот момент содержал изменения в:
  - `template-repo/scenario-pack/00-master-router.md`
  - `template-repo/scenario-pack/12-bug-analysis.md`
  - `template-repo/scenario-pack/15-handoff-to-codex.md`
  - `template-repo/scenario-pack/16-done-closeout.md`
  - `.chatgpt/*`
- [PROJECT] `.chatgpt/task-index.yaml` и `.chatgpt/codex-task-pack.md` оставались от предыдущего VPS layout change.

## Затронутый слой
factory-template

## Нужен ли feedback в фабрику
Да, потому что это reusable automation defect в source-of-truth repo: verified-sync metadata layer позволял wrong commit intent при post-done follow-up.

## Статус
зафиксировано
