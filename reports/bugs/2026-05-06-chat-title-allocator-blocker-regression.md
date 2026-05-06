# Bug: chat-title-allocator-blocker-regression

Date: 2026-05-06
Status: open

## Symptom

ChatGPT shows the exact allocator blocker:

```text
Нужно выделить номер через repo chat-handoff-index / allocator.
```

instead of a stable `FT-CH-.... <task-slug>` title, even when the repo write path is available and `.chatgpt/chat-handoff-index.yaml` can be updated.

## Impact

- The user cannot copy a stable chat title from the first substantive response.
- The first-answer contract degrades into a false blocker fallback.
- The previous remediation for `chatgpt-first-answer-allocation-not-attempted` is incomplete if it only enforces "title or blocker" but does not enforce "attempt allocator before blocker when write path exists".
- The dashboard/status chain can remain disconnected until a retrofix is performed.

## Expected Behavior

The first substantive ChatGPT answer in a new project task chat must first attempt a materialized repo reservation via `.chatgpt/chat-handoff-index.yaml` / allocator when write access is available.

Only if allocation is unavailable or the repo write cannot be confirmed may ChatGPT show exactly:

```text
Нужно выделить номер через repo chat-handoff-index / allocator.
```

## Actual Evidence

- User report: "Вместо названия для копирования дает - Нужно выделить номер через repo chat-handoff-index / allocator."
- Router already permits the blocker only when ChatGPT cannot reliably write and confirm the repo index reservation.
- Current repo reservation was successfully materialized as `FT-CH-0016 chat-title-allocator-blocker-regression`, proving that a write path can be available and should be attempted before blocker fallback.

## Layer Classification

- defect class: `chatgpt-first-answer-contract`
- affected layer: router / validator / runbook / allocator guidance
- reusable downstream issue: yes
- related closed defect: `chatgpt-first-answer-allocation-not-attempted`
- not in scope: auto-renaming ChatGPT UI or guessing the next number without materialized reservation

## Required Remediation

1. Tighten router wording so the fallback blocker is allowed only after a failed or unavailable write-confirmed allocator attempt.
2. Add validator coverage for the false-blocker path: when write allocator is reachable, `exact allocator blocker` alone is not acceptable.
3. Add or update a fixture simulating reachable allocator/write path and asserting stable title output.
4. Update operator/user runbook wording: if the blocker appears despite repo write access, treat it as a bug and reserve the number manually/through allocator, not as normal behavior.
5. Update dashboard/feedback closeout after implementation.

## Verification Target

- `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`
- `python3 template-repo/scripts/validate-chatgpt-first-answer-contract.py .`
- `bash template-repo/scripts/verify-all.sh quick`
- Full verify if scenario-pack, validators or runbook are changed.
