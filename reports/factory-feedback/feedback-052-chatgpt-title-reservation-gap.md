# Factory Feedback 052: ChatGPT title numbers must be materialized reservations

Source bug: `reports/bugs/2026-05-05-chatgpt-title-reservation-gap.md`

## Learning

The first-answer chat title block is only safe if a visible `FT-CH-....` is backed by an already-written repo index item. A proposed, dry-run or read-only next number creates a collision window when the user does not launch the handoff in Codex.

## Template Action

- Treat `.chatgpt/chat-handoff-index.yaml` as a reservation ledger, not only a display counter.
- Require `visible_chat_title_requires_materialized_index_item: true`.
- Require dry-run allocator output to be visibly non-reserved.
- If a handoff is not launched, keep the number allocated and close the item explicitly instead of reusing the number.
- Update ChatGPT Project snippets to show either a materialized title or the allocator blocker, never an unwritten suggestion.
