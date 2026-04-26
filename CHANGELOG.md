# Журнал изменений фабрики

## [Unreleased]

## [2.5.0] - 2026-04-26
### Добавлено
- canonical `template-repo/codex-model-routing.yaml` для mapping task class -> selected_profile -> selected_model/reasoning/plan-mode reasoning
- `check-codex-model-catalog.py` с live check через `codex debug models`, JSON output, proposal generation и safe snapshot refresh
- model-routing proposal artifact для controlled review новых Codex/OpenAI models
- full-KPI evidence layer для `G25-GA`: `docs/releases/2.5-ga-kpi-evidence.md`, controlled pilot checklist, downstream safe-sync report и handoff rework register
- `validate-25-ga-kpi-evidence.py`, подключенный к verify/audit контуру

### Изменено
- completion/handoff routing layer в template source теперь требует явный `Launch в Codex` boundary и launcher command для нового task launch
- resolver, launcher, validators и handoff generation теперь сохраняют `selected_plan_mode_reasoning_effort` и live catalog status
- docs теперь различают repo-configured mapping, live Codex catalog, ручной выбор в VS Code picker и optional strict launcher profile selection
- release-facing docs переведены в `2.5.0 GA Ready` после добавления измеримых KPI evidence
- versioning layer, manifests, launcher metadata и generated project factory-version strings синхронизированы под `2.5.0`

### Исправлено
- устранено ложное ожидание, что новый Codex chat сам переключает profile/model/reasoning без явного launcher path
- validators честно предупреждают, когда live catalog unavailable, и падают в strict mode только по явному запросу
- зафиксирован и исправлен `bug-031`: closeout больше не должен использовать англоязычные человекочитаемые headings или звучать как handoff обратно в ChatGPT, если внешний action не требуется
- зафиксирован и исправлен `bug-032`: upstream ChatGPT-generated handoff теперь проверяется на русский человекочитаемый слой через repo validator
- исправлен `bug-033`: active source-facing человекочитаемый слой очищен от английских headings, добавлены documented archival exceptions и validator в quick verify
- закрыт GA blocker `reports/bugs/2026-04-26-25-ga-readiness-gap.md`: `G25-GA` теперь валидируется измеримыми KPI для `M25-01`..`M25-08`

## [2.4.4] - 2026-04-22
### Добавлено
- отдельный optional/reference contour `optional-domain-packs/` для domain-specific reference-cases вне canonical core tree
- compatibility alias map для legacy preset names в `template-repo/project-presets.yaml` и runtime preset application
- универсальный workspace pack `workspace-packs/vscode-codex-bootstrap` вместо release-facing dogfood naming

### Изменено
- canonical entry naming приведён к нейтральным factory names: `greenfield-product`, `brownfield-without-repo`, `brownfield-with-repo-*`
- `README.md`, `ENTRY_MODES.md`, `docs/template-architecture-and-event-workflows.md`, manifests и template metadata теперь описывают одну и ту же универсальную иерархию
- `openclaw` вынесен из core/release-facing слоя в optional domain reference contour
- examples, bootstrap docs, runbooks и matrix/smoke routing синхронизированы с новым canonical naming

### Исправлено
- устранён release-facing drift между docs tree, manifests и фактической структурой optional/core слоёв
- устранён stale smoke-task контекст в root `.chatgpt` closeout/handoff артефактах перед новым релизом
- `CLEAN_VERIFY_ARTIFACTS.sh` теперь удаляет `.factory-runtime`, чтобы pre-release audit не падал на stale runtime reports
- automation layer `VERIFIED_SYNC` и release checks теперь корректно обрабатывают non-ASCII git paths через NUL-safe status parsing

## [2.4.3] - 2026-04-22
### Добавлено
- root-level `RELEASE_NOTES.md` как канонический источник публикуемых release notes и release executor notes source
- полный release-facing reference package по `factory-template`: функционал, архитектура, дерево проекта и ключевые workflows
- явное описание workflow `intake / classification`, `scenario routing`, `defect-capture`, `handoff`, `self-handoff`, `remediation`, `verification`, `release-followup`, `completion package`, `incidental bugs` и `release`
- release bundle artifacts и source/export manifests, синхронизированные с новым release-facing пакетом

### Изменено
- `docs/template-architecture-and-event-workflows.md` расширен до канонического reference-doc вместо частично обзорной заметки
- `README.md`, `CURRENT_FUNCTIONAL_STATE.md`, `VERIFY_SUMMARY.md`, `TEST_REPORT.md` и release checklist выровнены под один release-facing канон
- `RELEASE_NOTE_TEMPLATE.md` теперь является шаблоном подготовки следующего релиза, а не вторым опубликованным источником истины
- `sources-pack-release-20` теперь включает `RELEASE_NOTES.md` как часть канонического release-facing набора
- versioning layer и template/meta manifests синхронизированы под `2.4.3`

### Исправлено
- закрыт release-facing gap: в root repo отсутствовал канонический `RELEASE_NOTES.md`
- устранено дублирование роли release notes между draft-template и фактическим notes source
- `.chatgpt` closeout artifacts больше не описывают прошлый bugfix и синхронизированы с текущим release task

## [2.4.2] - 2026-04-20
### Добавлено
- отдельный contour `VERIFIED_SYNC.sh` для auto commit/push после successful verify
- отдельный contour `EXECUTE_RELEASE_DECISION.sh` для tag/release path только после явного release decision
- validators для verified sync prereqs, release decision, release notes source и publish outcome
- lightweight follow-up mode для `VERIFIED_SYNC.sh`, чтобы low-risk post-verify `.gitignore` и docs/closeout изменения тоже коммитились и пушились автоматически
- executable task router для Codex на границе новой задачи: `template-repo/codex-routing.yaml`, `resolve-codex-task-route.py`, `bootstrap-codex-task.py`, `launch-codex-task.sh`
- named profiles `quick / build / deep / review` и launch logging в `.chatgpt/task-launch.yaml`
- normalised routing artifacts `.chatgpt/normalized-codex-handoff.md`, `.chatgpt/direct-task-self-handoff.md` и visible direct-task response block `.chatgpt/direct-task-response.md`
- единый reference-doc `docs/template-architecture-and-event-workflows.md` с визуальной архитектурой шаблона и подробными workflows по ключевым событиям
- internal-followup precedence rule: user footer больше не должен вытеснять inline handoff, если remaining work еще остается внутренней Codex-eligible работой repo
- completion/handoff layer теперь требует completion package для factory ChatGPT Project instruction, downstream repo sync и battle ChatGPT Project instructions, когда change затрагивает downstream-consumed content
- immediate completion-package rule: обязательная инструкция пользователю должна быть в том же финальном ответе, а не после напоминания пользователя
- completion package больше не должен перекладывать на пользователя внутренние prepare/export команды; такие шаги выполняет Codex до финального ответа
- удалён legacy staging-sync contour для `core-hot-15/upload-to-sources/`
- удалены repo-side wrapper/validator/scripts, завязанные на внешний staging-sync
- `.env.example` для безопасной конфигурации folder URL и sync intent без секретов в repo
- удалены project-level drive config и placeholder-validator из generated projects
- launcher больше не требует внешний URL при создании проекта
- `POST_UNZIP_SETUP.sh` больше не требует внешнюю конфигурацию staging-контура
- repo полностью переведён на repo-first режим для ChatGPT Projects
- handoff source files и validator `validate-codex-task-pack.py` усилены явным правилом: при формировании handoff в Codex приоритет у правил repo
- handoff format rule усилен: пользователю нельзя выдавать handoff ссылкой на файл или несколькими блоками, только одним цельным copy-paste блоком
- добавлен validator `template-repo/scripts/validate-handoff-response-format.py` для проверки готового handoff markdown-ответа на single-block и anti-file-based rules

### Изменено
- release-facing слой зафиксировал factory-template defect remediation из `a9b05c0` без смены release semantics
- `CURRENT_FUNCTIONAL_STATE.md` и release notes теперь явно отражают обязательный inline Codex handoff при допустимом handoff и достаточной определенности задачи
- root `.chatgpt` и template `.chatgpt` теперь несут release decision templates и closeout artifacts для sync/release automation
- advisory layer и executable routing layer теперь явно разделены в runbooks, scenario-pack, template docs и Codex task pack artifacts
- direct task to Codex теперь обязан сначала проходить self-handoff по тем же routing fields и defect gates, что и handoff из ChatGPT Project
- direct task response layer теперь требует visible self-handoff block до remediation, а smoke/pre-release checks дополнительно это прикрывают
- direct hot-set `core-hot-15` теперь экспортируется как одна flat-папка без подпапок, с deterministic naming strategy при конфликтах имён
- `core-cold-5.tar.gz` теперь дублируется прямо в папке `core-hot-15/` как companion archive для ручной загрузки
- `core-hot-15` теперь физически разделяет uploadable и служебные файлы: всё для Sources лежит в `upload-to-sources/`
- export manifest теперь публикует детерминированные checksum metadata для hot export и bundled artifacts, чтобы compare layer мог строить `create/update/delete/skipped` план без эвристики только по mtime
- docs и completion layer теперь явно различают internal export/reference contour и отдельный внешний шаг обновления ChatGPT Project instruction

### Исправлено
- устранен reusable process gap, из-за которого ChatGPT мог остановиться на аналитике вместо готового handoff
- устранен reusable process gap, из-за которого ответ мог завершаться без финального блока `Инструкция пользователю` при pending user/external step
- устранен defect, из-за которого task-based выбор модели/режима оставался advisory и фактически сваливался в один static session profile
- устранено ложное ожидание mid-session auto-switch: routing теперь проверяется и фиксируется только на новом task launch
- устранен process gap, позволявший direct task пропустить явный self-handoff в самом ответе Codex и перейти к работе по неявному контексту
- подтверждено, что автопубликация релиза не добавлялась и existing release discipline сохранена

## [2.4.1] - 2026-04-20
### Добавлено
- declarative manifest `packaging/sources/sources-profiles.yaml` для archive/direct reference profiles
- direct reference profile `core-hot-15` для ежедневной работы в ChatGPT Project
- usage doc `docs/releases/sources-pack-usage.md` для hybrid-схемы `direct hot-set + canonical archive`

### Изменено
- export Sources теперь строит и canonical archive packs, и direct hot-set из одного источника правды
- boundary-actions и summary теперь рекомендуют `core-hot-15` как постоянный direct reference set
- `sources-pack-core-20` явно закреплён как canonical archive snapshot, а не как единственный ежедневный способ загрузки

## [2.4.0] - 2026-04-16
### Изменено
- подтвержден полный release-gate набор на чисто распакованном архиве: smoke, examples и matrix
- стабилизационный smoke-fix включен в основной финальный пакет
- release metadata переведены из `2.4.0-rc2` в финальную `2.4.0`

### Исправлено
- устранено зависание packaged `SMOKE_TEST.sh` за счет детерминированного наполнения smoke-артефактов через `tools/fill_smoke_artifacts.py`
- финальный архив и внутренний root-folder синхронизированы по имени `factory-v2.4.0`


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
- golden examples синхронизированы и по `.chatgpt/project-origin.md`, чтобы `validate-versioning-layer.py` проходил на rc2

## [2.4.0-rc1-consistency] - 2026-04-15
### Добавлено
- единый versioning/documentation layer для фабрики, шаблона и generated projects
- валидатор `validate-versioning-layer.py`
- стандартные `VERSION.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`

### Изменено
- launcher теперь создает versioning layer в generated project
- examples синхронизированы с актуальной версией фабрики

### Исправлено
- устранено расхождение между текущей версией фабрики и `project-origin.md` в template/examples
