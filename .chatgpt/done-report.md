# Итоговый отчёт по закрытию изменения

## Что было запрошено
- Переделать логику так, чтобы всё, что надо выгружать, лежало в одной подпапке, а служебные файлы не мешались рядом.

## Что реально сделано
- Export logic теперь кладёт все uploadable файлы в `core-hot-15/upload-to-sources/`.
- Manifest direct profile фиксирует `upload_subdir` и `upload_subdir_files`.
- Operator-facing docs и boundary template синхронизированы под subfolder-driven upload flow.

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
- Изменение состава hot-set
- Перестройка canonical archive layer

## Итог закрытия
- Для ручной загрузки в `core-hot-15` теперь достаточно открыть одну подпапку `upload-to-sources/` и загрузить всё её содержимое.
