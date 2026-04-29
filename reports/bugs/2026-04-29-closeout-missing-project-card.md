# Bug: closeout did not include compact project card

Date: 2026-04-29

## Summary

The final closeout could complete a repo change with verification and sync status but omit the compact project card, even though the project dashboard/card renderer is the intended user-facing status surface.

## Evidence

- `render-project-lifecycle-dashboard.py --format chatgpt-card` exists and renders the required lifecycle/module/handoff card.
- `docs/operator/factory-template/07-beginner-visual-dashboard-ux.md` says Codex should show visual cards, but `template-repo/scenario-pack/16-done-closeout.md` did not require the card in the final answer.
- `create-codex-task-pack.py` generated closeout checklist did not require `Карточка проекта`.

## Expected Behavior

Every final closeout for a `factory-template` repo change includes a `Карточка проекта` section with the fresh compact card:

- project name;
- lifecycle chain;
- `Модули:`;
- `В работе:`.

If the renderer/dashboard is unavailable, closeout must name a blocker instead of silently omitting the card.

## Classification

- Layer: closeout UX / dashboard card contract.
- Reusable template issue: yes.

## Remediation

- Update closeout scenario and docs.
- Update generated task checklist/direct-task response rules.
- Add validator coverage for direct-task closeout card rule.
