# Factory feedback 057: Compact card must show open handoff reservations

Дата: 2026-05-07

Reusable defect: compact status cards can falsely look green when open ChatGPT reservations without HIR links are filtered out.

Factory rule:
- non-terminal `FT-CH` reservations are active work unless explicitly closed, superseded, not applicable or archived;
- compact cards may group or wrap them, but must not silently hide them because `handoff_register_item_id` is empty;
- stale or excluded reservations need explicit evidence in the index/register.

Evidence:
- `reports/bugs/2026-05-07-compact-card-open-chat-handoff-drift.md`
- `template-repo/scripts/render-project-lifecycle-dashboard.py`
