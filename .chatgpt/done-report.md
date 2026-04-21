# Итоговый отчёт по закрытию изменения

## Что было запрошено
- Нормализовать hot15 Sources export так, чтобы все source-файлы для ChatGPT Project складывались в одну flat-папку без подпапок.

## Что реально сделано
- `core_hot_direct` переведен на канонический flat layout через declarative manifest и export logic.
- Добавлена deterministic naming strategy `basename_unless_conflict_then_path_joined_with_double_underscore` без silent overwrite.
- Operator-facing docs и boundary template синхронизированы под flat hot15 folder.

## Какие артефакты обновлены
- `.chatgpt/*` для текущего change
- `packaging/sources/sources-profiles.yaml`
- `tools/export_factory_template_sources.py`
- `tools/validate_factory_template_ops_policy.py`
- `docs/releases/sources-pack-usage.md`
- `factory_template_only_pack/04-chatgpt-project-sources-factory-template-20-cap.md`
- `factory_template_only_pack/templates/factory-template-boundary-actions.template.md`
- `README.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`

## Что осталось вне объёма
- Перестройка cold/archive export
- Изменение состава hot-set

## Итог закрытия
- Для ручной загрузки hot15 в ChatGPT Project теперь используется одна flat-папка без подпапок; docs и export layer больше не расходятся.
