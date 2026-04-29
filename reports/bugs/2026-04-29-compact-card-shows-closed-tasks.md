# Bug: compact project card shows closed tasks

Date: 2026-04-29

## Summary

The compact ChatGPT project card rendered verified/closed handoff items in `В работе:`. This made the closeout card noisy and less useful as an operator status readout.

## Evidence

- `active_handoff_lines_text()` excluded `superseded`, `not_applicable` and `archived`, but kept `verified`.
- As a result, old completed items like `FT-CH-0001`, `FT-CH-0005`, `FT-CH-0006` and `FT-CH-0007` appeared in the compact card.

## Expected Behavior

Compact card `В работе:` should show:

- the current chat/self-handoff task;
- not-closed tasks such as `open`, `codex_accepted`, `in_progress`, `implemented` or `blocked`.

Closed historical tasks should remain visible in the full dashboard report, not in the compact card.

## Remediation

- Filter terminal chat states from compact card.
- Always keep the current/latest chat task visible so final closeout can show the just-finished task.
- Document the distinction between compact card and full dashboard history.
