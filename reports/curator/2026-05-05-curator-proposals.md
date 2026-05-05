# Factory curator proposals / предложения куратора

Дата: 2026-05-05

## Policy / политика

Curator is read-only by default. No hidden self-learning is allowed; every learning must become a repo-reviewed artifact before it can change behavior.

## Evidence / подтверждения

- `.chatgpt/handoff-implementation-register.yaml`
- `template-repo/template/.chatgpt/task-registry.yaml`
- `template-repo/template/.chatgpt/handoff-implementation-register.yaml`
- `reports/task-queue.md`
- `reports/continuous-backlog-readout.md`
- `RELEASE_NOTES.md`

## Proposal 1 / предложение 1

- evidence: task queue and release notes are the active automation control plane.
- proposal: keep issue-autofix, bounded runner, Symphony-compatible spec and advanced automation gates in the same quick validation contour.
- risk: validator drift can make future automation look safer than it is.
- suggested validation: run `bash template-repo/scripts/verify-all.sh quick` and the advanced automation validators before release-facing closeout.

## Proposal 2 / предложение 2

- evidence: generated projects receive repo-owned docs and scripts.
- proposal: add downstream smoke coverage whenever a new automation workflow or support surface is added.
- risk: factory-only paths can leak into generated repos.
- suggested validation: generate a temp project and check `.github`, `WORKFLOW.md`, support docs and `SECURITY.md`.

## Write mode / режим записи

`--write` may create a curator-class FT-TASK in a future increment, but this MVP does not mutate the repo except for this proposal report.
