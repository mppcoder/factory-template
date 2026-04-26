# Field pilot evidence gap for 2.5.0 GA follow-up

- Date: 2026-04-26
- Task: `FIELD-PILOT-EVIDENCE`
- Type: release evidence / field validation gap
- Layer: release documentation, downstream validation, evidence taxonomy
- Status: fixed; roadmap/evidence taxonomy fixed, FP-01..FP-05 field evidence retained

## Summary

Release 2.5.0 has repository-controlled GA evidence, but the release-facing documentation initially did not give field pilot evidence its own explicit status, roadmap and pass/fail criteria. This could let readers confuse synthetic smoke, controlled novice scenarios and downstream safe-sync checks with real battle-project proof.

Update on 2026-04-26: FP-01 now has field evidence for real greenfield repo `mppcoder/greenfield-test` at commit `cca68d5`. FP-02 now has sanitized field evidence for a real brownfield without repo OpenClaw+ case, including creation and push of GitHub-backed project repo `mppcoder/openclaw-brownfield` at commit `7b3d1a4`. FP-03 now has brownfield-with-repo audit evidence on `mppcoder/openclaw-brownfield` at commit `3c026fd`. FP-04 and FP-05 now have same-lineage downstream sync evidence on `mppcoder/openclaw-brownfield` at commits `1826f07` and `2dc6515`. The field pilot is now complete: `5/5`.

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
- FP-01 now records a completed real greenfield launch-path run and created project repo.
- FP-02 now records a completed real sanitized brownfield without repo run and created project repo.
- Repository artifacts now record completed FP-04 and FP-05 downstream sync field pilot runs.
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
4. Update release docs to state that 2.5.0 GA is repo-controlled, while field proof is tracked separately as 2.5.1 follow-up.
5. Keep `TEST_REPORT.md` honest: only executed field scenarios are claimed.

## Verification

- `bash template-repo/scripts/verify-all.sh quick`

## Остаточный статус

Active follow-up for the original 2.5.1 field pilot roadmap is closed.
