# Закрытие: factory-template

## Критерии завершения

- User-runbook останавливается на takeover point, а не заставляет пользователя вручную выполнять Codex automation.
- Codex-runbook берет на себя install/clone/bootstrap/verify/dashboard/sync после remote context.
- Checklist является зеркалом пользовательских шагов `FT-000`..`FT-180` и не содержит process/meta checks.
- Verify разделен на user readiness до takeover и Codex automation после takeover.
- Targeted/quick verify green или documented blocker.
- `CURRENT_FUNCTIONAL_STATE.md`, `CHANGELOG.md` и `RELEASE_NOTES.md` обновлены, если change release-facing.
- Source/export manifests обновлены, если новые operator docs должны входить в curated/reference packs.
- Перед финалом выполнен `git status --short --branch`.
- При доступном verified sync указан commit hash / sync status.

## Внешние действия

Если внешних действий нет, финал должен явно сказать:

```text
Внешних действий не требуется.
```

Если есть external UI, secrets, release approval или protected-branch blocker, финал завершать разделом `## Инструкция пользователю` с точными окнами и шагами.
