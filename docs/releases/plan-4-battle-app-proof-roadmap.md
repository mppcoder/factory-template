# Plan №4: downstream/battle application proof preparation

Дата: 2026-04-27

## Текущее состояние после Plan №3

`Plan №3` завершил `factory-template` template/runtime proof. Repo уже доказал production preset infrastructure path на VPS: deploy, HTTPS healthcheck, backup, disposable restore и rollback drill прошли с `factory-template-placeholder-app:local`.

Граница Plan №4: не переоткрывать Plan №2 field proof и не смешивать template/runtime proof с proof реального downstream/battle приложения. Application-level proof становится отдельным optional future contour, который требует реального generated/battle repo, настоящего `APP_IMAGE`, approved target, secrets outside repo и sanitized transcript.

## Карта источников

| Источник | Вывод для Plan №4 | Граница |
|---|---|---|
| AIF chat 18 conclusions | Нужен доказуемый end-to-end путь от handoff до deploy evidence, а не только reusable artifact docs. | В factory-template фиксируем сценарий и критерии; field run требует downstream repo. |
| Existing `molyanov-ai-dev` comparison | Полезны Project Knowledge, `/done` closeout, wave/checkpoint/eval и pre/post deploy идеи. | Не импортируем `.claude`, Claude commands, TeamCreate или tool-specific workflow. |
| Plan №3 realized state | Template/runtime proof уже passed; reference runtime app существует; runtime QA boundary documented. | Placeholder app не является proof business workload downstream проекта. |
| 2.6 runtime proof report | Infrastructure gates и restore/rollback proof прошли на real VPS. | `APP_IMAGE=factory-template-placeholder-app:local`; real app proof остается будущей внешней границей. |
| Template runtime reference app | Есть repo-owned install/reinstall artifact для first install, smoke и recovery. | Downstream обязан заменить placeholder image своим application image перед app-level claim. |

## Карта gap'ов

| ID | Gap | Current evidence | Target stage | Boundary |
|---|---|---|---|---|
| `P4-GAP-01` | Нет отдельного downstream application proof сценария от placeholder к real `APP_IMAGE`. | `docs/template-runtime-reference-app.md`, 2.6 runtime proof report. | P4-S1 | repo docs/template |
| `P4-GAP-02` | Нет application-level proof report template для healthcheck, migrations, backup, restore, rollback, transcript и secrets boundary. | Runtime proof report есть только для factory infrastructure path. | P4-S1 | generated repo evidence |
| `P4-GAP-03` | Novice-to-deploy scorecard может overclaim pass без evidence. | Novice E2E/KPI evidence покрывают factory onboarding, не app deploy. | P4-S2 | validator/checklist |
| `P4-GAP-04` | Handoff transcript eval покрывает format, но не весь real ChatGPT->Codex handoff output boundary. | `codex-handoff-response` spec and validator. | P4-S3 | artifact eval |
| `P4-GAP-05` | Project Knowledge reuse across a second task не выделен как proof checklist. | Done Loop создает proposal, но reuse evidence is implicit. | P4-S4 | docs/eval |
| `P4-GAP-06` | Real downstream pilot cannot run inside `factory-template` alone. | Current repo has placeholder reference app only. | P4-S5 | external downstream/runtime |
| `P4-GAP-07` | Release continuity должна удерживать distinction: template proof complete, app proof optional future. | Current state/2.6 docs already state boundary. | P4-S6 | release docs |

## Решения add / do-not-add / already-covered

Добавить:

- Guided downstream application proof doc for replacing `factory-template-placeholder-app:local` with real downstream `APP_IMAGE`.
- Application-level proof report template under generated project reports.
- Novice-to-deploy scorecard fields with validator-backed evidence requirements.
- Artifact Eval specs/reports for handoff transcript eval and Project Knowledge reuse proof.
- Release-facing continuity notes that Plan №4 prepares an optional contour without claiming a completed downstream pilot.

Не добавлять:

- Real downstream deploy inside `factory-template` without an actual downstream repo and application image.
- Secrets, real `.env`, private runtime transcript or app-specific credentials in repo.
- Claim that placeholder image proves business workload.
- File-based or multi-block handoff as accepted transcript format.
- Blind copy of stale Project Knowledge into a second task.

Уже покрыто:

- Repo-first routing, self-handoff and advisory/executable split.
- Template/runtime proof with placeholder app image.
- Runtime QA boundary for pre-deploy, deploy, post-deploy healthcheck, backup, restore and rollback.
- Project Knowledge Done Loop proposal generation.
- Artifact Eval Harness baseline and routing-critical specs.

## Поэтапная дорожная карта

| Stage | Goal | Status | Output boundary |
|---|---|---|---|
| P4-S0 | Audit capture, source map, gap map and staged roadmap. | implemented in this artifact | Docs/release planning only. |
| P4-S1 | Add downstream app proof scenario. | implemented as preparation | `docs/downstream-application-proof.md` and generated report template. |
| P4-S2 | Add novice-to-deploy scorecard and evidence validator. | implemented as preparation | Validator plus positive/negative fixtures; no real deploy claim. |
| P4-S3 | Add handoff transcript eval/checklist. | implemented as eval preparation | Artifact Eval spec/report for transcript boundary. |
| P4-S4 | Add Project Knowledge reuse proof checklist. | implemented as eval preparation | Docs plus Artifact Eval spec/report for second-task reuse. |
| P4-S5 | Run real downstream pilot. | blocked by external inputs | Requires downstream repo, real app image, target, secrets outside repo and approval. |
| P4-S6 | Release continuity closeout after pilot. | future boundary | Update release docs only after real downstream evidence exists. |

## Граничное решение

`factory-template` template/runtime proof is complete. Downstream/battle app proof is an optional future contour and must not be claimed until a generated/battle project supplies a real application image and passes app-level deploy, healthcheck, backup, restore and rollback evidence.

## Рекомендация следующего шага

Recommended next step depends on whether a real downstream/battle app exists now:

1. If a real downstream/battle project is selected and has a real `APP_IMAGE`, run P4-S5/P4-S6 on that project. This is the canonical next stage for application-level proof.
2. If no real downstream app exists now, do not simulate P4-S5 inside `factory-template`. Open internal Plan №5 / hardening contour instead.

Recommended Plan №5 focus:

- runner layer and operational reports polish;
- curated/reference pack quality validator beyond structural checks;
- production hardening for git sync fallback strategy;
- novice acceptance expansion from parity smoke to domain scenarios.

This recommendation is part of roadmap closeout: future external proof remains optional, while internal hardening is the next actionable repo-local path when no downstream app is available.
