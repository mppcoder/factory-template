# Module readiness software update false green

Дата: 2026-05-08

## Симптом

`module_readiness.modules[ops]` был отмечен как `completed`, хотя тот же dashboard содержит:

```yaml
software_update_governance:
  baseline_status: pending
  upgrade_proposal_status: not_started
```

В rendered dashboard это выглядело как полностью green Ops module при незакрытом mandatory software-update governance baseline.

## Evidence

- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`
- `reports/project-lifecycle-dashboard.md`
- `template-repo/template/.chatgpt/software-inventory.yaml`
- `template-repo/template/.chatgpt/software-update-readiness.yaml`
- `python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` passed before this consistency rule existed.

## Root cause

Validator проверял, что green module status имеет evidence, но не проверял cross-field invariant: module green status must not cite `software_update_governance` as a source while that source remains pending.

## Classification

- layer: `shared`
- severity: `medium`
- defect type: false green / validator coverage gap
- reusable factory issue: yes, because generated projects inherit the dashboard schema and can repeat the same misleading readiness state.

## Remediation boundary

Сделать Ops readiness `in_progress` до закрытия software-update baseline and add a validator invariant for green modules that reference `software_update_governance`.
Не заявлять formal DORA/compliance readiness and do not auto-install or auto-upgrade dependencies.
