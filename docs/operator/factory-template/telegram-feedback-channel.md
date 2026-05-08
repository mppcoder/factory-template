# Канал Telegram Feedback

Telegram Feedback Channel - repo-native delivery/control layer for `factory-template` and downstream projects. It does not create a new task database and does not replace repo artifacts as source of truth.

## Источник истины

Telegram events are derived from existing repo contours:

- `.chatgpt/chat-handoff-index.yaml`
- `.chatgpt/codex-work-index.yaml`
- `.chatgpt/handoff-implementation-register.yaml`
- lifecycle dashboard/card artifacts
- `reports/factory-feedback/`
- `reports/bugs/`
- update/release governance artifacts
- validators and closeout scripts

Outbound delivery writes audit records to `reports/notifications/outbox.jsonl`. Inbound commands write sanitized audit records to `reports/notifications/inbound-audit.jsonl`. Runtime JSONL files are git-ignored.

## Артефакты

- Event schema: `template-repo/template/.chatgpt/telegram-feedback-event.schema.yaml`
- Example config: `template-repo/template/.chatgpt/telegram-feedback-channel.example.yaml`
- Notifier: `template-repo/scripts/factory_notify_telegram.py`
- Validator: `template-repo/scripts/validate-telegram-feedback-channel.py`
- P0 fixtures: `tests/telegram-feedback-channel/events/p0-events.yaml`

## Таксономия P0 событий

Supported P0 kinds:

- `task.completed`
- `codex.completed`
- `user_action.required`
- `bug.detected`
- `bug.fixed`
- `verification.failed`
- `update.available`
- `update.recommended`
- `release.published`
- `deploy.done`

`downstream.feedback` is also reserved for upstream feedback from battle projects into the factory.

## Маршрутизация Telegram

The example config defines topic names that can map to one chat or to Telegram forum topics:

- `factory-main`
- `codex-completions`
- `user-actions`
- `bugs`
- `updates`
- `downstream-projects`

If forum topics are not configured yet, keep `message_thread_id: null`. Replace `REPLACE_WITH_TELEGRAM_CHAT_ID` and `REPLACE_WITH_OPTIONAL_FORUM_TOPIC_ID` only in a local config copy, not in the template example.

## Безопасность

`TELEGRAM_BOT_TOKEN` must exist only in env or a secret store. It must not be committed.

Inbound commands require both allowlists:

- `TELEGRAM_ALLOWED_CHAT_IDS`
- `TELEGRAM_ALLOWED_USER_IDS`

Allowed inbound commands are intentionally narrow: `status`, `ack`, `defer`, `bug`, `handoff_draft`, `feedback`. Telegram must not launch arbitrary shell, Codex, deploy, merge, push or destructive actions.

## Dry-run

Validate schema, config and fixtures:

```bash
python3 template-repo/scripts/validate-telegram-feedback-channel.py --allow-placeholders
```

Run notifier without a token:

```bash
python3 template-repo/scripts/factory_notify_telegram.py send \
  --event tests/telegram-feedback-channel/events/p0-events.yaml \
  --dry-run \
  --outbox /tmp/telegram-feedback-outbox.jsonl
```

Audit an inbound safe command fixture:

```bash
TELEGRAM_ALLOWED_CHAT_IDS=123456789 TELEGRAM_ALLOWED_USER_IDS=987654321 \
python3 template-repo/scripts/factory_notify_telegram.py audit-inbound \
  --payload tests/telegram-feedback-channel/inbound/ack-command.json \
  --audit /tmp/telegram-feedback-inbound-audit.jsonl
```

## Live-настройка

1. Create a bot in BotFather and store the token outside the repo as `TELEGRAM_BOT_TOKEN`.
2. Get the destination chat id. If using Telegram forum topics, get each `message_thread_id`.
3. Create a local config from `.chatgpt/telegram-feedback-channel.example.yaml`.
4. Replace placeholders in the local config and set `enabled: true`.
5. Set `TELEGRAM_ALLOWED_CHAT_IDS` and `TELEGRAM_ALLOWED_USER_IDS`.
6. Run validator against the local config without `--allow-placeholders`.
7. Run one `--dry-run`, then run a real send only after the outbox entry looks safe.

## Точки интеграции

- Closeout task completed: emit `task.completed` from `.chatgpt/done-report.md` / `.chatgpt/task-index.yaml`.
- Codex completed: emit `codex.completed` from `.chatgpt/codex-work-index.yaml` or `.chatgpt/handoff-implementation-register.yaml`.
- User action required: emit `user_action.required` from `.chatgpt/boundary-actions.md`.
- Bug detected/fixed: emit `bug.detected` / `bug.fixed` from `reports/bugs/` and reusable feedback from `reports/factory-feedback/`.
- Validator failed: emit `verification.failed` only after failure evidence is captured.
- Update available/recommended: emit from `.chatgpt/software-update-watchlist.yaml` and `.chatgpt/software-update-readiness.yaml`.
- Release/deploy: emit `release.published` / `deploy.done` from release governance reports.
- Downstream feedback: emit `downstream.feedback` from `reports/factory-feedback/incoming-learnings/`.

## Границы

Telegram status is not canonical. The canonical state remains in repo artifacts. Dedupe uses `dedupe_key`, and the outbox records delivery attempts. A green Telegram delivery alone does not close a goal, task, bug, update, release or deploy.
