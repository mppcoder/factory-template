# Текущее функциональное состояние фабрики

## Что уже реализовано
- 3 canonical entry modes: новый проект с нуля, brownfield без репо, brownfield с репо
- нейтральная canonical иерархия core vs optional/reference layers без product-specific naming в core
- генерация greenfield и brownfield проектов
- scenario-pack, `.chatgpt` и launcher
- project presets, policy presets и change classes
- defect-capture layer и feedback loop
- drift detection, patch export и safe apply для разрешенных зон
- human-readable downstream upgrade report и rollback path для safe-zone materialization
- golden examples и scaffold-only examples
- curated reference/export packs, boundary-actions generator и ops-policy layer
- единый release-facing reference package по функционалу, архитектуре, дереву проекта и workflow
- нормализованный release-program framing для линии `2.5` с разделением треков `2.5-A` (engineering hardening) и `2.5-B` (beginner-first productization)

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
- curated reference/export packs с semantic validation по профилям `core / release / bugfix`, а не только по cap=20 и существованию файлов
- phase-aware recommendation layer для выбора `sources-pack-*` в `controlled-fixes / release / bugfix-drift`
- automatic phase detection из `git`-состояния для выбора рекомендованного `sources-pack-*`
- separate verified sync contour: auto commit/push после successful verify с lock, denylist и fallback push strategy
- lightweight follow-up verified sync для low-risk post-verify `.gitignore` и docs/closeout cleanup без отдельного ручного подтверждения
- separate release decision contour: auto tag/release path только после явного `release-decision.yaml`
- process layer явно различает internal repo follow-up, external boundary step и mixed follow-up, не позволяя user-only closeout вытеснить внутренний Codex handoff
- completion/handoff layer умеет требовать completion package с affected contours, delete-before-replace и repo-level sync steps для repo-first инструкций и downstream consumers
- completion/handoff layer теперь явно требует, чтобы обязательный completion package появлялся в том же финальном ответе, а не только после дополнительного запроса пользователя
- completion/handoff layer теперь различает готовые внешние boundary steps и внутренние prepare/export commands: сборка export artifacts выполняется Codex внутри repo до пользовательского блока
- repo-first instruction layer для ChatGPT Projects: сценарии читаются прямо из GitHub repo, а не из локально загруженных project artifacts
- launcher и template docs больше не требуют отдельную project-local staging-конфигурацию
- beginner-friendly acceptance smoke (`onboarding-smoke/run-novice-e2e.sh`) регулярно воспроизводит greenfield и brownfield novice launch path через wizard
- downstream apply-safe-zones теперь сохраняет rollback-state и backup, а `rollback-template-patch.sh` выполняет воспроизводимый откат; для mixed manual sessions доступен full-project snapshot restore
- handoff source files и validator `validate-codex-task-pack.py` теперь явно требуют фиксировать приоритет repo rules при передаче задачи в Codex
- handoff layer теперь явно запрещает выдачу handoff через файл или несколькими блоками: пользователю разрешён только один цельный copy-paste блок для Codex
- generated project tooling теперь включает validator `validate-handoff-response-format.py`, который проверяет сам markdown-ответ на single-block handoff и запрещает file-based handoff patterns
- task-based profile/model selection для Codex теперь вынесен в executable launch layer: named profiles, router scripts и launch log на границе новой задачи
- completion/handoff layer теперь выдает отдельный executable launch boundary и не подменяет новый task launch понятием "новый чат"
- completion package теперь по умолчанию не требует обновлять `factory-template ChatGPT Project`, если canonical repo/path/entrypoint и короткая repo-first instruction text не менялись
- direct task to Codex теперь проходит такой же нормализованный self-handoff, как и handoff из ChatGPT Project, включая `task_class`, `selected_profile`, `selected_model` и `defect_capture_path`
- direct task теперь дополнительно требует visible self-handoff block в первом substantive ответе, а не только artifact-level фиксацию
- репо больше не считает один static profile или старую сессию Codex надежной единицей маршрутизации
- в repo появился единый visual/workflow reference layer по самому шаблону, greenfield, brownfield и downstream update contour
- root-level `RELEASE_NOTES.md` теперь является каноническим source для опубликованных release notes и release executor
- release-facing документация нормализована вокруг одного reference-doc и больше не зависит от разрозненных описаний в runbooks и release-note draft
- canonical preset naming, workspace bootstrap naming и optional domain reference contour синхронизированы между docs, manifests и физической структурой repo
- release-facing docs теперь фиксируют, что линия `2.5` не сводится к process hardening и требует отдельного beginner-first/UI-friendly контура

## Программа 2.5 (статус на 2026-04-23)
- текущая стадия: `verify-closeout (RC prep)`
- канонический roadmap: `docs/releases/2.5-roadmap.md`
- канонические метрики: `docs/releases/2.5-success-metrics.md`
- dependency order зафиксирован: foundation hardening (`2.5-A`) -> beginner UX contracts (`2.5-B`) -> интеграция и downstream safety -> release closeout
- gate-лист для следующих 5 handoff нормализован в release-facing документах
- novice E2E acceptance (greenfield + brownfield) зафиксирован в `onboarding-smoke/ACCEPTANCE_REPORT.md`
- downstream upgrade UX closeout зафиксирован в `UPGRADE_SUMMARY.md`

## Что работает частично
- matrix runner как единый источник истины
- полный controlled back-sync как production flow
- насыщенность scaffold-only examples
- phase-aware состав curated packs пока задается статическим policy manifest без отдельного сценарного роутинга
- auto GitHub Release publication зависит от доступности и авторизации `gh` CLI в конкретной среде
- phase-aware export/reference packs остаются вспомогательным слоем, а не каноническим хранилищем сценариев
- эвристика классификации `task_class` пока keyword-based, а не semantic classifier
- release-facing описание дерева проекта и workflow требует дальнейшего поддержания в sync при каждой новой process-доработке шаблона
- roadmap `2.5` сформирован, но implementation-треки `2.5-A` и `2.5-B` ещё не закрыты фактическими engineering/product изменениями

## Что еще не закрыто
- финальная проверка на реальных greenfield и brownfield проектах
- окончательная polish-фаза для runner layer и operational reports
- отдельный release-facing validator/report для curated pack quality beyond structural checks
- дальнейшее production hardening runtime-нестабильности git sync beyond current fallback strategy
- выполнение следующих 5 handoff по roadmap `2.5` и закрытие gate'ов MVP/full
- подтверждение beginner-first KPI и downstream safety KPI из `docs/releases/2.5-success-metrics.md`
- дальнейшее расширение novice acceptance от текущего long-flow smoke к предметным domain-сценариям реальных downstream систем

## Граница core
Core включает фабрику, шаблон, versioning/documentation layer, `.chatgpt`, scenario-pack, examples и feedback loop.

## Optional layers
- workspace-packs
- optional-domain-packs
- advisory factory ops
