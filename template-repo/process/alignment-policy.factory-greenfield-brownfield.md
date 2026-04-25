# Политика выравнивания контуров

## Зачем нужен этот документ
Этот документ выравнивает три режима работы:
- доработка самой фабрики
- greenfield-проект
- brownfield-проект

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

### Factory improvement / улучшение фабрики
- feedback
- drift
- patch export
- controlled back-sync

## Правило handoff
Независимо от типа контура defect-flow должен одинаково отражаться в:
- classification.md
- bugflow-status.yaml
- reports/bugs/
- reports/factory-feedback/
- Codex task pack
