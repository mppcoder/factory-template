# Bug: stale chat index items appear as active compact-card tasks

Date: 2026-04-29

## Summary

The compact project card showed `FT-CH-0002 completion-report` and `FT-CH-0004 model-routing` as active work even though there were no matching unfinished handoff implementation register items.

## Evidence

- `.chatgpt/chat-handoff-index.yaml` had `FT-CH-0002` in `state: open` with an empty `handoff_register_item_id`.
- `.chatgpt/chat-handoff-index.yaml` had `FT-CH-0004` in `state: blocked` with an empty `handoff_register_item_id`.
- `.chatgpt/handoff-implementation-register.yaml` had no active items for those chat IDs.
- The compact renderer treated every non-terminal chat index item as active card work.

## Expected Behavior

Compact card `В работе:` should show real current/not-closed work, not stale seed/index entries without a matching register item.

## Remediation

- Mark stale `FT-CH-0002` and `FT-CH-0004` as `not_applicable` with accepted reasons.
- Keep stale entries in history only.
- Harden compact card filtering so unregistered non-current index entries do not appear as active work.
