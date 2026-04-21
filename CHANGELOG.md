# Журнал изменений фабрики

## [Unreleased]
### Добавлено
- отдельный contour `VERIFIED_SYNC.sh` для auto commit/push после successful verify
- отдельный contour `EXECUTE_RELEASE_DECISION.sh` для tag/release path только после явного release decision
- validators для verified sync prereqs, release decision, release notes source и publish outcome
- lightweight follow-up mode для `VERIFIED_SYNC.sh`, чтобы low-risk post-verify `.gitignore` и docs/closeout изменения тоже коммитились и пушились автоматически
- internal-followup precedence rule: user footer больше не должен вытеснять inline handoff, если remaining work еще остается внутренней Codex-eligible работой repo
- completion/handoff layer теперь требует source-update completion package для factory Sources, downstream repo sync и battle ChatGPT Project Sources, когда change затрагивает downstream-consumed content
- immediate completion-package rule: обязательная инструкция пользователю должна быть в том же финальном ответе, а не после напоминания пользователя
- completion package больше не должен перекладывать на пользователя внутренние prepare/export команды; такие шаги выполняет Codex до финального ответа
- удалён legacy staging-sync contour для `core-hot-15/upload-to-sources/`
- удалены repo-side wrapper/validator/scripts, завязанные на внешний staging-sync
- `.env.example` для безопасной конфигурации folder URL и sync intent без секретов в repo
- удалены project-level drive config и placeholder-validator из generated projects
- launcher больше не требует внешний URL при создании проекта
- `POST_UNZIP_SETUP.sh` больше не требует внешнюю конфигурацию staging-контура
- repo полностью переведён на repo-first режим для ChatGPT Projects
- handoff source files и validator `validate-codex-task-pack.sh` усилены явным правилом: при формировании handoff в Codex приоритет у правил repo
- handoff format rule усилен: пользователю нельзя выдавать handoff ссылкой на файл или несколькими блоками, только одним цельным copy-paste блоком
- добавлен validator `template-repo/scripts/validate-handoff-response-format.sh` для проверки готового handoff markdown-ответа на single-block и anti-file-based rules

### Изменено
- release-facing слой зафиксировал factory-template defect remediation из `a9b05c0` без смены release semantics
- `CURRENT_FUNCTIONAL_STATE.md` и release notes теперь явно отражают обязательный inline Codex handoff при допустимом handoff и достаточной определенности задачи
- root `.chatgpt` и template `.chatgpt` теперь несут release decision templates и closeout artifacts для sync/release automation
- direct hot-set `core-hot-15` теперь экспортируется как одна flat-папка без подпапок, с deterministic naming strategy при конфликтах имён
- `core-cold-5.tar.gz` теперь дублируется прямо в папке `core-hot-15/` как companion archive для ручной загрузки
- `core-hot-15` теперь физически разделяет uploadable и служебные файлы: всё для Sources лежит в `upload-to-sources/`
- export manifest теперь публикует детерминированные checksum metadata для hot export и bundled artifacts, чтобы compare layer мог строить `create/update/delete/skipped` план без эвристики только по mtime
- docs и completion layer теперь явно различают Codex connector contour для Drive folder и отдельный внешний шаг обновления ChatGPT Project Sources

### Исправлено
- устранен reusable process gap, из-за которого ChatGPT мог остановиться на аналитике вместо готового handoff
- устранен reusable process gap, из-за которого ответ мог завершаться без финального блока `Инструкция пользователю` при pending user/external step
- подтверждено, что автопубликация релиза не добавлялась и existing release discipline сохранена

## [2.4.2] - 2026-04-20
### Добавлено
- declarative manifest `packaging/sources/sources-profiles.yaml` для archive/direct Sources profiles
- direct Sources profile `core-hot-15` для ежедневной работы в ChatGPT Project
- usage doc `docs/releases/sources-pack-usage.md` для hybrid-схемы `direct hot-set + canonical archive`

### Изменено
- export Sources теперь строит и canonical archive packs, и direct hot-set из одного источника правды
- boundary-actions и summary теперь рекомендуют `core-hot-15` как постоянный direct Sources set
- `sources-pack-core-20` явно закреплён как canonical archive snapshot, а не как единственный ежедневный способ загрузки

## [2.4.1] - 2026-04-20
### Добавлено
- профиль `brownfield-dogfood-codex-assisted` для dogfood-сценария brownfield without repo
- класс изменения `brownfield-stabilization` с поддержкой `hybrid` и `codex-led`
- шаблонные `.codex` конфиги и подагенты для автоматического переключения режимов внутри одной живой сессии
- workspace pack `vscode-codex-dogfood-bootstrap` для старта из одного окна VS Code с дальнейшим переходом на отдельные окна по проектам
- декларативный `factory-template-ops-policy.yaml` для curated Sources packs и boundary-actions settings
- validator `VALIDATE_FACTORY_TEMPLATE_OPS.sh` / `tools/validate_factory_template_ops_policy.py`
- validator `template-repo/scripts/validate-codex-task-pack.sh` для generated Codex handoff pack
- semantic checks для `sources-pack-core-20`, `sources-pack-release-20` и `sources-pack-bugfix-20` внутри `tools/validate_factory_template_ops_policy.py`
- phase-aware recommendation matrix для `controlled-fixes`, `release` и `bugfix-drift` внутри `factory-template-ops-policy.yaml`
- automatic phase detection helper `DETECT_FACTORY_TEMPLATE_PHASE.sh` / `tools/factory_template_phase_detection.py`
- composite release-intent detection через checked markers в `RELEASE_CHECKLIST.md`
- bugfix-intent detection через document signals в `reports/bugs/*.md`
- synthetic self-test `PHASE_DETECTION_TEST.sh` для `controlled-fixes / release / bugfix-drift`

### Изменено
- launcher теперь предлагает новый профиль и новый класс изменения
- policy preset и scenario-pack расширены под evidence-first → stabilization → reconstructed repo → clean package flow
- curated Sources packs и boundary-actions generator теперь собираются из policy/template слоя, а не из хардкода
- `PRE_RELEASE_AUDIT.sh`, `SMOKE_TEST.sh` и `MATRIX_TEST.sh` теперь учитывают ops-policy validator
- feedback ingest теперь явно фиксирует режим `validated` / `allow-incomplete` в `incoming-learnings/INDEX.md`
- `create-codex-task-pack.sh` теперь корректно подхватывает `active_scenarios` и `scenario_pack.entrypoint` из `active-scenarios.yaml`
- `sources-pack-release-20` теперь ориентирован на release-facing docs, а `sources-pack-bugfix-20` включает feedback/handoff validators
- `SUMMARY.md` и boundary-actions guide теперь публикуют текущую phase recommendation и матрицу выбора pack'ов
- phase recommendation теперь вычисляется из `git` changed paths и policy rules, а не переключается вручную через `current_phase`
- `release` phase теперь требует не только release-path changes, но и document intent signals из checklist
- `bugfix-drift` phase теперь требует не только bug/validator path changes, но и document intent signals из bug reports
- `PRE_RELEASE_AUDIT.sh` теперь включает synthetic phase detection self-test

### Исправлено
- `tools/ingest_factory_feedback.py` больше не падает на runtime `NameError` при запуске validator перед ingest
- `MATRIX_TEST.sh` теперь проверяет feedback validator и dry-run ingest path на generated project
- очищены шумовые backlog/incoming-learning записи, появившиеся из placeholder feedback
- `boundary-actions.md` больше не теряет route line из-за чтения неверного ключа `active-scenarios.yaml`


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
