# Отчеты мониторинга стандартов

This directory is the report/proposal area for the lifecycle standards navigator.

Current default command:

```bash
python3 template-repo/scripts/check-standards-watchlist.py --root .
```

The check is offline-first. It validates freshness metadata in `template-repo/standards/standards-watchlist.yaml` and prints `proposal-needed` warnings when `last_checked_utc` is stale or a standard is marked unknown/stale/revision-pending.

It does not update standards versions, gates or dashboard claims. Version drift must go through:

```text
standards-update-proposal -> impact classification -> user approval -> template update
```

No formal certification is implied by these reports.
