# Factory feedback 061: ChatGPT GitHub confirmation gate during allocation

Источник: `reports/bugs/2026-05-07-chat-title-allocation-github-confirmation-gate-regression.md`

## Reusable issue

Repo-first ChatGPT Project instructions can require authenticated GitHub connector access, but the model may still ask a conversational confirmation question before attempting the required repo read/index read/allocation path.

## Expected factory behavior

- repo-first instruction authorizes configured GitHub connector for required read/index/allocation attempts.
- Do not ask conversational confirmation before the first-answer allocation attempt.
- platform-level OAuth / connector authorization remains an external boundary and must be reported as `external_auth_blocker`.
- Missing or rejected write action must be reported as `write_auth_blocker`.
- If write action exposed and confirm fetch succeeds, the exact allocator blocker is forbidden.

## Suggested validation

Add first-answer contract fixtures that fail on GitHub confirmation questions before materialized allocation or explicit auth/write blocker, and pass on connector-safe materialized allocation without confirmation.
