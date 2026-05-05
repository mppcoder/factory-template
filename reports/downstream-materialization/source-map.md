# Карта источников: downstream materialization Universal Task Control

## Подтверждение маршрута

- selected_project_profile: `factory-template self-improvement / downstream materialization`
- selected_scenario: `template-repo/scenario-pack/00-master-router.md`
- pipeline_stage: `implementation -> verification -> release-followup -> closeout`
- handoff_allowed: `true`
- handoff_shape: `codex-task-handoff`
- execution_policy: `continue-through-roadmap-until-done-or-real-blocker`

## Базовое состояние

Universal Task Control уже реализован в factory-facing слое как repo-native capability:

- canonical template registry: `template-repo/template/.chatgpt/task-registry.yaml`
- lifecycle dashboard section: `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` -> `universal_task_control`
- rendered dashboard/card: `reports/project-lifecycle-dashboard.md`, `reports/project-status-card.md`
- operator docs: `docs/operator/factory-template/07-universal-codex-handoff-factory.md`
- release/readout reports: `reports/universal-task-control-happy-path-smoke.md`, `reports/universal-task-control-release-readiness.md`, `reports/universal-task-control-final-readout.md`
- task queue report: `reports/task-queue.md`

Generated downstream canonical path must be `.chatgpt/task-registry.yaml`. Factory self-improvement canonical path stays `template-repo/template/.chatgpt/task-registry.yaml`.

## Контрольные артефакты

| Layer | Artifact | Current state | Downstream expectation |
|---|---|---|---|
| Registry | `template-repo/template/.chatgpt/task-registry.yaml` | Present, schema `factory-task-registry/v1`, example task terminal `not_applicable`. | Materializes as `.chatgpt/task-registry.yaml`; must not be overwritten blindly during downstream sync. |
| Dashboard source | `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` | Includes `universal_task_control` counters, evidence and no false green status (`pending`). | Materializes as `.chatgpt/project-lifecycle-dashboard.yaml`; registry path should be `.chatgpt/task-registry.yaml` after generation. |
| Queue report | `reports/task-queue.md` | Factory rendered report points to template source. | Generated project should have reports directory placeholder and renderer should write `reports/task-queue.md` from root. |
| Handoff outputs | `reports/handoffs/*.md` | Factory examples exist for `FT-TASK-0001`. | Generated project may create task packs under `reports/handoffs/`; existing examples are not required as downstream state. |
| Issue templates | `.github/ISSUE_TEMPLATE/*.yml` | Present in factory repo. | Must materialize into generated repo and keep local-issue vs upstream-factory-feedback boundary explicit. |
| Scripts | `template-repo/scripts/{validate-task-registry,allocate-task-id,issue-to-task-registry,preview-task-handoff,prepare-task-pack,render-task-queue,task-to-codex-handoff,update-task-status,validate-codex-task-handoff}.py` | Present and covered by `verify-all quick` factory smoke. | Materialize as `scripts/*.py`; defaults must resolve generated root paths without `template-repo/template/` assumptions. |
| Tests policy | `tests/universal-task-control/*` | Factory positive/negative fixtures exist. | Factory-only by default unless a downstream generated-project quick smoke explicitly needs a minimal copy. |
| Operator docs | `docs/operator/factory-template/07-universal-codex-handoff-factory.md` | Factory operator doc exists and mentions generated registry path. | Need downstream-facing docs under `template-repo/template/docs/operator/`. |

## Слой materialization

Primary launcher path:

- `template-repo/launcher.sh` copies `template-repo/template` to destination.
- It then copies `template-repo/scripts/.` to generated `scripts/`.
- It copies scenario pack to generated `template-repo/scenario-pack`.
- It creates/updates generated `.chatgpt/*`, project metadata and placeholder reports.

Wrapper paths:

- root `launcher.sh` delegates to `template-repo/launcher.sh`.
- `template-repo/scripts/first-project-wizard.py` calls `template-repo/launcher.sh`.
- `template-repo/scripts/factory-launcher.py` calls `first-project-wizard.py` for project creation and supports generated-project `--continue`.

## Риски для roadmap

1. Several Universal Task Control scripts default to factory paths like `template-repo/template/.chatgpt/task-registry.yaml`; generated projects need root-relative defaults like `.chatgpt/task-registry.yaml`.
2. Dashboard template currently stores `universal_task_control.registry_path: template-repo/template/.chatgpt/task-registry.yaml`; generated project should materialize `.chatgpt/task-registry.yaml`.
3. Generated template does not yet include downstream-facing operator docs for allocate -> preview -> prepare pack -> ready_for_codex -> queue.
4. Issue templates must be confirmed as copied, because `template-repo/launcher.sh` currently copies only `template/`, scripts, configs and scenario-pack explicitly.
5. Existing `verify-all quick` has factory Universal Task Control smoke, but no generated-project smoke that exercises the materialized root layout.

## P0 targeted-проверка

Use:

```bash
python3 template-repo/scripts/validate-task-registry.py template-repo/template/.chatgpt/task-registry.yaml
python3 template-repo/scripts/render-task-queue.py --registry template-repo/template/.chatgpt/task-registry.yaml --stdout
```
