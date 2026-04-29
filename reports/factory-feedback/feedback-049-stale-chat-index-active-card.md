# Factory Feedback 049: compact card needs register-backed active work

Date: 2026-04-29

## Learning

The chat handoff index is the counter/source of chat identity, but compact `В работе:` is an operator active-work readout. Old index seeds without register linkage can look like real work if state alone is used.

## Template Change

- Compact card active lines require either a linked `handoff_register_item_id` or the current/latest chat item.
- Stale unregistered items should be written off as `not_applicable` or `superseded` with evidence or accepted reason.
- Full markdown history may still show the historical index entries.
