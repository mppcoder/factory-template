# Bug: chatgpt-first-answer-allocation-not-attempted

Date: 2026-05-06
Status: verified

## Symptom

ChatGPT can start a new task chat and continue to route receipt, analysis or handoff without first attempting repo allocator materialization and without showing the exact allocator blocker.

This creates a visible third state: no materialized allocation, no allocator blocker, answer continues.

## Impact

- The user does not receive a stable `FT-CH-.... <task-slug>` title.
- `.chatgpt/chat-handoff-index.yaml` has no materialized reservation for the visible task identity.
- The project dashboard/status card can lose the link between the ChatGPT task chat and the implementation state.
- A guessed, dry-run or read-only number can be mistaken for a stable title.

## Expected Behavior

The first substantive answer in a new ChatGPT task chat must begin with:

```text
## Название чата для копирования
<materialized stable title or exact allocator blocker>

## Карточка проекта
<compact project status card>
```

The title block must show exactly one of two outcomes:

- materialized allocation confirmed, then the stable `FT-CH-.... <task-slug>` title from `.chatgpt/chat-handoff-index.yaml`;
- allocation unavailable or repo write not confirmed, then exactly `Нужно выделить номер через repo chat-handoff-index / allocator.`

The third state is forbidden: no allocation attempted / no blocker / answer continues.

## Layer Classification

- defect class: `chatgpt-first-answer-contract`
- affected layer: router / handoff scenario / validator / operator runbook
- reusable downstream issue: yes
- not in scope: auto-renaming ChatGPT UI, global scan of all project chats, changing counter semantics, or promising model/profile/reasoning auto-switch in an already-open Codex session

## Evidence

- `.chatgpt/chat-handoff-index.yaml` already requires `first_chat_response_allocates_handoff_id: true`, `visible_chat_title_requires_materialized_index_item: true` and `allocator_blocker_required_without_write_access: true`.
- `template-repo/scripts/allocate-chat-handoff-id.py` can materialize the reservation and print the stable title.
- `template-repo/scripts/validate-chatgpt-first-answer-contract.py` previously checked title/card phrases but did not separately guard `allocation-not-attempted`.
- Current task reservation: `FT-CH-0012 chatgpt-first-answer-allocation-not-attempted`.

## Remediation

- Router now names `chatgpt-first-answer-allocation-not-attempted` as a first-answer contract violation.
- Handoff scenario now treats missing allocation attempt/blocker before ChatGPT-generated handoff as blocker/defect, not fallback.
- Validator now requires explicit allocation-not-attempted guard wording and checks a negative fixture.
- Operator docs now tell beginners to stop the route if neither `FT-CH-....` nor allocator blocker appears.
- Factory feedback created for reusable downstream propagation.

## Verification

- `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`
- `python3 template-repo/scripts/validate-chatgpt-first-answer-contract.py .`
- `bash template-repo/scripts/verify-all.sh quick`
