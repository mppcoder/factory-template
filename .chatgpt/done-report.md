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

## Что осталось вне объёма
- Массовое применение этих правок в уже созданных downstream project repos.
- Перегенерация и раздача обновлённых exported sources/boundary artifacts для внешних контуров.

## Итог закрытия
- Для VPS layout теперь действует единое правило: в `/projects` остаются только project roots, а вся служебная brownfield-инфраструктура уходит внутрь конкретного проекта.
