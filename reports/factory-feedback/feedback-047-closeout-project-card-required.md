# Factory Feedback 047: project card required in closeout

Date: 2026-04-29

## Learning

The compact project card is not just a dashboard artifact. It must appear in the final user-facing closeout so the operator immediately sees lifecycle state, module readiness and active handoff status without asking again.

## Template Change

- Final closeout must include a `Карточка проекта` section.
- The card must come from `render-project-lifecycle-dashboard.py --format chatgpt-card --stdout`.
- The card must include project name, lifecycle chain, `Модули:` and `В работе:`.
- If the card cannot be generated, the task is not fully closed and the blocker must be stated.
