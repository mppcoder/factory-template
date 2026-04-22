# Итоговый отчёт по закрытию изменения

## Что было запрошено
- Внедрить каноническое правило хранения repo-папок на VPS: `/projects` содержит только project roots, `_incoming` живёт внутри проекта, brownfield temporary/intermediate/reconstructed repos не раскладываются плоско рядом.

## Что реально сделано
- Сценарный слой получил явное canonical VPS layout rule.
- Brownfield entry и codex-assisted stabilization теперь отдельно запрещают top-level temporary/intermediate/reconstructed repos в `/projects`.
- User/operator/workspace docs переведены на project-local `_incoming` и иерархию `/projects/<project-root>/...`.
- Boundary template и generator default path синхронизированы с project-local incoming layout.
- `_boundary-actions/factory-template-boundary-actions.md` перегенерирован на новых правилах.
- Текущие `.chatgpt` артефакты обновлены под этот change.
- После выявленного process miss дополнительно оформлен defect capture:
  - `reports/bugs/bug-012-missed-verified-sync-and-user-instruction-after-closeout.md`
  - `reports/factory-feedback/feedback-012-missed-verified-sync-and-user-instruction-after-closeout.md`
- Затем выполнена remediation этого defect:
  - `check-dod.py` теперь требует successful `verified-sync-report` при настроенном `origin`
  - generated `done-checklist.md` теперь требует `VALIDATE_VERIFIED_SYNC_PREREQS.sh` -> `VERIFIED_SYNC.sh`
  - closeout rules и Codex runbook теперь явно запрещают завершение без sync или без документированного blocker
  - template closeout example обновлён под sync/user-instruction discipline

## Какие артефакты обновлены
- `.chatgpt/*` для текущего change
- `template-repo/scenario-pack/01-global-rules.md`
- `template-repo/scenario-pack/brownfield/00-brownfield-entry.md`
- `template-repo/scenario-pack/brownfield/11-codex-assisted-stabilization.md`
- `template-repo/template/docs/codex-workflow.md`
- `factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md`
- `factory_template_only_pack/README.md`
- `factory_template_only_pack/templates/factory-template-boundary-actions.template.md`
- `tools/generate_factory_template_boundary_actions.py`
- `workspace-packs/vscode-codex-dogfood-bootstrap/*`
- `factory-template.code-workspace`
- `README.md`
- `ENTRY_MODES.md`
- `docs/template-architecture-and-event-workflows.md`
- `reports/bugs/bug-012-missed-verified-sync-and-user-instruction-after-closeout.md`
- `reports/factory-feedback/feedback-012-missed-verified-sync-and-user-instruction-after-closeout.md`
- `.chatgpt/reuse-check.md`
- `.chatgpt/reality-check.md`
- `.chatgpt/evidence-register.md`
- `template-repo/scripts/check-dod.py`
- `template-repo/scripts/create-codex-task-pack.py`
- `template-repo/scripts/validate-codex-task-pack.py`
- `template-repo/process/definition-of-done.bugfix-feature-change.md`
- `template-repo/scenario-pack/16-done-closeout.md`
- `factory_template_only_pack/02-runbook-dlya-codex-factory-template.md`
- `template-repo/template/.chatgpt/examples/done-report.example.md`

## Что осталось вне объёма
- Массовое применение этих правок в уже созданных downstream project repos.
- Перегенерация и раздача обновлённых exported sources/boundary artifacts для внешних контуров.
- Отдельная remediation для pre-existing root routing/config inconsistency, из-за которой `create-codex-task-pack.py` не валидируется на самом factory root.

## Итог закрытия
- Для VPS layout теперь действует единое правило: в `/projects` остаются только project roots, а вся служебная brownfield-инфраструктура уходит внутрь конкретного проекта.
- Дополнительно factory closeout теперь жёстче защищён от “мнимого done” без verified sync и без same-response `Инструкция пользователю`.
