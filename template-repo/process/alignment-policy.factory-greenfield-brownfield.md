# Политика выравнивания контуров

## Зачем нужен этот документ
Этот документ выравнивает один lifecycle core для трех ownership/transition контуров:
- доработка самой фабрики как `greenfield-product` проекта с factory producer layer
- greenfield-продукт
- brownfield transition существующего проекта к `greenfield-product`

## Общее обязательное правило
Во всех контурах:
- найденный дефект оформляется через bug report
- дефект классифицируется как `project-only`, `factory-template` или `shared-unknown`
- reusable-дефект требует factory feedback
- silent fixes запрещены
- задача не считается done, если найденный defect исправлен без bug report

## Что может различаться
### Greenfield / новый проект
- bootstrap
- user spec
- tech spec
- decomposition

### Brownfield / существующий проект
- reverse engineering
- system inventory
- gap register
- remediation planning
- mandatory conversion to `greenfield-product` or documented blocker

### Factory improvement / улучшение фабрики
- feedback
- drift
- patch export
- controlled back-sync
- factory-producer-owned layer excluded from battle project sync

## Правило handoff
Независимо от типа контура defect-flow должен одинаково отражаться в:
- classification.md
- bugflow-status.yaml
- reports/bugs/
- reports/factory-feedback/
- Codex task pack
