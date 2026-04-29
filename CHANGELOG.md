# Журнал изменений фабрики

## [Unreleased]
### Добавлено
- Release package artifact refresh for `2.5.1`: install ZIP теперь собирается с ASCII-only archive paths для GUI/Windows-compatible распаковки; `bootstrap/*.md` нормализуются только в staging archive, source repo filenames не меняются в этом fix.
- `validate-release-package.py` теперь отклоняет release archives с non-ASCII paths, чтобы не выпускать ZIP, который может открываться в Linux CLI, но ломаться в пользовательских archive tools.
- Release package updated bootstrap for `2.5.1`: `RELEASE_BUILD.sh` теперь выпускает canonical zip, sidecar manifest и SHA256 checksum, а `validate-release-package.py` проверяет single root folder, forbidden paths, manifest, checksum и required files.
- Defect report `reports/bugs/2026-04-29-release-package-updated-bootstrap-gaps.md` для package/install-from-scratch gaps: отсутствовали manifest/checksum gate, fallback archive verification и явное npm support status.
- Handoff implementation control layer: template-owned `.chatgpt/handoff-implementation-register.yaml`, validator `validate-handoff-implementation-register.py`, deterministic dependency/priority calculation и lifecycle dashboard cards для queued/ready, blocked, blockers, in-progress, implemented-not-verified, stale и closed handoff/self-handoff задач.
- Replacement/write-off policy для handoff implementation register: `superseded`, `handoff_group`, `handoff_revision`, `replaces`, `superseded_by`, `replacement_reason` и validator coverage для нескольких active handoff в одной группе.
- Defect report `reports/bugs/2026-04-29-superseded-handoff-not-written-off.md` для gap, где replacement handoff мог оставить старый handoff активным.
- Lifecycle dashboard integration теперь читает handoff implementation register как отдельный source artifact и не смешивает его с `.chatgpt/handoff-rework-register.yaml`.
- Scenario guidance теперь требует Codex closeout обновлять matching handoff implementation item, добавлять evidence, материализовать новые self-handoff items и снимать задачи только через explicit `not_applicable`/archive path.
- Defect report `reports/bugs/2026-04-29-clean-verify-misses-artifacts.md` для cleanup gap, где ignored `_artifacts` ломал `PRE_RELEASE_AUDIT`.
- Defect report `reports/bugs/2026-04-29-beginner-intake-missing-default-decisions.md` для beginner UX gap, где intake/questionnaire задавал expert-only blank questions вместо recommendation-first defaults.
- Default-decision layer для intake/questionnaire flows: `global-defaults`, `confirm-each-default` и `manual`, accepted/overridden defaults, default source basis, uncertainty notes и explicit confirmation для risky/paid/destructive/security/privacy/legal/secret decisions.
- Validator coverage в `validate-runbook-packages.py` и lifecycle dashboard validator для `default_decision_mode`, accepted/overridden defaults, unresolved decisions, override path и запрета forced/risky defaults.
- Нормализованное поле `handoff_shape` для выбора между `single-agent-handoff` и `parent-orchestration-handoff`, включая hard triggers, soft scoring и запрет ложного parent/default выбора.
- Shape-aware validator coverage для handoff UX: positive fixtures для single-agent и parent orchestration, negative fixtures для missing shape и очевидно неверного выбора shape.
- Defect/factory feedback для drift, где beginner UX validator ошибочно требовал parent orchestration markers для любого handoff.
- Controlled software update governance layer: policy/spec `docs/operator/software-update-governance.md`, generated artifacts `.chatgpt/software-inventory.yaml`, `.chatgpt/software-update-watchlist.yaml`, `.chatgpt/software-update-readiness.yaml` и `reports/software-updates/README.md`.
- Report-only helpers `validate-software-update-governance.py` и `render-software-update-readiness.py`, подключенные к quick/generated verify.
- Lifecycle dashboard block `software_update_governance` для baseline status, auto-update policy, update intelligence freshness, findings count, upgrade proposal status, next safe action, fallback и blockers.
- Reusable factory feedback `reports/factory-feedback/feedback-043-controlled-software-update-governance-gap.md` для отсутствующего governance contour.
- Defect report `reports/bugs/2026-04-28-runbook-packages-missing-beginner-copy-paste-flow.md` для gap, где package layer был abstract routing/checklist, а не beginner zero-to-Codex-ready flow.
- Beginner-first runbook contract: packages теперь обязаны разделять `USER-ONLY SETUP` и `CODEX-AUTOMATION`, фиксировать Codex takeover point и использовать copy-paste step cards с окном, командами, expected result и диагностикой.
- Validator coverage для beginner runbook flow: обязательные factory steps `FT-000`..`FT-180`, contours `codex-app-remote-ssh` / `vscode-remote-ssh-codex-extension`, Timeweb/VPS/SSH/Codex setup tokens и automation boundary.
- Второй remediation pass закрепил точный beginner flow `FT-000`..`FT-180`, включая `FT-150A` для Codex App Remote SSH, `FT-150B` для VS Code Remote SSH + Codex extension, `FT-170` takeover checkpoint и `FT-180` диагностику неудачного запуска.
- Dashboard `runbook_packages` получил поля `current_step`, `active_contour`, `takeover_ready` и `checklist_path`.
- Defect report `reports/bugs/2026-04-29-greenfield-runbook-wrong-user-github-boundary.md` для gap, где greenfield package ошибочно относил GitHub repo/access к user-only действиям.
- Defect report `reports/bugs/2026-04-29-greenfield-runbook-bypasses-factory-chatgpt-intake.md` для gap, где greenfield package bypass-ил factory-template ChatGPT Project intake и начинался напрямую в Codex.
- Defect report `reports/bugs/2026-04-29-codex-cannot-create-chatgpt-project-boundary.md` для gap, где greenfield boundary нужно было явно отделить Codex-prepared repo-first instruction от ручного создания/редактирования ChatGPT Project в UI.
- Финальный слой `docs/operator/runbook-packages/` с package contract и четырьмя complete runbook-checklist packages: `factory-template`, `greenfield-product`, `brownfield-with-repo-to-greenfield`, `brownfield-without-repo-to-greenfield`.
- Validator `validate-runbook-packages.py`, подключенный к quick verify: проверяет existence, command/path lint, brownfield conversion gates, greenfield final state, dashboard integration, archive/cleanup wording и handoff language/routing boundary.
- Dashboard contract `runbook_packages` для current phase, gates, blockers, next action и owner boundary по каждому package.
- Defect report `reports/bugs/2026-04-28-runbook-package-layer-gap.md` для gap, где отдельные runbooks/presets/validators не давали complete package layer для четырех входов.
- Project-root boundary для intermediate repos: machine-readable `workspace_layout_policy`, validator coverage и Artifact Eval `project-root-boundary` закрепляют, что temporary/intermediate/reconstructed/helper repos живут внутри repo целевого `greenfield-product`, а не как siblings в `/projects`.
- Defect/factory feedback для gap, где промежуточные brownfield/reconstruction repo могли трактоваться как отдельные project roots в плоском `/projects` дереве.
- Связка model promotion и prompt policy update: `prompt_migration_policy` в `codex-model-routing.yaml`, prompt migration section в model-routing proposal, validator `validate-model-prompt-policy.py` и Artifact Eval spec/report `model-prompt-policy`.
- Defect/factory feedback для gap, где новая model могла пройти через proposal только как `selected_model` update без prompt-policy migration по official OpenAI docs.
- GPT-5.5 prompt migration contract: `validate-gpt55-prompt-contract.py`, Artifact Eval spec/report `gpt-5-5-prompt-contract`, prompt inventory и migration reports.
- Reusable defect report `reports/bugs/2026-04-28-gpt-5-5-prompt-migration-gap.md` и factory feedback для stale/prompt-contract drift gap.
- Plan №6 beginner-first orchestration productization: cockpit-lite, parent plan normalization wrapper, route-explain layer, beginner full handoff UX scorecard and safe synthetic rehearsal.
- `docs/operator/factory-template/05-orchestration-cockpit-lite.md`, cockpit YAML template, cockpit renderer/validator and parent orchestration plan template.
- `explain-codex-route.py` / `validate-route-explain.py` for deterministic keyword/rule-based route explanations with live catalog boundary.
- `validate-beginner-handoff-ux.py` with positive/negative fixtures and Artifact Eval report `beginner-full-handoff-ux`.
- Plan №5 internal hardening roadmap, VPS Remote SSH-first orchestration runbook, repo-native dry-run parent orchestrator and orchestration validator.
- orchestration rule `user_actions_policy: defer-to-final-closeout`: user-required actions move to final parent closeout, safe temporary placeholders can unblock internal child subtasks, and final reports list replacement reminders.
- curated/reference pack quality validator with positive/negative fixtures and quick verify integration.
- verified sync fallback evidence report/validator for blocked push, remote drift, protected branch, branch ahead, dirty state and fallback instructions.
- domain scenario acceptance template with CRM and inventory examples beyond parity smoke.
- defect report `reports/bugs/2026-04-27-external-actions-oververbose-closeout.md` для чрезмерно длинного closeout внешних действий.
- post-2.5 planning layer: `docs/releases/2.5.1-roadmap.md`, `docs/releases/2.6-roadmap.md` и `docs/releases/post-2.5-gap-register.md`.
- defect report `reports/bugs/2026-04-27-post-25-release-planning-gap.md` для release-followup planning gap после `2.5.0 GA Ready`.
- comparison register for `pavel-molyanov/molyanov-ai-dev`: already adapted, useful-not-yet-adapted and intentionally-not-adapted ideas.
- defect report `reports/bugs/2026-04-26-root-still-has-nonstandard-top-level-folders.md` и ADR `docs/decisions/2026-04-26-root-physical-normalization.md` для physical root normalization.
- bounded namespace `factory/producer/` для factory-producer-owned ops, packaging, registry, sync, reference, extensions и archive content.
- bug report `reports/bugs/2026-04-26-handoff-codex-language-leak.md` для повторной утечки английского handoff/ответов Codex.
- mandatory language contract in generated Codex handoff: `Язык ответа Codex: русский`.
- ADR `docs/decisions/2026-04-26-project-core-producer-layer-and-brownfield-transition.md` фиксирует единый lifecycle core, factory producer layer и обязательный brownfield -> greenfield conversion.
- `validate-brownfield-transition.py` и `validate-greenfield-conversion.py` добавлены в template validators и `verify-all.sh quick`.
- `docs/brownfield-to-greenfield-transition.md` описывает without-repo и with-repo transition paths, conversion gates и done rule.

### Изменено
- Versioning layer, manifests, release checklist, install-from-scratch runbooks and release truth markers synchronized under patch release `2.5.1`.
- User and Codex runbooks now document GitHub clone/download or release artifact as canonical path, manual archive upload to `/projects/factory-template/_incoming` as fallback, and npm path as unsupported without `package.json`.
- Greenfield intake теперь идет как `новый проект` -> выбор default-decision mode -> recommendation-first опрос -> generated Codex handoff, где handoff содержит accepted defaults, overrides и unresolved decisions/blockers.
- Brownfield with repo / without repo packages теперь применяют default-decision layer для canonical root, no-overwrite, evidence-first audit, `_incoming` и reconstruction-inside-target-root defaults.
- Lifecycle dashboard `runbook_packages` показывает default decision mode, defaults/overrides/unresolved counters, next decision и readiness to generate handoff.
- Scenario-pack, routing contract, route explanation и VPS Remote SSH orchestration runbook теперь явно фиксируют, что `single-agent-handoff` является default для цельных задач, а parent orchestration нужен только для больших/multi-agent задач.
- Runbook packages теперь требуют фиксировать Ubuntu/VPS image release, later package update state, `unattended-upgrades`, package sources, Docker/Compose, Node/Python, GitHub Actions, base images/tags/digests, lockfiles и critical runtime dependencies без auto-upgrade.
- Mode parity и project presets теперь считают software update governance core capability для всех generated greenfield/brownfield projects.
- `01-factory-template/01-user-runbook.md` переписан как novice runbook от Windows PC до remote Codex takeover; `02-codex-runbook.md` теперь явно берет на себя VPS preflight, package install, clone, bootstrap, verify, dashboard update и verified sync.
- `01-factory-template/03-checklist.md` теперь является таблицей-зеркалом пользовательских шагов и не содержит process/meta checks; process checks перенесены в Codex/verify слой.
- `01-factory-template/04-verify.md` разделен на user readiness verify до takeover и Codex automation verify после takeover.
- Greenfield и оба brownfield packages выровнены под ту же user-only/Codex-automation архитектуру, чтобы external setup не смешивался с internal repo follow-up.
- `02-greenfield-product` теперь фиксирует правильную boundary: пользователь стартует в ChatGPT Project шаблона фабрики командой `новый проект`, отвечает на опрос, вставляет generated handoff в Codex, а после automation сам создает ChatGPT Project боевого проекта, открывает Project settings/instructions, вставляет подготовленную Codex repo-first instruction и сохраняет настройки; GitHub repo/origin/initial push/project root/wizard/verify/sync выполняет Codex при отсутствии blocker.
- `02-greenfield-product` теперь стартует канонически: ChatGPT Project шаблона фабрики -> новый чат -> `новый проект` -> scenario-pack опрос -> readiness check -> generated Codex handoff. Codex получает handoff, а не raw project name.
- Greenfield validator теперь падает на claims, что Codex создает ChatGPT Project или вставляет/сохраняет instructions через ChatGPT UI; canonical wording: Codex готовит repo-first instruction для боевого ChatGPT Project, пользователь создает Project в UI и вставляет готовый текст.
- Release-facing workflow map, lifecycle dashboard doc и source manifest теперь знают про runbook package layer; отдельный export profile `sources-pack-runbook-packages` включает полный набор package files.
- Canonical VPS layout в active docs, scenario-pack и bootstrap guidance теперь явно требует размещать все intermediate repos внутри repo целевого `greenfield-product`.
- `check-codex-model-catalog.py --write-proposal` теперь требует companion prompt migration review: fresh prompt baseline, affected prompt-like artifacts, validators/evals и official OpenAI source map до profile promotion.
- Codex task-pack и normalized handoff generators теперь добавляют базовый prompt contract для GPT-5.5: fresh baseline, outcome, success criteria, constraints, evidence requirements, output shape и stop rules.
- Template `.chatgpt/codex-input.md` переведен на русскоязычный outcome-first prompt shape; `quick` profile сохранен на `gpt-5.4-mini` без silent promotion.
- Full handoff orchestration docs now explain beginner-visible cockpit/status, parent plan normalization, deterministic route explanation and UX scorecard without making model/profile switching the main product value.
- Parent orchestration placeholder metadata now accepts both `final-user-action` and `future-user-action` so future P4-S5/P4-S6 placeholders remain explicit without claiming real downstream proof.
- Codex workflow docs and handoff scenario now document VPS Remote SSH-first as default for full handoff orchestration, with Codex App/Cloud Director optional only.
- curated sources profiles now include the VPS Remote SSH orchestration runbook and routing config in core packs.
- closeout guidance теперь использует compact default: если внешних действий нет, финал говорит `Внешних действий не требуется.`, а если действия есть, `## Инструкция пользователю` перечисляет только реальные действия снаружи Codex.
- `Реестр внешних действий` больше не должен быть audit table всех возможных contour'ов со статусом `не требуется`; полный register допускается только по явному запросу или для release/security approval.
- release-facing docs теперь явно разделяют `2.5.1` stabilization scope и `2.6` runtime/advanced execution scope без изменения `2.5.0` scorecard.
- post-2.5 docs фиксируют completed repo-controlled/synthetic proof отдельно от pending external runtime proof: real VPS deploy, backup restore и rollback drill остаются external/manual boundary.
- legacy/factory-only root folders физически перенесены или растворены: `.dogfood-bootstrap`, `factory_template_only_pack`, `meta-template-project`, `onboarding-smoke`, `optional-domain-packs`, `packaging`, `registry`, `working-project-examples`, `workspace-packs`.
- `template-repo/tree-contract.yaml` и `validate-tree-contract.py` теперь запрещают старые active root paths, проверяют `factory/producer/*` namespace и блокируют factory-producer-owned paths в generated/battle projects.
- downstream sync tooling, source profiles, release scripts, docs и smoke/matrix paths обновлены на новые producer/test/reference locations.
- `tree-contract.yaml`, `mode-parity.yaml`, presets и sync manifest теперь разделяют project preset, recommended mode, lifecycle state и ownership class.
- Brownfield presets помечены как transitional adoption labels с target `greenfield-product` / `greenfield-converted`.
- Launcher, first-project wizard и VPS preflight теперь объясняют brownfield как intake/reconstruction или audit/adoption path, а greenfield как steady-state product development.
- Downstream sync model теперь явно исключает `factory-producer-owned` paths и защищает brownfield historical evidence.

### Исправлено
- `CLEAN_VERIFY_ARTIFACTS.sh` и `PRE_RELEASE_AUDIT.sh` теперь учитывают `_artifacts`, чтобы release audit не сканировал stale generated release/source packs.
- зафиксирован и исправлен reusable closeout UX defect: отсутствие внешних действий больше не разворачивается в длинный completion package с no-op строками.
- `create-codex-task-pack.py`, `codex_task_router.py`, `validate-handoff-response-format.py`, `validate-handoff-language.py` теперь блокируют англоязычные labels `Repo:`, `Goal:`, `Entry point:`, `Scope:` и требуют прямую инструкцию Codex отвечать по-русски.
- зафиксирован и исправлен reusable architecture defect: brownfield adoption больше не может считаться финальным project class без conversion или blocker.
- зафиксирован и исправлен `bug-034`: финальный closeout теперь должен содержать `Рекомендация по внешним действиям` с явным статусом для factory ChatGPT Project, downstream sync, downstream ChatGPT Project и Sources fallback.

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
- отдельный optional/reference contour `factory/producer/reference/domain-packs/` для domain-specific reference-cases вне canonical core tree
- compatibility alias map для legacy preset names в `template-repo/project-presets.yaml` и runtime preset application
- универсальный workspace pack `factory/producer/extensions/workspace-packs/vscode-codex-bootstrap` вместо release-facing dogfood naming

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
- declarative manifest `factory/producer/packaging/sources/sources-profiles.yaml` для archive/direct reference profiles
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
