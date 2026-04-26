# chg-20260426-root-physical-normalization

Date: 2026-04-26
Status: completed
Scenario: defect-capture -> structural remediation -> verification -> release-followup

## Summary

Physically normalized the `factory-template` root after lifecycle/ownership contract remediation. The repository now presents standard project lifecycle core plus bounded `factory/producer/*` factory-producer-owned content.

## Defect and decision

- Defect report: `reports/bugs/2026-04-26-root-still-has-nonstandard-top-level-folders.md`
- ADR: `docs/decisions/2026-04-26-root-physical-normalization.md`

## Moves

- `.dogfood-bootstrap/` -> `factory/producer/archive/legacy-bootstrap/`
- `factory_template_only_pack/*.md` -> `docs/operator/factory-template/`
- `factory_template_only_pack/templates/` -> `factory/producer/ops/templates/`
- `factory_template_only_pack/06-codex-config-factory-template.toml` -> `factory/producer/ops/codex-config-factory-template.toml`
- `meta-template-project/RELEASE_NOTES.md` -> `docs/releases/factory-template-release-notes.md`
- `meta-template-project/incoming-learnings/` -> `reports/factory-feedback/incoming-learnings/`
- `meta-template-project/scenario-audits/` -> `reports/factory-feedback/scenario-audits/`
- `meta-template-project/templates/` -> `work-templates/factory-feedback/`
- remaining `meta-template-project/*` -> `project-knowledge/factory/template-evolution/`
- `onboarding-smoke/` -> `tests/onboarding-smoke/`
- `optional-domain-packs/` -> `factory/producer/reference/domain-packs/`
- `packaging/` -> `factory/producer/packaging/`
- `registry/` -> `factory/producer/registry/`
- `working-project-examples/` -> `factory/producer/reference/examples/`
- `workspace-packs/` -> `factory/producer/extensions/workspace-packs/`

## Verification

- `python3 template-repo/scripts/validate-tree-contract.py .` -> pass
- `python3 template-repo/scripts/validate-mode-parity.py .` -> pass
- `python3 template-repo/scripts/validate-brownfield-transition.py .` -> pass
- `python3 template-repo/scripts/validate-greenfield-conversion.py .` -> pass
- `bash template-repo/scripts/verify-all.sh quick` -> pass
- `bash MATRIX_TEST.sh` -> pass
- `bash template-repo/scripts/verify-all.sh ci` -> pass
