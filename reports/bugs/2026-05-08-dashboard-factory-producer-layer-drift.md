# Dashboard factory producer layer drift

Дата: 2026-05-08

## Симптом

`FACTORY_MANIFEST.yaml` для root проекта `factory-template` содержит:

```yaml
factory_producer_layer: true
```

При этом repo renderer для карточки и `reports/project-lifecycle-dashboard.md` показывал:

```text
Factory producer layer: False
```

## Evidence

- `FACTORY_MANIFEST.yaml`
- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`
- `reports/project-lifecycle-dashboard.md`
- `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout`

## Root cause

Dashboard YAML является template/generated-project artifact и правильно держит `project.factory_producer_owned_layer: false` как downstream default.
Но renderer при использовании этого YAML для самого `factory-template` не учитывал root `FACTORY_MANIFEST.yaml`, где producer layer является фактом текущего repo.

## Classification

- layer: `factory-template`
- severity: `medium`
- defect type: release/dashboard consistency drift
- reusable factory issue: yes, because root-vs-generated renderer overlays must not leak generated defaults into factory-template status cards.

## Remediation boundary

Исправить renderer так, чтобы root `FACTORY_MANIFEST.yaml` переопределял только readout для factory-template root. Не менять generated-project default на `true` и не превращать `factory/producer/*` в downstream dependency.
