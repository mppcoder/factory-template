# Итоговый отчёт по закрытию изменения

## Что было запрошено
- Пометить в `core-hot-15`, какие файлы нужно выгружать в Sources проекта, а какие не нужно.

## Что реально сделано
- Export logic теперь генерирует `UPLOAD_TO_SOURCES.txt` и `DO_NOT_UPLOAD.txt` прямо внутри `core-hot-15/`.
- Manifest direct profile фиксирует `upload_to_sources` и `do_not_upload` отдельными списками.
- Operator-facing docs и boundary template синхронизированы под marker-driven upload flow.

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
- Для ручной загрузки в `core-hot-15` теперь есть явная маркировка: что загружать в Sources и какие служебные файлы выгружать не нужно.
