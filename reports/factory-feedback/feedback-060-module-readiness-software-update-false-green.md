# Factory feedback 060: module readiness software update false green

Источник: `reports/bugs/2026-05-08-module-readiness-software-update-false-green.md`

## Reusable issue

Module readiness can look fully green when a referenced mandatory governance source is still pending.

## Expected factory behavior

- If a green module cites `software_update_governance`, the software-update baseline must also be green or the module must be downgraded to a non-green status with explicit next action.
- Update governance remains manual-approved and report-first.
- No auto-install, auto-upgrade, daemon or production deploy behavior is introduced by this fix.

## Suggested validation

Add dashboard validator coverage for `module_readiness.modules[*].source_refs` cross-checks and keep `validate-project-lifecycle-dashboard.py` in quick verification.
