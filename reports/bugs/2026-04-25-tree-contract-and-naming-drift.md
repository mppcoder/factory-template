# Bug Report: tree contract and naming drift

- Date: `2026-04-25`
- Type: audit-remediation defect from `2.5-ga/tree-contract-and-naming`
- Layer: `factory-template / template-repo / generated project UX`
- Scope decision: `fixed-in-scope`

## Reproduce

1. Read repo-first route from `template-repo/scenario-pack/00-master-router.md`.
2. Inspect active entry and preset artifacts:
   - `ENTRY_MODES.md`
   - `template-repo/project-presets.yaml`
   - `README.md`
   - `docs/template-architecture-and-event-workflows.md`
3. Search active source-facing layer for legacy/product-specific naming:
   - `dogfood`
   - `openclaw`
   - old preset aliases such as `product-dev` and `brownfield-dogfood-codex-assisted`
4. Check whether a machine-readable tree contract exists for factory root, template base and generated project contours.

## Evidence

- `template-repo/project-presets.yaml` exposed `preset_aliases` in the same active file as canonical presets.
- `ENTRY_MODES.md` listed old aliases as a normal UX section.
- No `template-repo/tree-contract.yaml` or `template-repo/scripts/validate-tree-contract.py` existed.
- `docs/template-architecture-and-event-workflows.md` documented a broad tree map, but not a strict machine-readable contract for:
  - `factory_root`
  - `template_base`
  - `generated_greenfield`
  - `generated_brownfield_without_repo`
  - `generated_brownfield_with_repo`

## Expected

- Canonical beginner UX exposes only neutral universal entry names.
- Legacy aliases remain accepted only through an explicit compatibility layer.
- Product-specific or historical names are not treated as canonical core paths.
- A validator can confirm the factory root, template base and generated project contours against a strict contract.

## Actual

- Legacy aliases were mixed into active preset configuration and beginner-facing documentation.
- Tree expectations were human-readable only and spread across docs.
- Active validation did not protect the repo from reintroducing historical/product-specific naming into core UX.

## Classification

- `defect_layer`: `factory-template`
- `reusable`: yes
- `current_scope`: yes
- `factory_feedback_required`: no, because this is the factory repo itself

## Self-Handoff

```text
launch_source: chatgpt-handoff
task_class: audit-remediation
selected_profile: deep
selected_model: gpt-5.5
selected_reasoning_effort: high
project_profile: factory-template
selected_scenario: 2.5-ga/tree-contract-and-naming
pipeline_stage: defect-capture -> remediation
handoff_allowed: true
defect_capture_path: reports/bugs/2026-04-25-tree-contract-and-naming-drift.md

Scope decision: continue-in-current-route.
Remediation remains in the same factory-template audit/remediation route.
Advisory text does not switch profile/model/reasoning inside an already-open session; this self-handoff documents the repo boundary and permits current-scope remediation.
```

## Fix Plan

- Add `template-repo/tree-contract.yaml`.
- Add `template-repo/scripts/validate-tree-contract.py`.
- Move preset aliases into `template-repo/compatibility-aliases.yaml`.
- Keep alias resolution in launcher/scripts for backward compatibility.
- Remove old aliases from beginner UX docs.
- Integrate the validator into quick, pre-release audit and matrix checks.
- Update release-facing docs and verification evidence.

## Verification

- `python3 template-repo/scripts/validate-tree-contract.py .` — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass.
- `bash template-repo/scripts/verify-all.sh ci` — pass.
- `MATRIX_TEST.sh` inside ci validates generated greenfield, generated brownfield-without-repo and generated brownfield-with-repo contours with `validate-tree-contract.py`.
