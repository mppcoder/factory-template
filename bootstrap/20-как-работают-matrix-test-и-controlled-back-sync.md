# Как работают MATRIX TEST и controlled back-sync

## MATRIX TEST
`MATRIX_TEST.sh` — главный сводный раннер стабилизационного релиза.
Он проверяет fresh scaffold, golden examples и контур factory bugflow.

## Controlled back-sync
Back-sync в версии 2.3.6 работает по манифесту безопасных зон.

### Safe apply
Safe apply допускается только для `sync_zones` из `factory-sync-manifest.yaml`.

### Advisory only
Для `advisory_only_zones` фабрика собирает patch bundle и summary, но не применяет изменения автоматически.
