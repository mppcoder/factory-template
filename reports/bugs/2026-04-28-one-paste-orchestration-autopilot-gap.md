# One-paste orchestration autopilot gap

Date: 2026-04-28

## Summary

The VPS Remote SSH-first orchestration docs still described an operator-visible extra shell step after pasting a parent handoff into Codex. The intended UX is one user action: paste the parent handoff into Codex connected to the VPS/repo context; parent Codex then validates and runs the repo-native orchestrator automatically.

## Severity

Medium. The gap does not break runner behavior, but it creates workflow friction and contradicts the desired full handoff orchestration model.

## Expected behavior

- Operator opens VS Code Remote SSH on the VPS repo.
- Operator opens a new Codex chat/session with the selected parent route.
- Operator pastes one parent handoff.
- Parent Codex emits handoff receipt, validates the embedded/materialized orchestration plan and runs `orchestrate-codex-handoff.py --execute`.
- Child Codex CLI sessions run with their own explicit `selected_profile`, `selected_model`, `selected_reasoning_effort`, `selected_plan_mode_reasoning_effort` and `selected_scenario`.
- Manual shell commands are documented only as troubleshooting/strict fallback, not as the normal next user action.

## Actual behavior

The runbook still showed a separate operator step to run orchestration dry-run after paste. That made the workflow look like two actions: paste handoff, then manually run the orchestrator.

## Layer classification

- advisory/operator runbook layer: full handoff orchestration UX wording.
- generated handoff layer: handoff instructions should tell parent Codex to run the orchestrator, not ask the user for a second internal command.
- validator/eval layer: artifact eval should check one-paste autopilot wording.

## Security/integrity boundary

- Autopilot must still validate before writing session files or executing child sessions.
- Invalid/secret-like plans must fail before child session creation.
- User/external/runtime/downstream actions still defer to final closeout.

## Remediation plan

1. Update the VPS Remote SSH orchestration runbook: operator action ends after paste; parent Codex runs validate + execute.
2. Update handoff scenario/generated handoff text to express one-paste autopilot for full orchestration handoffs.
3. Add artifact eval coverage for one-paste autopilot.
4. Run targeted validators and quick verify.

## Verification plan

1. Artifact Eval for `vps-remote-ssh-orchestration`.
2. `validate-codex-orchestration.py`.
3. `validate-codex-task-pack.py`.
4. `validate-human-language-layer.py`.
5. `bash template-repo/scripts/verify-all.sh quick`.

## Factory feedback

Required. This is reusable full handoff orchestration workflow guidance.

Factory feedback report: `reports/factory-feedback/feedback-042-one-paste-orchestration-autopilot-gap.md`
