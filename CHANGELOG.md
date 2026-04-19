# Журнал изменений фабрики

## [Unreleased] - 2026-04-19
### Добавлено
- профиль `brownfield-dogfood-codex-assisted` для dogfood-сценария brownfield without repo
- класс изменения `brownfield-stabilization` с поддержкой `hybrid` и `codex-led`
- шаблонные `.codex` конфиги и подагенты для автоматического переключения режимов внутри одной живой сессии
- workspace pack `vscode-codex-dogfood-bootstrap` для старта из одного окна VS Code с дальнейшим переходом на отдельные окна по проектам
- декларативный `factory-template-ops-policy.yaml` для curated Sources packs и boundary-actions settings
- validator `VALIDATE_FACTORY_TEMPLATE_OPS.sh` / `tools/validate_factory_template_ops_policy.py`

### Изменено
- launcher теперь предлагает новый профиль и новый класс изменения
- policy preset и scenario-pack расширены под evidence-first → stabilization → reconstructed repo → clean package flow
- curated Sources packs и boundary-actions generator теперь собираются из policy/template слоя, а не из хардкода
- `PRE_RELEASE_AUDIT.sh`, `SMOKE_TEST.sh` и `MATRIX_TEST.sh` теперь учитывают ops-policy validator


## [2.4.0] - 2026-04-16
### Изменено
- подтвержден полный release-gate набор на чисто распакованном архиве: smoke, examples и matrix
- стабилизационный smoke-fix включен в основной финальный пакет
- release metadata переведены из `2.4.0-rc2` в финальную `2.4.0`

### Исправлено
- устранено зависание packaged `SMOKE_TEST.sh` за счет детерминированного наполнения smoke-артефактов через `tools/fill_smoke_artifacts.py`
- финальный архив и внутренний root-folder синхронизированы по имени `factory-v2.4.0`

## [2.4.0-rc2] - 2026-04-15
### Изменено
- синхронизированы version/release ссылки между root, template, meta-template и working examples
- `RELEASE_BUILD.sh` переведен на вычисление версии из `VERSION.md`
- `PRE_RELEASE_AUDIT.sh` усилен проверками version drift и legacy-ссылок

### Исправлено
- устранен legacy-id `factory-v2.3.9-alignment-layer` в build-слое
- template launcher больше не генерирует устаревший `2.4.0-versioning-layer`
- golden examples синхронизированы и по `.chatgpt/project-origin.md`, чтобы `validate-versioning-layer.sh` проходил на rc2

## [2.4.0-rc1-consistency] - 2026-04-15
### Добавлено
- единый versioning/documentation layer для фабрики, шаблона и generated projects
- валидатор `validate-versioning-layer.sh`
- стандартные `VERSION.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`

### Изменено
- launcher теперь создает versioning layer в generated project
- examples синхронизированы с актуальной версией фабрики

### Исправлено
- устранено расхождение между текущей версией фабрики и `project-origin.md` в template/examples
