# Bug: rehearsal route check wrote noncanonical chat-handoff index item

- id: `bug-2026-05-07-rehearsal-route-check-noncanonical-chat-index`
- detected: `2026-05-07`
- source: downstream `Beginner First Rehearsal E` route-check confirmation
- owner_boundary: generated repo ChatGPT Project write flow / chat handoff index schema discipline
- severity: medium

## Symptom

The ChatGPT Project route-check report said `FT-CH-0001 repo-first-route-check` was reserved and verified. The commits existed, but the generated `.chatgpt/chat-handoff-index.yaml` item used noncanonical fields:

- `title` instead of `chat_title`;
- `slug` instead of `task_slug`;
- `created_at` / `verified_at` instead of `created_utc` / `updated_utc`;
- missing `chat_number`, `source_type`, `handoff_group`, `handoff_revision`, `status_chain`, `evidence`, and `next_action`.

`python3 scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml` rejected the item.

## Expected behavior

Any materialized ChatGPT title reservation must match `chat-handoff-index/v1` exactly and pass the repo validator before the route-check is reported as verified.

## Evidence

- Downstream reservation commit: `498c30d7337fc7ebf5acf8e9b3a5f0651737427c`
- Downstream verified commit before repair: `f090a07f093560d17360eccbb4f53f67b4134b27`
- Downstream repair commit: `004dc63`
- Downstream validation after repair:
  - `python3 scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`
  - `bash scripts/verify-all.sh quick`
  - `python3 scripts/check-dod.py .`

## Fix

Normalized the downstream item to canonical fields and pushed `004dc63 fix: normalize route check chat index`.

Factory already has a schema validator for this file; the main lesson is operational: a ChatGPT connector write must use the repo allocator/schema shape, not a hand-written approximation.
