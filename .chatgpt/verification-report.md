# Отчёт о проверке результата

## Что проверяли
- `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh`
- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- проверка, что `_sources-export/factory-template/core-hot-15/upload-to-sources/` существует
- проверка корня `_sources-export/factory-template/core-hot-15/` на отсутствие uploadable файлов
- проверка `_sources-export/factory-template/core-hot-15/manifest.json` на `upload_subdir` и `upload_subdir_files`
- grep по `upload-to-sources`
- `git diff --check`

## Что подтверждено
- `core-hot-15` теперь физически разделяет uploadable и служебные файлы.
- `manifest.json` фиксирует `upload_subdir` и `upload_subdir_files`.
- Docs и boundary guidance теперь отправляют пользователя прямо в одну подпапку `upload-to-sources/`.

## Что не подтверждено или требует повторной проверки
- При будущих изменениях состава hot-set нужно сохранять flat layout внутри `upload-to-sources/` без вложенных подпапок.

## Итоговый вывод
- Внутри `core-hot-15` больше не нужно угадывать, что загружать: всё для Sources лежит в одной подпапке `upload-to-sources/`.
