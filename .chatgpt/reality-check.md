# Reality Check

## Что подтверждено в проекте
- Repo `factory-template` уже содержит canonical `VERIFIED_SYNC.sh`, `VALIDATE_VERIFIED_SYNC_PREREQS.sh` и runtime report layer в `.factory-runtime/reports/`.
- В scenario-pack и runbook уже есть явные правила про обязательный `## Инструкция пользователю` и запрет deferred completion package.
- Реальный miss воспроизвёлся не из-за отсутствия правил, а из-за недостаточно жёсткого closeout enforcement.

## Какие расхождения найдены
- `check-dod.py` раньше не требовал successful `verified-sync-report` даже при настроенном `origin`.
- Generated `done-checklist.md` раньше не фиксировал обязательную связку `VALIDATE_VERIFIED_SYNC_PREREQS.sh` -> `VERIFIED_SYNC.sh`.
- Template closeout examples и closeout rule layer не делали omission of available verified sync отдельным reusable process defect.

## Что это означает
- Проблема находится в closeout/validation discipline, а не в отсутствии automation contour.
- Для remediation нужно усиливать существующие validator/checklist/rule layers, а не изобретать новый sync path.

## Предварительный вывод
- Исправление должно блокировать `done` без successful verified sync report при доступном `origin`.
- Исправление должно отдельно закреплять, что same-response `## Инструкция пользователю` и verified sync являются частью честного closeout.
