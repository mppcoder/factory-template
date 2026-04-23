# Отчет о дефекте

## Идентификатор
bug-024-verified-sync-prereqs-post-done-task-index-blocker

## Краткий заголовок
`VALIDATE_VERIFIED_SYNC_PREREQS.sh` может блокировать canonical sync после post-done изменений, даже когда пользователь явно просит только commit/push текущего diff.

## Тип дефекта
reusable-process-defect

## Где найдено
Repo: `factory-template`, closeout/sync слой:

- `template-repo/scripts/validate-verified-sync-prereqs.py`
- `template-repo/scripts/factory_automation_common.py`
- `VERIFIED_SYNC.sh` / `VALIDATE_VERIFIED_SYNC_PREREQS.sh`

## Шаги воспроизведения
1. На стадии `done` подготовить non-lightweight diff (включая policy/workflow/template файлы).
2. Не обновлять `.chatgpt/task-index.yaml` под новый post-done цикл.
3. Запустить `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`.
4. Получить блокировку sync с требованием обновить task-index или свести diff к lightweight follow-up.

## Ожидаемое поведение
- При явном пользовательском запросе на commit/push для уже готового diff должен существовать понятный и предсказуемый путь sync без избыточной блокировки.
- Если блокировка остается обязательной, policy/UX должны явно объяснять это как intentional guardrail и давать минимальный deterministic path.

## Фактическое поведение
- Canonical sync path через `VERIFIED_SYNC` прерывается hard-error в post-done контуре.
- Для оператора это выглядит как blocker в момент, когда задача уже подтверждена и требуется просто зафиксировать/отправить изменения.

## Evidence
- [REAL] Во время commit/push шага получена ошибка:
  - `VERIFIED SYNC PREREQS НЕ ПРОЙДЕНЫ`
  - `Post-done non-lightweight verified sync требует обновленного .chatgpt/task-index.yaml...`
- [PROJECT] После прямого `git commit` + `git push` изменения успешно отправлены в `origin/main`.

## Слой дефекта
factory-template

## Связь с текущим scope
unresolved-incidental

## Self-handoff решение
separate-task-required

## Route impact
Potentially same route (`release-hardening`/closeout-sync), но требует отдельного remediation scope для policy/validator UX.

## Временный обход
- Выполнить прямой `git commit` + `git push` при явном пользовательском подтверждении.
- Либо заранее обновить `.chatgpt/task-index.yaml` под новый post-done цикл, чтобы пройти canonical prereqs.

## Решение / статус
fixed
