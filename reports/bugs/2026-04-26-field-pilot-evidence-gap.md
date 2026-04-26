# Field pilot evidence gap for 2.5.0 GA follow-up

- Date: 2026-04-26
- Task: `FIELD-PILOT-EVIDENCE`
- Type: release evidence / field validation gap
- Layer: release documentation, downstream validation, evidence taxonomy
- Status: fixed in current scope as documentation and roadmap remediation

## Summary

Release 2.5.0 has repository-controlled GA evidence, but the release-facing documentation did not yet give field pilot evidence its own explicit status, roadmap and pass/fail criteria. This could let readers confuse synthetic smoke, controlled novice scenarios and downstream safe-sync checks with real battle-project proof.

## Reproduction

1. Open `docs/releases/2.5-success-metrics.md`.
2. Open `docs/releases/2.5-ga-kpi-evidence.md`.
3. Open `TEST_REPORT.md`.
4. Compare those files with the required field paths:
   - battle greenfield project;
   - battle brownfield without repo;
   - battle brownfield with repo;
   - downstream sync cycle 1;
   - downstream sync cycle 2.

## Evidence

- Repo-controlled evidence exists for novice smoke, controlled pilot checklist, validators and downstream safe-sync dry-run/apply/rollback checks.
- No repository artifact currently records completed real external or battle-project field pilot runs.
- `CURRENT_FUNCTIONAL_STATE.md` already lists real greenfield/brownfield checks and production feedback as not closed, but the release evidence package lacks a dedicated field pilot roadmap and scenario checklist.

## Impact

- Operators can overread `2.5.0 GA Ready` as field-proven across real projects.
- Future release follow-up can lose the distinction between reproducible repo evidence and external pilot evidence.
- Field pilot execution lacks one normalized checklist per scenario, making pass/fail and retained artifacts ambiguous.

## Classification

- Defect layer: release-facing evidence taxonomy and post-GA field validation planning.
- Reusable issue: yes. Future release lines need the same separation between repo-controlled release gates and field proof.
- Current-scope remediation: yes, as documentation and roadmap updates only.

## Fix Plan

1. Add `docs/releases/2.5.1-field-pilot-roadmap.md`.
2. Add `reports/release/2.5-field-pilot-evidence.md`.
3. Add field scenario checklists under `reports/release/field-pilot-scenarios/`.
4. Update release docs to state that 2.5.0 GA is repo-controlled, while field proof is pending for 2.5.1 follow-up.
5. Keep `TEST_REPORT.md` honest: no field evidence is claimed until real projects are executed.

## Verification

- `bash template-repo/scripts/verify-all.sh quick`
