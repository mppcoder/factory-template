# Plan №3: repo-native audit AIF/Molyanov

Дата: 2026-04-27

## Текущее состояние после Plan №2

`Plan №3` начинается после завершенного `Plan №2` field-proof слоя и не переписывает его evidence.

Уже закрыто:

- `2.5.0` остается `GA Ready` по repo-controlled scorecard и KPI evidence.
- `FP-01`..`FP-05` field proof завершен на GitHub-backed проектах и downstream lineage.
- Downstream sync v3 имеет synthetic multi-cycle proof.
- Artifact Eval Harness уже существует как optional advanced contour с sample specs/reports.
- Project Knowledge Done Loop уже существует и подключен к quick verify.
- `feature-execution-lite` уже существует как optional advanced path с fixtures, validator и Artifact Eval sample target.
- Production VPS path подготовлен как dry-run/report-ready; позднее approved 2.6 runtime proof выполнил deploy, HTTPS healthcheck, backup, disposable restore и rollback drill для infrastructure path с local placeholder application image.

`Plan №3` начался как audit-only follow-up в P3-S0. По состоянию на P3-S6 закрыты repo-local task-state, learning patch loop, expanded Artifact Eval coverage, один real `feature-execution-lite` adoption closeout, runtime QA boundary preparation, approved infrastructure runtime proof и release-facing roadmap continuity pass. Real business application image proof относится к будущему downstream/battle project contour, а не к обязательному proof внутри `factory-template`.

## Карта источников

External ideas используются только как input ideas, а не как foreign workflow import.

| Идея источника | Repo-native интерпретация | Граница |
|---|---|---|
| AIF-lite task-state board | Легкий читаемый слой текущего состояния, owner boundary, next action и blockers. | Без web app, daemon, DB или always-on runtime. |
| Plan -> implement -> review -> done | Уже совместимо с feature workspaces, handoff routing, verification и Project Knowledge Done Loop. | Beginner default должен оставаться легким. |
| Fix/evolve/verify loop | Полезно как learning patch proposal flow, связанный с defect-capture и Project Knowledge. | Без автоматической мутации Project Knowledge без явного proposal. |
| Human-on-the-loop и review convergence | Сохранить явные owner/manual/runtime boundaries и ограниченные review/fix rounds. | Не обещать autonomous background completion. |
| Runtime selection | Оставить в executable routing layer через profiles/launcher/model-routing. | Не делать model switching core value продукта. |
| Subagents vs Skills | Оставить optional advanced helpers там, где они полезны. | Без mandatory TeamCreate или parallel agents для каждой задачи. |
| Molyanov Project Knowledge и `/done` ideas | Уже адаптировано через `project-knowledge/`, Done Loop и archive/proposal flow. | Не импортировать `.claude` layout или Claude-specific commands. |
| Molyanov waves/checkpoint/evals/pre-post deploy ideas | Частично адаптировано через `feature-execution-lite`, Artifact Eval и Production VPS report-first path. | Расширять только через repo-native docs, validators и evidence. |

## Карта gap'ов

| Plan №3 gap | Связанный gap | Текущий evidence | Target stage |
|---|---|---|---|
| `P3-GAP-01` AIF-lite task-state visibility | новый / связан с `P25-GAP-08` | Реализовано через `docs/task-state-lite.md`, template `.chatgpt/task-state.yaml` и validator. | P3-S1 |
| `P3-GAP-02` learning patch / evolve proposal loop | связан с feedback loop и Done Loop | Реализовано через `docs/learning-patch-loop.md`, learning proposal template и validator для reusable bug reports. | P3-S2 |
| `P3-GAP-03` Artifact Eval coverage expansion | `P25-GAP-06` | Реализованы routing-critical specs/reports и negative fixtures; quick smoke расширен. | P3-S3 |
| `P3-GAP-04` `feature-execution-lite` real adoption adoption | `P25-GAP-07` | Реальный workspace `work/completed/plan-3-eval-adoption` закрыт через advanced path и Done Loop. | P3-S4 |
| `P3-GAP-05` pre/post deploy QA as runtime proof boundary | `P25-GAP-04`, `P25-GAP-05` | Реализована prep boundary; approved 2.6 runtime proof выполнил deploy, HTTPS healthcheck, backup, disposable restore и rollback drill для infrastructure path. | P3-S5 / 2.6 |
| `P3-GAP-06` runtime/source-hygiene boundary classifier | `P25-GAP-08` | Реализована docs/report classification для repo-local dry-run, manual secrets, sanitized transcript, downstream sync, external runtime proof и real app proof boundary. | P3-S5 / 2.6 |
| `P3-GAP-07` release-facing consistency pass | `251-STAB-05` | Release-facing docs обновлены после P3-S0..P3-S5 closeouts. | каждый P3 closeout |
| `P3-GAP-08` roadmap continuity after runtime proof | `251-STAB-05`, `P25-GAP-08` | Зафиксирован defect `reports/bugs/2026-04-27-roadmap-continuity-gap.md`; roadmap теперь называет P3-S6/P3-S7 и не оставляет stale pending/demo claims. | P3-S6 |

Plan №3 gaps не reopen `2.5.0 GA Ready` и не превращают placeholder infrastructure proof в proof реального бизнес-приложения. P3-S0..P3-S6 являются implemented/verified evidence для template repo; real app image proof является optional future downstream/battle runtime boundary.

## Добавить / не добавлять / уже покрыто

Добавить:

- Repo-native task-state visibility that can live in docs or `.chatgpt` artifacts.
- Learning patch / evolve proposal loop tied to defect-capture, incoming learnings and Project Knowledge Done Loop.
- Expanded Artifact Eval specs/reports for routing-critical artifacts and negative cases.
- One real `feature-execution-lite` adoption workspace closed through Done Loop.
- Pre-deploy and post-deploy QA boundary docs for 2.6 runtime proof.
- Runtime/source-hygiene boundary classifier for internal repo, downstream sync, manual-only and external runtime work.

Не добавлять:

- AIF Handoff web app.
- Always-on daemon or autonomous background worker promises.
- SQLite, Telegram stack or other runtime service dependencies for the beginner default.
- Claude-specific `.claude` layout, commands or mandatory TeamCreate execution.
- Model switching as the core value proposition of `factory-template`.
- Claims that an already-open Codex live session auto-switches profile/model/reasoning.

Уже покрыто:

- Repo-first routing and self-handoff.
- Executable profile/model routing through repo launcher/config.
- Defect-capture and factory feedback loop.
- Project Knowledge Done Loop and closeout archive/proposal artifacts.
- Optional `feature-execution-lite` structure and validator.
- Artifact Eval Harness baseline.
- Production VPS report-first dry-run boundary.

## Поэтапная дорожная карта

| Stage | Goal | Output boundary |
|---|---|---|
| P3-S0 | Audit capture, карта источников, карта gap'ов и staged roadmap. | Docs-only; без task-state/evolve/eval implementation. |
| P3-S1 | Добавить lightweight AIF-lite task-state visibility. | Реализовано через template `.chatgpt/task-state.yaml`, docs и validator; beginner path остается легким. |
| P3-S2 | Добавить learning patch / evolve proposal loop. | Реализовано через docs, template proposal, template `reports/learnings/` и validator для reusable bugs. |
| P3-S3 | Расширить Artifact Eval coverage. | Реализовано: routing-critical specs/reports и meaningful negative fixtures подключены к quick smoke. |
| P3-S4 | Adoption `feature-execution-lite` на одном real factory change. | Реализовано: `work/completed/plan-3-eval-adoption` закрыт через Done Loop с evidence. |
| P3-S5 | Подготовить runtime QA boundary для 2.6. | Реализовано: pre/post deploy QA, restore, rollback и sanitized transcript requirements documented; на момент P3-S5 это была prep boundary, execution evidence записан в 2.6 runtime proof. |
| P3-S6 | Закрыть roadmap continuity после approved runtime proof. | Реализовано: release-facing status docs выровнены вокруг placeholder infrastructure proof и next external app-proof boundary. |
| P3-S7 | Downstream/battle application proof. | Optional future external/runtime contour: нужен generated/battle project с настоящим application Docker image; внутри `factory-template` этот этап не обязателен. |

## Граничные решения

- Beginner default остается guided и lightweight; advanced execution остается opt-in.
- Dry-run, fake Docker, synthetic downstream и report-ready artifacts не являются production proof.
- Real VPS deploy, restore и rollback требуют explicit user approval, access, secrets entered outside repo и sanitized runtime transcript. Infrastructure path already passed with placeholder app image for this template repo; business app proof belongs to a separate future downstream/battle project boundary.
- Advisory/policy layer и executable routing layer остаются разделенными.
- Надежная единица routing - new task launch; manual UI model selection не равен launcher-driven executable routing.
- `factory-template` остается repo-first handoff/vibecoding template product; model routing поддерживает продукт, но не является его main value.
