# Текущее функциональное состояние фабрики

## Что уже реализовано
- 3 canonical entry modes: новый проект с нуля, brownfield без репо, brownfield с репо
- нейтральная canonical иерархия core vs optional/reference layers без product-specific naming в core
- strict machine-readable tree contract для factory root, template base и generated project contours
- strict machine-readable mode parity contract для template base и всех generated presets
- lifecycle state model отделен от project preset: greenfield-active, brownfield transitional states, brownfield-to-greenfield-conversion и greenfield-converted
- ownership taxonomy отделяет project-core, template-owned zones, project-owned zones, brownfield evidence/audit/reconstruction, factory-producer-owned, archives и transient-generated
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
- completion/handoff layer теперь требует `Рекомендация по внешним действиям` с явным статусом для factory ChatGPT Project, downstream repo sync, downstream ChatGPT Project и Sources fallback
- repo-first instruction layer для ChatGPT Projects: сценарии читаются прямо из GitHub repo, а не из локально загруженных project artifacts
- launcher и template docs больше не требуют отдельную project-local staging-конфигурацию
- beginner-friendly acceptance smoke (`tests/onboarding-smoke/run-novice-e2e.sh`) регулярно воспроизводит greenfield и brownfield novice launch path через wizard
- beginner-friendly acceptance smoke теперь покрывает все canonical presets: `greenfield-product`, `brownfield-without-repo`, `brownfield-with-repo-modernization`, `brownfield-with-repo-integration`, `brownfield-with-repo-audit`
- guided launcher теперь поддерживает полный beginner path через `--guided`: preflight, создание проекта, проверка `project-knowledge`, workspace первой задачи и следующий шаг оператора
- novice E2E теперь отдельно подтверждает `--guided` для greenfield, brownfield без repo, brownfield с repo и `--continue` flow
- downstream apply-safe-zones теперь сохраняет rollback-state и backup, а `rollback-template-patch.sh` выполняет воспроизводимый откат; для mixed manual sessions доступен full-project snapshot restore
- novice E2E теперь фиксирует duration и manual intervention count, а `validate-25-ga-kpi-evidence.py` валидирует full-KPI evidence перед `ga_ready: true`
- handoff source files и validator `validate-codex-task-pack.py` теперь явно требуют фиксировать приоритет repo rules при передаче задачи в Codex
- handoff layer теперь явно запрещает выдачу handoff через файл или несколькими блоками: пользователю разрешён только один цельный блок для вставки в Codex
- handoff layer теперь машинно требует language contract: generated handoff содержит `Язык ответа Codex: русский`, а Codex должен отвечать пользователю по-русски
- generated project tooling теперь включает validator `validate-handoff-response-format.py`, который проверяет сам markdown-ответ на single-block handoff и запрещает file-based handoff patterns
- task-based profile/model selection для Codex теперь вынесен в executable launch layer: named profiles, router scripts и launch log на границе новой задачи
- completion/handoff layer теперь выдает отдельный executable launch boundary и не подменяет новый task launch понятием "новый чат"
- completion package теперь по умолчанию не требует обновлять `factory-template ChatGPT Project`, если canonical repo/path/entrypoint и короткая repo-first instruction text не менялись
- direct task to Codex теперь проходит такой же нормализованный self-handoff, как и handoff из ChatGPT Project, включая `task_class`, `selected_profile`, `selected_model` и `defect_capture_path`
- direct task теперь дополнительно требует visible self-handoff block в первом substantive ответе, а не только artifact-level фиксацию
- direct-task response теперь является publishable handoff package и содержит continuation guardrail: совместимый internal follow-up выполняется без ручного "продолжай", а финальный closeout обязан дать `## Инструкция пользователю` или явно сказать `Внешних действий не требуется.`
- brownfield source-candidate map, reconstruction allowlist/denylist и change-map закреплены как internal Codex-eligible follow-up, а не пользовательский ручной шаг
- field pilot roadmap завершен до completed evidence: FP-01 greenfield выполнен на `https://github.com/mppcoder/greenfield-test` latest commit `cca68d5`, FP-02 brownfield without repo выполнен на `https://github.com/mppcoder/openclaw-brownfield` commit `7b3d1a4`, FP-03 brownfield with repo выполнен на `https://github.com/mppcoder/openclaw-brownfield` commit `3c026fd`, FP-04/FP-05 downstream sync cycles выполнены на той же lineage commits `1826f07` и `2dc6515`, post-field OpenClaw+ lifecycle conversion выполнен commit `1f8fb6d`
- closeout layer теперь запрещает оставлять GitHub repo/remote creation пользователю, если `gh`/connector write path доступен и owner/name однозначны
- generated `scripts/verify-all.sh` теперь поддерживает materialized root-level scripts contour в downstream projects
- recommended Codex handoff model routing обновлен под GPT-5.5: `build`, `deep` и `review` используют `gpt-5.5`, а `quick` сохраняет `gpt-5.4-mini` для lightweight задач
- model availability auto-check добавлен в executable routing layer: `codex-model-routing.yaml`, `check-codex-model-catalog.py`, live validation через `codex debug models`, proposal-only promotion policy и strict/unavailable validator modes
- optional skills/prompt-artifact quality loop добавлен как advanced maintenance contour: `skill-master-lite`, `skill-tester-lite`, test design guide и report template помогают улучшать trigger/usefulness без утяжеления beginner default path
- репо больше не считает один static profile или старую сессию Codex надежной единицей маршрутизации
- в repo появился единый visual/workflow reference layer по самому шаблону, greenfield, brownfield и downstream update contour
- root-level `RELEASE_NOTES.md` теперь является каноническим source для опубликованных release notes и release executor
- release-facing документация нормализована вокруг одного reference-doc и больше не зависит от разрозненных описаний в runbooks и release-note draft
- canonical preset naming, workspace bootstrap naming и optional domain reference contour синхронизированы между docs, manifests и физической структурой repo
- release-facing docs теперь фиксируют, что линия `2.5` не сводится к process hardening и требует отдельного beginner-first/UI-friendly контура
- очередь обновлений GitHub Actions workflow сведена и закрыта: CI и Release используют согласованные `checkout@v6`, `setup-python@v6` и `upload-artifact@v7`, а устаревший Dependabot PR cluster закрывается через единый remediation path
- closeout layer теперь требует проверять доступный GitHub write path перед передачей PR merge пользователю; если blockers нет, ready/merge/delete-branch/local sync выполняет Codex
- русскоязычный человекочитаемый слой закреплен как правило: ответы, инструкции, отчеты, closeout и generated guidance пишутся на русском, а английский остается только для технических идентификаторов
- repo-wide language cleanup закрыт для active source-facing слоя: `validate-human-language-layer.py` дает `active findings: 0`, а historical reports/work/release evidence закреплены как documented archival exceptions
- user-facing output operator env validator русифицирован, чтобы quick verify не возвращал англоязычные описательные сообщения
- tree contract validator подключен к quick/audit/matrix контуру и фиксирует compatibility-only слой для старых preset aliases
- physical root tree нормализован под project lifecycle core + bounded `factory/producer/` layer; старые factory-only и historical top-level folders запрещены контрактом
- factory-producer-owned content живет под `factory/producer/*`, а generated/battle project validation блокирует попадание `factory/producer/*` в downstream root
- mode parity validator подключен к quick/ci контуру и фиксирует одинаковый core layer: repo-first instructions, scenario-pack, AGENTS materialization, `.chatgpt`, Codex handoff pack, defect capture, versioning/docs, project-knowledge, `work/features`, `work/completed`, verify/done checklist и downstream sync metadata
- brownfield transition validator и greenfield conversion validator подключены к quick verify и matrix; brownfield adoption считается done только после conversion в `greenfield-product` или documented blocker
- `factory-template` зафиксирован как обычный `greenfield-product` с дополнительным factory producer layer, а не как отдельный workflow
- downstream sync contract защищает brownfield history/project-owned zones и исключает factory-producer-owned paths из battle project sync
- optional advanced path `feature-execution-lite` добавлен для больших фич: execution plan, task waves, checkpoint/resume, decisions journal, reviewer/audit hints, max review/fix rounds и final verification перед архивом
- `init-feature-workspace.sh --advanced-execution` создаёт advanced execution artifacts только по явному флагу, поэтому beginner path не усложнён
- `validate-feature-execution-lite.py` подключен к quick verify и проверяет checkpoint, wave dependencies, decisions, verify-smoke/verify-user и запрет закрытия `done` без final verification
- feature execution docs явно разделяют internal repo work, external user action и runtime backlog, чтобы не повторять field-pilot классы сбоев premature closeout, wrong boundary и evidence overclaim

## Программа 2.5 (release truth)
- release truth source: `docs/releases/release-scorecard.yaml`
- текущая стадия: `release-decision (GA passed)`
- статус: `2.5.0 GA Ready`
- GA-ready: `true`
- канонический roadmap: `docs/releases/2.5-roadmap.md`
- канонические метрики: `docs/releases/2.5-success-metrics.md`
- `TEST_REPORT.md` является evidence/reporting layer, а не отдельным источником статуса релиза
- dependency order зафиксирован: framing -> RC closeout evidence -> explicit GA/no-go по KPI
- scorecard gates нормализованы в `docs/releases/release-scorecard.yaml`
- novice E2E acceptance (все canonical presets + guided launcher smoke) зафиксирован в `tests/onboarding-smoke/ACCEPTANCE_REPORT.md`
- downstream upgrade UX closeout зафиксирован в `UPGRADE_SUMMARY.md`
- `G25-GA` прошел на `2026-04-26`: full-KPI evidence зафиксирован для всех `M25-*`
- consolidated evidence: `docs/releases/2.5-ga-kpi-evidence.md`
- граница evidence: `2.5.0 GA Ready` означает repo-controlled GA evidence; field-proven статус для real battle projects пока не заявлен
- post-GA field pilot roadmap: `docs/releases/2.5.1-field-pilot-roadmap.md`
- field pilot evidence register: `reports/release/2.5-field-pilot-evidence.md`
- текущий field evidence status: `completed-field-evidence` (`FP-01`..`FP-05` passed, `5/5`)

## Что работает частично
- matrix runner как единый источник истины
- полный controlled back-sync как production flow
- насыщенность scaffold-only examples
- phase-aware состав curated packs пока задается статическим policy manifest без отдельного сценарного роутинга
- auto GitHub Release publication зависит от доступности и авторизации `gh` CLI в конкретной среде
- phase-aware export/reference packs остаются вспомогательным слоем, а не каноническим хранилищем сценариев
- эвристика классификации `task_class` пока keyword-based, а не semantic classifier
- release-facing описание дерева проекта и workflow требует дальнейшего поддержания в sync при каждой новой process-доработке шаблона
- `2.5` объявлен GA-ready после добавления измеримого KPI evidence

## Что еще не закрыто
- финальная проверка на реальных greenfield и brownfield проектах
- production feedback от реальных converted brownfield проектов после нескольких template sync циклов
- дальнейший field hardening beyond FP-01..FP-05 при появлении новых real downstream программ
- окончательная polish-фаза для runner layer и operational reports
- отдельный release-facing validator/report для curated pack quality beyond structural checks
- дальнейшее production hardening runtime-нестабильности git sync beyond current fallback strategy
- дальнейшее расширение KPI evidence за пределы repo-controlled pilot к внешним downstream программам
- дальнейшее расширение novice acceptance от parity-level long-flow smoke к предметным domain-сценариям реальных downstream систем

## Граница core
Core включает фабрику, шаблон, versioning/documentation layer, `.chatgpt`, scenario-pack, examples и feedback loop.

## Optional layers / дополнительные слои
- factory/producer/extensions/workspace-packs
- factory/producer/reference/domain-packs
- factory/producer/reference/examples
- factory/producer/packaging
- factory/producer/registry
- factory/producer/archive
- advisory factory ops
