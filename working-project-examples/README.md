# Примеры рабочих проектов

## Статусы примеров
- scaffold-only — стартовая структура, не обязана проходить полный контур валидации
- golden-example — эталонный пример, обязан проходить полный контур валидации

## Как они валидируются
- `golden-example` проверяются каноническими validator-ами из `template-repo/scripts/`
- локальная папка `scripts/` внутри примеров не является обязательной частью example contract
- это делает `working-project-examples/` content fixtures для проверки совместимости с актуальным template layer

| Пример | Статус | VERSION | CHANGELOG | CURRENT_FUNCTIONAL_STATE |
|---|---|---|---|---|
| example-greenfield-project | scaffold-only | да | да | да |
| example-brownfield-project | scaffold-only | да | да | да |
| example-brownfield-saas | scaffold-only | да | да | да |
| example-brownfield-legacy-app | scaffold-only | да | да | да |
| example-brownfield-openclaw | scaffold-only | да | да | да |
| example-change-small-fix | golden-example | да | да | да |
| example-change-brownfield-audit | golden-example | да | да | да |
| example-change-end-to-end | golden-example | да | да | да |
