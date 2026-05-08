# Канал Telegram Feedback

Telegram Feedback Channel is an optional delivery/control layer over repo-first project artifacts. It does not replace `.chatgpt` indexes, reports, validators, GitHub Issues or the lifecycle dashboard.

## Файлы

- `.chatgpt/telegram-feedback-event.schema.yaml` - event envelope schema.
- `.chatgpt/telegram-feedback-channel.example.yaml` - safe config example without secrets.
- `reports/notifications/outbox.jsonl` - runtime outbound delivery log, git-ignored.
- `reports/notifications/inbound-audit.jsonl` - runtime inbound command audit, git-ignored.

## Типы событий

P0 event kinds are `task.completed`, `codex.completed`, `user_action.required`, `bug.detected`, `bug.fixed`, `verification.failed`, `update.available`, `update.recommended`, `release.published` and `deploy.done`.

## Безопасность

Keep `TELEGRAM_BOT_TOKEN` in env or a secret store only. Inbound commands require `TELEGRAM_ALLOWED_CHAT_IDS` and `TELEGRAM_ALLOWED_USER_IDS`.

Allowed inbound commands are only `status`, `ack`, `defer`, `bug`, `handoff_draft` and `feedback`. Telegram commands must not launch shell, Codex, deploy, merge, push or destructive actions.

## Настройка

1. Copy `.chatgpt/telegram-feedback-channel.example.yaml` to a local, untracked config if the project needs live Telegram delivery.
2. Replace chat ids and optional forum topic ids in that local config.
3. Set `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_CHAT_IDS` and `TELEGRAM_ALLOWED_USER_IDS` outside the repo.
4. Validate the local config and run dry-run before real delivery.

Telegram delivery is evidence of notification only. The project is still closed or reopened only through repo-native artifacts and validators.
