# Журналы уведомлений

`reports/notifications/` is the repo-native runtime location for Telegram notification outbox and inbound command audit logs.

Tracked files in this directory are documentation only. Runtime `*.jsonl` files are ignored by git because they may contain operational metadata and chat identifiers. They must not contain bot tokens, `.env` contents, private transcripts, or secrets.
