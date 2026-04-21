# Отчёт о проверке результата

## Что проверяли
- `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh`
- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- проверка, что `_sources-export/factory-template/core-hot-15/UPLOAD_TO_SOURCES.txt` и `DO_NOT_UPLOAD.txt` существуют
- проверка `_sources-export/factory-template/core-hot-15/manifest.json` на `upload_to_sources` и `do_not_upload`
- grep по `UPLOAD_TO_SOURCES.txt`, `DO_NOT_UPLOAD.txt`, `что загружать`, `что не загружать`
- `git diff --check`

## Что подтверждено
- `core-hot-15` теперь явно маркирует uploadable и non-uploadable файлы.
- `manifest.json` фиксирует `upload_to_sources` и `do_not_upload` отдельными списками.
- Docs и boundary guidance теперь ссылаются на marker-файлы, а не заставляют пользователя гадать по содержимому папки.

## Что не подтверждено или требует повторной проверки
- Marker-файлы отражают текущее содержимое export-папки; при будущих изменениях состава hot-set валидатор должен оставаться источником правды.

## Итоговый вывод
- Внутри `core-hot-15` теперь явно видно, что загружать в Sources, а какие служебные файлы выгружать не нужно.
