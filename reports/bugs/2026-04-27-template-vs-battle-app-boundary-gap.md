# Дефект: roadmap смешал template proof и battle app proof

Date: 2026-04-27

reusable: yes
learning_patch_status: not_required
learning_patch_reason: This is a release-facing boundary wording defect; remediation directly updates roadmap/status docs so future closeouts distinguish template proof from downstream/battle application proof.

## Summary

2.6 roadmap wording treated "real application image proof" like a remaining blocker for the `factory-template` template test. That is ambiguous and misleading: this repo tests the template/runtime/deploy path. A real business application image belongs to a generated downstream/battle project, not to the template repo itself.

## Evidence

User asked: "что за приложение имеется ввиду? мы же шаблон тестируем или боевой проект?"

The docs used phrases like:

- "real business application image proof remains pending"
- "`P3-S7` real application image proof boundary"
- "main remaining `2.6` blocker is application-level proof"

These phrases did not clearly say that the blocker is only for a future downstream/battle app proof, not for the factory-template runtime proof.

## Layer Classification

- Layer: release-facing roadmap/status docs.
- Defect class: boundary ambiguity / evidence taxonomy bug.
- Owner boundary: repo docs and release reports.
- External boundary: downstream/battle project with a real app may later run app-level proof, but that is not required to validate this template repo.

## Remediation

Reword roadmap/status docs:

- factory-template 2.6 template/runtime proof is complete for the placeholder infrastructure path;
- no real app is required inside `factory-template`;
- future real app proof is a separate downstream/battle project contour, only when validating a generated project that actually has an application.

## Status

Captured and remediated in current scope.
