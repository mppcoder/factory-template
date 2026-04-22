# Evidence Register

- [PROJECT] `reports/bugs/bug-012-missed-verified-sync-and-user-instruction-after-closeout.md` фиксирует реальный process miss: change был локально закрыт до canonical verified sync и без same-response user instruction.
- [PROJECT] `.factory-runtime/reports/verified-sync-report.yaml` существует и показывает, что canonical sync path уже умеет делать `pushed`/`success`; проблема была не в отсутствии механизма, а в closeout discipline.
- [PROJECT] `template-repo/scripts/check-dod.py` до remediation не проверял наличие successful verified sync report при настроенном `origin`.
- [PROJECT] `template-repo/scripts/create-codex-task-pack.py` до remediation не включал в generated `done-checklist.md` обязательные пункты про `VALIDATE_VERIFIED_SYNC_PREREQS.sh`, `VERIFIED_SYNC.sh` и same-response `## Инструкция пользователю`.
- [FIX] После remediation `check-dod.py`, `definition-of-done`, `done-closeout` и generated checklist теперь явно блокируют нечестный closeout без verified sync или без documented blocker.
