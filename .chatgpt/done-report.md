# Итоговый отчёт по закрытию изменения

## Что было запрошено
- Добавить архив `core-cold-5.tar.gz` в ту же папку `core-hot-15`.

## Что реально сделано
- Export logic теперь дублирует ready-to-upload `core-cold-5.tar.gz` прямо в папку `core-hot-15/`.
- Manifest direct profile фиксирует bundled artifact отдельно от hot source-files.
- Operator-facing docs и boundary template синхронизированы под one-folder daily upload flow.

## Какие артефакты обновлены
- `.chatgpt/*` для текущего change
- `tools/export_factory_template_sources.py`
- `tools/validate_factory_template_ops_policy.py`
- `docs/releases/sources-pack-usage.md`
- `factory_template_only_pack/04-chatgpt-project-sources-factory-template-20-cap.md`
- `factory_template_only_pack/templates/factory-template-boundary-actions.template.md`
- `README.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`

## Что осталось вне объёма
- Изменение состава hot-set
- Перестройка canonical archive layer

## Итог закрытия
- Для ручной загрузки весь daily набор теперь лежит в одной папке `core-hot-15/`: 15 hot-файлов плюс `core-cold-5.tar.gz`.
