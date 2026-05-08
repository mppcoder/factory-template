# Журналы уведомлений

Generated projects use this directory for Telegram notification outbox and inbound command audit logs:

- `reports/notifications/outbox.jsonl`
- `reports/notifications/inbound-audit.jsonl`

Runtime `*.jsonl` files are ignored by git. Do not store bot tokens, `.env` contents, private transcripts, or secrets here.
