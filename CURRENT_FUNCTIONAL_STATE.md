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
- router / policy / handoff layer больше не допускает purely-analytic ответ вместо готового Codex handoff, если handoff уже допустим и задача достаточно определена
- финальный блок `Инструкция пользователю` теперь канонически обязателен для pending external/user steps
- базовые structural validators
- release hygiene, pre-release audit и version sync checks
- автоматическая проверка `factory-template-ops-policy.yaml` и boundary-actions template
- feedback loop с проверкой качества `meta-feedback` до ingest и matrix-покрытием dry-run ingest path
- codex handoff pack с автоматической проверкой `codex-context.md`, `codex-task-pack.md`, `boundary-actions.md` и `done-checklist.md`
- curated Sources packs с semantic validation по профилям `core / release / bugfix`, а не только по cap=20 и существованию файлов
- phase-aware recommendation layer для выбора `sources-pack-*` в `controlled-fixes / release / bugfix-drift`
- automatic phase detection из `git`-состояния для выбора рекомендованного `sources-pack-*`

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
