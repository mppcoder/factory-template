# Factory Feedback 055: ChatGPT first-answer must use connector write fallback

Source bug: `reports/bugs/2026-05-07-chat-title-allocation-blocker-still-returned.md`

## Problem

The first-answer contract still allowed a false blocker in practice: ChatGPT could read the router, discover that repo-local Python allocator execution was unavailable in connector context, and stop at the generic allocator blocker even when GitHub connector write path could safely update `.chatgpt/chat-handoff-index.yaml`.

## Required Factory Change

- Treat repo-local allocator unavailability as a tool-context limitation, not as a global write blocker.
- If GitHub connector write path is available, materialize the chat title reservation through connector update and confirm fetch/readback before showing `FT-CH-....`.
- Only show the exact allocator blocker after a real write blocker: no write path, permission denied, write rejected, or confirm fetch failed.
- Validate the regression with a fixture for `GitHub connector write path available` plus `repo-local allocator unavailable in ChatGPT connector context`.

## Downstream Reuse

Generated/battle repos that use repo-first ChatGPT Project instructions should inherit the same fallback contract through scenario-pack, runbooks, validator, and chat index allocation policy.
