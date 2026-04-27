# Отчет TEST REPORT v2.5.0 GA

Status source of truth: `docs/releases/release-scorecard.yaml`.
Current scorecard state: `2.5.0 GA Ready`.
TEST_REPORT.md is verification evidence, not the canonical release-status source.

## Проверка Production VPS Field Pilot

Дата: `2026-04-27`.

Подготовлен safe field pilot path для single-VPS deploy без destructive действий по умолчанию.

- `docs/production-vps-field-pilot.md` добавляет runbook `starter -> app-db -> reverse-proxy-tls -> backup -> healthcheck -> rollback drill`.
- `docs/deploy-on-vps.md` теперь явно отделяет dry-run/report evidence от real production proof.
- `reports/release/production-vps-field-pilot-report.md` фиксирует текущий статус: `repo-controlled-dry-run-ready-real-vps-pending`.
- `template-repo/scripts/deploy-dry-run.sh --field-pilot-report` пишет markdown field pilot report после успешного dry-run.
- `template-repo/scripts/deploy-local-vps.sh --field-pilot-report` пишет report после operator-approved deploy.
- `template-repo/scripts/operator-dashboard.py --field-pilot-report` собирает runtime/evidence summary без deploy.
- `template-repo/scripts/validate-operator-env.py --field-pilot-report` пишет env readiness report.
- Starter остаётся default, production presets остаются opt-in.
- DNS, firewall, Docker Compose, env secrets и backup restore checklist зафиксированы в runbook/report.
- Real VPS deploy, restore test и rollback drill не выполнялись без user approval; статус field deploy остаётся pending.

Проверки:

- `template-repo/scripts/verify-all.sh quick` включает fake-Docker smoke для `starter`, `app-db` и `production --field-pilot-report`.
- `validate-operator-env.py --field-pilot-report` проверен на production fixture.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-27`.

## Проверка Project Knowledge Done Loop

Дата: `2026-04-27`.

Добавлен factory-native closeout после feature work, чтобы `decisions.md` не терялся после завершения задачи, а обновление `project-knowledge/` стало явным проверяемым шагом.

- `docs/done-and-project-knowledge-loop.md` объясняет beginner-friendly loop: прочитать `user-spec`, `tech-spec`, `decisions.md`, создать proposal для Project Knowledge, зафиксировать downstream impact и архивировать feature.
- `template-repo/scripts/close-feature-workspace.py` создает `done-report.md`, `project-knowledge-update-proposal.md`, `downstream-impact.md` и переносит workspace в `work/completed/`.
- `template-repo/scripts/validate-project-knowledge-update.py` проверяет done report, непустые decisions, Project Knowledge proposal, downstream impact и archive/blocker.
- Для `feature-execution-lite` closeout/validator проверяют execution-plan, checkpoint, task waves, decisions, final verification и artifact-eval evidence link/justification.
- `template-repo/scripts/check-dod.py` подключает validator для closed feature workspaces.
- `template-repo/scripts/verify-all.sh quick` запускает `project-knowledge-done-loop-smoke` на fixture из `tests/project-knowledge-done-loop/`.
- `template-repo/template/project-knowledge/*` и `decisions.md.template` обновлены правилами closeout/proposal/archive.

Проверки:

- `python3 template-repo/scripts/validate-project-knowledge-update.py . --allow-empty` — pass.
- Project Knowledge Done Loop smoke: `close-feature-workspace.py` -> archive в `/tmp/work/completed/feat-closeout-smoke` -> `validate-project-knowledge-update.py` — pass.
- `python3 template-repo/scripts/validate-feature-execution-lite.py .` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass.

## Проверка external actions closeout

Дата: `2026-04-27`.

Исправлен reusable closeout gap: completion package мог содержать общий `## Инструкция пользователю`, но не давать отдельный actionable реестр внешних действий.

- Добавлен defect report `reports/bugs/2026-04-27-external-actions-closeout-gap.md`.
- `template-repo/scenario-pack/00-master-router.md` и `16-done-closeout.md` теперь требуют `Реестр внешних действий` для downstream-consumed changes.
- `template-repo/template/.chatgpt/done-checklist.md` синхронизирован с расширенным generated checklist.
- `template-repo/scripts/create-codex-task-pack.py` добавляет `Когда выполнять` и `Реестр внешних действий` в boundary/checklist.
- `template-repo/scripts/validate-codex-task-pack.py` проверяет, что boundary/checklist не регрессируют к общей фразе вместо actionable external action ledger.

Проверки:

- `python3 template-repo/scripts/validate-codex-task-pack.py .` — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass.

## Проверка Artifact Eval Harness

Дата: `2026-04-27`.

Добавлен optional advanced harness для deterministic desk-eval reusable artifacts без Claude-specific runners и без утяжеления beginner path.

- `docs/artifact-eval-harness.md` описывает общий spec для scenario-pack, handoff blocks, runbooks, policy docs, prompt-like artifacts, template skills и advanced execution artifacts.
- `template-repo/scripts/eval-artifact.py` генерирует deterministic markdown report из `artifact-eval/v1` YAML.
- `template-repo/scripts/validate-artifact-eval-report.py` валидирует report и ловит пустые/фиктивные outputs.
- `template-repo/skills/skill-tester-lite/` обновлён: ручной lite-loop сохранён, machine-readable spec вынесен в optional advanced path.
- `tests/artifact-eval/specs/` содержит sample evals для `master-router`, Codex handoff response, `skill-tester-lite` и `feature-execution-lite`.
- `tests/artifact-eval/reports/` содержит static sample reports; минимум два sample reports теперь доступны как reusable evidence.
- `verify-all.sh quick` запускает `artifact-eval-smoke` в `/tmp` и валидирует static reports.

Проверки:

- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/master-router.yaml --output tests/artifact-eval/reports/master-router.md --json` — pass.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/codex-handoff-response.yaml --output tests/artifact-eval/reports/codex-handoff-response.md --json` — pass.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/skill-tester-lite.yaml --output tests/artifact-eval/reports/skill-tester-lite.md --json` — pass.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/feature-execution-lite.yaml --output tests/artifact-eval/reports/feature-execution-lite.md --json` — pass.
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/*.md` — pass.
- Negative empty/fake report fixture — validator returns non-zero.

## Проверка feature-execution-lite

Дата: `2026-04-27`.

Добавлен optional advanced path для выполнения больших фич волнами. Beginner path не меняется: advanced artifacts создаются только при `--advanced-execution`, а quick verify проверяет структуру шаблонов без требования иметь advanced workspace в каждом проекте.

- `docs/feature-execution-lite.md` описывает Codex-friendly lightweight процесс: dispatcher-not-doer, waves, checkpoint/resume, decisions journal, audit/final wave, max review/fix rounds и final done archival.
- `template-repo/template/work-templates/execution-plan.md.template` добавлен как readable план волн и closeout guardrails.
- `template-repo/template/work-templates/checkpoint.yaml.template` добавлен как resume/checkpoint source.
- `template-repo/template/work-templates/tasks/task.md.template` расширен полями `wave`, `reviewers`, `reviewer_hints`.
- `template-repo/template/work-templates/decisions.md.template` расширен полями execution wave, review rounds и boundary classification.
- `template-repo/scripts/init-feature-workspace.sh --advanced-execution` создаёт `logs/execution-plan.md` и `logs/checkpoint.yaml`; без флага beginner workspace остаётся прежним.
- `template-repo/scripts/validate-feature-execution-lite.py` подключен в `verify-all.sh quick` и generated-project quick contour.

Проверки:

- `python3 template-repo/scripts/validate-feature-execution-lite.py .` — pass.
- `bash template-repo/scripts/init-feature-workspace.sh --feature-id feat-lite-smoke --title "Lite smoke" --advanced-execution --base-dir /tmp/factory-template-feature-lite-work --force` — pass.
- `python3 template-repo/scripts/validate-feature-execution-lite.py --workspace /tmp/factory-template-feature-lite-work/feat-lite-smoke --require-advanced` — pass.
- Positive advanced workspace fixture with done task and `final_verification.status: passed` — pass.
- Negative fixture без checkpoint — validator ловит `missing checkpoint`.
- Negative fixture с пустым `Verify-smoke` и `feature_status: done` без final verification — validator ловит `missing verify-smoke` и `done without final verification`.
- Negative fixture с dependency на более позднюю wave — validator ловит `invalid wave dependency`.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass.
- `bash template-repo/scripts/verify-all.sh ci` — pass.

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

## Проверка physical root normalization

Дата: `2026-04-26`.

- `find . -maxdepth 1 -type d` больше не показывает `.dogfood-bootstrap`, `factory_template_only_pack`, `meta-template-project`, `onboarding-smoke`, `optional-domain-packs`, `packaging`, `registry`, `working-project-examples`, `workspace-packs`.
- `python3 template-repo/scripts/validate-tree-contract.py .` — pass; contract запрещает old active root folders и проверяет approved `factory/producer/*` namespace.
- `python3 template-repo/scripts/validate-mode-parity.py .` — pass.
- `python3 template-repo/scripts/validate-brownfield-transition.py .` — pass.
- `python3 template-repo/scripts/validate-greenfield-conversion.py .` — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass.
- `bash MATRIX_TEST.sh` — pass.
- `bash template-repo/scripts/verify-all.sh ci` — pass.

## Проверка language-contract для handoff

Дата: `2026-04-26`.

- `python3 template-repo/scripts/validate-handoff-response-format.py .chatgpt/handoff-response.md` — pass.
- `python3 template-repo/scripts/validate-handoff-language.py .chatgpt/handoff-response.md` — pass.
- `python3 template-repo/scripts/validate-codex-task-pack.py .` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- Negative matrix case `reject-english-handoff-labels` blocks `Repo:` / `Goal:` labels in copy-paste handoff.

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

## Field pilot evidence / полевая проверка

Статус field evidence на `2026-04-26`: `completed-field-evidence`.

Что реально проверено: repo-controlled GA evidence, controlled novice scenarios, validators, `MATRIX_TEST.sh` и synthetic downstream safe-sync checks.

Что добавлено как field evidence:

- FP-01 `Battle greenfield project` выполнен на real GitHub-backed project repo `mppcoder/greenfield-test`, latest commit `cca68d5`.
- FP-02 `Battle brownfield without repo` выполнен на реальном sanitized OpenClaw+ кейсе с корнями `/root/.openclaw` и `/root/openclaw-plus`.
- Created project repo: `/projects/openclaw-brownfield`, remote `https://github.com/mppcoder/openclaw-brownfield`, latest commit `7b3d1a4`.
- FP-03 `Battle brownfield with repo` выполнен на existing GitHub-backed brownfield repo `mppcoder/openclaw-brownfield`, latest audit commit `3c026fd`.
- Retained artifacts: `/projects/openclaw-brownfield/brownfield/repo-audit.md`, `system-inventory.md`, `as-is-architecture.md`, `change-map.md`, `risks-and-constraints.md`.
- FP-04 `Downstream sync cycle 1` выполнен на той же lineage `mppcoder/openclaw-brownfield`, evidence commit `1826f07`.
- FP-05 `Downstream sync cycle 2` выполнен на той же lineage `mppcoder/openclaw-brownfield`, evidence commit `2dc6515`.
- Post-field conversion: `mppcoder/openclaw-brownfield` converted to `greenfield-product` / `greenfield-converted`, latest pushed commit `1f8fb6d`; live runtime was not mutated.
- Retained sync artifacts: `/projects/openclaw-brownfield/downstream-sync/cycle-1.md`, `/projects/openclaw-brownfield/downstream-sync/cycle-2.md`.
- Retained artifacts: `brownfield/system-inventory.md`, `brownfield/repo-audit.md`, `brownfield/as-is-architecture.md`, `brownfield/source-candidate-map.md`, `brownfield/reconstruction-allowlist.md`, `brownfield/reconstruction-denylist.md`, `brownfield/reconstruction-repo-report.md`, `brownfield/change-map.md`, `reports/release/field-pilot-scenarios/02-brownfield-without-repo.md`, `reports/bugs/bug-037-github-repo-creation-misclassified-as-user-step.md`, `reports/bugs/bug-038-generated-project-root-script-verify-all-wrong-root.md`.
- Runtime remediation не выполнялась; evidence sanitized, secret values не переносились.

Все пять field pilot scenarios выполнены; completed field proof остается post-GA evidence и не переписывает исходную repo-controlled природу решения `2.5.0 GA Ready`.

Полевой roadmap: `docs/releases/2.5.1-field-pilot-roadmap.md`.
Полевой evidence register: `reports/release/2.5-field-pilot-evidence.md`.
Gap report: `reports/bugs/2026-04-26-field-pilot-evidence-gap.md`.

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
- novice onboarding acceptance fixtures (`tests/onboarding-smoke/run-novice-e2e.sh`)
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
- `bash tests/onboarding-smoke/run-novice-e2e.sh` проходит: покрыты wizard fallback-сценарии для всех canonical presets, `--guided` greenfield, `--guided` brownfield без repo, `--guided` brownfield с repo и `--continue` flow.
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
- field evidence для двух downstream sync cycles завершен на same-lineage repo `mppcoder/openclaw-brownfield`; synthetic smoke и controlled pilot не смешиваются с field proof.

## Открытые вопросы
- По bug set `bug-026/027/028` критичных открытых дефектов после remediation не осталось.
- Follow-up для будущего улучшения (не blocker текущего RC): расширить novice long-flow с synthetic smoke до более предметных domain сценариев в downstream проектах.
- GA blocker `reports/bugs/2026-04-26-25-ga-readiness-gap.md` закрыт после добавления KPI evidence.
- Field pilot для `2.5.1-field-pilot` выполнил пять scenarios из `reports/release/field-pilot-scenarios/`.

## Статус CI baseline
- Статус: `green` (GitHub Actions run `24840192862`, 2026-04-23: `verify-baseline` = success, `release-bundle-dry-run` = success; локально подтверждено 2026-04-26 через `verify-all.sh ci`).
- Residual risk: шаг `release-executor` в release workflow остаётся manual/optional и по-прежнему зависит от валидного verified-sync контекста и GitHub auth.
