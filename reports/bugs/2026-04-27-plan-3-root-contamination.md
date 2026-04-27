# Defect: Plan №3 P3-S1/S2 root contamination

reusable: true
learning_patch_status: not_required
learning_patch_reason: "Remediation updates template/source boundary and validator routing directly; separate learning proposal would duplicate this bug report."

## Где найдено

User review after commit `37327b5` for Plan №3 P3-S1/S2.

## Что ожидалось

Generated-project artifacts for task-state and learning proposals should be added to the template source under `template-repo/template/`, plus docs/validators/tests. Factory root should not receive new project-instance state folders unless they are factory-level evidence or release artifacts.

## Что произошло фактически

Commit `37327b5` added root-level `.chatgpt/task-state.yaml` and `reports/learnings/.gitkeep`. This made the factory root look like the runtime project instance for the new feature, instead of keeping the new artifacts in the generated-project template source.

## Evidence

- Added root file: `.chatgpt/task-state.yaml`
- Added root folder marker: `reports/learnings/.gitkeep`
- Correct template files also exist under:
  - `template-repo/template/.chatgpt/task-state.yaml`
  - `template-repo/template/reports/learnings/learning-patch-proposal.md.template`

## Classification

- Layer: `factory-template`
- Scope: Plan №3 P3-S1/S2 remediation
- Owner boundary: internal repo
- Reusable issue: yes, root/template boundary discipline

## Remediation

- Remove root-level `.chatgpt/task-state.yaml`.
- Remove root-level `reports/learnings/.gitkeep`.
- Keep generated-project source artifacts in `template-repo/template/`.
- Update quick verify so factory root validates the template source for task-state-lite.
- Keep generated-project quick path validating generated root `.chatgpt/task-state.yaml`.
