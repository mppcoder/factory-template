# Factory feedback 040: orchestration runner write-before-fail

Date: 2026-04-28

Source bug: `reports/bugs/2026-04-28-plan-5-orchestration-runner-write-before-fail.md`

## Summary

The reusable Codex orchestration runner allowed invalid parent plans to create child session artifacts before returning non-zero. The reusable verify contract also lacked runner-level negative smoke for this class of integrity regression.

## Reusable template lesson

For any handoff/session generator, validation must be a hard pre-write gate. Validator-only negative fixtures are insufficient when a separate executable runner can still write artifacts before failing.

## Required template rule

- Validate parent plan first.
- If validation errors exist, print only sanitized error summaries and exit non-zero.
- Do not create output directories, child session files, prompt artifacts or parent reports from invalid plans.
- Add runner-level negative smoke to quick verify for security/integrity boundaries.

## Applied remediation

Tracked in the Plan №5 integrity/security follow-up. Expected changed areas:

- `template-repo/scripts/orchestrate-codex-handoff.py`
- `template-repo/scripts/verify-all.sh`
- Plan №5 release-facing status/evidence docs

## Downstream impact

Downstream repos that consume the template orchestration runner should receive this fix through the normal template sync path. No battle repo claim is made until a real downstream sync is performed.
