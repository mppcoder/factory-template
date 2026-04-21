# Техническая спецификация

## Архитектура
- Process layer должен требовать source-update completion package, когда change затрагивает downstream-consumed content.
- Lightweight impact model живет в существующем boundary policy и done-checklist, а не в новом тяжёлом subsystem.
- Codex task pack generation/validation должен проверять наличие impact model, source-update sections, delete-before-replace и repo-level sync script references.

## Impact Model
- `impact.factory_sources`
- `impact.downstream_template_sync`
- `impact.downstream_project_sources`
- `impact.manual_archive_required`
- `impact.delete_before_replace`

## Boundary Actions
- Boundary template должен перечислять affected contours, downloadable artifacts, repo-level sync scripts и window-by-window instructions.
- Если contour не затронут, это должно быть сказано явно.
