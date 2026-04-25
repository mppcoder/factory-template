# Как работают MATRIX TEST и controlled back-sync

## MATRIX TEST
`MATRIX_TEST.sh` — главный сводный раннер стабилизационного релиза.
Он проверяет fresh scaffold, golden examples и контур factory bugflow.

## Controlled back-sync
Back-sync работает по tiered manifest безопасных и preview-only зон.

### Safe apply
Safe apply допускается только для tier `safe` из `factory-sync-manifest.yaml`.

### Advisory
Для tier `advisory` фабрика собирает patch bundle и summary, но не применяет изменения автоматически.

### Manual only
Для tier `manual-only` фабрика показывает impact preview, но не генерирует файлы для automatic apply.
