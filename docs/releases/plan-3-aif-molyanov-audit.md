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
- Production VPS path подготовлен как dry-run/report-ready, но real VPS deploy, backup restore и rollback drill остаются external runtime proof.

`Plan №3` является audit-only follow-up: он фиксирует карту источников, карту gap'ов и поэтапную дорожную карту для AIF/Molyanov-inspired улучшений, не реализуя task-state, evolve loop или новые eval specs в этом stage.

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
| `P3-GAP-01` AIF-lite task-state visibility | новый / связан с `P25-GAP-08` | Current state есть в release docs, но компактного task-state artifact пока нет. | P3-S1 |
| `P3-GAP-02` learning patch / evolve proposal loop | связан с feedback loop и Done Loop | Defect-capture и Project Knowledge proposal уже есть, но reusable bug learnings не классифицируются единообразно как proposal vs `not_required`. | P3-S2 |
| `P3-GAP-03` Artifact Eval coverage expansion | `P25-GAP-06` | Harness имеет sample coverage для routing-critical artifacts, но не broad negative coverage. | P3-S3 |
| `P3-GAP-04` `feature-execution-lite` real dogfood adoption | `P25-GAP-07` | Validator и fixtures есть, но real factory feature еще не закрывалась через advanced path как durable evidence. | P3-S4 |
| `P3-GAP-05` pre/post deploy QA as runtime proof boundary | `P25-GAP-04`, `P25-GAP-05` | Production path report-ready; real deploy, restore и rollback не заявлены как выполненные. | P3-S5 |
| `P3-GAP-06` runtime/source-hygiene boundary classifier | `P25-GAP-08` | Boundary concepts есть, но runtime/source-hygiene backlog требует явного classifier. | P3-S5 / 2.6 |
| `P3-GAP-07` release-facing consistency pass | `251-STAB-05` | Release-facing docs требуют consistency pass после P3 planning и будущих implementation stages. | каждый P3 closeout |

Plan №3 gaps являются follow-up planning items. Они не reopen `2.5.0 GA Ready` и не превращают pending runtime proof в completed proof.

## Добавить / не добавлять / уже покрыто

Добавить:

- Repo-native task-state visibility that can live in docs or `.chatgpt` artifacts.
- Learning patch / evolve proposal loop tied to defect-capture, incoming learnings and Project Knowledge Done Loop.
- Expanded Artifact Eval specs/reports for routing-critical artifacts and negative cases.
- One real `feature-execution-lite` dogfood workspace closed through Done Loop.
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
| P3-S1 | Добавить lightweight AIF-lite task-state visibility. | Только beginner-safe doc/template/validator layer. |
| P3-S2 | Добавить learning patch / evolve proposal loop. | Reusable bugs требуют proposal или `not_required` reason. |
| P3-S3 | Расширить Artifact Eval coverage. | Больше routing-critical specs/reports и meaningful negative fixtures. |
| P3-S4 | Dogfood `feature-execution-lite` на одном real factory change. | Real workspace закрыт через Done Loop с evidence. |
| P3-S5 | Подготовить runtime QA boundary для 2.6. | Pre/post deploy QA, restore, rollback и transcript requirements documented; без real VPS mutation. |

## Граничные решения

- Beginner default остается guided и lightweight; advanced execution остается opt-in.
- Dry-run, fake Docker, synthetic downstream и report-ready artifacts не являются production proof.
- Real VPS deploy, restore и rollback требуют explicit user approval, access, secrets entered outside repo и sanitized runtime transcript.
- Advisory/policy layer и executable routing layer остаются разделенными.
- Надежная единица routing - new task launch; manual UI model selection не равен launcher-driven executable routing.
- `factory-template` остается repo-first handoff/vibecoding template product; model routing поддерживает продукт, но не является его main value.
