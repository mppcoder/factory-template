# Plan №4 audit gap

Дата: 2026-04-27

## Summary контекст

After Plan №3, `factory-template` correctly completed template/runtime proof, but the optional downstream/battle application proof needed a separate roadmap so future work would not overclaim placeholder runtime evidence.

## Evidence данные

- `reports/release/2.6-runtime-proof-report.md` says proof used `factory-template-placeholder-app:local`.
- `docs/template-runtime-reference-app.md` says downstream must replace placeholder image before app-level proof.
- Current roadmap closure says downstream/battle app proof is outside the completed template/runtime scope.

## Classification слой

- Layer: release planning / downstream runtime boundary.
- Severity: planning gap, not current runtime regression.
- Owner boundary: repo docs and future downstream runtime.

## Remediation план

Create `docs/releases/plan-4-battle-app-proof-roadmap.md`, update gap/current/test docs and keep P4-S5/P4-S6 blocked until a real downstream project is selected.
