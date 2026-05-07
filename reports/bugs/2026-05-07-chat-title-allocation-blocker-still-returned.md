# Bug: chat-title-allocation-blocker-still-returned

Date: 2026-05-07
Status: verified

## Symptom

ChatGPT Project first substantive answer again returned the exact allocator blocker:

```text
Нужно выделить номер через repo chat-handoff-index / allocator.
```

This happened even though the GitHub connector write path was available and could materialize `.chatgpt/chat-handoff-index.yaml`.

## Impact

- The user still does not get a stable one-click `FT-CH-.... <task-slug>` title in the first answer.
- The first-answer workflow treats "repo-local allocator unavailable in ChatGPT connector context" as if all write paths were unavailable.
- The earlier fixes for `FT-CH-0016` and `FT-CH-0018` were incomplete because they did not explicitly validate connector-based materialized reservation after local allocator unavailability.

## Evidence

- Current task reservation was materialized as `FT-CH-0020 chat-title-allocation-blocker-still-returned`.
- `.chatgpt/chat-handoff-index.yaml` evidence records that the router was read first and that direct GitHub connector update created the item because the repo-local allocator script could not run in ChatGPT connector context.
- Related open reservations:
  - `FT-CH-0016 chat-title-allocator-blocker-regression`
  - `FT-CH-0018 chat-title-allocator-write-path-regression`

## Layer Classification

- defect class: `chatgpt-first-answer-contract`
- affected layer: ChatGPT Project first-answer workflow / repo connector write-path / allocator fallback contract
- reusable downstream issue: yes
- not in scope: ChatGPT UI auto-rename, dry-run title suggestions, public `github.com` / `raw.githubusercontent.com` fallback

## Expected Behavior

First substantive ChatGPT Project answer must:

1. read `template-repo/scenario-pack/00-master-router.md`;
2. attempt repo-local allocator when executable;
3. if repo-local allocator is unavailable in ChatGPT connector context but GitHub connector write path is available, materialize the reservation by connector update to `.chatgpt/chat-handoff-index.yaml`;
4. confirm fetch/readback of the updated index;
5. show stable title only after confirmed write.

The exact allocator blocker is allowed only when write path is unavailable, write is rejected, or confirm fetch does not prove the item exists. The blocker must not be shown merely because the repo-local Python script cannot run in connector context.

## Remediation

- Add explicit router/handoff/runbook contract for `repo-local allocator unavailable -> GitHub connector materialized write -> confirm fetch -> stable title`.
- Add allocation policy keys to chat handoff index tooling and template state.
- Add validator coverage for the false blocker path where `GitHub connector write path available` and `repo-local allocator unavailable in ChatGPT connector context`.
- Update handoff implementation register and dashboard/card closeout evidence.

## Resolution

Closed in `HIR-013`.

The first-answer contract now requires:

1. repo-local allocator attempt when executable;
2. GitHub connector write fallback when local allocator execution is unavailable in ChatGPT connector context;
3. confirm fetch/readback before showing `FT-CH-....`;
4. exact allocator blocker only for true write/confirm blockers.

## Verification Target

- `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`
- `python3 template-repo/scripts/validate-chatgpt-first-answer-contract.py .`
- `bash template-repo/scripts/verify-all.sh quick`
- `bash template-repo/scripts/verify-all.sh`

## Verification Result

- `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml` passed.
- `python3 template-repo/scripts/validate-chatgpt-first-answer-contract.py .` passed.
- `bash template-repo/scripts/verify-all.sh quick` passed.
- `bash template-repo/scripts/verify-all.sh` passed after fixing an incidental generated `boundary-actions.md` marker drift in `template-repo/scripts/create-codex-task-pack.py`.
