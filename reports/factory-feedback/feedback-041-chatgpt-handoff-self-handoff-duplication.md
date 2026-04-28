# Factory feedback 041: ChatGPT handoff receipt vs self-handoff

Date: 2026-04-28

Source bug: `reports/bugs/2026-04-28-chatgpt-handoff-self-handoff-duplication.md`

## Summary

The reusable handoff contract must reserve `self-handoff` for direct tasks and separate incidental defect task boundaries. A ChatGPT-generated handoff should be accepted with a short `handoff receipt` / `route receipt`, not rewritten as another handoff.

## Reusable rule

- `launch_source: chatgpt-handoff` means execute the incoming handoff.
- Codex may print a visible receipt confirming profile, scenario, stage, artifacts, `handoff_allowed` and `defect_capture_path`.
- That receipt is not a new handoff, not a replacement source, and not a new task launch.
- `self-handoff` means Codex creates the launch-normalized task boundary itself because no external handoff exists, or because an incidental defect needs its own task boundary.

## Downstream impact

Downstream/battle repos that consume the scenario-pack should receive this wording on the next template sync. No executable routing change is required.
