# Дефект: roadmap closure status оставался незакрытым после template proof

Date: 2026-04-27

reusable: yes
learning_patch_status: not_required
learning_patch_reason: This is a release-facing status correction in the same closeout family; remediation updates the roadmap, gap register and current/test status directly.

## Summary

After clarifying that `factory-template` does not require a downstream/battle application image, the 2.6 roadmap still looked open because optional future contours were listed like next stages.

## Evidence

- `docs/releases/2.6-roadmap.md` still had a "Следующие стадии" table with `P3-S7`.
- `CURRENT_FUNCTIONAL_STATE.md` described optional future proof but did not explicitly say the current 2.6 roadmap is complete.
- `docs/releases/post-2.5-gap-register.md` still carried continuing-backlog wording for items that were complete for the current template roadmap.

## Layer Classification

- Layer: release-facing roadmap/status docs.
- Defect class: roadmap closure status drift.
- Owner boundary: repo docs/reports.
- External boundary: future downstream/battle app proof is optional and belongs to a separate roadmap if selected.

## Remediation

Mark the 2.6 `factory-template` template/runtime roadmap as completed:

- P3-S0..P3-S6 complete.
- Template reference runtime app defined.
- Runtime proof, restore, rollback, eval expansion and real feature-execution adoption complete.
- Optional downstream/battle app proof moved out of current roadmap closure.

## Status

Captured and remediated in current scope.
