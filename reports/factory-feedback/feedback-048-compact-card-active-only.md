# Factory Feedback 048: compact card should not be history

Date: 2026-04-29

## Learning

The compact project card is an operator glance view, not a historical ledger. Showing all verified tasks in `В работе:` hides the current state.

## Template Change

- `chatgpt-card` shows only the current/latest handoff item plus not-closed handoff items.
- Verified/archived/superseded history stays in `reports/project-lifecycle-dashboard.md`.
- Final closeout still includes the current task even after it is verified.
