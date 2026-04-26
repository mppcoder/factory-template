# Отчет TEST REPORT v2.5.0 GA

Status source of truth: `docs/releases/release-scorecard.yaml`.
Current scorecard state: `2.5.0 GA Ready`.
TEST_REPORT.md is verification evidence, not the canonical release-status source.

## Проверка brownfield transition architecture

Дата: `2026-04-26`.

Проверены новые lifecycle/ownership/conversion контуры:

- `python3 template-repo/scripts/validate-tree-contract.py .` — pass.
- `python3 template-repo/scripts/validate-mode-parity.py .` — pass.
- `python3 template-repo/scripts/validate-brownfield-transition.py .` — pass.
- `python3 template-repo/scripts/validate-greenfield-conversion.py .` — pass.
- generated brownfield-without-repo smoke: launcher -> `validate-brownfield-transition.py --without-repo` -> tree/mode parity — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass.
- `bash MATRIX_TEST.sh` — pass; matrix covers factory-template producer layer, new greenfield, brownfield-without-repo transitional/conversion-ready/converted, brownfield-with-repo transitional/converted, and downstream sync preservation.
- `bash template-repo/scripts/verify-all.sh ci` — pass.
- `bash PRE_RELEASE_AUDIT.sh` — pass.

Conversion gates enforced:

- repo-first core and master router present;
- scenario-pack accessible;
- active project profile updated to `greenfield-product`;
- lifecycle state `greenfield-converted`;
- greenfield required artifacts present;
- brownfield evidence retained as history/reference;
- project-owned and template-owned zones marked;
- sync manifest safe for downstream;
- validators green.

## Доказательства решения GA

`G25-GA` получает pass на `2026-04-26`: RC evidence остается зеленым, а full-KPI evidence для GA теперь измерим и валиден.

- `M25-01`: timed first-success measurement ниже `25` минут.
- `M25-02`: controlled pilot checklist фиксирует `9/9`, `100%`.
- `M25-03`: manual intervention count равен `0`.
- `M25-04`: downstream safe-sync report фиксирует `6/6`, `100%`.
- `M25-05`: открытых critical defects в текущем verification scope нет.
- `M25-06`: aggregate handoff rework-loop register фиксирует max `1`.
- `M25-07`: release-facing docs синхронизированы на состояние GA.
- `M25-08`: текущий remediation начат с чтения `template-repo/scenario-pack/00-master-router.md`.

Blocker report: `reports/bugs/2026-04-26-25-ga-readiness-gap.md`.

## Что проверено
- strict tree contract для factory root, template base и generated project contours
- consolidated verify entrypoint (`template-repo/scripts/verify-all.sh`)
- CI baseline checks (`CI / verify-baseline`, `CI / release-bundle-dry-run`)
- release workflow preflight + bundle baseline (`.github/workflows/release.yml`)
- Dependabot baseline (`.github/dependabot.yml`)
- routing validator normalization for generated repos
- security baseline (`SECURITY.md`, `CODEOWNERS`, secret-handling guidance)
- pre-release audit
- factory-template ops policy validator
- fresh scaffold: greenfield + small-fix + manual
- fresh scaffold: brownfield + brownfield-audit + manual
- golden examples
- versioning / defect-capture / alignment layer
- curated reference/export packs and boundary-actions policy layer
- feedback validator and ingest dry-run path
- codex task pack validator
- semantic validator для curated reference/export packs
- phase-aware recommendation layer для boundary-actions и pack summary
- automatic phase detection helper
- synthetic phase detection self-test
- repo-first ChatGPT Project instruction mode
- release-facing reference package and canonical root release notes source
- novice onboarding acceptance fixtures (`onboarding-smoke/run-novice-e2e.sh`)
- mode parity manifest, matrix and validator (`template-repo/mode-parity.yaml`, `docs/mode-parity-matrix.md`, `validate-mode-parity.py`)
- downstream upgrade v3 dry-run/apply/rollback UX (`upgrade-report.py`, `rollback-template-patch.sh`)
- lightweight spec-governance traceability: `decisions.md.template`, expanded tech/task templates, approval-aware deviations, task verification anchors
- опциональные production VPS presets: `starter`, `app-db`, `reverse-proxy-tls`, `backup`, `healthcheck`

## Ожидаемое поведение на fresh scaffold
Проходят structural / versioning / defect / alignment проверки.
Evidence / quality / DoD до смыслового наполнения артефактов не проходят.

## Фактический результат
- `bash template-repo/scripts/verify-all.sh ci` проходит на `2026-04-26` и подтверждает текущий GA scorecard.
- `bash CLEAN_VERIFY_ARTIFACTS.sh` проходит на `2026-04-26`.
- `bash PRE_RELEASE_AUDIT.sh` проходит на `2026-04-26`.
- `bash RELEASE_BUILD.sh /tmp/factory-template-2.5.zip` проходит на `2026-04-26`; собран архив `/tmp/factory-template-2.5.zip`.
- `python3 template-repo/scripts/validate-tree-contract.py .` проходит.
- `python3 template-repo/scripts/validate-mode-parity.py .` проходит и подтверждает общий core layer для template base, greenfield, brownfield-without-repo и всех brownfield-with-repo presets.
- `bash template-repo/scripts/verify-all.sh quick` проходит.
- `bash template-repo/scripts/verify-all.sh ci` проходит.
- `deploy-dry-run-smoke-starter-app-db` входит в `verify-all.sh quick/ci` и проверяет dry-run для `starter` и `app-db` через локальный fake `docker compose`, без зависимости от Docker daemon.
- Production VPS preset gap зафиксирован и исправлен in-scope: `reports/bugs/2026-04-26-production-vps-preset-gap.md`.
- `MATRIX_TEST.sh` подтверждает `validate-tree-contract.py` на generated greenfield, brownfield-without-repo и brownfield-with-repo контурах.
- Compatibility aliases проверены через `apply-project-preset.py`: старый greenfield alias резолвится в `greenfield-product`, старый no-repo brownfield alias резолвится в `brownfield-without-repo`.
- `bash onboarding-smoke/run-novice-e2e.sh` проходит: покрыты wizard fallback-сценарии для всех canonical presets, `--guided` greenfield, `--guided` brownfield без repo, `--guided` brownfield с repo и `--continue` flow.
- `python3 template-repo/scripts/factory-launcher.py --guided` ведет новичка через preflight, создание проекта, проверку `project-knowledge`, создание workspace первой задачи и operator next step; старые прямые scripts остаются fallback-путями.
- Defect-capture по guided launcher UX gap зафиксирован и исправлен in-scope: `reports/bugs/2026-04-25-guided-launcher-ux-gap.md`.
- `validate-mode-parity.py` подключен в `verify-all.sh quick`, поэтому входит и в `verify-all.sh ci`.
- `validate-spec-traceability.py` входит в `verify-all.sh quick` и `verify-all.sh ci`; подтверждает наличие `User Intent Anchors`, `User Intent Binding`, `User-Spec Deviations`, `Decisions`, `Acceptance Criteria`, `Audit Wave Lite`, `Final Verification` и task verification anchors в шаблонах.
- Synthetic feature workspace подтверждает green path: `init-feature-workspace.sh` -> `resume-setup.py` -> `generate-user-spec.py` -> `decompose-feature.py` -> `validate-spec-traceability.py`.
- Negative traceability checks подтверждены: validator ловит task без verification path и approved tech-spec с `DEV-* approval=pending`.
- Incidental placeholder audit defect зафиксирован и исправлен in-scope: `reports/bugs/2026-04-25-user-spec-audit-placeholder-tech-spec.md`.
- `template-repo/project-presets.yaml` теперь явно фиксирует `parity_mode` и общий required core artifact set для каждого canonical preset.
- `template-repo/launcher.sh` materializes `template-repo/mode-parity.yaml` в generated projects.
- Incidental parity defect `work/features` gap зафиксирован и исправлен in-scope: `reports/bugs/2026-04-25-mode-parity-gap.md`.
- `bash RELEASE_BUILD.sh /tmp/factory-template-release.zip` проходит как packaging dry-run.
- `validate-codex-routing.py` теперь корректно проверяет и template repo, и generated repos (без false-negative по `template/docs/*`).
- `tools/fill_smoke_artifacts.py` теперь поддерживает target path и не перезаписывает root `.chatgpt/*` при `MATRIX_TEST.sh`.
- `PRE_RELEASE_AUDIT.sh` проходит на чистом пакете.
- `VALIDATE_FACTORY_TEMPLATE_OPS.sh` проходит на чистом пакете.
- `SMOKE_TEST.sh` проходит на чисто распакованном финальном архиве.
- `EXAMPLES_TEST.sh` проверяет 36 из 36 комбинаций и проходит зелёно.
- `EXAMPLES_TEST.sh` теперь выводит diagnostic block `[DETAIL]` при падении checker-а и больше не скрывает root cause за `/dev/null`.
- `template-repo/scripts/validate-versioning-layer.py` переведен на self-contained Python-проверку (без runtime-зависимости от `rg`).
- `MATRIX_TEST.sh` проходит на чисто распакованном финальном архиве.
- `MATRIX_TEST.sh` подтверждает, что сырой `meta-feedback` блокируется validator, а после заполнения dry-run ingest проходит.
- `MATRIX_TEST.sh` подтверждает, что generated `codex task pack` проходит отдельный semantic validator и подхватывает active scenario routing.
- `MATRIX_TEST.sh` подтверждает upgrade closeout path v3: `upgrade-report.py`, `apply-template-patch.sh --apply-safe-zones`, `rollback-template-patch.sh --check|--rollback`.
- `MATRIX_TEST.sh` подтверждает multi-zone downstream preview: `safe-generated` materializes больше двух template-owned файлов, `advisory-review` показывает `project-knowledge` только как diff/merge guidance, `manual-project-owned` показывает live `work/` только как impact signal.
- `MATRIX_TEST.sh` подтверждает, что `upgrade-report.py` не возвращает известные англоязычные человекочитаемые фразы в markdown summary.
- `validate-codex-task-pack.py` теперь проверяет auto-closeout guardrails: финальный `git status --short --branch`, запрет dirty/ahead closeout без blocker и обязательное отражение commit hash / sync status.
- `VALIDATE_FACTORY_TEMPLATE_OPS.sh` подтверждает semantic profile для `sources-pack-core-20`, `sources-pack-release-20` и `sources-pack-bugfix-20`.
- `EXPORT_FACTORY_TEMPLATE_SOURCES.sh` и `GENERATE_BOUNDARY_ACTIONS.sh` публикуют phase-aware рекомендацию для `controlled-fixes`, `release` и `bugfix-drift`.
- `DETECT_FACTORY_TEMPLATE_PHASE.sh` корректно различает `release` и `bugfix-drift` на rule-based changed path signals.
- `PHASE_DETECTION_TEST.sh` автоматически проверяет synthetic `controlled-fixes`, `release` и `bugfix-drift` сценарии.
- launcher smoke на временном scaffold подтверждает, что создание проекта больше не зависит от внешнего staging URL и сразу переводит проект в repo-first режим.
- `UPGRADE_SUMMARY.md` подтверждает человекочитаемый downstream upgrade UX v3: safe/advisory/manual-only distinction, what will change, why each tier is safe/advisory/manual, rollback path и обязательный review list.
- `POST_UNZIP_SETUP.sh` остаётся безопасным для non-interactive verify path и не блокирует test runs prompt'ом.
- validator `validate-codex-task-pack.py` теперь требует, чтобы handoff pack явно фиксировал приоритет правил repo.
- validator `validate-codex-task-pack.py` теперь также требует правило: handoff пользователю выдаётся только одним цельным copy-paste блоком, а не ссылкой на файл и не несколькими блоками.
- `validate-handoff-response-format.py` проверяет готовый markdown handoff-response и ловит file-based handoff, несколько handoff-заголовков и отсутствие fenced copy-paste блока.
- `release` определяется только при сочетании release-path signals и checked intent markers в `RELEASE_CHECKLIST.md`.
- `bugfix-drift` определяется только при сочетании bug/validator path signals и bug-report intent markers в `reports/bugs/*.md`.
- Golden examples и fresh scaffold синхронизированы с финальным versioning layer.
- curated `sources-pack-core-20`, `sources-pack-release-20`, `sources-pack-bugfix-20` собираются из декларативного policy manifest.
- boundary-actions guide генерируется из markdown template и проверяется вместе с ops-policy слоем.
- incidental defect `utcnow()` warning зафиксирован и исправлен in-scope: `reports/bugs/2026-04-23-factory-ops-utcnow-warning.md`.
- Defect-capture по утечке английского текста в downstream sync v3 зафиксирован и исправлен in-scope: `reports/bugs/2026-04-26-downstream-sync-v3-language-leak.md`.
- Defect-capture по пропуску автозавершения closeout sync зафиксирован и исправлен in-scope: `reports/bugs/2026-04-26-autocloseout-sync-skip.md`.

## Что вошло в релиз 2.5.0
- full-KPI evidence layer для `G25-GA`;
- timed novice onboarding measurements и manual intervention counters;
- controlled pilot checklist для beginner-first path;
- downstream safe-sync success-rate report;
- validator `validate-25-ga-kpi-evidence.py`;
- template/meta/root versioning и release metadata синхронизированы под `2.5.0`.

## Известные ограничения
- `MATRIX_TEST.sh` остаётся representative prerelease runner, а не exhaustive full-matrix coverage для всех 22 допустимых комбинаций;
- back-sync по-прежнему controlled safe/advisory/manual flow, а не full auto-sync.
- semantic/relevance оценка curated packs пока остается rule-based, а не phase-aware recommendation engine.
- phase detection пока rule-based по changed paths и может не уловить более сложный operator intent без явных файловых сигналов.
- документальные intent signals сейчас реализованы только для `release`, а не для всех фаз.
- document intent signals сейчас реализованы для `release` и `bugfix-drift`, но ещё не покрывают возможные более тонкие подфазы внутри controlled fixes.
- phase-aware export/reference packs остаются вспомогательным слоем и не заменяют чтение сценариев из GitHub repo.

## Открытые вопросы
- По bug set `bug-026/027/028` критичных открытых дефектов после remediation не осталось.
- Follow-up для будущего улучшения (не blocker текущего RC): расширить novice long-flow с synthetic smoke до более предметных domain сценариев в downstream проектах.
- GA blocker `reports/bugs/2026-04-26-25-ga-readiness-gap.md` закрыт после добавления KPI evidence.

## Статус CI baseline
- Статус: `green` (GitHub Actions run `24840192862`, 2026-04-23: `verify-baseline` = success, `release-bundle-dry-run` = success; локально подтверждено 2026-04-26 через `verify-all.sh ci`).
- Residual risk: шаг `release-executor` в release workflow остаётся manual/optional и по-прежнему зависит от валидного verified-sync контекста и GitHub auth.
