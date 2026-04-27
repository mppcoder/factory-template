# Реестр gap'ов после 2.5

Date: 2026-04-27

## Область

This register tracks follow-up after `2.5.0 GA Ready`.

Release truth source remains `docs/releases/release-scorecard.yaml`. This file is a planning/evidence register, not a release decision.

## Таблица gap'ов

| ID | Gap | Current evidence | Target line | Status | Owner boundary |
|---|---|---|---|---|---|
| `P25-GAP-01` | Patch/stabilization roadmap was missing after field pilot completion. | This register and `docs/releases/2.5.1-roadmap.md`. | `2.5.1` | planned/remediated docs | repo |
| `P25-GAP-02` | Need explicit split between completed repo-controlled/synthetic proof and pending external runtime proof. | `2.5.1-roadmap`, `2.6-roadmap`, production VPS report. | `2.5.1` | planned/remediated docs | repo |
| `P25-GAP-03` | Downstream sync v3 has synthetic multi-cycle proof, but optional real downstream adoption remains limited. | `reports/release/downstream-multi-cycle-sync-report.md`. | `2.5.1` then `2.6` | open follow-up | downstream repo sync |
| `P25-GAP-04` | Production VPS path is dry-run/report-ready, not real production proof. | `reports/release/production-vps-field-pilot-report.md`. | `2.6` | external pending | real VPS / user approval / secrets |
| `P25-GAP-05` | Backup restore and rollback drill are documented but not executed on real runtime. | `docs/production-vps-field-pilot.md`. | `2.6` | external pending | real VPS / restore target |
| `P25-GAP-06` | Artifact Eval Harness had sample coverage, not broad routing-critical coverage. | `docs/artifact-eval-harness.md`, expanded `tests/artifact-eval/specs/*`, validator-backed reports. | `2.6` | remediated for P3-S3 | repo |
| `P25-GAP-07` | `feature-execution-lite` was implemented and fixture-tested, but real factory feature adoption was pending. | `docs/feature-execution-lite.md`, quick verify smoke, `work/completed/plan-3-eval-adoption`. | `2.6` | remediated for P3-S4 | repo |
| `P25-GAP-08` | Runtime/source-hygiene backlog needs explicit classification by internal/external/downstream/manual boundary. | Current state docs and known limitations. | `2.6` | open | mixed |

## Plan №3 AIF/Molyanov follow-up gaps

Plan №3 records AIF/Molyanov-inspired improvements as repo-native follow-up work. These gaps do not reopen `2.5.0 GA Ready`, do not mix Plan №2 completion evidence with future work and do not import foreign runtime workflow assumptions.

| ID | Gap | Current evidence | Target stage | Status | Owner boundary |
|---|---|---|---|---|---|
| `P3-GAP-01` | AIF-lite task-state visibility is missing as one compact repo artifact. | `docs/task-state-lite.md`, template `.chatgpt/task-state.yaml`, `validate-task-state-lite.py`, quick verify. | P3-S1 | implemented/verified | repo |
| `P3-GAP-02` | Learning patch / evolve proposal loop is not explicit for reusable bugs. | `docs/learning-patch-loop.md`, template `reports/learnings/`, learning proposal template, `validate-learning-patch-loop.py`, negative fixtures and quick verify. | P3-S2 | implemented/verified | repo |
| `P3-GAP-03` | Artifact Eval coverage needs expansion beyond current samples. | Related to `P25-GAP-06`; added routing-critical specs/reports for direct self-handoff, closeout ledger, downstream sync boundary, production proof boundary and extra negative fixtures. | P3-S3 / 2.6 | implemented/verified | repo |
| `P3-GAP-04` | `feature-execution-lite` needs real factory adoption. | Related to `P25-GAP-07`; `work/completed/plan-3-eval-adoption` closes one real advanced workspace through Done Loop with artifact-eval evidence. | P3-S4 / 2.6 | implemented/verified | repo |
| `P3-GAP-05` | Pre/post deploy QA must become an explicit runtime proof boundary. | Related to `P25-GAP-04` and `P25-GAP-05`; P3-S5 prepared pre-deploy QA, post-deploy QA, sanitized transcript and proof-boundary docs, while real deploy/restore/rollback proof remains external pending. | P3-S5 / 2.6 | prepared/not-executed | external runtime |
| `P3-GAP-06` | Runtime/source-hygiene boundary classifier needs a repo-native form. | Related to `P25-GAP-08`; docs now classify repo-local report-ready, manual secrets, sanitized transcript, downstream sync and external runtime proof boundaries. | P3-S5 / 2.6 | prepared/not-executed | mixed |
| `P3-GAP-07` | Release-facing consistency pass is needed after Plan №3 planning and implementation stages. | P3-S0..P3-S5 status is reflected in this register, current state, test report, production VPS report and 2.6 roadmap. | each P3 closeout | implemented/verified | repo |

## `molyanov-ai-dev` adaptation register

Reference snapshot: `pavel-molyanov/molyanov-ai-dev` HEAD `1bfe745d43b0602d8279cb4c9cb7894b1bb56bba`.

| Idea | Factory status | Notes |
|---|---|---|
| Project Knowledge separated from root instruction file | already adapted | Factory uses repo-first `project-knowledge/` and keeps AGENTS/router as policy/routing layer. |
| `/done` style closeout updating Project Knowledge and archiving feature work | already adapted | Factory has `Project Knowledge Done Loop`, `close-feature-workspace.py` and validator. |
| User spec / tech spec / task decomposition with traceability | already adapted | Factory templates and validators preserve user intent and task verification anchors. |
| Wave execution with checkpoint/resume and decisions journal | partially adapted | `feature-execution-lite` exists as optional advanced contour; real adoption is a 2.6 gap. |
| Skill testing through trigger-positive/negative cases and reports | partially adapted | Factory translated the useful part into deterministic Artifact Eval Harness. |
| Pre-deploy and post-deploy QA concepts | useful but not yet fully adapted | Needed for 2.6 production VPS proof and runtime gates. |
| Infrastructure migration/backlog document | useful but not yet fully adapted | Should inform runtime/source-hygiene backlog without importing dev/main assumptions wholesale. |
| Claude-specific command names, agents directory and `.claude` runtime layout | intentionally not adapted | Factory must remain Codex/repo-first and generated-project neutral. |
| Mandatory parallel TeamCreate execution for every task | intentionally not adapted | Good for mature advanced work, too heavy for beginner default path. |
| English-only tech specs | intentionally not adapted as a hard rule | Factory keeps Russian human-facing layer and uses English only for technical identifiers where needed. |

## Release-facing правила

- Do not declare `2.5.1` ready until stabilization gates and verify evidence exist.
- Do not declare `2.6` ready until runtime proof exists for every runtime gate being claimed.
- Do not treat dry-run, fake Docker, synthetic downstream or controlled repo evidence as real production proof.
- Do not commit secrets, runtime transcripts with sensitive values or real `.env` files.
