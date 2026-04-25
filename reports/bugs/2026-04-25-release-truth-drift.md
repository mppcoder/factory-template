# Bug: release truth drift across 2.5 release-facing docs

- Date: 2026-04-25
- Task: `FT-2.5.1-release-truth`
- Type: release-facing documentation / gate consistency defect
- Layer: release engineering, documentation source-of-truth, CI/pre-release gates
- Status: fixed in current scope

## Summary

Release 2.5 state is described by multiple manually maintained markdown files without a single machine-readable source of truth. The files disagree on the current stage and on whether the 2.5 line is only planned, in remediation prep, or already in RC closeout.

## Reproduction

1. Open `docs/releases/2.5-roadmap.md`.
2. Open `CURRENT_FUNCTIONAL_STATE.md`.
3. Open `README.md`.
4. Open `RELEASE_CHECKLIST.md`.
5. Compare the stated release line, stage, readiness status, gates, and canonical references.

## Evidence

- `docs/releases/2.5-roadmap.md` says current pipeline stage is `remediation-prep`.
- `CURRENT_FUNCTIONAL_STATE.md` says the 2.5 program is at `verify-closeout (RC prep)`.
- `TEST_REPORT.md` is titled `TEST REPORT v2.5 RC (verify-closeout)`.
- `README.md` describes 2.5 as a program in progress without naming the same RC stage.
- `RELEASE_CHECKLIST.md` contains both `2.5 Program Framing Gate (Remediation-Prep)` and `2.5 RC Closeout Gate (Verify-Closeout)`, but there is no machine-readable gate that prevents future drift.

## Impact

- Release operators can read different release readiness states depending on entrypoint.
- `PRE_RELEASE_AUDIT.sh` can pass even when release-facing docs drift.
- CI can validate release scripts without validating release truth consistency.
- `TEST_REPORT.md` can become a manually maintained status source instead of evidence that points back to a canonical scorecard.

## Classification

- Defect layer: release-facing source-of-truth and validation layer.
- Reusable issue: yes. The template needs a stable release-truth pattern for future release lines.
- Current-scope remediation: yes.

## Fix Plan

1. Add `docs/releases/release-scorecard.yaml` as the canonical machine-readable release truth.
2. Add `template-repo/scripts/validate-release-scorecard.py`.
3. Wire the validator into `PRE_RELEASE_AUDIT.sh` and `template-repo/scripts/verify-all.sh`.
4. Update release-facing docs to point to the scorecard and describe one state: `2.5` is an RC closeout candidate / RC prep, not GA.
5. Update `TEST_REPORT.md` so it is evidence and verification output, not the only status source.

## Verification

- `python3 template-repo/scripts/validate-release-scorecard.py .`
- `bash PRE_RELEASE_AUDIT.sh`
- `bash template-repo/scripts/verify-all.sh quick`
