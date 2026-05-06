# Factory Feedback 053: Missing first-answer allocation attempt must be a defect

Source bug: `reports/bugs/2026-05-06-chatgpt-first-answer-allocation-not-attempted.md`

## Learning

The first substantive ChatGPT task answer needs a visible allocator outcome before route receipt, analysis or handoff. It is not enough to require a title/card block if the route can continue without either a materialized `FT-CH-....` reservation or the exact allocator blocker.

## Template Action

- Require materialized allocation or allocator blocker before any ChatGPT-generated handoff.
- Treat `allocation-not-attempted` as a contract violation, not a fallback mode.
- Forbid the third state: no allocation attempted / no blocker / answer continues.
- Add validator coverage that fails if router/runbook artifacts stop naming this failure mode.
- Tell beginners to stop the route and run allocator/Codex remediation instead of continuing with a guessed number.
