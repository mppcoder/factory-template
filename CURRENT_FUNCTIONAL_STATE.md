# Текущее функциональное состояние фабрики

## Что уже реализовано
- 3 canonical entry modes: новый проект с нуля, brownfield без репо, brownfield с репо
- генерация greenfield и brownfield проектов
- scenario-pack, `.chatgpt` и launcher
- project presets, policy presets и change classes
- defect-capture layer и feedback loop
- drift detection, patch export и safe apply для разрешенных зон
- golden examples и scaffold-only examples
- curated Sources packs, boundary-actions generator и ops-policy layer

## Что работает стабильно
- создание fresh scaffold через launcher
- явное покрытие 3 целевых вариантов входа через presets и scenario-pack
- defect-aware handoff и Codex task pack
- базовые structural validators
- release hygiene, pre-release audit и version sync checks
- автоматическая проверка `factory-template-ops-policy.yaml` и boundary-actions template

## Что работает частично
- matrix runner как единый источник истины
- полный controlled back-sync как production flow
- насыщенность scaffold-only examples
- phase-aware состав curated packs пока задается статическим policy manifest без отдельного сценарного роутинга

## Что еще не закрыто
- финальное dogfooding на реальных greenfield и brownfield проектах
- окончательная polish-фаза для runner layer и operational reports
- отдельный release-facing validator/report для curated pack quality beyond structural checks
- investigation и устранение runtime-нестабильности git sync, пока покрытой только documented workaround

## Граница core
Core включает фабрику, шаблон, versioning/documentation layer, `.chatgpt`, scenario-pack, examples и feedback loop.

## Optional layers
- workspace-packs
- domain-packs
- advisory factory ops
