# Factory feedback 042: one-paste orchestration autopilot

Date: 2026-04-28

Source bug: `reports/bugs/2026-04-28-one-paste-orchestration-autopilot-gap.md`

## Summary

Full handoff orchestration should be user-facing one-paste: after the operator pastes the parent handoff into Codex in the VPS Remote SSH repo context, parent Codex should run the repo-native orchestrator itself.

## Reusable rule

- Do not make the operator run internal orchestration commands after paste during the normal path.
- Keep manual commands as troubleshooting, strict fallback or reproduction evidence.
- Parent Codex must validate before executing child sessions.
- Child sessions must use explicit profile/model/reasoning/scenario fields.

## Downstream impact

Downstream/battle repos that consume the full handoff orchestration runbook should receive this wording through template sync. No project secret or runtime action is implied.
