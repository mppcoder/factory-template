# Universal Task Control downstream materialization / release-отчет

## Сводка

Universal Task Control is now materialized into generated downstream projects instead of remaining only a factory-facing capability.

## Что доставлено

| Area | Delivered artifact | Evidence |
|---|---|---|
| Source map | `reports/downstream-materialization/source-map.md` | factory vs generated paths mapped |
| Contract | `docs/operator/factory-template/universal-task-control-downstream-materialization.md` | downstream payload and acceptance criteria |
| Materializer | `template-repo/launcher.sh` | copies Issue Forms, creates report dirs, normalizes generated dashboard/registry paths |
| Path defaults | `template-repo/scripts/task_control_paths.py` plus task-control scripts | factory defaults stay factory-facing; generated defaults use `.chatgpt/task-registry.yaml` and `scripts/*` |
| Downstream docs | `template-repo/template/docs/operator/universal-task-control.md` | generated operator flow: allocate -> preview -> prepare pack -> `ready_for_codex` -> queue |
| Issue Forms | `.github/ISSUE_TEMPLATE/*.yml` | local issue vs upstream factory feedback wording clarified |
| Smoke report | `reports/downstream-materialization/smoke-report.md` | temporary generated project verified end-to-end |
| Fixtures policy | `reports/downstream-materialization/fixtures-policy.md` | fixtures stay factory-only by default |
| Verify integration | `template-repo/scripts/verify-all.sh` | `downstream-task-control-materialization-smoke` included in quick mode |
| Sync docs | `docs/operator/factory-template/universal-task-control-downstream-sync.md` | no blind overwrite of `.chatgpt/task-registry.yaml` |

## Verification evidence / подтверждения

Targeted:

```bash
python3 template-repo/scripts/validate-task-registry.py
python3 template-repo/scripts/validate-human-language-layer.py .
bash -n template-repo/scripts/verify-all.sh
```

Generated smoke:

```bash
python3 scripts/validate-task-registry.py
python3 scripts/allocate-task-id.py
python3 scripts/preview-task-handoff.py --task-id FT-TASK-0002 --output reports/handoffs/FT-TASK-0002-preview.md
python3 scripts/prepare-task-pack.py --task-id FT-TASK-0002 --mark-ready-for-codex --sync-dashboard --write
python3 scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0002-codex-handoff.md
python3 scripts/render-task-queue.py --output reports/task-queue.md
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
```

Canonical:

```bash
bash template-repo/scripts/verify-all.sh quick
```

Result: `VERIFY-ALL ПРОЙДЕН (quick)`.

## Boundaries / границы

- No Codex child sessions were launched by the generated smoke.
- No GitHub API was used by the generated smoke.
- No production deploy, release publication, auto-merge, security approval or public external report was performed.
- Existing downstream `.chatgpt/task-registry.yaml` remains user-state and must be migrated, not overwritten.
