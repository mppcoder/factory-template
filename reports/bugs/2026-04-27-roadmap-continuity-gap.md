# Bug: roadmap continuity broke after 2.6 runtime proof

Date: 2026-04-27

reusable: yes
learning_patch_status: not_required
learning_patch_reason: This is the same closeout continuity class already covered by the repo's internal follow-up and release-facing consistency rules; this report records the concrete 2.6 instance.

## Summary

After the approved 2.6 runtime proof and placeholder app image remediation, several roadmap/status artifacts still described the runtime work as pending, demo-nginx based or not executed. The final closeout also did not name the next roadmap stage clearly enough.

## Evidence

- `CURRENT_FUNCTIONAL_STATE.md` still said real VPS proof remained external pending and referenced demo `nginx`.
- `TEST_REPORT.md` still said the 2.6 runtime proof had only a demo `APP_IMAGE=nginx:1.27-alpine`.
- `docs/releases/plan-3-aif-molyanov-audit.md` stopped at P3-S5 and did not record the executed runtime proof / continuity pass.
- `docs/releases/2.6-roadmap.md` did not name the next stages after placeholder infrastructure proof.
- `reports/release/production-vps-field-pilot-report.md` still carried a pending-first status while also mentioning executed runtime proof.

## Layer Classification

- Layer: release-facing roadmap/status docs.
- Defect class: roadmap continuity gap / stale release truth after runtime proof.
- Owner boundary: repo/template docs and reports.
- External boundary: real business application image proof remains future work and requires a real app artifact.

## Remediation

Align the release-facing roadmap chain:

- P3-S0..P3-S5: implemented/verified.
- 2.6 runtime infrastructure proof: executed on approved VPS with local placeholder application image.
- P3-S6: release-facing continuity pass.
- P3-S7 / next external boundary: replace placeholder image with real application image and repeat application-level proof only when a real app exists.

## Status

Captured and remediated in current scope.
