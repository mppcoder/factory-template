# Brownfield adoption must convert to greenfield-product

## Статус

зафиксировано, remediation в текущем change

## Дата

2026-04-26

## Найдено в

- `template-repo/tree-contract.yaml`
- `template-repo/mode-parity.yaml`
- `template-repo/project-presets.yaml`
- `workspace-packs/factory-ops/factory-sync-manifest.yaml`
- `docs/tree-contract.md`
- `docs/template-architecture-and-event-workflows.md`

## Ожидаемое поведение

Brownfield presets describe transitional adoption paths for existing projects. A successful adoption must end by updating the active project profile to `project_preset: greenfield-product`, `recommended_mode: greenfield`, and lifecycle state `greenfield-converted`.

The same lifecycle core applies to `factory-template` and downstream projects. The difference is ownership: `factory-template` has the factory producer layer in addition to normal product/project work.

## Фактическое поведение

Existing contracts present `brownfield-without-repo` and brownfield-with-repo variants as generated project contours/presets without a machine-readable requirement that they exit into `greenfield-product`.

The factory-root wording can also be read as a separate workflow for improving the template itself, instead of one lifecycle core plus producer/ownership layers.

## Риск

- Brownfield adoption can be considered done after audit or evidence collection.
- Future template sync may keep treating converted projects as brownfield.
- Brownfield evidence may remain an active mode driver instead of historical evidence.
- Factory-template work may drift into a special workflow instead of using the same lifecycle core as downstream work.

## Граница ответственности

This is a template architecture defect. It belongs to the reusable factory layer, not a single generated project.

## Remediation scope

- Add lifecycle states separate from project preset names.
- Add ownership classes for project core, template-owned zones, producer-owned zones, brownfield evidence/audit/reconstruction, historical archive, and transient generated files.
- Mark brownfield contours/presets as transitional compatibility labels.
- Add conversion gates and validators.
- Update sync tooling so converted projects receive greenfield sync while preserving brownfield history.
- Align launcher/wizard/preflight wording and docs.

## Affected files

- `docs/decisions/2026-04-26-project-core-producer-layer-and-brownfield-transition.md`
- `template-repo/tree-contract.yaml`
- `template-repo/mode-parity.yaml`
- `template-repo/project-presets.yaml`
- `template-repo/policy-presets.yaml`
- `template-repo/scripts/validate-tree-contract.py`
- `template-repo/scripts/validate-mode-parity.py`
- `template-repo/scripts/validate-brownfield-transition.py`
- `template-repo/scripts/validate-greenfield-conversion.py`
- `template-repo/scripts/verify-all.sh`
- `template-repo/scripts/factory-launcher.py`
- `template-repo/scripts/first-project-wizard.py`
- `template-repo/scripts/preflight-vps-check.py`
- `workspace-packs/factory-ops/factory-sync-manifest.yaml`
- `workspace-packs/factory-ops/check-template-drift.py`
- `workspace-packs/factory-ops/export-template-patch.sh`
- `workspace-packs/factory-ops/apply-template-patch.sh`
- `docs/tree-contract.md`
- `docs/template-architecture-and-event-workflows.md`
- `docs/brownfield-to-greenfield-transition.md`
- `README.md`
- `factory-template-ops-policy.yaml`
- `packaging/sources/sources-profiles.yaml`
- release closeout artifacts

## Done rule

A brownfield transition is not complete when audit is complete. It is complete only when the project becomes a full `greenfield-product` project on the factory template, or when a documented blocker prevents conversion.
