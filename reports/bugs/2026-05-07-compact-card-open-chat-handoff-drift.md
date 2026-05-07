# Bug: Compact project card hides open ChatGPT handoff reservations

Дата: 2026-05-07

## Симптом
`reports/project-status-card.md` показывал `Tasks: 0` и только verified work, хотя `.chatgpt/chat-handoff-index.yaml` содержал open `FT-CH` reservations.

## Root cause
`render-project-lifecycle-dashboard.py` filtered active ChatGPT handoff lines by non-empty `handoff_register_item_id`, so connector-created or research/open reservations without HIR disappeared from the compact card.

## Remediation
- Active ChatGPT handoff rendering now includes every non-terminal `FT-CH` item, even when it has no HIR link yet.
- `FT-CH-0021`, `FT-CH-0022` and `FT-CH-0024` were closed with evidence where this remediation or previous verified work covered them.
- `FT-CH-0023` remains visible as an open active reservation until it is explicitly closed, superseded or implemented.

## Verification
- `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout`
- `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`
