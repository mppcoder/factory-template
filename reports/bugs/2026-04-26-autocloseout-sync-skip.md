# Пропуск автозавершения closeout sync

## Сводка

После зеленой проверки и исправления downstream sync v3 работа была завершена текстовым closeout без немедленного commit/push. Commit/push был выполнен только после отдельного напоминания пользователя.

## Как воспроизвести

1. Выполнить repo change в `factory-template`.
2. Получить green verification.
3. Иметь настроенный `origin` и синхронизированную ветку.
4. Завершить ответом-summary без `VERIFIED_SYNC.sh`, commit/push или явного blocker.

## Доказательства

- Перед напоминанием пользователя в рабочем дереве оставались изменения.
- `origin` был настроен на `git@github.com:mppcoder/factory-template.git`.
- После напоминания commit/push выполнился успешно: `96cc467 feat: expand downstream sync contract v3`.

## Ожидаемое поведение

Если verify green, `origin` настроен и sync технически доступен, Codex должен закрыть внутренний repo follow-up сам:

- проверить `git status --short --branch`;
- выполнить canonical sync path (`VALIDATE_VERIFIED_SYNC_PREREQS.sh` -> `VERIFIED_SYNC.sh`) или зафиксировать конкретный blocker;
- перед финальным ответом снова проверить, что branch не ahead и рабочее дерево чистое.

## Фактическое поведение

Closeout был выдан до commit/push. Пользователь был вынужден отдельно спросить, почему работа не закрыта.

## Классификация слоя

- Слой: closeout / verified sync / Codex task-pack guardrails.
- Класс дефекта: reusable process defect.
- Factory feedback: не требуется отдельно, потому что исправление вносится прямо в source-of-truth factory repo.

## Цель исправления

Сделать автозавершение проверяемым:

- усилить closeout rules;
- добавить обязательные пункты в generated `boundary-actions.md` и `done-checklist.md`;
- расширить validator task-pack, чтобы он ловил отсутствие auto-sync closeout guardrails.

## Проверка

- `python3 template-repo/scripts/validate-codex-task-pack.py .`
- `bash MATRIX_TEST.sh`
- `bash template-repo/scripts/verify-all.sh ci`
- после проверки выполнить canonical sync или явно зафиксировать blocker
