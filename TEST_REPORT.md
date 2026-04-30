# Отчет TEST REPORT v2.5.3 package-ready

Status source of truth: `docs/releases/release-scorecard.yaml`.
Current scorecard state: `2.5.3 Package Ready`.
TEST_REPORT.md is verification evidence, not the canonical release-status source.

## Проверка Windows beginner bootstrapper MVP

Дата: `2026-04-30`.

Добавлен прозрачный Windows-first путь установки `factory-template` с нуля на VPS: PowerShell entrypoint, remote bash installer, prompts для Codex/ChatGPT Project, README, future exe packaging boundary и targeted validator. Для `2.5.3` bootstrapper дополнительно рекомендует PowerShell 7, показывает `winget` update command и предлагает safe defaults для SSH username, SSH port, target root, incoming dir и fallback archive names. Recommended source остается GitHub clone/download из `mppcoder/factory-template`; release archive + manifest + SHA256 остается fallback; npm install path не поддерживается.

Проверки:

- `python3 -m py_compile windows-bootstrap/tests/validate-windows-bootstrap.py template-repo/scripts/validate-release-package.py` — pass.
- `bash -n windows-bootstrap/scripts/remote-install-factory-template.sh RELEASE_BUILD.sh PRE_RELEASE_AUDIT.sh template-repo/scripts/verify-all.sh` — pass.
- `python3 windows-bootstrap/tests/validate-windows-bootstrap.py .` — pass.
- `python3 template-repo/scripts/validate-tree-contract.py .` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass; active findings `0`.
- `bash RELEASE_BUILD.sh /tmp/factory-v2.5.3-windows-bootstrap-test.zip` — pass; release ZIP, sidecar manifest and SHA256 produced and validated.
- PowerShell runtime check — skipped: PowerShell is not available in this Linux environment; `build-windows-bootstrap.ps1` remains a documented check/build contract.
- Npm support grep — pass: no supported `npm install factory-template` path or `npm_path_supported: true` claim found.
- `bash template-repo/scripts/verify-all.sh quick` — pass.

Full verify decision: не запускался, потому что change затрагивает install UX, release package integration, docs and validators; quick verify plus release build validation cover affected contours.

## Проверка beginner visual dashboard UX

Дата: `2026-04-29`.

Добавлен beginner-first визуальный слой поверх repo-native Project Lifecycle Dashboard без web app, daemon, SQLite, Telegram layer, websocket/live-refresh или background worker default.

- Gap capture: `reports/gaps/beginner-visual-dashboard-ux-gap.md`.
- Operator docs: `docs/operator/factory-template/07-beginner-visual-dashboard-ux.md`, `docs/operator/factory-template/06-project-lifecycle-dashboard.md`, `docs/operator/factory-template/05-orchestration-cockpit-lite.md`.
- Templates: `template-repo/template/.chatgpt/visual-status-card.md.template`, `template-repo/template/.chatgpt/codex-execution-card.md.template`.
- Dashboard contract: `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`.
- Renderer/validator: `template-repo/scripts/render-project-lifecycle-dashboard.py`, `template-repo/scripts/validate-project-lifecycle-dashboard.py`.
- Fixtures: `tests/project-lifecycle-dashboard/valid/`, `tests/project-lifecycle-dashboard/external-action-no-user-required/`, `tests/project-lifecycle-dashboard/codex-completed-no-evidence/`, existing false-green and false-autoswitch fixtures.

Проверки:

- `python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` — pass.
- `python3 template-repo/scripts/validate-project-lifecycle-dashboard.py tests/project-lifecycle-dashboard/valid/project-lifecycle-dashboard.yaml` — pass.
- `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --format markdown-full --output reports/project-lifecycle-dashboard.md` — pass.
- `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input tests/project-lifecycle-dashboard/valid/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout` — pass; карточка показывает external action вместо “ничего”.
- `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input tests/project-lifecycle-dashboard/valid/project-lifecycle-dashboard.yaml --format codex-card --stdout` — pass; карточка показывает route receipt и `selected_model: gpt-5.5`.
- Negative fixture `external-action-no-user-required` — validator returns non-zero as expected.
- Negative fixture `codex-completed-no-evidence` — validator returns non-zero as expected.
- Existing negative fixture `false-autoswitch` — validator returns non-zero as expected.
- `bash template-repo/scripts/verify-all.sh quick` — pass on `2026-04-29`; includes visual dashboard card render smoke and targeted negative fixtures.

Full verify decision: не запускался, потому что change затрагивает docs/templates/dashboard renderer/validator/fixtures и не меняет launcher/runtime/scaffold matrix. Quick verify покрывает affected contours.

## Проверка handoff_shape routing UX

Дата: `2026-04-29`.

Добавлен обязательный выбор вида handoff для новой задачи: `single-agent-handoff` как default для цельных задач и `parent-orchestration-handoff` для больших/multi-agent задач с hard triggers или 3+ soft signals.

- Scenario policy: `template-repo/scenario-pack/00-master-router.md`, `template-repo/scenario-pack/15-handoff-to-codex.md`.
- Routing contract and explanation: `template-repo/codex-routing.yaml`, `template-repo/scripts/explain-codex-route.py`, `template-repo/scripts/validate-route-explain.py`.
- UX validation: `template-repo/scripts/validate-beginner-handoff-ux.py`, `tests/beginner-handoff-ux/`.
- Parent orchestration contract: `template-repo/scripts/orchestrate-codex-handoff.py`, `template-repo/template/.chatgpt/parent-orchestration-plan.yaml.template`, `docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md`.
- Defect capture: `reports/bugs/2026-04-29-handoff-shape-validator-drift.md`, `reports/factory-feedback/feedback-044-handoff-shape-validator-drift.md`.

Проверки:

- `python3 -m py_compile ...` для измененных routing/validator/generator scripts — pass.
- `python3 template-repo/scripts/validate-beginner-handoff-ux.py` — pass.
- Positive fixtures `positive/handoff.md`, `positive/single-agent-handoff.md`, `positive/parent-orchestration-handoff.md` — pass.
- Negative fixtures `multi-block`, `hidden-shell`, `missing-shape`, `wrong-single-large`, `wrong-parent-small` — validators return non-zero as expected.
- `python3 template-repo/scripts/validate-parent-orchestration-plan.py --root . --plan tests/codex-orchestration/fixtures/valid/parent-plan.yaml` — pass.
- `python3 template-repo/scripts/validate-route-explain.py .` — pass.
- `python3 template-repo/scripts/validate-codex-orchestration.py . --plan tests/codex-orchestration/fixtures/valid/parent-plan.yaml` — pass.
- `python3 template-repo/scripts/validate-codex-task-pack.py . && python3 template-repo/scripts/validate-codex-routing.py . && python3 template-repo/scripts/validate-gpt55-prompt-contract.py .` — pass.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/beginner-full-handoff-ux.yaml --output tests/artifact-eval/reports/beginner-full-handoff-ux.md --json` — pass.
- `git diff --check` — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass на финальном состоянии.

Full verify decision: не запускался, потому что change затрагивает scenario/routing/docs/validators/fixtures and generated `.chatgpt` handoff artifacts без runtime, package matrix или onboarding E2E changes; quick verify покрывает affected smoke contours.

## Проверка P9 lifecycle standards navigator

Дата: `2026-04-29`.

P9 добавил standards-based lifecycle navigator/control layer для самого `factory-template` и generated projects без web UI, daemon, background worker или formal certification claim.

- Gap capture: `reports/gaps/lifecycle-standards-navigator-gap.md`.
- ADR: `docs/decisions/lifecycle-standards-stack.md`.
- Registry/watchlist/stage map: `template-repo/standards/lifecycle-standards-registry.yaml`, `template-repo/standards/standards-watchlist.yaml`, `template-repo/standards/lifecycle-stage-map.yaml`.
- Generated gates: `template-repo/template/.chatgpt/standards-gates.yaml`.
- Dashboard integration: `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`, `template-repo/scripts/render-project-lifecycle-dashboard.py`, `template-repo/scripts/validate-project-lifecycle-dashboard.py`.
- Validators/monitoring: `template-repo/scripts/validate-standards-gates.py`, `template-repo/scripts/check-standards-watchlist.py`.
- Docs/beginner UX: `docs/standards/lifecycle-standards-navigator.md`, `docs/operator/factory-template/07-beginner-visual-dashboard-ux.md`.
- Parent orchestration: `reports/orchestration/p9-lifecycle-standards-navigator-parent-plan.yaml`, `reports/orchestration/p9-lifecycle-standards-navigator-report.md`, `reports/orchestration/p9-sessions/`.

Проверки:

- `python3 template-repo/scripts/validate-parent-orchestration-plan.py --root . --plan reports/orchestration/p9-lifecycle-standards-navigator-parent-plan.yaml` — pass.
- `python3 template-repo/scripts/validate-standards-gates.py template-repo/template/.chatgpt/standards-gates.yaml` — pass.
- `python3 template-repo/scripts/check-standards-watchlist.py --root .` — pass.
- Positive standards fixtures `solo-intake` and `commercial-production` — pass.
- Negative standards fixtures `production-claim-solo`, `security-no-evidence`, `accessibility-na-no-reason`, `ai-no-safety`, `stale-overclaim`, `compliance-claim-no-evidence` — validators return non-zero as expected.
- `python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` — pass.
- `python3 template-repo/scripts/validate-orchestration-cockpit.py template-repo/template/.chatgpt/orchestration-cockpit.yaml` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass on `2026-04-29`; includes `standards-navigator-smoke` and extended lifecycle dashboard negative smoke.

Full verify decision: не запускался, потому что change затрагивает docs/templates/validators/fixtures/dashboard reports без изменения launcher/runtime/scaffold matrix. Quick verify покрывает targeted validator layer and release-facing guardrails.

## Проверка Plan №6 orchestration productization

Дата: `2026-04-28`.

Plan №6 добавил beginner-first productization слой поверх Plan №5, не переоткрывая runner/fallback/curated validator и не заявляя real downstream/battle app proof.

- Roadmap/source map: `docs/releases/plan-6-orchestration-productization-roadmap.md`.
- Defect/gap capture: `reports/bugs/2026-04-28-plan-6-orchestration-productization-gap.md`.
- Cockpit guide: `docs/operator/factory-template/05-orchestration-cockpit-lite.md`.
- Cockpit template/report: `template-repo/template/.chatgpt/orchestration-cockpit.yaml`, `reports/orchestration/orchestration-cockpit.md`.
- Parent plan template/validator: `template-repo/template/.chatgpt/parent-orchestration-plan.yaml.template`, `template-repo/scripts/validate-parent-orchestration-plan.py`.
- Route explanation: `template-repo/scripts/explain-codex-route.py`, `template-repo/scripts/validate-route-explain.py`.
- Beginner UX scorecard: `template-repo/scripts/validate-beginner-handoff-ux.py`, `tests/beginner-handoff-ux/`, `tests/artifact-eval/specs/beginner-full-handoff-ux.yaml`.
- Safe rehearsal: `reports/orchestration/plan-6-safe-rehearsal.md`.

Проверки:

- `python3 -m py_compile template-repo/scripts/orchestrate-codex-handoff.py template-repo/scripts/validate-orchestration-cockpit.py template-repo/scripts/render-orchestration-cockpit.py template-repo/scripts/validate_orchestration_cockpit_import.py template-repo/scripts/validate-parent-orchestration-plan.py template-repo/scripts/explain-codex-route.py template-repo/scripts/validate-route-explain.py template-repo/scripts/validate-beginner-handoff-ux.py` — pass.
- `python3 template-repo/scripts/validate-parent-orchestration-plan.py --root . --plan tests/codex-orchestration/fixtures/future-placeholder/parent-plan.yaml` — pass.
- Negative parent plan fixture `missing-child-routing` — validator returns non-zero as expected.
- `python3 template-repo/scripts/validate-orchestration-cockpit.py template-repo/template/.chatgpt/orchestration-cockpit.yaml` — pass.
- `python3 template-repo/scripts/render-orchestration-cockpit.py --input template-repo/template/.chatgpt/orchestration-cockpit.yaml --output reports/orchestration/orchestration-cockpit.md` — pass.
- `python3 template-repo/scripts/validate-route-explain.py .` — pass.
- `python3 template-repo/scripts/validate-beginner-handoff-ux.py tests/beginner-handoff-ux/positive/handoff.md` — pass.
- Negative beginner UX fixtures `multi-block` and `hidden-shell` — validator returns non-zero as expected.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/beginner-full-handoff-ux.yaml --output tests/artifact-eval/reports/beginner-full-handoff-ux.md --json` — pass.
- `python3 template-repo/scripts/validate-codex-orchestration.py . --plan tests/codex-orchestration/fixtures/future-placeholder/parent-plan.yaml` — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-28`; includes `plan6-productization-smoke`.

Full verify decision: не запускался, потому что Plan №6 изменяет docs/templates/validators/fixtures и quick verification уже покрывает targeted productization smoke plus existing release-facing validators. Runtime, packaging matrix, onboarding E2E and downstream examples не менялись.

## Проверка Plan №5 internal hardening

Дата: `2026-04-28`.

Plan №5 добавил internal hardening contour после Plan №4 без переоткрытия `2.6` template/runtime proof и без заявления P4-S5 real downstream app pilot.

- Roadmap/source map: `docs/releases/plan-5-internal-hardening-roadmap.md`.
- VPS Remote SSH-first runbook: `docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md`.
- Runner: `template-repo/scripts/orchestrate-codex-handoff.py`.
- Orchestration validator: `template-repo/scripts/validate-codex-orchestration.py`.
- Curated pack validator: `template-repo/scripts/validate-curated-pack-quality.py`.
- Git sync fallback evidence validator: `template-repo/scripts/validate-verified-sync-fallback-evidence.py`.
- Positive/negative fixtures: `tests/codex-orchestration/`, `tests/curated-pack-quality/`.
- Artifact Eval: `vps-remote-ssh-orchestration`.
- Domain acceptance expansion: `docs/domain-scenario-acceptance.md`.
- Fallback evidence: `reports/release/verified-sync-fallback-evidence.md`.

Проверки:

- `python3 -m py_compile template-repo/scripts/orchestrate-codex-handoff.py template-repo/scripts/validate-codex-orchestration.py template-repo/scripts/orchestrate_codex_handoff_import.py template-repo/scripts/validate-curated-pack-quality.py template-repo/scripts/validate-verified-sync-fallback-evidence.py` — pass.
- `python3 template-repo/scripts/validate-codex-orchestration.py .` — pass.
- Negative orchestration fixtures for missing child routing, secret-like content, multi-block handoff, user action as child subtask and invalid placeholder metadata — pass, validators return non-zero.
- `python3 template-repo/scripts/orchestrate-codex-handoff.py --root . --plan tests/codex-orchestration/fixtures/valid/parent-plan.yaml --report reports/orchestration/parent-orchestration-report.md` — pass, dry-run report written.
- `python3 template-repo/scripts/validate-curated-pack-quality.py .` — pass.
- Curated pack positive fixture — pass; missing-routing-doc negative fixture returns non-zero as expected.
- `python3 template-repo/scripts/validate-verified-sync-fallback-evidence.py reports/release/verified-sync-fallback-evidence.md` — pass.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/vps-remote-ssh-orchestration.yaml --output tests/artifact-eval/reports/vps-remote-ssh-orchestration.md --json` — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-28`.

Follow-up на `2026-04-28`: orchestration contract усилен правилом `user_actions_policy: defer-to-final-closeout`. Все user-required/external/runtime/downstream действия уходят в конец parent plan, internal child subtasks продолжают работу на safe temporary placeholders, а parent report выводит `deferred_user_actions` и `placeholder_replacements` как финальные напоминания о замене на real data.

Integrity/security follow-up на `2026-04-28`: runner fail-fast исправлен после post-audit finding. Invalid/secret-like orchestration plans now fail before `sessions_dir`, child session files, prompt/session artifacts or parent reports are created.

Дополнительные проверки:

- Direct runner negative smoke against `tests/codex-orchestration/fixtures/secret-like/parent-plan.yaml` — pass, runner returns non-zero and does not create `sessions/secret-child.md`.
- `template-repo/scripts/verify-all.sh quick` now includes `codex-orchestration-runner-negative-smoke` with regression message `FAIL: invalid orchestration plan wrote child session files before failing`.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-28` after integrity follow-up.
- `bash template-repo/scripts/verify-all.sh full` — pass на `2026-04-28` after integrity follow-up; onboarding acceptance evidence refreshed in `tests/onboarding-smoke/ACCEPTANCE_REPORT.md`.
- Defect report: `reports/bugs/2026-04-28-plan-5-orchestration-runner-write-before-fail.md`.
- Factory feedback: `reports/factory-feedback/feedback-040-plan-5-orchestration-runner-write-before-fail.md`.

Handoff terminology follow-up на `2026-04-28`: исправлена ambiguity, при которой `chatgpt-handoff` acceptance мог называться `self-handoff`. Теперь `chatgpt-handoff` исполняет входящий handoff и допускает только `handoff receipt` / `route receipt`; `self-handoff` зарезервирован для `direct-task` и отдельного incidental defect task boundary.

- Defect report: `reports/bugs/2026-04-28-chatgpt-handoff-self-handoff-duplication.md`.
- Factory feedback: `reports/factory-feedback/feedback-041-chatgpt-handoff-self-handoff-duplication.md`.

One-paste orchestration follow-up на `2026-04-28`: full handoff UX уточнен как one-paste autopilot. После вставки parent handoff в Codex в VPS Remote SSH repo context parent Codex сам запускает repo-native orchestrator с validation gate и `--execute`; ручной shell-запуск оператора оставлен только как troubleshooting/strict fallback.

- Defect report: `reports/bugs/2026-04-28-one-paste-orchestration-autopilot-gap.md`.
- Factory feedback: `reports/factory-feedback/feedback-042-one-paste-orchestration-autopilot-gap.md`.

## Проверка Plan №4 P4-S0/P4-S4 preparation

Дата: `2026-04-27`.

Plan №4 подготовил optional downstream/battle application proof contour после Plan №3, не смешивая его с уже passed `factory-template` template/runtime proof.

- Audit/roadmap: `docs/releases/plan-4-battle-app-proof-roadmap.md`.
- Gap capture: `reports/bugs/2026-04-27-plan-4-audit-gap.md`, `reports/bugs/2026-04-27-plan-4-downstream-proof-gap.md`, `reports/bugs/2026-04-27-plan-4-handoff-pk-reuse-gap.md`.
- Downstream proof scenario: `docs/downstream-application-proof.md`.
- Report template: `template-repo/template/reports/release/downstream-application-proof-report.md.template`.
- Validator: `template-repo/scripts/validate-downstream-application-proof.py`.
- Positive/negative fixtures: `tests/downstream-application-proof/valid/` and `tests/downstream-application-proof/missing-evidence/`.
- Artifact Eval additions: `handoff-transcript-eval` and `project-knowledge-reuse-proof` specs/reports.
- Boundary: P4-S5/P4-S6 real pilot is blocked until downstream repo, real app image, target, external secrets/approval and sanitized transcript exist.
- Next-step recommendation: if a real downstream/battle app exists, run P4-S5/P4-S6 there; otherwise open internal Plan №5 / hardening contour.

## Проверка roadmap next-step recommendation

Дата: `2026-04-28`.

Исправлен guidance defect: roadmap closeout now names the recommended next step instead of leaving the user with two unranked branches.

- Defect report: `reports/bugs/2026-04-28-roadmap-next-step-recommendation-gap.md`.
- `docs/releases/plan-4-battle-app-proof-roadmap.md` now recommends P4-S5/P4-S6 only when a real downstream/battle app exists.
- If no real downstream app exists, the recommended actionable path is internal Plan №5 / hardening contour.
- Router, `16-done-closeout`, boundary-actions and checklist now require roadmap readouts with multiple branches to name the recommended branch and fallback branch.
- `done-closeout-external-actions` Artifact Eval now includes a regression case for roadmap branch recommendation.

Проверки:

- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/done-closeout-external-actions.yaml --output tests/artifact-eval/reports/done-closeout-external-actions.md --json` — pass.
- `python3 template-repo/scripts/validate-codex-task-pack.py .` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-28`.

Проверки:

- `python3 template-repo/scripts/validate-downstream-application-proof.py tests/downstream-application-proof/valid/downstream-application-proof-report.md` — pass.
- Negative fixture `tests/downstream-application-proof/missing-evidence/downstream-application-proof-report.md` — validator returns non-zero as expected.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/handoff-transcript-eval.yaml --output tests/artifact-eval/reports/handoff-transcript-eval.md --json` — pass.
- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/project-knowledge-reuse-proof.yaml --output tests/artifact-eval/reports/project-knowledge-reuse-proof.md --json` — pass.
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/handoff-transcript-eval.md tests/artifact-eval/reports/project-knowledge-reuse-proof.md` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-27`.

## Проверка 2.6 runtime proof

Дата: `2026-04-27`.

Approved runtime proof выполнен на VPS `72.56.26.209` в `/projects/factory-template` с preset `production`.

- Pre-deploy env validation — pass; initial demo `APP_IMAGE` warning remediated by local placeholder app image.
- Production dry-run — pass.
- Real deploy — pass.
- HTTPS healthcheck — pass.
- Backup run — pass, SQL dump created.
- Restore test — pass into disposable DB, then dropped.
- Rollback drill — pass with local candidate tag and rollback to previous image.
- Sanitized report: `reports/release/2.6-runtime-proof-report.md`.
- Boundary: `APP_IMAGE=factory-template-placeholder-app:local`, so this is `factory-template` template infrastructure proof with a placeholder application image; it is not proof of a separate generated/battle project's real business workload.
- Generated placeholder app image and static page installed after runtime proof; live URL `https://72-56-26-209.sslip.io/`, image URL `https://72-56-26-209.sslip.io/placeholder.svg`.

Runtime defects remediated:

- `reports/bugs/2026-04-27-runtime-env-user-burden-gap.md`.
- `reports/bugs/2026-04-27-backup-hook-command-splitting.md`.
- `reports/bugs/2026-04-27-skip-pull-defeated-by-pull-policy.md`.
- `reports/bugs/2026-04-27-app-image-placeholder-burden-gap.md`.
- `reports/bugs/2026-04-27-roadmap-continuity-gap.md`.

Проверки repo после remediation:

- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-27`.

## Проверка template runtime reference app

Дата: `2026-04-27`.

Уточнен install/reinstall contract для самого `factory-template`: шаблон имеет repo-owned reference runtime app, а не требует внешний npm package или боевое приложение.

- Reference docs: `docs/template-runtime-reference-app.md`.
- Build script: `template-repo/scripts/build-placeholder-app-image.py`.
- Runtime image tag: `factory-template-placeholder-app:local`.
- Назначение: first install, smoke check, recovery после VPS падения, пока downstream/battle app отсутствует.
- Boundary: public Docker registry image или npm package остаются optional future packaging contour, не blocker текущего template proof.

## Проверка 2.6 roadmap closeout

Дата: `2026-04-27`.

2.6 roadmap закрыт для `factory-template` template/runtime scope.

- P3-S0..P3-S6 выполнены и проверены.
- Production VPS deploy, HTTPS healthcheck, backup, disposable restore and rollback drill выполнены.
- Reference runtime app для install/reinstall определен.
- Optional downstream/battle application proof вынесен за пределы текущего roadmap closure.
- Defect report: `reports/bugs/2026-04-27-roadmap-closure-status-gap.md`.

## Проверка closeout continuation outcome

Дата: `2026-04-27`.

Исправлен reusable closeout defect: финал больше не может ограничиться только `Внешних действий не требуется.` без ответа "что дальше" или "текущий scope полностью закрыт".

- Defect report: `reports/bugs/2026-04-27-closeout-continuation-outcome-gap.md`.
- `template-repo/scenario-pack/00-master-router.md` и `16-done-closeout.md` требуют continuation outcome.
- `.chatgpt/boundary-actions.md`, `.chatgpt/done-checklist.md` и template checklist обновлены.
- `validate-codex-task-pack.py` проверяет generated closeout guidance на continuation outcome.
- Direct-task completion rule теперь требует fully-done формулировку для no-external-action closeout.

## Проверка Plan №3 P3-S6 roadmap continuity

Дата: `2026-04-27`.

Исправлен release-facing разрыв после 2.6 runtime proof: roadmap/status docs больше не говорят одновременно `pending VPS proof`, `demo nginx` и `placeholder app live`.

- `docs/releases/2.6-roadmap.md` теперь фиксирует P3-S6 closeout и отделяет optional future downstream/battle application proof boundary.
- `docs/releases/plan-3-aif-molyanov-audit.md` расширен до P3-S6 roadmap closeout.
- `CURRENT_FUNCTIONAL_STATE.md`, `reports/release/production-vps-field-pilot-report.md` и этот report выровнены вокруг статуса `template-runtime-proof-passed`.
- Новый release-ready status не объявлен.

## Проверка Plan №3 P3-S5

Дата: `2026-04-27`.

Подготовлена runtime QA boundary для 2.6 без real VPS mutation, без запроса/хранения secrets и без заявления production proof.

- `docs/production-vps-field-pilot.md` явно разделяет pre-deploy QA, post-deploy QA, backup restore test, rollback drill и sanitized runtime transcript requirements.
- `docs/deploy-on-vps.md` фиксирует, что dry-run/report-ready не является production proof.
- `reports/release/production-vps-field-pilot-report.md` обновлен как P3-S5 prepared/not-executed evidence.
- `operator-dashboard.py` и `validate-operator-env.py` field-pilot reports теперь пишут sanitized transcript boundary.
- `verify-all.sh quick` проверяет наличие transcript boundary в generated field-pilot reports.
- `production-vps-proof-boundary` Artifact Eval spec/report покрывает pre/post deploy QA и запрет runtime proof overclaim.

Проверки:

- `python3 template-repo/scripts/eval-artifact.py tests/artifact-eval/specs/production-vps-proof-boundary.yaml --output tests/artifact-eval/reports/production-vps-proof-boundary.md --json` — pass.
- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/production-vps-proof-boundary.md` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-27`.

## Проверка Plan №3 P3-S3/P3-S4

Дата: `2026-04-27`.

Расширены Artifact Eval coverage и real `feature-execution-lite` adoption без изменения beginner default и без заявления production proof.

- Добавлены specs/reports для `direct-task-self-handoff`, `done-closeout-external-actions`, `downstream-sync-boundary` и `production-vps-proof-boundary`.
- Существующие `codex-handoff-response` и `feature-execution-lite` specs получили negative fixtures для multi-block/file-based handoff и done without final verification.
- `template-repo/scripts/verify-all.sh quick` теперь smoke-проверяет расширенный набор Artifact Eval reports.
- Закрыт real advanced workspace `work/completed/plan-3-eval-adoption` с `done-report.md`, `project-knowledge-update-proposal.md`, `downstream-impact.md`, task waves, checkpoint и decisions.
- Incidental naming defect закрыт в текущем scope: `reports/bugs/2026-04-27-plan-3-restricted-term-workspace-id.md`; workspace evidence переименован в `plan-3-eval-adoption`, чтобы не нарушать tree contract.
- At P3-S3/P3-S4 time P3-S5 runtime QA была будущей boundary; later approved 2.6 runtime proof completed infrastructure deploy, backup, restore and rollback evidence with placeholder app boundary.

Проверки:

- `python3 template-repo/scripts/validate-artifact-eval-report.py tests/artifact-eval/reports/*.md` — pass.
- `python3 template-repo/scripts/validate-feature-execution-lite.py --workspace work/features/plan-3-eval-adoption --require-advanced` — pass до closeout.
- `python3 template-repo/scripts/validate-project-knowledge-update.py . --workspace work/completed/plan-3-eval-adoption` — pass.
- `python3 template-repo/scripts/validate-feature-execution-lite.py .` — pass.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-27`.

## Проверка Plan №3 P3-S1/P3-S2

Дата: `2026-04-27`.

Добавлены repo-native lightweight улучшения без AIF Handoff web app, daemon, SQLite, Telegram stack или autonomous background promises.

- `docs/task-state-lite.md` описывает отдельный `.chatgpt/task-state.yaml` слой для current state, owner boundary, next action, blockers и boundary-разделения.
- `template-repo/template/.chatgpt/task-state.yaml` добавлен как beginner-safe template artifact; root-level project-instance state artifact не требуется.
- `template-repo/scripts/validate-task-state-lite.py` проверяет schema, current_state, owner boundary, next action, blocker и internal/external/runtime/downstream separation.
- `docs/learning-patch-loop.md` описывает proposal loop для reusable bugs поверх defect-capture и Project Knowledge Done Loop.
- `template-repo/template/reports/learnings/learning-patch-proposal.md.template` добавлен как repo-native proposal template для generated projects.
- `template-repo/scripts/validate-learning-patch-loop.py` требует learning proposal или `not_required` reason для явно reusable bug reports и блокирует fake/overclaim proposals.
- `template-repo/scripts/verify-all.sh quick` подключает оба validators и targeted negative fixtures для missing state, fake learning proposal и overclaim.
- Beginner default остается легким: advanced execution, web UI и runtime services не стали обязательными.
- Root contamination remediation зафиксирован в `reports/bugs/2026-04-27-plan-3-root-contamination.md`: root-level `.chatgpt/task-state.yaml` и `reports/learnings/.gitkeep` удалены, source-of-truth оставлен в `template-repo/template/`.

Проверки:

- `python3 template-repo/scripts/validate-task-state-lite.py .` — pass.
- `python3 template-repo/scripts/validate-learning-patch-loop.py .` — pass.
- Targeted negative fixtures: missing state, fake learning proposal, overclaim — pass, validator возвращает non-zero.
- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-27`.

## Проверка Plan №3 AIF/Molyanov audit P3-S0

Дата: `2026-04-27`.

Добавлен audit-only planning artifact для Plan №3 без реализации task-state/evolve/eval кода.

- `docs/releases/plan-3-aif-molyanov-audit.md` фиксирует current state after Plan №2, source map, gap map, add/do-not-add/already-covered decisions, staged roadmap и runtime boundary decisions.
- `docs/releases/post-2.5-gap-register.md` расширен gap'ами `P3-GAP-01`..`P3-GAP-07`.
- `CURRENT_FUNCTIONAL_STATE.md` обновлен так, чтобы Plan №3 P3-S0 был виден как planning/audit status, а completed FP-01..FP-05 не выглядели pending.
- Этот stage не добавлял task-state artifact, learning/evolve validator, новые Artifact Eval specs или real `feature-execution-lite` adoption workspace.
- Новый release-ready status для этого historical stage не объявлялся; актуальный scorecard позже переведен в `2.5.3 Package Ready`.

Проверки:

- `python3 template-repo/scripts/validate-human-language-layer.py .` — pass, active findings `0`.
- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-27`.

## Проверка post-2.5 release planning

Дата: `2026-04-27`.

Добавлен planning layer после `2.5.0 GA Ready`.

- `docs/releases/2.5.1-roadmap.md` фиксирует patch/stabilization scope: downstream sync v3 stabilization, field pilot evidence, closeout/boundary guardrails, optional downstream sync adoption.
- `docs/releases/2.6-roadmap.md` выносит deeper scope: real production VPS deploy, backup restore, rollback drill, expanded artifact eval, `feature-execution-lite` adoption и runtime/source-hygiene backlog.
- `docs/releases/post-2.5-gap-register.md` разделяет completed repo-controlled/synthetic/template-infrastructure proof и optional downstream/battle application proof.
- `reports/bugs/2026-04-27-post-25-release-planning-gap.md` фиксирует release-followup planning gap как remediated in current scope.
- Сравнение с `pavel-molyanov/molyanov-ai-dev` записано как adaptation register: already adapted, useful but not yet adapted, intentionally not adapted.
- Новый release-ready status для этого historical stage не объявлялся; актуальный scorecard позже переведен в `2.5.3 Package Ready`.

Проверки:

- `bash template-repo/scripts/verify-all.sh quick` — pass на `2026-04-27`.

## Проверка Production VPS Field Pilot

Дата: `2026-04-27`.

Подготовлен safe field pilot path для single-VPS deploy без destructive действий по умолчанию.

- `docs/production-vps-field-pilot.md` добавляет runbook `starter -> app-db -> reverse-proxy-tls -> backup -> healthcheck -> rollback drill`.
- `docs/deploy-on-vps.md` теперь явно отделяет dry-run/report evidence от real production proof.
- `reports/release/production-vps-field-pilot-report.md` фиксирует текущий статус: `template-runtime-proof-passed`.
- `template-repo/scripts/deploy-dry-run.sh --field-pilot-report` пишет markdown field pilot report после успешного dry-run.
- `template-repo/scripts/deploy-local-vps.sh --field-pilot-report` пишет report после operator-approved deploy.
- `template-repo/scripts/operator-dashboard.py --field-pilot-report` собирает runtime/evidence summary без deploy.
- `template-repo/scripts/validate-operator-env.py --field-pilot-report` пишет env readiness report.
- Starter остаётся default, production presets остаются opt-in.
- DNS, firewall, Docker Compose, env secrets и backup restore checklist зафиксированы в runbook/report.
- Real VPS deploy, restore test и rollback drill выполнены после explicit approval для `factory-template` template infrastructure path; real business application image proof относится только к будущему downstream/battle project.

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
Затем закрыт follow-up UX defect: отсутствие внешних действий больше не должно превращаться в длинный audit-style register с no-op строками.

- Добавлен defect report `reports/bugs/2026-04-27-external-actions-closeout-gap.md`.
- Добавлен defect report `reports/bugs/2026-04-27-external-actions-oververbose-closeout.md`.
- `template-repo/scenario-pack/00-master-router.md` и `16-done-closeout.md` теперь требуют `Реестр внешних действий` для downstream-consumed changes.
- Для no-action closeout теперь требуется compact outcome: `Внешних действий не требуется.` или `Внешние действия: нет`.
- Если реальные external actions есть, `Реестр внешних действий` содержит только actionable строки, а не все возможные contour'ы.
- `template-repo/template/.chatgpt/done-checklist.md` синхронизирован с расширенным generated checklist.
- `template-repo/scripts/create-codex-task-pack.py` добавляет compact external-actions contract в boundary/checklist.
- `template-repo/scripts/validate-codex-task-pack.py` проверяет, что boundary/checklist не регрессируют к общей фразе и ловит oververbose no-op ledger.
- Manual sample check подтверждает: no-action closeout принимается как `Внешних действий не требуется.`, one-action ledger принимается, all-noop ledger блокируется.

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
- `bash template-repo/scripts/verify-all.sh ci` повторно проходит на `2026-04-27` после добавления downstream multi-cycle sync proof.
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
- `MATRIX_TEST.sh` подтверждает downstream multi-cycle sync proof: initial safe sync, project-owned manual edits, advisory-review без auto-apply, safe-generated/safe-clone update, rollback после нескольких циклов и `converted_greenfield` brownfield history protection.
- Production VPS field-pilot downstream boundary проверен synthetic proof: deploy templates/scripts идут как `safe-generated`, field-pilot docs/report как `advisory-review`, а `deploy/.env`, `.factory-runtime/`, runtime transcripts, real VPS approval и secrets остаются manual-only.
- Release evidence: `reports/release/downstream-multi-cycle-sync-report.md`.
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
- 2.6 runtime proof follow-up исправил лишнее требование к пользователю принести `APP_IMAGE`: добавлен local placeholder application image builder `template-repo/scripts/build-placeholder-app-image.py`; live VPS использует `factory-template-placeholder-app:local` для template proof. Реальный application image нужен только в отдельном downstream/battle project proof.

## Что вошло в релиз 2.5.1
- install-from-scratch release package contract: manifest, SHA256 checksum and zip validator;
- fallback manual upload path through `/projects/factory-template/_incoming`;
- explicit npm support status: npm path is not supported without `package.json`;
- template/meta/root versioning and release package metadata synchronized under `2.5.1`.

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
