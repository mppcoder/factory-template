# Post-2.5 release planning gap

Date: 2026-04-27

## Summary

After `2.5.0 GA Ready`, repo-facing docs had completed evidence for `2.5.1-field-pilot`, production VPS dry-run/report readiness, downstream sync v3 synthetic proof, `feature-execution-lite` and Artifact Eval Harness. They did not yet provide one release-facing planning layer that separates:

- `2.5.1` patch/stabilization scope;
- `2.6` deeper execution/runtime scope;
- completed repo-controlled/synthetic proof;
- pending external runtime proof;
- adaptation status for useful ideas from `pavel-molyanov/molyanov-ai-dev`.

## Classification

- Layer: `factory-template`
- Severity: `medium`
- Type: `release-followup planning gap`
- Current route: `post-2.5/release-2.5.1-2.6-planning`
- Defect capture path: `reports/bugs/YYYY-MM-DD-post-25-release-planning-gap.md`

## Evidence

- `docs/releases/release-scorecard.yaml` correctly keeps `2.5.0 GA Ready` as the release truth.
- `docs/releases/2.5.1-field-pilot-roadmap.md` tracks completed `FP-01`..`FP-05` field proof, but it is narrower than a patch/stabilization roadmap.
- `reports/release/production-vps-field-pilot-report.md` states `repo-controlled-dry-run-ready-real-vps-pending`.
- `reports/release/downstream-multi-cycle-sync-report.md` states that downstream sync v3 proof is synthetic repo-controlled evidence and does not replace real runtime proof.
- No `docs/releases/2.5.1-roadmap.md`, `docs/releases/2.6-roadmap.md` or `docs/releases/post-2.5-gap-register.md` existed before this task.

## Remediation

Add release-facing planning artifacts and synchronize state docs:

- `docs/releases/2.5.1-roadmap.md`
- `docs/releases/2.6-roadmap.md`
- `docs/releases/post-2.5-gap-register.md`
- `CHANGELOG.md`
- `CURRENT_FUNCTIONAL_STATE.md`
- `RELEASE_NOTES.md`
- `TEST_REPORT.md`
- `VERIFY_SUMMARY.md`

## Non-goals

- Do not change `docs/releases/release-scorecard.yaml`.
- Do not declare `2.5.1` or `2.6` release-ready.
- Do not claim real VPS production proof without operator approval, secrets and runtime transcript.

## Status

`remediated-in-current-scope`
