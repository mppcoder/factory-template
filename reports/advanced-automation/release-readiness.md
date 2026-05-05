# Release readiness / готовность

Дата: 2026-05-05

## Route / маршрут

- selected_project_profile: `factory-template self-improvement / advanced automation`
- selected_scenario: `template-repo/scenario-pack/00-master-router.md`, `template-repo/scenario-pack/15-handoff-to-codex.md`
- pipeline_stage: `implementation -> verification -> release-followup -> closeout`
- handoff_shape: `codex-task-handoff`
- actual_execution_mode: `single-session execution`
- child/subagent count: `0`

## M0-M8 readiness / готовность

| Item | Status | Evidence |
|---|---|---|
| M0 source map | done | `reports/advanced-automation/source-map.md` |
| M1 issue-autofix dispatcher | done | workflow, gate, renderer, runner, issue forms, labels, docs |
| M2 Symphony-compatible spec | done | `WORKFLOW.md`, downstream `WORKFLOW.md`, validator |
| M3 bounded runner | done | `bounded-task-runner.py`, docs, validator |
| M4 curator | done | `factory-curator.py`, curator proposal report, validator |
| M5 advanced gates | done | gates docs root/template, validator |
| M6 downstream materialization | done | generated project smoke in `verify-all quick` |
| M7 verification integration | done | new validators wired into `verify-all quick` |
| M8 release/readout | done | release notes, state docs, advanced automation reports |

## Verification evidence / проверка

- `python3 template-repo/scripts/validate-issue-autofix-support.py .` -> pass
- `python3 template-repo/scripts/validate-symphony-workflow.py .` -> pass
- `python3 template-repo/scripts/validate-bounded-runner.py .` -> pass
- `python3 template-repo/scripts/validate-factory-curator.py .` -> pass
- `python3 template-repo/scripts/validate-advanced-automation-gates.py .` -> pass
- `python3 template-repo/scripts/validate-human-language-layer.py .` -> active findings 0
- `bash VALIDATE_RELEASE_NOTES_SOURCE.sh` -> pass
- `bash template-repo/scripts/verify-all.sh quick` -> `VERIFY-ALL ПРОЙДЕН (quick)`

## Release boundary / граница релиза

This increment prepares advanced automation gates but does not enable full automation, auto-merge, production deploy, security issue autofix, public external submit or unbounded parallel agents.
