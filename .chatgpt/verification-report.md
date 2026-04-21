# Отчёт о проверке результата

## Что проверяли
- `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh`
- `bash GENERATE_BOUNDARY_ACTIONS.sh`
- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- проверка, что `_sources-export/factory-template/core-hot-15/core-cold-5.tar.gz` существует
- проверка `_sources-export/factory-template/core-hot-15/manifest.json` на `bundled_artifacts`
- grep по `той же папке`, `core-cold-5.tar.gz`, `companion archive`
- `git diff --check`

## Что подтверждено
- `core-cold-5.tar.gz` теперь дублируется прямо в `core-hot-15/`.
- `manifest.json` фиксирует bundled artifact отдельным списком без смешивания с hot source-files.
- Docs и boundary guidance теперь явно говорят, что daily upload набор лежит в одной папке.

## Что не подтверждено или требует повторной проверки
- Архив дублируется для удобства в папке hot15, но его канонический origin по-прежнему остаётся `_sources-export/factory-template/core-cold-5.tar.gz`.

## Итоговый вывод
- Daily upload набор теперь физически лежит в одном месте: hot15 flat folder плюс companion `core-cold-5.tar.gz` в той же папке.
